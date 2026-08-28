# AWS Secrets Manager — Custom Secret Provider for Itential Gateway

## What This Is

A custom secret-provider plugin so Itential Gateway resolves AWS Secrets Manager credentials at runtime instead of storing them in Gateway's own encrypted store — for device inventory passwords, Integration Model API credentials, and other Gateway-executed actions. One less place your team manages credentials, and rotation in AWS Secrets Manager propagates automatically on the next run — no VPN needed between a SaaS Platform and an on-prem secrets manager, since only Gateway ever resolves the value.

The interesting part of this integration isn't the Secrets Manager API call itself (a single `GetSecretValue`) — it's **how the plugin process authenticates to AWS**, since that varies a lot depending on where Itential Gateway is actually running. This example implements and tests three patterns and lets you pick per-provider.

Itential Gateway 5.5+ supports **external secret providers** out of the box for **HashiCorp Vault (KV v2)** and **CyberArk CCP** — see Itential's docs on [configuring a custom secret provider plugin](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider) and [managing secret aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases). AWS Secrets Manager isn't a built-in type, so this uses the third option — **`plugin`** — a small executable you provide that Itential Gateway calls to fetch a secret on demand.

## Table of Contents

- [What This Is](#what-this-is)
- [Prerequisites](#prerequisites)
- [The Plugin](#the-plugin)
- [Authenticating to AWS: Three Patterns](#authenticating-to-aws-three-patterns)
  - [Pattern 1 — EC2 Instance Role](#pattern-1--ec2-instance-role-best-when-itential-gateway-runs-on-ec2)
  - [Pattern 2 — IAM Roles Anywhere](#pattern-2--iam-roles-anywhere-recommended-for-on-prem--non-ec2)
  - [Pattern 3 — Static IAM User Access Key](#pattern-3--static-iam-user-access-key-simplest-quick-start)
  - [Cross-account note](#cross-account-note)
- [Registering the Provider and Alias](#registering-the-provider-and-alias)
- [Referencing the Alias](#referencing-the-alias)
  - [In Device Inventory](#in-device-inventory)
  - [In an Integration Model Instance](#in-an-integration-model-instance)
- [Verifying It's Working](#verifying-its-working)
- [Adapting This Example](#adapting-this-example)
- [References](#references)

## Prerequisites

- Itential Gateway 5.5 or later, with the `secret-provider` feature available (`iagctl create secret-provider --help` should show the `plugin`, `vault`, and `cyberark` provider types).
- Python 3 on the Itential Gateway host (already required by Itential Gateway itself). No third-party Python packages — the plugin hand-implements AWS Signature Version 4 using only the standard library, the same convention used by the Azure Key Vault and Delinea Secret Server plugins in this repo.
- An AWS Secrets Manager secret to read. A structured JSON secret (e.g. `{"username": "...", "password": "..."}`) works well with the `--key` option shown below; a plain string secret works too if you omit `--key`.

## The Plugin

Itential Gateway invokes the plugin as `<command> get`, writing a JSON request to stdin and reading a JSON response from stdout. Configuration (the non-sensitive values registered with the provider) arrives via the JSON on stdin, in `config.env` — the plugin process does not otherwise inherit Itential Gateway's environment.

**Request (stdin):**
```json
{
  "path": "AWS-IOSXE-PASSWORD",
  "key": "password",
  "config": {
    "env": {
      "AWS_REGION": "us-east-1",
      "...": "... one of the three auth patterns below ..."
    }
  }
}
```

**Response (stdout, exit 0):**
```json
{"value": "the-plaintext-secret"}
```

On failure: write a message to stderr and exit non-zero.

See [`plugin.py`](./plugin.py) for the full implementation. Copy it to the Itential Gateway host — renaming it to something provider-specific like `aws-plugin.py` if you'll have more than one provider's plugin on the same host — and make it executable:

```bash
cp plugin.py /opt/gateway/aws-plugin.py
chmod +x /opt/gateway/aws-plugin.py
```

`path` is the secret's **name or full ARN** — see the [cross-account note](#cross-account-note) for why the ARN matters. If the secret's `SecretString` is a JSON object and `key` is given, the plugin parses it and pulls out that one field; otherwise it returns the whole string.

## Authenticating to AWS: Three Patterns

Every pattern ends with the plugin process having, in one form or another, an AWS access key + secret key (+ optional session token) to sign the `GetSecretValue` request with. The plugin tries these in order, so the `config.env` you register with the provider determines which one actually runs:

1. `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` / `AWS_SECRET_ACCESS_KEY_FILE` — static keys.
2. `AWS_CREDENTIAL_PROCESS` — a shell command that prints the [standard `credential_process` JSON](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html) (`{"Version":1,"AccessKeyId":...,"SecretAccessKey":...,"SessionToken":...,"Expiration":...}`). This is how Pattern 2 (IAM Roles Anywhere) plugs in — AWS's own `aws_signing_helper credential-process` command produces exactly this output.
3. The EC2 instance's attached IAM role, fetched via IMDSv2. No configuration needed — this is the fallback when neither of the above is set.

### Pattern 1 — EC2 Instance Role (best when Itential Gateway runs on EC2)

If Itential Gateway itself runs on an EC2 instance, attach an IAM role to it and grant that role `secretsmanager:GetSecretValue` scoped to the secret's ARN. No credentials are configured on the provider at all — the plugin's IMDSv2 fallback picks them up automatically.

```bash
iagctl create secret-provider aws-secretsmanager-instancerole-plugin \
  --type plugin \
  --command /opt/gateway/aws-plugin.py \
  --env AWS_REGION=us-east-1 \
  --description "AWS Secrets Manager via EC2 instance role (IMDSv2)"
```

IAM policy on the instance's role, scoped to one secret:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "secretsmanager:GetSecretValue",
    "Resource": "arn:aws:secretsmanager:<region>:<account-id>:secret:<secret-name>-<random-suffix>"
  }]
}
```

This is the closest analog to Azure's Managed Identity option — nothing to rotate, nothing on disk. It only applies if Itential Gateway is on EC2, which most customer deployments aren't (see Pattern 2). It's also the pattern most affected by the [cross-account note](#cross-account-note) below.

### Pattern 2 — IAM Roles Anywhere (recommended for on-prem / non-EC2)

**This is the pattern most customers will actually use** — Itential Gateway is typically deployed on-prem or in a customer's own VM, not as an EC2 instance. [IAM Roles Anywhere](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/introduction.html) lets a non-AWS server exchange an X.509 client certificate for short-lived AWS credentials, so there's still no long-lived AWS access key sitting on disk — only a certificate and private key, which are easier to scope, rotate, and revoke.

**One-time AWS setup** (in the account that owns the secret):

```bash
# 1. Trust anchor: register your CA (can be your own self-managed CA — no
#    AWS Private CA required/billed — or an AWS Private CA if you have one)
aws rolesanywhere create-trust-anchor \
  --name my-iag5-trust-anchor \
  --source '{"sourceType":"CERTIFICATE_BUNDLE","sourceData":{"x509CertificateData":"'"$(cat ca-cert.pem)"'"}}' \
  --enabled

# 2. IAM role that Roles Anywhere is allowed to hand out sessions for
cat > role-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "rolesanywhere.amazonaws.com"},
    "Action": ["sts:AssumeRole", "sts:TagSession", "sts:SetSourceIdentity"],
    "Condition": {"ArnEquals": {"aws:SourceArn": "<trust-anchor-arn>"}}
  }]
}
EOF
aws iam create-role --role-name iag5-secretsmanager-reader --assume-role-policy-document file://role-trust-policy.json
aws iam put-role-policy --role-name iag5-secretsmanager-reader --policy-name read-secret \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"secretsmanager:GetSecretValue","Resource":"<secret-arn>"}]}'

# 3. Profile: associates the role with the trust anchor
aws rolesanywhere create-profile \
  --name iag5-secretsmanager-reader \
  --role-arns arn:aws:iam::<account-id>:role/iag5-secretsmanager-reader \
  --enabled
```

Generate a CA + client certificate (a self-managed CA via `openssl` is fine for this — Roles Anywhere doesn't require AWS Private CA):

```bash
openssl genrsa -out ca-key.pem 4096
openssl req -x509 -new -nodes -key ca-key.pem -sha256 -days 3650 \
  -subj "/CN=my-iag5-ca" -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign" -out ca-cert.pem

openssl genrsa -out client-key.pem 2048
openssl req -new -key client-key.pem -subj "/CN=my-iag5-host" -out client.csr
openssl x509 -req -in client.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial \
  -days 825 -sha256 -extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=clientAuth") \
  -out client-cert.pem
```

On the Itential Gateway host, copy `client-cert.pem`, `client-key.pem` (mode `400`), and `ca-cert.pem`, plus the [`aws_signing_helper`](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/credential-helper.html) binary for your platform (verify the published SHA256 checksum after downloading). Then register the provider with `AWS_CREDENTIAL_PROCESS` pointing at it:

```bash
iagctl create secret-provider aws-secretsmanager-rolesanywhere-plugin \
  --type plugin \
  --command /opt/gateway/aws-plugin.py \
  --env AWS_REGION=us-east-1 \
  --env "AWS_CREDENTIAL_PROCESS=/opt/gateway/aws_signing_helper credential-process --certificate /etc/gateway/aws-rolesanywhere-client-cert.pem --private-key /etc/gateway/aws-rolesanywhere-client-key.pem --intermediates /etc/gateway/aws-rolesanywhere-ca-cert.pem --trust-anchor-arn <trust-anchor-arn> --profile-arn <profile-arn> --role-arn <role-arn>" \
  --description "AWS Secrets Manager via IAM Roles Anywhere"
```

Each `get` call re-runs `credential-process`, which does a full `CreateSession` round trip (adds a little latency, but keeps every call using freshly-issued, short-lived credentials — never a cached long-lived key).

### Pattern 3 — Static IAM User Access Key (simplest, quick-start)

The same shape the Azure/Delinea plugins in this repo already use for their credentials — a scoped IAM user with one access key, the secret half stored in a locked-down file:

```bash
aws iam create-user --user-name svc-iag5-secretsmanager-reader
aws iam put-user-policy --user-name svc-iag5-secretsmanager-reader --policy-name read-secret \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"secretsmanager:GetSecretValue","Resource":"<secret-arn>"}]}'
aws iam create-access-key --user-name svc-iag5-secretsmanager-reader
```

Store the secret half in a file, never as a raw `--env` value (which would be stored in the gateway's provider configuration in plaintext):

```bash
sudo tee /etc/gateway/aws_secret_access_key <<< 'the-secret-access-key' > /dev/null
sudo chown itential:itential /etc/gateway/aws_secret_access_key
sudo chmod 400 /etc/gateway/aws_secret_access_key
```

```bash
iagctl create secret-provider aws-secretsmanager-static-plugin \
  --type plugin \
  --command /opt/gateway/aws-plugin.py \
  --env AWS_REGION=us-east-1 \
  --env AWS_ACCESS_KEY_ID=<access-key-id> \
  --env AWS_SECRET_ACCESS_KEY_FILE=/etc/gateway/aws_secret_access_key \
  --description "AWS Secrets Manager via static IAM user access key"
```

Simplest to set up, works regardless of where Itential Gateway runs — but it's a long-lived credential that needs manual rotation, so prefer Pattern 2 for anything on-prem and Pattern 1 when running on EC2.

### Cross-account note

If the IAM identity calling `GetSecretValue` (the EC2 instance role, the Roles Anywhere role, or the IAM user) lives in a **different AWS account** than the secret:

- You must pass the secret's **full ARN** as `path`, not just its friendly name — cross-account calls can't resolve a bare name, only an ARN.
- The secret's owning account needs a [resource policy](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_resource-based-policies.html) naming the external principal, in addition to that principal's own identity policy.
- **The secret must be encrypted with a customer-managed KMS key**, not the default `aws/secretsmanager` key. AWS hard-blocks cross-account decryption of secrets under the default key — no IAM policy on either side can override this. The KMS key's key policy also needs a statement granting the external principal `kms:Decrypt` + `kms:DescribeKey`.

None of this applies when the calling identity and the secret share an account, which is the common case and why Patterns 2 and 3 above are shown same-account.

## Registering the Provider and Alias

Pick one pattern above and register its provider, then create the alias mapping a friendly name to the specific secret:

```bash
iagctl create secret AWS-IOSXE-PASSWORD \
  --provider aws-secretsmanager-rolesanywhere-plugin \
  --secret AWS-IOSXE-PASSWORD \
  --key password
```

Verify:
```bash
iagctl get secret-providers
iagctl describe secret AWS-IOSXE-PASSWORD
```

`describe secret` only shows the alias's metadata (provider/secret/key) — it never displays the resolved value.

## Referencing the Alias

Use `$GATEWAYSECRET_(alias-name)` anywhere Itential Gateway resolves secrets at execution time. This doc covers two callers in detail below — Inventory Manager Nodes and Integration Model instances — but Gateway resolves the same alias for other Gateway-executed actions too, including Config Manager command templates and GatewayManager tasks like `runService`/`runCode`/`sendCommand`/`sendConfig`. See [Itential Gateway — External Secrets Overview](https://docs.itential.com/itential-gateway/5/secrets/external-secrets/overview) for the complete list. Whichever one triggers it, the path is identical, and the plaintext secret never travels back to Platform:

```
Itential Platform
  • Inventory Manager Nodes
  • Integration Model instances (Gateway-executed)
  • Config Manager command templates
  • GatewayManager tasks (runService, runCode, sendCommand, sendConfig, ...)
        │
        ▼
Itential Gateway
        │  resolves $GATEWAYSECRET_(alias)
        ▼
aws-plugin.py
        │  SigV4-signed request
        ▼
AWS Secrets Manager
```

### In Device Inventory

For example, a Cisco IOS device synced into Itential Platform:

```json
{
  "name": "device-name",
  "attributes": {
    "itential_host": "10.0.25.20",
    "itential_port": 22,
    "itential_driver": "netmiko",
    "itential_platform": "cisco_ios",
    "itential_user": "itential",
    "itential_password": "$GATEWAYSECRET_(AWS-IOSXE-PASSWORD)"
  }
}
```

Itential Gateway resolves the alias just before the device driver call, so the real password is fetched fresh from Secrets Manager on every run rather than stored anywhere on the platform.

### In an Integration Model Instance

The same alias resolves in an **Integration Model instance's** credential fields too, as long as that instance's calls actually execute through Itential Gateway rather than directly from the Platform cluster:

- Set `proxyOverride.executionMode` to `cluster_no_proxy` or `proxy` — **not** `direct`. `direct` means Platform makes the call itself, Gateway is never involved, and the alias won't resolve.
- Optionally set `clusterOverride` to target a specific Gateway cluster instead of the Admin Essentials default.

```json
{
  "security": {
    "apiKey": {
      "value": "$GATEWAYSECRET_(AWS-API-TOKEN)"
    }
  },
  "proxyOverride": {
    "overrideProxyBehavior": true,
    "executionMode": "cluster_no_proxy",
    "proxy": {
      "auth": {
        "authMode": "none"
      }
    }
  }
}
```

Gateway resolves the alias just before the outbound call executes, same as the device inventory case — the real token is never sent back to Platform.

## Verifying It's Working

- `iagctl get secret-providers` shows your provider(s).
- `iagctl describe secret <alias>` shows the correct provider/secret/key.
- The gateway log (`journalctl -u iagctl`) shows a line like `secret_resolution alias="..." provider="..." path="..." outcome=success` for each call that uses the alias.
- The device/API call using the resolved secret succeeds end to end.
- To test a provider directly without going through a real device call, pipe a request straight into the plugin using the exact `config.env` you registered — this is exactly what Itential Gateway does internally:
  ```bash
  echo '{"path":"AWS-IOSXE-PASSWORD","key":"password","config":{"env":{"AWS_REGION":"us-east-1"}}}' \
    | /opt/gateway/aws-plugin.py get
  ```

## Adapting This Example

- **Multiple secrets**: register one provider, then create as many `secret` aliases as you need against it — each just needs its own `--secret <name>`.
- **Plain-string secrets**: omit `--key` when creating the alias; the plugin returns the whole `SecretString` value as-is.
- **Session tokens with static keys**: if you're using temporary credentials rather than a permanent IAM user (e.g. from `aws sts assume-role`), also set `AWS_SESSION_TOKEN` — the plugin picks it up automatically alongside `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`.
- **Any other `credential_process`-compatible tool**: `AWS_CREDENTIAL_PROCESS` isn't specific to Roles Anywhere — any command that prints the standard JSON (SSO, a custom broker, etc.) works the same way.

## References

- [Itential Gateway — Configure a Custom Plugin Secret Provider](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider)
- [Itential Gateway — Manage Secret Aliases](https://docs.itential.com/itential-gateway/secrets/external-secrets/manage-secret-aliases)
- [AWS Secrets Manager — GetSecretValue API reference](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)
- [AWS Signature Version 4 signing process](https://docs.aws.amazon.com/IAM/latest/UserGuide/create-signed-request.html)
- [IAM Roles Anywhere — credential helper](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/credential-helper.html)
- [AWS SDKs — sourcing credentials from an external process](https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html)
- [Secrets Manager cross-account access with a customer-managed key](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html#security-encryption-cross-account)
