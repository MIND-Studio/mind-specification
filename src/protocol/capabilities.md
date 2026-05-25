# Mind Protocol §3 — Capability companion docs

Interface contracts for each capability IRI listed in the [§3 services manifest](03-services-manifest.md). A service that declares `mind:offers <capability>` MUST implement the contract specified here. Apps and workers that *consume* a capability MUST work against any service that declares it.

<div class="diagram-block protocol-intro">
  <div class="protocol-intro-meta">
    <span class="protocol-intro-tag">§3 COMPANION · DRAFTED v0.1</span>
    <h3 class="protocol-intro-title">Capability = interface, not implementation</h3>
  </div>
  <p class="protocol-intro-body">Each IRI in §3's capability vocab (<code>mind:SpeechToText</code>, <code>mind:LocalLLM</code>, <code>mind:OCR</code>, …) names a request/response shape that every service offering that capability must implement. Two providers of <code>mind:SpeechToText</code> are interchangeable — same multipart body, same JSON response, same error model.</p>
  <div class="protocol-intro-key">
    <div class="key-item"><span class="key-label">KEY IDEA</span><span class="key-value">Shared HTTP+JSON conventions across all capabilities. Async via <code>mind:ServiceCall</code> (§4).</span></div>
    <div class="key-item"><span class="key-label">DEPENDS ON</span><span class="key-value"><a href="03-services-manifest.md">§3 Services manifest</a> · <a href="04-ldn-inbox-outbox.md">§4 LDN</a> (async)</span></div>
    <div class="key-item"><span class="key-label">11 CAPABILITIES</span><span class="key-value">SpeechToText · TextToSpeech · LocalLLM · HostedLLM · Transcription · OCR · Translation · PrivacyClassification · ImageClassification · Embedding · Summarization</span></div>
  </div>
</div>

> Status: drafted v0.1. Anchored to [§3](03-services-manifest.md). Depends on [§1](01-pod-layout.md) and [§4](04-ldn-inbox-outbox.md) (for async results).

---

## Purpose

§3 says *which* capability a service offers. This document says *what shape* the request and response take, so a `mind:SpeechToText` request to one provider works against any other `mind:SpeechToText` provider with no per-vendor code.

Without these contracts, "capability vocabulary" is just naming — you'd still have per-vendor adapters. With them, capability becomes interface, and services become interchangeable per their declared offerings.

---

## Shared conventions

These apply to every capability unless overridden in a specific section.

### Transport

- **Protocol:** HTTPS, HTTP/1.1 or HTTP/2.
- **Method:** `POST` for invocation. `HEAD` MAY be used for health checks (see §3).
- **Path:** the `mind:endpoint` URL from the services manifest is the base; the capability is identified by the `Content-Type` of the request (no per-capability path required). A service offering multiple capabilities at the same endpoint discriminates by request content type or a `Capability:` header.

### Authentication

Inherited from `mind:auth` in the manifest. The capability contract does not redefine it.

| `mind:auth` | What the client sends |
|---|---|
| `mind:BearerToken` | `Authorization: Bearer <token>` |
| `mind:CapabilityURL` | Credential is baked into the endpoint URL |
| `mind:mTLS` | Client cert at TLS handshake |
| `mind:WebIDAuth` | WebID + DPoP per Solid-OIDC |
| `mind:None` | No credential |

### Content types

| When | Content-Type |
|---|---|
| Text-only input | `application/json` |
| Binary input (audio, image, file) | `multipart/form-data` |
| JSON response | `application/json; charset=utf-8` |
| Binary response (audio) | per the requested format (`audio/wav`, `audio/mpeg`, …) |
| Streaming response | `text/event-stream` (Server-Sent Events) |

### Capability discriminator header

When a service offers multiple capabilities at one endpoint:

```
POST /v1/ HTTP/1.1
Capability: mind:SpeechToText
Authorization: Bearer …
Content-Type: multipart/form-data; boundary=…
```

The `Capability:` header carries the full IRI. Services SHOULD reject mismatched bodies with `400 Bad Request`.

### Errors

All capability errors use this shape (JSON body, appropriate 4xx/5xx status):

```json
{
  "error": "invalid_input",
  "message": "audio format opus not supported",
  "capability": "mind:SpeechToText",
  "requestId": "01HVZA1K3M4P9X7B5R0YBNM8W2D"
}
```

Standard `error` values: `invalid_input`, `unsupported_format`, `authentication_failed`, `rate_limited`, `quota_exceeded`, `service_unavailable`, `internal_error`. Capability-specific errors MAY add more.

### Async vs sync

Short-running capabilities (TTS for a sentence, OCR of a single image, classification, embedding) MUST respond synchronously. Long-running capabilities (full transcription of a multi-minute recording, summarization of a long document, large-batch embedding) MAY return `202 Accepted` and post the result asynchronously.

<div class="diagram-block diagram-call-flow">
  <div class="call-flow-grid">
    <div class="call-flow-col call-flow-sync">
      <div class="call-flow-tag">SYNC · short work</div>
      <ol class="call-flow-steps">
        <li><span class="step-num">1</span><span class="step-text">Caller <code>POST</code>s request</span></li>
        <li><span class="step-num">2</span><span class="step-text">Service processes inline</span></li>
        <li><span class="step-num">3</span><span class="step-text">Service returns <code>200 OK</code> with the result in the body</span></li>
      </ol>
      <div class="call-flow-note">Caller blocks on the response. Typical for TTS, OCR, classification, embedding, translation.</div>
    </div>
    <div class="call-flow-col call-flow-async">
      <div class="call-flow-tag">ASYNC · long work</div>
      <ol class="call-flow-steps">
        <li><span class="step-num">1</span><span class="step-text">Caller <code>POST</code>s request</span></li>
        <li><span class="step-num">2</span><span class="step-text">Service returns <code>202 Accepted</code> with a <code>jobId</code></span></li>
        <li><span class="step-num">3</span><span class="step-text">Service processes (seconds to minutes)</span></li>
        <li><span class="step-num">4</span><span class="step-text">Service <code>POST</code>s a <code>mind:ServiceCall</code> notification to caller's <code>/inbox/</code> (<a href="04-ldn-inbox-outbox.md">§4</a>)</span></li>
        <li><span class="step-num">5</span><span class="step-text">Caller's router worker reads inbox, hands the result to the original requester</span></li>
      </ol>
      <div class="call-flow-note">Caller doesn't block. Typical for long transcription, summarization, large batches.</div>
    </div>
  </div>

  <div class="call-flow-202">
    <div class="call-flow-202-label">202 Accepted body</div>
    <pre class="call-flow-202-code"><code>{
  "jobId": "job_01HVZA1K3M4P9X7B5R0YBNM8W2D",
  "status": "accepted",
  "estimatedSeconds": 45,
  "resultCallback": "ldn"
}</code></pre>
  </div>
</div>

Clients that don't want async delivery MAY pass `?sync=true` to force synchronous response (service may reject with `413` or `408` if the work is too large).

---

## Index

<div class="diagram-block diagram-cap-index">
  <a class="cap-chip" href="#mindspeechtotext"><span class="cap-iri">mind:SpeechToText</span><span class="cap-summary">audio → text</span></a>
  <a class="cap-chip" href="#mindtexttospeech"><span class="cap-iri">mind:TextToSpeech</span><span class="cap-summary">text → audio</span></a>
  <a class="cap-chip" href="#mindlocalllm"><span class="cap-iri">mind:LocalLLM</span><span class="cap-summary">prompt → completion (local model)</span></a>
  <a class="cap-chip" href="#mindhostedllm"><span class="cap-iri">mind:HostedLLM</span><span class="cap-summary">prompt → completion (hosted provider)</span></a>
  <a class="cap-chip" href="#mindtranscription"><span class="cap-iri">mind:Transcription</span><span class="cap-summary">long-audio → time-aligned transcript</span></a>
  <a class="cap-chip" href="#mindocr"><span class="cap-iri">mind:OCR</span><span class="cap-summary">image → text + regions</span></a>
  <a class="cap-chip" href="#mindtranslation"><span class="cap-iri">mind:Translation</span><span class="cap-summary">text + langs → translated text</span></a>
  <a class="cap-chip" href="#mindprivacyclassification"><span class="cap-iri">mind:PrivacyClassification</span><span class="cap-summary">content → privacy posture</span></a>
  <a class="cap-chip" href="#mindimageclassification"><span class="cap-iri">mind:ImageClassification</span><span class="cap-summary">image → labels</span></a>
  <a class="cap-chip" href="#mindembedding"><span class="cap-iri">mind:Embedding</span><span class="cap-summary">text → vector(s)</span></a>
  <a class="cap-chip" href="#mindsummarization"><span class="cap-iri">mind:Summarization</span><span class="cap-summary">long text → short text</span></a>
</div>

---

## mind:SpeechToText

Audio in → text out. Short utterances (≤ 30 seconds). For long recordings, use [`mind:Transcription`](#mindtranscription) instead.

**Request:** `multipart/form-data`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `audio` | file | yes | Audio recording. Supported formats: `audio/wav`, `audio/mpeg`, `audio/ogg`, `audio/flac`, `audio/webm` (opus). Service MAY support more. |
| `language` | string | no | BCP-47 tag (`en`, `de-CH`, `auto`). Default `auto`. |
| `prompt` | string | no | Bias text — words the user is likely to say (names, jargon). |

**Response:** `application/json`

```json
{
  "text": "Hi, can you book a table at Café Bistro for Friday?",
  "language": "en",
  "confidence": 0.94,
  "durationSeconds": 3.8
}
```

**Notes**

- If `audio` exceeds the service's max duration, return `413 Payload Too Large` and suggest `mind:Transcription`.
- Confidence is overall (single number 0–1). Word-level timing is the domain of `mind:Transcription`.

---

## mind:TextToSpeech

Text in → audio out.

**Request:** `application/json`

```json
{
  "text": "Hi, your reservation is confirmed for Friday at 7.",
  "voice": "amy",
  "format": "audio/mpeg",
  "language": "en-GB",
  "speed": 1.0,
  "pitch": 0
}
```

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | yes | Text to synthesize. Plain text or SSML (declared via `?ssml=true`). |
| `voice` | string | yes | Service-defined voice identifier. List via `GET <endpoint>/voices`. |
| `format` | string | no | MIME type. Default `audio/mpeg`. |
| `language` | string | no | BCP-47 tag. Defaults to the voice's primary language. |
| `speed` | number | no | 0.5–2.0. Default 1.0. |
| `pitch` | number | no | -10 to +10 semitones. Default 0. |

**Response:** binary audio body in the requested format.

**Notes**

- Long text (≥ 10,000 characters) MAY be handled async per the shared conventions.
- Services SHOULD support an SSE streaming variant (`?stream=true`) that returns chunks as they're synthesized, for lower-latency playback.

---

## mind:LocalLLM

Prompt → completion. Specifically for **locally-hosted** models (your home box, on-device, LAN). The contract is identical to `mind:HostedLLM`; the distinction is trust posture (local-LLM responses can carry sensitive prompts).

**Request:** `application/json`

```json
{
  "prompt": "Rewrite the following email more concisely:\n\n…",
  "maxTokens": 500,
  "temperature": 0.7,
  "stop": ["\n\nUser:"],
  "stream": false
}
```

| Field | Type | Required | Meaning |
|---|---|---|---|
| `prompt` | string | yes | Input text. For chat-style, use `messages` instead (see below). |
| `messages` | array | no | Alternative to `prompt` — array of `{role: "system"|"user"|"assistant", content: "…"}`. |
| `maxTokens` | int | no | Cap output length. Service default applies if absent. |
| `temperature` | number | no | 0.0–2.0. Default 1.0. |
| `stop` | string[] | no | Stop sequences. |
| `stream` | bool | no | If `true`, respond with SSE. |

**Response (non-stream):** `application/json`

```json
{
  "text": "Thanks for the offer. I'll pass for now.",
  "finishReason": "stop",
  "usage": { "promptTokens": 84, "completionTokens": 12 }
}
```

`finishReason`: `stop` | `length` | `content_filter` | `error`.

**Response (stream):** `text/event-stream` with `data: {"delta": "..."}` events, terminated by `data: [DONE]`.

**Notes**

- Privacy: callers SHOULD prefer `mind:LocalLLM` over `mind:HostedLLM` for prompts containing PII or sensitive data, when both are available.

---

## mind:HostedLLM

Same contract as `mind:LocalLLM`, with two differences:

- Requires a `model` field naming the hosted model (`gpt-4o`, `claude-sonnet-4-6`, `llama-3.1-70b`, …)
- Service MAY add provider-specific fields (top-p, presence_penalty, …); apps SHOULD ignore unknown response fields

**Request:** `application/json` — superset of `mind:LocalLLM`

```json
{
  "model": "claude-sonnet-4-6",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Summarize this:\n\n…"}
  ],
  "maxTokens": 1000,
  "temperature": 0.7
}
```

**Response:** identical shape to `mind:LocalLLM`, with an additional `model` field echoing the model used.

**Notes**

- `GET <endpoint>/models` SHOULD return `{models: [{id, contextWindow, costPerMillionTokens?}]}` so apps can pick.
- Privacy: services SHOULD declare `mind:dataPolicy` in §3 manifest (`mind:UsedForTraining` is a strong negative signal — clients may refuse PII-bearing prompts).

---

## mind:Transcription

Long audio → time-aligned transcript with optional speaker diarization. Use this when the audio is too long for `mind:SpeechToText` (typically > 30 s).

**Request:** `multipart/form-data`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `audio` | file | yes | Recording. Same formats as `mind:SpeechToText`. |
| `language` | string | no | BCP-47 tag. Default `auto`. |
| `diarize` | bool | no | If `true`, return per-speaker labels. Default `false`. |
| `wordTimestamps` | bool | no | If `true`, return per-word timing. Default `false`. |

**Response (sync, short audio):** `application/json`

```json
{
  "text": "...",
  "language": "de",
  "durationSeconds": 124.5,
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "speaker": "S1",
      "text": "Guten Tag, wie kann ich helfen?",
      "words": [
        {"word": "Guten", "start": 0.1, "end": 0.4, "confidence": 0.96},
        ...
      ]
    },
    ...
  ]
}
```

**Response (async, long audio):** `202 Accepted` per shared async conventions. Result POSTed to caller's `/inbox/` as `mind:ServiceCall`, where `mind:result` points to a JSON document with the shape above.

**Notes**

- `speaker` labels (`S1`, `S2`, …) are stable within a single call. Cross-call speaker identification is out of scope.
- Word timestamps significantly increase response size; opt in only when needed.

---

## mind:OCR

Image → text. Optional per-region positions.

**Request:** `multipart/form-data`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `image` | file | yes | `image/png`, `image/jpeg`, `image/webp`, `application/pdf` (multi-page allowed). |
| `language` | string | no | BCP-47 hint, helps with ambiguous scripts. |
| `regions` | bool | no | If `true`, include per-region bounding boxes. Default `false`. |

**Response:** `application/json`

```json
{
  "text": "Café Bistro\nReservation\nFriday 19:00",
  "language": "en",
  "pages": [
    {
      "pageNumber": 1,
      "text": "Café Bistro\nReservation\nFriday 19:00",
      "regions": [
        {"text": "Café Bistro", "bbox": [120, 40, 380, 78], "confidence": 0.98},
        ...
      ]
    }
  ]
}
```

**Notes**

- `bbox` is `[x_min, y_min, x_max, y_max]` in pixels of the source image.
- For multi-page PDFs, each page is a separate entry in `pages`.

---

## mind:Translation

Text in + target language → translated text. Source language is auto-detected unless specified.

**Request:** `application/json`

```json
{
  "text": "Wo ist der Hauptbahnhof?",
  "sourceLanguage": "de",
  "targetLanguage": "en",
  "context": "asking for directions"
}
```

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | yes | Source text. May be a single string or an array of strings (batch). |
| `sourceLanguage` | string | no | BCP-47. Omit for auto-detect. |
| `targetLanguage` | string | yes | BCP-47. |
| `context` | string | no | Disambiguating context (formality, domain, …). |

**Response:** `application/json`

```json
{
  "text": "Where is the main train station?",
  "sourceLanguageDetected": "de",
  "targetLanguage": "en"
}
```

For batch input (`text` as array), `text` in response is also an array, same order.

---

## mind:PrivacyClassification

Content in → privacy posture out. Used by apps and the Privacy Guardian agent to route data through services with appropriate trust levels.

**Request:** `application/json`

```json
{
  "content": "My passport number is X12345678 and I was born 1985-03-12.",
  "contentType": "text/plain",
  "context": "drafting a reply to a hotel"
}
```

**Response:** `application/json`

```json
{
  "classification": "sensitive",
  "confidence": 0.97,
  "categories": ["pii", "identity_document", "date_of_birth"],
  "suggestedDataPolicies": ["mind:ZeroRetention"],
  "redactions": [
    {"start": 23, "end": 33, "category": "identity_document"},
    {"start": 56, "end": 66, "category": "date_of_birth"}
  ]
}
```

| `classification` | Meaning |
|---|---|
| `public` | Safe for any service (no `mind:dataPolicy` constraint) |
| `personal` | Personal but not sensitive — `mind:ZeroRetention` recommended |
| `sensitive` | PII / health / financial / identity — `mind:TrustHigh` or `mind:TrustMedium` only |
| `restricted` | Should not leave the user's trust zone — `mind:TrustHigh` only |

**Notes**

- `redactions` are byte offsets into `content`. Apps can use them to redact before sending to lower-trust services.
- `categories` are open-ended; common: `pii`, `financial`, `health`, `credentials`, `location`, `identity_document`, `date_of_birth`, `private_communication`.

---

## mind:ImageClassification

Image → labels.

**Request:** `multipart/form-data`

| Field | Type | Required | Meaning |
|---|---|---|---|
| `image` | file | yes | `image/png`, `image/jpeg`, `image/webp`. |
| `topK` | int | no | Return top K labels by confidence. Default 5. |
| `detectObjects` | bool | no | If `true`, return per-object bounding boxes. Default `false`. |

**Response:** `application/json`

```json
{
  "labels": [
    {"label": "bicycle", "confidence": 0.94},
    {"label": "cargo bike", "confidence": 0.87},
    {"label": "outdoor", "confidence": 0.81}
  ],
  "objects": [
    {"label": "bicycle", "bbox": [40, 120, 580, 720], "confidence": 0.94}
  ]
}
```

**Notes**

- Labels are strings — vocabulary is service-defined. Apps that need a controlled vocabulary should specify it via `?vocabulary=<iri>` and the service may reject unknown vocabularies.

---

## mind:Embedding

Text → vector. Used for semantic search, similarity, RAG.

**Request:** `application/json`

```json
{
  "text": "Café Bistro on Hauptstraße",
  "model": "all-minilm-l6-v2"
}
```

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string \| string[] | yes | One string or a batch. |
| `model` | string | no | Service-defined model id. Defaults to service primary. |

**Response (single):** `application/json`

```json
{
  "model": "all-minilm-l6-v2",
  "dimensions": 384,
  "vector": [0.0123, -0.0456, ..., 0.0789]
}
```

**Response (batch):** `vectors` array instead of `vector`, same order as input.

**Notes**

- Different models produce vectors of different dimensionality and aren't comparable. Apps SHOULD record `model` alongside any stored vectors.
- Services SHOULD expose `GET <endpoint>/models` listing available embedding models with their dimensionality.

---

## mind:Summarization

Long text → short text.

**Request:** `application/json`

```json
{
  "text": "...",
  "targetWords": 80,
  "style": "bullet_list"
}
```

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | yes | Source text. |
| `targetWords` | int | no | Target length in words. Default 150. |
| `style` | string | no | `prose` (default), `bullet_list`, `headline`, `tl_dr`. |
| `audience` | string | no | Free-text hint about the reader. |

**Response:** `application/json`

```json
{
  "summary": "- Café Bistro confirms reservation for Friday 19:00\n- Party of 4 with one vegan\n- Parking on Hauptstraße, not the rear lot",
  "originalWordCount": 870,
  "summaryWordCount": 26,
  "style": "bullet_list"
}
```

**Notes**

- Long source documents MAY be handled async per shared conventions.

---

## Adding a new capability

The vocab is open. To mint a new capability:

1. Pick an IRI under your own prefix (e.g. `acme:SongRecognition`). Do not extend `mind:` — that's reserved for the protocol.
2. Write a contract document modelled on the sections above (request shape, response shape, error model, notes).
3. Publish the contract at the IRI (Linked Data convention: dereferencing the IRI returns the contract).
4. Services that implement it declare `mind:offers acme:SongRecognition` in their §3 manifest entry.
5. Apps that recognize the IRI use it; apps that don't, ignore it.

There is no central registry. Capability IRIs propagate via use.

---

## Open questions

- **Streaming for capabilities other than LLM?** SSE for `mind:TextToSpeech` is noted as a SHOULD. Should other capabilities (`mind:Transcription` for partial results, `mind:Summarization` for progressive output) also support streaming?
- **Batch interfaces.** Embedding has batch support inline; should other capabilities (translation, classification) follow the same `text` ↔ `text[]` pattern, or use a dedicated `/batch` endpoint?
- **Capability versioning.** When `mind:SpeechToText` v2 needs an incompatible response shape, do we mint `mind:SpeechToTextV2` or rely on `mind:apiVersion` in the §3 manifest entry?
- **Cost reporting.** Should responses optionally carry a `cost` field (`{"currency": "USD", "amount": 0.0034}`) so apps can budget? Today this is out-of-band.
- **Idempotency.** Should all capabilities accept an `Idempotency-Key` header so retries don't double-bill?
- **Rate limit headers.** Standardize `X-RateLimit-*` headers across all capabilities, or leave to each service?
