# Reviewer roster for the review skill

The coordinator reads this file and the subject (a plan, or a document's table
of contents and introduction), then picks reviewers. Each entry states when to
activate the reviewer and, where it matters, when NOT to. Activate on what the
subject text shows, not on what the topic might involve. Narrow reviewers are
preferred: a reviewer whose subject is absent from the text is not taken.

Selection logic and several conditions are adapted from Compound Engineering,
`skills/ce-doc-review/references/persona-selection.md`
(https://github.com/EveryInc/compound-engineering-plugin, MIT). Document lenses
come from the author's own multi-agent HLD review method.

The task tells you the subject type: `plan`, `ADR`, or `document` with its
genre (HLD, LLD, ТЗ, runbook, concept, report…), and for a document its size.

## Plan

### Always

| Reviewer | Agent | Lens |
|---|---|---|
| Coherence | `review-coherence` | The plan does not contradict itself |
| Feasibility | `review-feasibility` | The plan can be started without decisions it should have made; what already exists; past lessons recorded in the project |

### Always for a plan (skip only for a single ADR)

| Reviewer | Agent | Lens |
|---|---|---|
| Scope | `review-scope` | Size fits the goal; every new entity earns its keep |

### Conditional

| Reviewer | Agent | Activate when the plan shows ANY of | Do NOT activate when |
|---|---|---|---|
| Adversary | `review-adversary` | a new abstraction, tool, framework or architectural pattern; an irreversible action (deletion, migration, production change, public release); an explicit alternatives section or unresolved trade-off; a goal that was not agreed before the plan (no source decision, task or request is cited) | a routine plan inside an already agreed goal, with no new abstraction and nothing irreversible. A well-argued plan is not a trigger by itself |
| Security | `review-security` | access rights, roles, credentials, secrets, tokens, keys; personal or customer data; network exposure or a new external integration (trust boundary); a public repository or publishing outside the owner's machine; actions on a physical home system (heating, power, locks) | ordinary data handling that does not change who can read or write it; local read-only scripts that send nothing anywhere |
| Operations | `review-operations` | the result lives longer than one session: a script run more than once, an automation, a scheduled task, a service, a dashboard, a skill or agent | a one-off analysis, a document with no running part |
| Reality check | `review-reality` | the plan relies on an external tool, library, API, product version, limit, price or a third-party claim (a video, post, blog) | everything the plan relies on is already in the project and was used before. Tools, scripts and commands named in the project's own rules (`MAINTAINING.md`, `CLAUDE.md`, the project map) count as already in the project: checking the plan against them is Feasibility's job |
| Requirements | `review-requirements` | the plan cites a task, specification or request with explicit requirements or acceptance conditions | the goal is a single sentence with no listed requirements |
| Architecture | `review-architecture` | the plan changes infrastructure: components, clusters, availability, failure domains, scaling | the plan touches no running infrastructure |
| Network | `review-network` | the plan changes network topology, VLANs, routing, firewall rules, DNS or connectivity | no network change |
| Platform | `review-platform` | the plan changes cloud or hybrid dependencies: Azure resources, Arc, subscriptions, management plane | no cloud dependency changes |
| Capacity | `review-capacity` | the plan adds load, moves workloads, or needs temporary capacity (migration, snapshot, backup before a change) | no resource impact |

## Document

### Ceiling and scope of judgement

- The task names a ceiling: the maximum number of agents including the
  Verifier. For a document within one reader's limit, a partial run, an ADR or
  a single chapter the ceiling is five. Never return more `yes` rows than the
  ceiling.
- Under a ceiling, rank the conditional reviewers by how strong their signal is
  in the text and take the strongest. A borderline reviewer is NOT taken under
  a ceiling: say which taken reviewer covers its subject (network inside an
  isolation chapter — Security; diagrams — Coherence).
- In a partial run judge only the selected parts named in the task. A signal
  that appears only in parts outside the run (another chapter, the
  introduction's overview) is not a signal.
- A derivative document (summary, digest for management) gets only Coherence,
  checked against its source document in both directions.

### Always for a document

| Reviewer | Agent | Lens |
|---|---|---|
| Coherence | `review-coherence` | Parts of the document do not contradict each other |
| Verifier | `review-verifier` | Runs after the others: checks every finding (quote, level, already known, severity) |

### Conditional

| Reviewer | Agent | Activate when the document shows ANY of | Do NOT activate when |
|---|---|---|---|
| Structure | `review-structure` | a table of contents, appendices, a sources section, a register of open questions, or more than five sections | a short single-section document (one ADR, one note) |
| Feasibility | `review-feasibility` | the document is meant to be implemented or followed: HLD, LLD, ТЗ, runbook, procedure, step-by-step | a report, a concept explanation, a summary |
| Scope | `review-scope` | the genre has a boundary with a neighbouring genre (HLD/LLD, ADR, ТЗ) or the document has an "out of scope" section | a report or a summary |
| Adversary | `review-adversary` | the document records architectural decisions with alternatives or trade-offs; every ADR | the document only describes an existing installation |
| Requirements | `review-requirements` | the task or the project profile names a baseline requirement set, or the document cites requirements, technical conditions or a specification it must satisfy | no requirement source exists; say so in the reason |
| Architecture | `review-architecture` | the document describes components, availability, failure domains, scaling or fault tolerance | no system design in the text |
| Operations | `review-operations` | the document describes a system someone must deploy, update, monitor, back up or restore | a decision record with no running system |
| Security | `review-security` | identity, access, roles, secrets, encryption, isolation, trust boundaries, audit | none of these appear |
| Network | `review-network` | network topology, VLANs, routing, traffic classes, connectivity, DNS | none of these appear |
| Platform | `review-platform` | cloud or hybrid dependencies: Azure services, Arc, control or management plane, behaviour when the cloud is unreachable | a purely on-premises design with no cloud dependency |
| Capacity | `review-capacity` | hardware requirements, sizing, capacity, resiliency overhead, growth | none of these appear |
| Diagrams | `review-diagrams` | the document contains or links diagrams (`.drawio`, `.svg`, images) | no diagrams |

`review-reality` is never taken for a document: checking a document's claims
against vendor documentation is a separate fact-checking pass.

## Domain experts (activate by project, at most one)

Domain agents are not part of this plugin. A project that has one names it in
its profile, slot "Рецензія" (agent name and when to activate it). The task
then carries that line. Activate the domain expert only under the condition the
profile states, and only for the project of this subject. No such line in the
task — no domain expert.

For a document under a ceiling, or larger than one reviewer's reading limit
(about 170 KB), a domain expert's lenses are covered by Architecture, Platform,
Requirements and the cross-check, unless the profile says otherwise.

## Second model (decided by the main session, not by you)

The whole-plan review on Codex (OpenAI) depends on data sensitivity, which only
the owner classifies. Do not select or reject it. Mention nothing about it.

## Output

Return exactly this table, one row per reviewer in the section for the subject
type (domain experts: only the one for this project, if any):

| Reviewer | Take | Reason (max 15 words, quote the subject where possible) |
|---|---|---|

`Take` is `yes` or `no`. Every `no` for a conditional reviewer names which
activation signal is absent. Do not research, do not review the subject, do
not suggest changes, do not split the document into parts — the main session
does that.
