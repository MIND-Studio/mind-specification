# Mind Protocol §3 — Services manifest

How **external services** — a Mind Cube appliance on your LAN, a hosted transcription API, a Verein's shared LLM, a friend's home box — advertise themselves so apps and workers can discover and call them, without per-app out-of-band setup.

<div class="diagram-block protocol-intro">
  <div class="protocol-intro-meta">
    <span class="protocol-intro-tag">§3 · DRAFTED v0.1</span>
    <h3 class="protocol-intro-title">Per-user manifest of services you've added</h3>
  </div>
  <p class="protocol-intro-body">A pointer in your profile (<code>mind:services</code>) leads to a Turtle manifest listing every service you've added — Mind Cube, hosted APIs, a Verein's shared LLM. Apps and workers read it, find a service offering the capability they need, and call. No per-app config, no central registry.</p>
  <div class="protocol-intro-key">
    <div class="key-item"><span class="key-label">KEY IDEA</span><span class="key-value">Two-tier discovery: profile pointer → manifest → service endpoint.</span></div>
    <div class="key-item"><span class="key-label">DEPENDS ON</span><span class="key-value"><a href="01-pod-layout.md">§1</a> (paths) · Solid (profile)</span></div>
    <div class="key-item"><span class="key-label">COMPANION</span><span class="key-value"><a href="capabilities.md">Capabilities reference</a> — interface contracts</span></div>
  </div>
</div>

<div class="diagram-block diagram-discovery">
  <div class="discovery-title">DISCOVERY · how a worker finds a service</div>
  <ol class="discovery-steps">
    <li>
      <span class="discovery-num">01</span>
      <div class="discovery-body">
        <div class="discovery-head">Resolve the user's WebID</div>
        <div class="discovery-detail"><code>https://alice.example.org/profile/card#me</code> → fetch the profile document</div>
      </div>
    </li>
    <li>
      <span class="discovery-num">02</span>
      <div class="discovery-body">
        <div class="discovery-head">Read the <code>mind:services</code> pointer</div>
        <div class="discovery-detail">Profile says: <code>&lt;#me&gt; mind:services &lt;/services/manifest.ttl&gt; .</code></div>
      </div>
    </li>
    <li>
      <span class="discovery-num">03</span>
      <div class="discovery-body">
        <div class="discovery-head">Fetch the manifest</div>
        <div class="discovery-detail">Turtle document listing every <code>mind:Service</code> the user has added — endpoint, capabilities, auth, trust level, data policy</div>
      </div>
    </li>
    <li>
      <span class="discovery-num">04</span>
      <div class="discovery-body">
        <div class="discovery-head">Pick a service that offers the needed capability</div>
        <div class="discovery-detail">Filter by <code>mind:offers</code>; prefer higher <code>mind:trustLevel</code>; resolve <code>mind:auth</code> + credentials</div>
      </div>
    </li>
    <li>
      <span class="discovery-num">05</span>
      <div class="discovery-body">
        <div class="discovery-head">Call</div>
        <div class="discovery-detail">POST to the service's <code>mind:endpoint</code> per the capability's interface contract (see <a href="capabilities.md">Capabilities reference</a>). Sync response, or async via <a href="04-ldn-inbox-outbox.md">§4 <code>mind:ServiceCall</code></a></div>
      </div>
    </li>
  </ol>
</div>

---

## Purpose

A capability like "speech-to-text" can be provided by many things: a Mind Cube in the room, a cloud API, a self-hosted Whisper instance, a friend's home box. Each app shouldn't have to be configured for each service. Each service shouldn't have to be registered with each app.

§3 gives every user a single pod-anchored manifest that says: *"these are the services I've decided to trust; here's what each one offers and how to reach it."* Any Mind-aware app or worker can read that manifest, find a service that offers the capability it needs, and call it.

The manifest is per-user — Verein-shared or public manifests are possible but out of scope for v0.1.

---

## Two-tier discovery

To find a user's services, an app starts from the user's WebID and follows one pointer.

**Tier 1 — the pointer in the profile.** The user's profile document (`profile/card`) carries a `mind:services` predicate pointing at the manifest URL:

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .

<#me>
  mind:services </services/manifest.ttl> .
```

**Tier 2 — the manifest at the pointed URL.** A single Turtle document listing every service the user has added.

This indirection lets users move the manifest, share it across pods (e.g., a Verein-managed manifest mirrored into each member's profile), or expose different manifests to different audiences via ACLs.

---

## The manifest

`/services/manifest.ttl` (or wherever `mind:services` points) lists every service the user has registered.

### Shape — `mind:Service`

```turtle
@prefix mind: <https://mind.dev/ns/v1#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .

<#home-cube>
  a                mind:Service ;
  mind:label       "Home Cube" ;
  mind:endpoint    <https://my-cube.local/v1/> ;
  mind:offers      mind:SpeechToText ,
                   mind:TextToSpeech ,
                   mind:LocalLLM ,
                   mind:PrivacyClassification ;
  mind:auth        mind:BearerToken ;
  mind:authConfig  </services/auth/home-cube.ttl> ;   # private; how to get tokens
  mind:trustLevel  mind:TrustHigh ;
  mind:dataPolicy  mind:ZeroRetention ;
  mind:apiVersion  "1.2" ;
  mind:addedAt     "2026-05-24T10:00:00Z"^^xsd:dateTime .

<#acme-transcribe>
  a                mind:Service ;
  mind:label       "ACME Transcription API" ;
  mind:endpoint    <https://api.acme.example/transcribe> ;
  mind:offers      mind:Transcription ;
  mind:auth        mind:CapabilityURL ;
  mind:authConfig  </services/auth/acme.ttl> ;
  mind:trustLevel  mind:TrustExternal ;
  mind:dataPolicy  mind:LoggedShortTerm ;
  mind:apiVersion  "2024-09" ;
  mind:addedAt     "2026-04-01T12:00:00Z"^^xsd:dateTime .
```

### Required predicates

| Predicate | Type | Meaning |
|---|---|---|
| `mind:label` | string | Human-readable name |
| `mind:endpoint` | URL | Where to send requests |
| `mind:offers` | one or more `mind:Capability` IRIs | What this service can do |
| `mind:auth` | `mind:AuthMethod` IRI | How to authenticate |
| `mind:trustLevel` | `mind:TrustLevel` IRI | Sender's trust assessment |
| `mind:addedAt` | xsd:dateTime | When added (for audit / rotation) |

### Optional predicates

| Predicate | Type | Meaning |
|---|---|---|
| `mind:authConfig` | URL (pod-local) | Where to find credentials. **Must not** be world-readable. |
| `mind:dataPolicy` | `mind:DataPolicy` IRI | Retention / training-use posture |
| `mind:apiVersion` | string | Vendor-defined version tag |
| `mind:fallback` | another `mind:Service` IRI | Use this service if primary is unavailable |
| `mind:disabledAt` | xsd:dateTime | When the user disabled the service (kept for history) |

---

## Capability vocabulary

A small fixed set of capability classes apps and workers can declare and look for. Open-ended — third parties can mint their own under their own prefixes; apps that don't recognize a capability ignore it.

| IRI | What |
|---|---|
| `mind:SpeechToText` | Audio in → text out |
| `mind:TextToSpeech` | Text in → audio out |
| `mind:LocalLLM` | Text prompt → text completion (local model) |
| `mind:HostedLLM` | Text prompt → text completion (third-party LLM) |
| `mind:Transcription` | Recording → transcript with timestamps |
| `mind:OCR` | Image → text |
| `mind:Translation` | Text + language pair → translated text |
| `mind:PrivacyClassification` | Data → PII / sensitive / public classification |
| `mind:ImageClassification` | Image → labels |
| `mind:Embedding` | Text → vector |
| `mind:Summarization` | Long text → short text |

A capability IRI represents an *interface contract*, not an implementation. Two services offering `mind:SpeechToText` accept the same audio formats and return the same response shape.

**The contracts themselves live in a companion document** — see [§3 capability companion docs](capabilities.md). Each IRI has its own section with request/response shapes, error model, and notes. Implementers should read it before shipping a service.

---

## Authentication

The manifest declares **which** method to use; how the client actually **obtains** credentials is out of band (config file, OAuth flow, vendor-specific). Credentials never live in the manifest itself — only the method and a pointer to where credentials are managed.

| IRI | Method |
|---|---|
| `mind:BearerToken` | `Authorization: Bearer <token>` header |
| `mind:CapabilityURL` | The endpoint URL itself contains a signed credential |
| `mind:mTLS` | Mutual TLS with client certificate |
| `mind:WebIDAuth` | Present requester's WebID + DPoP token (Solid-native; for pod-aware services) |
| `mind:None` | No auth (read-only public services) |

Credentials in `mind:authConfig` typically live in a separate pod-local file with restrictive ACLs (owner read/write only). Workers acting on the user's behalf are granted read access to specific entries.

---

## Trust levels and data policies

Apps making routing decisions need to know how much they can trust a service with the data they're about to send.

### `mind:TrustLevel`

| IRI | Meaning |
|---|---|
| `mind:TrustHigh` | Fully trusted — local home box, your own VPS, your hardware |
| `mind:TrustMedium` | Partly trusted — Verein-run, contractual relationship |
| `mind:TrustExternal` | Arms-length — third-party API, no special relationship |

### `mind:DataPolicy`

| IRI | Meaning |
|---|---|
| `mind:ZeroRetention` | Service does not store request or response |
| `mind:LoggedShortTerm` | Service logs for ≤30 days, no training use |
| `mind:LoggedLongTerm` | Service logs indefinitely |
| `mind:UsedForTraining` | Service uses requests/responses for model training |
| `mind:Unknown` | Service does not specify |

Apps may refuse to send sensitive data to services with `mind:TrustExternal` + `mind:UsedForTraining`. The Privacy Guardian agent (when present) enforces this automatically.

### Routing matrix — what's safe to send where

Sending **sensitive** content (PII, health, financial, credentials — as classified by [`mind:PrivacyClassification`](capabilities.md#mindprivacyclassification)). Pick a cell to know the default app policy.

<div class="diagram-block diagram-trust-matrix">
  <div class="trust-grid">
    <div class="trust-corner"></div>
    <div class="trust-col-head">ZeroRetention</div>
    <div class="trust-col-head">LoggedShortTerm</div>
    <div class="trust-col-head">LoggedLongTerm</div>
    <div class="trust-col-head danger">UsedForTraining</div>

    <div class="trust-row-head">TrustHigh<br/><span class="trust-sub">your own / local</span></div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell ok">✓ send</div>

    <div class="trust-row-head">TrustMedium<br/><span class="trust-sub">Verein / contractual</span></div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell warn">⚠ caution</div>
    <div class="trust-cell warn">⚠ caution</div>

    <div class="trust-row-head">TrustExternal<br/><span class="trust-sub">third-party / public</span></div>
    <div class="trust-cell ok">✓ send</div>
    <div class="trust-cell warn">⚠ caution</div>
    <div class="trust-cell warn">⚠ caution</div>
    <div class="trust-cell bad">✗ refuse</div>
  </div>
  <div class="trust-legend">
    <span class="trust-legend-item"><span class="trust-dot ok"></span> safe by default</span>
    <span class="trust-legend-item"><span class="trust-dot warn"></span> warn user / redact PII first</span>
    <span class="trust-legend-item"><span class="trust-dot bad"></span> refuse without explicit override</span>
  </div>
  <div class="trust-note">Non-sensitive content (public / personal-but-not-sensitive) follows the user's preferences — usually all green. The matrix is for sensitive content; it's what makes the Privacy Guardian agent's job mechanical rather than judgment-based.</div>
</div>

---

## Calling a service

End-to-end flow for an app or worker that needs capability `C`:

1. **Discover.** Read `mind:services` from the user's profile → fetch the manifest.
2. **Select.** Find services where `mind:offers` includes `C`. If multiple match, prefer higher trust level; break ties by `mind:addedAt` (oldest = most established).
3. **Auth.** Resolve `mind:auth` + `mind:authConfig` to get credentials.
4. **Call.** Issue the request to `mind:endpoint` per the capability's interface contract.
5. **Handle response.**
   - **Sync** — response comes back inline.
   - **Async** — service responds with `202 Accepted` + a job ID, then POSTs result to the requester's `/inbox/` as a `mind:ServiceCall` notification (see [§4](04-ldn-inbox-outbox.md)).

If the request fails and the service declares `mind:fallback`, the client SHOULD retry against the fallback before failing the caller.

---

## Service health

A service SHOULD expose a `HEAD <endpoint>` that returns `200 OK` when healthy and `503 Service Unavailable` otherwise. Clients MAY cache health status for up to 60 seconds.

Workers (specifically indexers) MAY poll `HEAD` on all services in the manifest at a low cadence (e.g. every 5 minutes) and cache results, so dependent apps don't each pay the latency.

---

## Shared services across users

A Verein running a shared transcription service for its members doesn't need a federated registry. Each member adds the same `<https://verein.example/transcribe>` entry to their own manifest. The service auths each request individually using whatever auth method it declared.

When the Verein rotates credentials or moves the endpoint, it publishes the new manifest entry (e.g. via a "Verein services" page); members copy it into their own manifests. Future versions may automate this with a sub-manifest reference (`mind:include <verein-manifest.ttl>`), but v0.1 keeps each manifest self-contained.

---

## Out of scope for v0.1

- **Service marketplace / federated directory.** Manifests are per-user. Cross-user discovery (e.g. "show me all transcription services my friends use") is not specified.
- **Pricing or billing.** The manifest doesn't carry cost information. Billing happens between user and service provider out of band.
- **SLA contracts.** No standardized uptime / latency commitments.
- **DNS- or well-known-URL-based service discovery.** Services aren't expected to advertise themselves to the world — they wait to be added to users' manifests.
- **Capability interface contracts.** Each `mind:Capability` IRI implies a request/response shape, but the shapes themselves are defined in the [§3 capability companion docs](capabilities.md), not §3 itself.

---

## Open questions

- **Should there be a standard `/.well-known/mind-service.ttl` on the service side?** Useful for "I have a service URL — what does it claim to offer?" but creates a discovery vector that may not be desired for private services.
- **Should `mind:trustLevel` be a fixed enum or user-defined?** Fixed is interoperable; user-defined is more honest about variability. v0.1 picks fixed.
- **How does a Verein-shared service get into multiple users' manifests automatically?** Future `mind:include` predicate to reference a shared sub-manifest, with the Verein's manifest as the upstream source of truth.
- **Capability versioning.** When `mind:SpeechToText` v1 and v2 have different response shapes, do we mint `mind:SpeechTextV2` or use `mind:apiVersion`? v0.1 uses `apiVersion`, but per-capability migration may need more.
- **Service identity verification.** When you add a "Mind Cube" entry, how do you verify the endpoint actually belongs to a Mind Cube (and isn't a malicious lookalike on your LAN)? Pairing flows are out of scope for v0.1.
