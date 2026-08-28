#!/usr/bin/env python3
"""IAG custom secret-provider plugin for AWS Secrets Manager.

IAG invokes this as `aws-plugin.py get`, writing a JSON request to
stdin (`{"path": "<secret name or ARN>", "key": "<optional field>", "config":
{"env": {...}}}`) and reading a JSON response from stdout
(`{"value": "..."}`) on success. On failure, write a message to stderr
and exit non-zero.
"""
import sys
import json
import os
import hmac
import hashlib
import datetime
import shlex
import subprocess
import urllib.request
import urllib.error

IMDS_BASE = "http://169.254.169.254"


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def imds_get(path, headers=None, method="GET"):
    req = urllib.request.Request(f"{IMDS_BASE}{path}", headers=headers or {}, method=method)
    return urllib.request.urlopen(req, timeout=2).read().decode()


def instance_role_credentials():
    """Temporary credentials for the EC2 instance profile, via IMDSv2.

    Returns None (rather than raising) on any failure so callers can treat
    "not running on EC2" / "no role attached" as just another reason to fall
    through to a clearer, actionable error message.
    """
    try:
        token = imds_get(
            "/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
            method="PUT",
        )
        role = imds_get(
            "/latest/meta-data/iam/security-credentials/",
            headers={"X-aws-ec2-metadata-token": token},
        ).strip()
        if not role:
            return None
        creds = json.loads(
            imds_get(
                f"/latest/meta-data/iam/security-credentials/{role}",
                headers={"X-aws-ec2-metadata-token": token},
            )
        )
        return creds["AccessKeyId"], creds["SecretAccessKey"], creds.get("Token")
    except Exception:
        return None


def read_secret_key(cfg_env):
    key_file = cfg_env.get("AWS_SECRET_ACCESS_KEY_FILE") or os.environ.get("AWS_SECRET_ACCESS_KEY_FILE")
    if key_file:
        try:
            with open(key_file, "r") as f:
                return f.read().strip()
        except OSError as e:
            fail(f"failed to read AWS_SECRET_ACCESS_KEY_FILE: {e}")
    return cfg_env.get("AWS_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")


def credential_process_credentials(cfg_env):
    """Run an external credential process (e.g. `aws_signing_helper
    credential-process ...` for IAM Roles Anywhere) and parse its standard
    JSON output — the same `credential_process` contract the AWS CLI/SDKs
    support. See https://docs.aws.amazon.com/sdkref/latest/guide/feature-process-credentials.html
    """
    command = cfg_env.get("AWS_CREDENTIAL_PROCESS") or os.environ.get("AWS_CREDENTIAL_PROCESS")
    if not command:
        return None
    try:
        result = subprocess.run(
            shlex.split(command), capture_output=True, text=True, timeout=30, check=True
        )
    except (subprocess.SubprocessError, OSError) as e:
        fail(f"AWS_CREDENTIAL_PROCESS failed: {e}")
    try:
        creds = json.loads(result.stdout)
        return creds["AccessKeyId"], creds["SecretAccessKey"], creds.get("SessionToken")
    except (json.JSONDecodeError, KeyError) as e:
        fail(f"AWS_CREDENTIAL_PROCESS returned unparseable output: {e}")


def resolve_credentials(cfg_env):
    """Three ways to authenticate, tried in order — mirrors the AWS SDK's own
    default provider chain:
    1. Static keys (env/file) — simplest, works anywhere, needs manual rotation.
    2. AWS_CREDENTIAL_PROCESS — an external command (e.g. `aws_signing_helper
       credential-process` for IAM Roles Anywhere) that returns short-lived
       credentials. Recommended for on-prem/non-EC2 hosts: no long-lived
       AWS keys stored anywhere, only an X.509 client certificate.
    3. EC2 instance role via IMDSv2 — recommended only when Itential Gateway
       itself runs on an EC2 instance; same idea as Azure Managed Identity
       for the Key Vault plugin.
    """
    access_key = cfg_env.get("AWS_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = read_secret_key(cfg_env)
    session_token = cfg_env.get("AWS_SESSION_TOKEN") or os.environ.get("AWS_SESSION_TOKEN")
    if access_key and secret_key:
        return access_key, secret_key, session_token

    process_creds = credential_process_credentials(cfg_env)
    if process_creds:
        return process_creds

    role_creds = instance_role_credentials()
    if role_creds:
        return role_creds
    fail(
        "no AWS credentials: set AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY(_FILE), or "
        "AWS_CREDENTIAL_PROCESS, in the provider's env, or run Itential Gateway on an "
        "EC2 instance with an attached role"
    )


def sigv4_headers(method, host, region, service, payload, access_key, secret_key, session_token, amz_target):
    """Build the signed request headers for a single AWS Signature Version 4
    request. See https://docs.aws.amazon.com/IAM/latest/UserGuide/create-signed-request.html
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(payload).hexdigest()

    sign_headers = {
        "content-type": "application/x-amz-json-1.1",
        "host": host,
        "x-amz-date": amz_date,
        "x-amz-target": amz_target,
    }
    if session_token:
        sign_headers["x-amz-security-token"] = session_token

    signed_header_names = ";".join(sorted(sign_headers))
    canonical_headers = "".join(f"{k}:{sign_headers[k]}\n" for k in sorted(sign_headers))
    canonical_request = "\n".join(
        ["POST", "/", "", canonical_headers, signed_header_names, payload_hash]
    )

    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode()).hexdigest(),
        ]
    )

    def hmac_sha256(key, msg):
        return hmac.new(key, msg.encode(), hashlib.sha256).digest()

    k_date = hmac_sha256(("AWS4" + secret_key).encode(), date_stamp)
    k_region = hmac_sha256(k_date, region)
    k_service = hmac_sha256(k_region, service)
    k_signing = hmac_sha256(k_service, "aws4_request")
    signature = hmac.new(k_signing, string_to_sign.encode(), hashlib.sha256).hexdigest()

    authorization = (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_header_names}, Signature={signature}"
    )

    # `host` is left out here — urllib sets it automatically from the URL,
    # and sending it twice would create a duplicate Host header on the wire.
    request_headers = {k: v for k, v in sign_headers.items() if k != "host"}
    request_headers["authorization"] = authorization
    return request_headers


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "get":
        fail("usage: aws-plugin.py get")

    try:
        req_in = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        fail(f"failed to parse stdin: {e}")

    path = req_in.get("path")
    key = req_in.get("key", "")
    cfg_env = req_in.get("config", {}).get("env", {})

    region = cfg_env.get("AWS_REGION") or os.environ.get("AWS_REGION")
    if not region:
        fail("AWS_REGION must be set in the plugin's environment")
    if not path:
        fail("no secret name or ARN provided")

    access_key, secret_key, session_token = resolve_credentials(cfg_env)

    host = f"secretsmanager.{region}.amazonaws.com"
    payload = json.dumps({"SecretId": path}).encode()
    headers = sigv4_headers(
        "POST", host, region, "secretsmanager", payload,
        access_key, secret_key, session_token, "secretsmanager.GetSecretValue",
    )

    req = urllib.request.Request(f"https://{host}/", data=payload, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        body = resp.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        fail(f"secret fetch failed: status {e.code}: {detail}")
    except Exception as e:
        fail(f"secret fetch failed: {e}")

    try:
        result = json.loads(body)
    except json.JSONDecodeError:
        fail("failed to parse secret response")

    value = result.get("SecretString")
    if value is None:
        fail("secret has no SecretString (binary secrets are not supported)")

    # Optional: if the secret's value is itself a JSON object (e.g. a
    # username+password pair stored as one secret) and `key` was given,
    # pull that one field out. Otherwise return the value as-is.
    if key:
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict) and key in parsed:
                value = parsed[key]
        except (json.JSONDecodeError, TypeError):
            pass

    print(json.dumps({"value": value}))


if __name__ == "__main__":
    main()
