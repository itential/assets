# Microsoft Teams Assets

Send rich, adaptive-card notifications from an Itential workflow to a Microsoft Teams channel — job results, compliance reports, ticket updates, anything — via a Power Automate flow instead of a deprecated direct webhook.

## Table of Contents

- [Why Power Automate](#why-power-automate)
- [Architecture](#architecture)
- [Building the Power Automate Flow](#building-the-power-automate-flow)
- [The Itential Workflow](#the-itential-workflow)
  - [Inputs](#inputs)
  - [Sample Payload](#sample-payload)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Projects](#projects)
  - [Microsoft Teams Project](#microsoft-teams-project)

## Why Power Automate

Microsoft retired direct Incoming Webhooks (Office 365 Connectors) for Teams channels. A Power Automate flow with a **"When a Teams webhook request is received"** trigger is the supported replacement — it gives you an HTTP endpoint that posts an Adaptive Card into a chat or channel, without needing a Teams-specific adapter or connector on the Itential side.

## Architecture

```
Itential workflow (runCode, Python)
        │  builds an Adaptive Card, POSTs it
        ▼
Power Automate flow
  trigger: "When a Teams webhook request is received"
        │
        ▼
  action: "Post card in a chat or channel"
        │
        ▼
Microsoft Teams channel
```

The workflow runs the card-building/POST logic directly on the Itential Gateway via a `runCode` task — no custom adapter or pre-registered Itential Gateway service required.

## Building the Power Automate Flow

1. In [Power Automate](https://make.powerautomate.com), create a new flow.
2. Add the trigger **"When a Teams webhook request is received."** Search for "Teams webhook" specifically — don't confuse this with the generic **"When an HTTP request is received"** trigger, which is a different trigger kind and won't behave the same way. Under **Who can trigger the flow?**, choose based on your security needs — "Anyone" is simplest, but the URL itself is the only thing authorizing the request (see **Security** below).
3. Add the action **"Post card in a chat or channel"** (Microsoft Teams connector):
   - **Post as**: Flow bot (or a user, per your preference)
   - **Post in**: Channel (or Chat)
   - Select the **Team** and **Channel**
   - **Message**: click into the field, open **Add dynamic content**, and select the trigger's **Body** — this binds the whole incoming request directly as the message (equivalent to `@triggerBody()` if you look at the underlying flow expression).
4. Save the flow, then open the trigger step and copy its **HTTP URL**. This is `webhook_url` below.
5. **Test the flow by itself, before touching Itential.** This isolates flow-configuration problems from workflow problems. From any terminal:

   ```bash
   curl -X POST "<your trigger HTTP URL>" \
     -H "Content-Type: application/json" \
     -d '{
       "type": "AdaptiveCard",
       "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
       "version": "1.4",
       "body": [
         { "type": "TextBlock", "text": "Test message", "weight": "Bolder", "size": "Large" }
       ]
     }'
   ```

   If this posts into your channel, the flow is configured correctly and any further issues are on the Itential side.

## The Itential Workflow

Import [`Studio Projects/Microsoft Teams.project.json`](./Studio%20Projects/Microsoft%20Teams.project.json) into Automation Studio. It contains one workflow, **"Send Microsoft Teams Notification"** — a generic, reusable notifier with a single `runCode` (Python) task that builds an Adaptive Card and POSTs it to the flow's trigger URL.

**Gotcha, confirmed by testing**: POST the **bare `AdaptiveCard` object directly** as the request body. Do not wrap it in the Bot Framework `{"type": "message", "attachments": [...]}` envelope — even though the trigger's own declared input schema suggests that shape, the "Post card in a chat or channel" action's `messageBody` parameter expects the raw card and will fail with `Property 'type' must be 'AdaptiveCard'` if you wrap it.

**This is one way to do it, not the only way.** The Power Automate trigger just receives an HTTP request body — it doesn't have to be an Adaptive Card at all. This example builds the whole card in Itential's `runCode` and posts it as-is because the "Post card in a chat or channel" action's message is bound directly to `@triggerBody()`, which is the simplest possible flow. You could instead:
- Send a plain string or a small JSON object (e.g. `{"text": "..."}`) and use a **"Compose"** or **"Post message in a chat or channel"** action in Power Automate to format it there instead of in Python.
- Send raw data (device name, status, links, etc.) and have the *flow* build the Adaptive Card, using Power Automate's own Adaptive Card designer.

Which side does the formatting is a design choice — this example puts it in Itential because it's easier to keep the card's structure under version control alongside the workflow, but the split is entirely up to you.

### Inputs

Automation Studio requires every declared job variable to be present in the start-job payload — you can't just omit the ones you're not using. For `facts`, `link_url`, and `link_text`, pass `null` (or an empty array/string) rather than leaving the key out; the Python code treats falsy values as "not provided."

| Field | Description |
|---|---|
| `webhook_url` | The Power Automate trigger's HTTP URL. **Sensitive** — see Security below. |
| `title` | Card header text. |
| `message` | Main body text. |
| `facts` | Array of `{title, value}` pairs rendered as a FactSet (e.g. Device, Status, Owner), or `null`. |
| `link_url` | URL for an action button (e.g. link back to a job or ticket), or `null`. |
| `link_text` | Label for the action button (defaults to `"View Details"` if falsy), or `null`. |

### Sample Payload

```json
{
  "webhook_url": "https://<tenant>.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/<flow-id>/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=<signature>",
  "title": "Compliance Check Complete",
  "message": "Golden config compliance check finished for router edge-01.",
  "facts": [
    { "title": "Device", "value": "edge-01.lab.local" },
    { "title": "Status", "value": "COMPLIANT" },
    { "title": "Checked by", "value": "Itential Platform" }
  ],
  "link_url": "https://your-platform.example.com/operations-manager/#/jobs/<job-id>",
  "link_text": "View Job"
}
```

Minimal version — `facts`, `link_url`, and `link_text` are still present, just `null`:

```json
{
  "webhook_url": "https://<tenant>.environment.api.powerplatform.com:443/powerautomate/...",
  "title": "Job Complete",
  "message": "The automation finished successfully.",
  "facts": null,
  "link_url": null,
  "link_text": null
}
```

## Security

The trigger URL is not just a configuration value — it functions as a bearer credential. Anyone who has it can post into your Teams channel, regardless of the "Who can trigger the flow?" setting. Treat it accordingly:

- Never commit it to version control or share it in plaintext.
- Prefer resolving it at execution time from wherever your organization manages secrets (e.g. an Itential Gateway [external secret provider](https://docs.itential.com/itential-gateway/secrets/external-secrets/configure-custom-plugin-provider)) rather than passing it as a plain job input, if your workflow triggers aren't tightly access-controlled.
- Rotate the flow's trigger if the URL is ever exposed (regenerate it in Power Automate — this invalidates the old URL).

## Troubleshooting

Real errors we hit building this — likely the same ones you'll hit if something's misconfigured.

| Error | Cause | Fix |
|---|---|---|
| `socket.gaierror` / `NameResolutionError` in the job's stderr | `webhook_url` isn't a real, resolvable URL (e.g. a placeholder like `<your-tenant>` was left in) | Use the actual HTTP URL copied from your flow's trigger step |
| Job succeeds (`"ok": true, "status_code": 202"`), but nothing posts to Teams, and the flow run in Power Automate shows: `Property 'type' must be 'AdaptiveCard'` | The request body was wrapped in a `{"type": "message", "attachments": [...]}` envelope | Post the bare `AdaptiveCard` object directly — see the gotcha above |
| Job fails immediately with `Invalid input parameters: Property '': must have required property 'facts'` (or `link_url`/`link_text`) | One of the optional fields was omitted from the payload entirely | Include all six keys in every payload; use `null` for the ones you're not using — see **Inputs** above |

If the job succeeds and the flow run also succeeds but you still don't see a message, double check you picked the Teams-specific trigger (step 2 above) and that **Post in** points to a channel/chat you actually have open.

## Projects

### Microsoft Teams Project
- **Send Microsoft Teams Notification** — generic notifier, see above.

#### Dependencies
- A Power Automate flow with a "When a Teams webhook request is received" trigger (see above)
- [Automation Gateway 5.x](https://www.itential.com/automation-gateway/) — the `runCode` task executes on a connected Gateway cluster
