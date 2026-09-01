# KanPi Foundry — Five Pilot Products Feature and Usage Review

**Scope:** Ember Signal — Mail Pilot, Selene Agents, Kinetic Mesh, Folio Forms, and Peregrine Editions.  
**Method:** Local source inspection of the current route registry and pilot page components. No paid service, external connector, deployment, or account-specific credit calculation was used.

> **Key result:** All five pilot routes are currently showcase experiences. Their buttons trigger local demo notifications or local menu state; the reviewed pilot components do not currently call an API, LLM, mail provider, payment provider, or form-submission backend. Therefore, current production usage for these pilot-page interactions is **zero API/LLM calls from the route components**, while the public website still incurs normal browser hosting and asset-delivery requests.

## Pilot feature map

| Pilot | Route | Core features evidenced in current source | Current interaction state |
|---|---|---|---|
| Ember Signal — Mail Pilot | `/ember-signal` | Source intelligence; creative brief engine; momentum map; campaign memory; campaign-surface stories; audience-signal and evidence artifacts | Showcase-only. CTA buttons call a local toast notifier. No mail inbox, sending, or campaign API is implemented in this route. |
| Selene Agents | `/selene-agents` | Agent workrooms; assembled sources for human judgement; visible task/source/responsible-person framing; summaries and high-stakes planning concepts; controlled agent workspace language | Showcase-only. CTAs call a local notification handler; no agent orchestration, retrieval, or LLM request is wired in the page. |
| Kinetic Mesh | `/kinetic-mesh` | No-code operations flows; signal → logic → people sequence; form/inbox/API/database input concepts; check/score/enrich/route logic concepts; flow exploration and build-session CTA | Showcase-only. CTAs call a local notification handler; no workflow runner, webhook, database, or API execution is implemented in the route. |
| Folio Forms | `/folio-forms` | Brand-system generation concept; first-spark-to-system journey; repeatable campaign outputs; pages/social/launch-material framing; visual system exploration | Showcase-only. CTAs call a local contact notifier; no brief submission, copy-generation call, or asset-generation backend is wired in the route. |
| Peregrine Editions | `/peregrine-editions` | Contemporary object archive; material-led exhibition framing; object acquisition; viewing-room request; editorial gallery/collection presentation | Showcase-only. Viewing/acquisition actions call a local handler; no catalogue API, enquiry form, CRM, or LLM behavior is implemented in the route. |

## Provider-neutral usage model

Account-specific Manus credits and pricing are intentionally not estimated here. When real integrations are approved, usage should be measured from application telemetry using the following neutral fields:

| Measurement | Meaning |
|---|---|
| `request_count` | Number of server-side API or LLM requests per product and action. |
| `input_tokens` / `output_tokens` | Token counts returned by the selected model provider, when applicable. Character counts can be retained as a fallback but must not be presented as tokens. |
| `tool_call_count` | Number of retrieval, search, database, email, webhook, or other tool calls inside one user action. |
| `file_count` / `file_bytes` | Number and size of uploaded or processed assets, kept separate from text-token usage. |
| `retry_count` / `error_count` | Failed and retried operations, so repeated calls are not hidden. |
| `latency_ms` | Time from request start to completion, useful for product quality and cost-control decisions. |
| `cache_hit` | Whether a response was served from an approved cache rather than recomputed. |
| `human_review` | Whether a person approved or edited the generated result before delivery. |

A later provider invoice or account dashboard should be joined to these counters by a release, date window, model, and product-action identifier. The formula must use the provider’s own published metering definitions; do not infer provider tokens from visual length or multiply them by an assumed Manus-credit rate.

## Integration readiness by pilot

| Pilot | Likely future API/LLM touchpoints | Minimum usage counters when activated | Current launch boundary |
|---|---|---|---|
| Ember Signal — Mail Pilot | Market-language ingestion; evidence retrieval; brief drafting; campaign-signal summarization; optional email/campaign provider integration | Refresh requests; source items; input/output tokens; retrieved documents; campaign actions; email sends; retries; human approvals | The current route is not an email product yet. “Mail Pilot” should not be marketed as inbox/send functionality until a mail provider, consent model, sending domain, unsubscribe handling, and delivery monitoring exist. |
| Selene Agents | Agent-room task execution; retrieval; planning; summarization; bounded tool calls; human approval | Room tasks; model requests; input/output tokens; tool calls; context-window size; approval/edit events; errors | The current page communicates an agent workspace but does not execute agents or LLM calls. |
| Kinetic Mesh | Workflow trigger; external API/webhook actions; database steps; optional LLM classification or routing | Workflow runs; steps per run; API calls; webhook retries; database operations; LLM input/output tokens only for AI steps; failed runs | The current page is a visual operations concept. Do not describe it as a live automation runner until execution infrastructure is connected and tested. |
| Folio Forms | Structured brand brief intake; copy/voice generation; optional asset transformation or generation; human editing | Brief submissions; input/output tokens; generated variants; asset jobs; files/bytes; human edits; retry/error counts | The current page presents a brand-system concept and local CTA notifications, not a working generator. |
| Peregrine Editions | Product catalogue lookup; viewing/enquiry form; CRM handoff; optional recommendation assistant | Catalogue reads; enquiry submissions; files/bytes if used; CRM calls; response latency; LLM tokens only if a recommendation feature is explicitly added | The current route is an editorial object catalogue concept. No purchase, enquiry, CRM, or LLM system is wired in. |

## What is connected now

The five routes are connected to the public catalogue as navigable product routes. They are not connected to functional product backends. In particular, current route code shows no `fetch`, tRPC query/mutation, `invokeLLM`, `onSubmit`, mail send, or external API call for these five pilot pages. Their visible CTA behavior is local presentation behavior.

## Recommended pilot order

For a real pilot, **Ember Signal — Mail Pilot** should be treated as a product-naming decision first: the current source describes AI marketing intelligence, not an email client. If the intended product is campaign intelligence, keep the current feature language and add evidence ingestion plus brief generation. If the intended product is mail operations, define the mailbox provider, permissions, sending safeguards, unsubscribe handling, and audit trail before using “Mail Pilot” as a functional promise.

After that decision, Kinetic Mesh is the most integration-heavy pilot because workflow execution, API/webhook reliability, retries, permissions, and observability are required. Selene Agents and Folio Forms can follow with bounded LLM actions and human approval. Peregrine Editions is the lightest technical pilot if it remains a catalogue and enquiry surface without AI recommendations.

## Explicit exclusions

This review does not estimate Manus credits, provider prices, token budgets, billing, or account usage. It does not activate APIs, LLMs, mail, payment, checkout, webhooks, automated delivery, or background sync. It also does not certify commercial/IP clearance or legal readiness.
