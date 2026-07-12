OpenAI provides hosted large language models and generative AI capabilities — chat and text completions, embeddings, image generation, speech-to-text and text-to-speech, moderation, fine-tuning, and the Assistants/Responses APIs for building conversational and agentic applications.

This project provides OpenAPI specs for automating against the OpenAI REST API via an Integration Model. The `-latest` spec is a curated subset covering common CRUD for automation — see **OpenAPIs** below.

## Contents

| Asset | Description |
|---|---|
| [OpenAPIs/](./OpenAPIs/) | OpenAI REST API OpenAPI specs — curated `-latest` plus the full dated spec |

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

## OpenAPIs

### `openai-latest.json` (curated)

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

### Full, unmodified spec

| Spec | Description |
|---|---|
| [`openai-2.3.0.json`](./OpenAPIs/openai-2.3.0.json) | Full spec for the OpenAI API, version 2.3.0. |

## Dependencies

| Dependency | Notes |
|---|---|
| OpenAI Integration Model | Import from an OpenAPI spec above to build automation against the REST API. |
