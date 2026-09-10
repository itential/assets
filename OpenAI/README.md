OpenAI provides hosted large language models and generative AI capabilities — chat and text completions, embeddings, image generation, speech-to-text and text-to-speech, moderation, fine-tuning, and the Assistants/Responses APIs for building conversational and agentic applications.

This project provides OpenAPI specs for automating against the OpenAI REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Table of Contents

- [Contents](#contents)
- [Requirements](#requirements)
- [Integration Configuration](#integration-configuration)
- [OpenAPIs](#openapis)
  - [`openai-latest.json`](#openai-latestjson)
  - [`openai-2.3.0.json`](#openai-230json)
- [Studio Projects](#studio-projects)
  - [OpenAI Project](#openai-project)
    - [Folder Structure](#folder-structure)
    - [Dependencies](#dependencies)

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OpenAI REST API OpenAPI specs — curated `-latest` plus the full dated spec |
| [Studio Projects/OpenAI](./Studio%20Projects/OpenAI.project.json) | 22 workflows covering common CRUD automation |

## Requirements

| Requirement | Version |
|---|---|
| Itential Platform | 6.x |
| OpenAI API | 2.3.0 |
| OpenAI Integration Model | Required to build automation against the OpenAPI specs |

## Integration Configuration

Import one of the OpenAPI specs from `OpenAPIs/` as an Integration Model in **Admin > Integrations**, then create an integration pointing at the OpenAI API.

Authentication is a bearer token in the `Authorization` header:

```
Authorization: Bearer <your-openai-api-key>
```

Generate an API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

The instance's `authentication`/`server` properties should look like this once configured:

```json
{
  "authentication": {
    "ApiKeyAuth": "<your-bearer-token>"
  },
  "server": {
    "protocol": "https",
    "host": "api.openai.com",
    "base_path": "/v1"
  }
}
```

## OpenAPIs

| Spec | Version | Operations | Description |
|---|---|---|---|
| [`openai-latest.json`](./OpenAPIs/openai-latest.json) | latest (curated) | 84 | Trimmed to 84 of 242 upstream operations — see breakdown below |
| [`openai-2.3.0.json`](./OpenAPIs/openai-2.3.0.json) | 2.3.0 | 242 | Full, unmodified vendor spec |

### `openai-latest.json`

Actively-maintained spec (`x-vendor-api-version: 2.3.0`). Trimmed to 84 of 242 upstream operations covering common CRUD for automation.

Resources included, by category:

- **Chat & Text Generation**: Chat Completions, legacy Completions, Responses (create/get/cancel/list input items)
- **Conversations**: Conversations and conversation items (used with the Responses API for stateful multi-turn state)
- **Assistants**: Assistants, Threads, Messages, Runs, Run Steps, tool-output submission
- **Embeddings**: Embeddings
- **Models**: List and retrieve available models
- **Moderations**: Content moderation
- **Files**: Files (upload/list/get/delete/content) — used by Assistants, fine-tuning, and vector stores
- **Fine-tuning**: Fine-tuning jobs (create/get/cancel)
- **Images**: Image generation, edits, variations
- **Audio**: Speech synthesis, transcription, translation
- **Batches**: Batch job create/get/cancel
- **Vector Stores**: Vector stores and vector store files/search (retrieval for Assistants/Responses)
- **Videos**: Video generation create/get/delete/content

Excluded: administration/org-management (API keys, users, roles, groups, invites, projects, audit logs, usage/cost reporting), Realtime voice API, ChatKit, Containers (code interpreter sandboxes), Evals, Skills, Uploads (large multipart upload flow), voice cloning/consents, webhooks, and niche video sub-features (characters, remix, extensions, edits). See the repo README for the full scope, or pull the full spec below if you need one of the excluded areas.

### `openai-2.3.0.json`

Full, unmodified vendor spec covering all 242 upstream operations — the vendor's complete API surface, preserved as-is. See `openai-latest.json` above for the curated subset if you just need common CRUD automation.

---

## Studio Projects

### OpenAI Project

Backed by the **`OpenAI:latest`** Integration Model (see [`openai-latest.json`](./OpenAPIs/openai-latest.json) above). The project contains **22 workflows** organized into **5 folders**, one atomic workflow per API operation, covering the common-CRUD subset of the curated spec.

#### Folder Structure

| Folder | Workflows | Scope |
|---|---|---|
| Models | List, Retrieve, Delete Model | Model catalog |
| Chat Completions | List, Create, Get, Update, Delete Chat Completion | Chat completion lifecycle |
| Files | List, Create, Retrieve, Delete File, Download File Content | File lifecycle |
| Fine-tuning Jobs | List, Create, Retrieve, Cancel Fine-tuning Job | Fine-tuning job lifecycle |
| Assistants | List, Create, Get, Modify, Delete Assistant | Assistant lifecycle |

#### Dependencies

| Dependency | Notes |
|---|---|
| `OpenAI:latest` Integration Model | Import from [`openai-latest.json`](./OpenAPIs/openai-latest.json) before importing the project |
| `OpenAI` integration instance | Create in **Admin > Integrations** with the connection properties above. Workflows are wired to an integration instance named `OpenAI` — update the `adapter_id` value in each workflow task if yours is named differently |
