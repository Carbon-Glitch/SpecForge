# Reality Research

- Product idea: AI meeting notes for sales teams
- Status: demo-complete
- Stage: gate1
- Research status: verified-demo-sample

## Research Status

This demo uses a small public-source sample to show SpecForge's expected evidence format. A production pack should expand the source list before final stack selection.

## Market Reality

AI meeting notes are a crowded product category. The strongest wedge for this concept is not generic summarization; it is sales-specific structured follow-up, CRM sync, review-before-write, and transcript-grounded evidence.

## Competitors And Substitutes

| Product / Project | Type | Relevant signal |
|---|---|---|
| Meetily | open-source local-first app | Public repo and site emphasize local processing, transcription, diarization, and summarization. |
| OpenWhispr | open-source desktop voice-to-notes | Shows market interest in local/offline voice capture and note/action generation. |
| Vexa | open-source meeting transcription API | GitHub topic page shows active open-source bot/API approaches for Teams, Meet, and Zoom. |
| Manual CRM notes | substitute | Still common when teams need control and review before syncing. |

## User Behavior Evidence

- Users care about privacy and data control for recorded meetings, especially when calls include customer or regulated information.
- Sales workflows require structured fields, not only prose summaries.
- Review-before-sync reduces the risk of incorrect CRM updates.

## Official Documentation Findings

| Source | Finding |
|---|---|
| OpenAI Whisper GitHub | Whisper is an open-source speech recognition model with multilingual transcription and translation capabilities. |
| OpenAI Whisper announcement | Whisper was trained for robustness across accents, noise, and technical language. |

## GitHub And Open Source Findings

| Candidate | Reuse decision | Reason |
|---|---|---|
| `openai/whisper` | extract pattern / optional model backend | Good reference for speech recognition capability, but product needs app workflow, review UI, and CRM sync. |
| `ggml-org/whisper.cpp` | integrate or wrap | Suitable for local/offline transcription experiments. |
| `Zackriya-Solutions/meetily` | extract pattern | Useful local-first architecture reference; do not fork for sales CRM workflow without deeper license and code review. |
| `Vexa-ai/vexa` | evaluate API integration later | Bot/API model may fit live meetings, but MVP starts with upload. |

## Open Source Reuse Decisions

| Subsystem | Decision | Notes |
|---|---|---|
| Transcription | wrap existing engine | Start with pluggable adapter for cloud or local engines. |
| Summarization | build prompt/eval layer | Needs sales-specific schema and transcript citations. |
| CRM sync | build minimal adapter | Product value is controlled write workflow. |
| Review UI | build | Needs domain-specific confidence and citation display. |

## Risk And Compliance Findings

- Meeting audio and transcripts may contain sensitive customer data.
- Recording consent must be handled outside the summarizer; the product should surface consent metadata and retention policy.
- CRM writes are external side effects and must require explicit user approval.

## Implementation Prior Art

- Local-first open-source tools show a viable privacy wedge.
- Whisper-family tools show that transcription can be modularized behind an adapter.
- Meeting bot products add complexity; upload-first MVP is safer.

## Rejected Options

| Option | Rejection reason |
|---|---|
| Start with auto-joining meeting bot | Too much platform and consent complexity for MVP. |
| Sync AI notes directly to CRM without review | Risky external side effect. |
| Build speech recognition from scratch | Existing open-source engines are strong enough to wrap or evaluate first. |

## Sources

| ID | Source | URL | Claim supported |
|---|---|---|---|
| SRC-001 | Meetily GitHub | https://github.com/Zackriya-Solutions/meetily | Local-first open-source AI meeting note taker positioning. |
| SRC-002 | Meetily site | https://meetily.ai/ | Local processing and privacy positioning. |
| SRC-003 | OpenAI Whisper GitHub | https://github.com/openai/whisper | Whisper speech recognition capability and license signal. |
| SRC-004 | OpenAI Whisper announcement | https://openai.com/index/whisper/ | Whisper robustness and multilingual capability claim. |
| SRC-005 | whisper.cpp GitHub | https://github.com/ggml-org/whisper.cpp | Local C/C++ Whisper implementation option. |
| SRC-006 | GitHub meeting-notes topic | https://github.com/topics/meeting-notes | Active open-source meeting-notes projects and API/bot patterns. |
