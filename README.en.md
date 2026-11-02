# Claude skills for writing in Ukrainian

[Українська](README.md) · **English**

Two Claude plugins that help write Ukrainian text that doesn't read like a
translation or machine output: no calques, no bureaucratese, no AI clichés.
The technical plugin has seven skills, the fiction plugin one. You can install
one plugin or both.

The skills themselves are written in Ukrainian and are meant for Ukrainian text.

| Plugin | Purpose |
|---|---|
| `ukrainian-tech-docs` | Technical documentation — a dispatcher and six skills: writing, language check, fact-checking, export, planning, multi-agent review. A work contract before writing, source discipline and uncertainty markers, living language, genre rules (HLD, LLD, ADR, technical specification (ТЗ), how-to and runbook, concept, reference, troubleshooting, postmortem, diagram, plan), questions to adjacent teams, export to .docx, .xlsx, .pdf or email. Inputs to prepare (in Ukrainian): [docs/ukrainian-tech-docs-inputs.md](docs/ukrainian-tech-docs-inputs.md); what each genre is and how to ask for it (in Ukrainian): [docs/ukrainian-tech-docs-genres.md](docs/ukrainian-tech-docs-genres.md) |
| `ukrainian-fiction` | Fiction prose: language without calques and AI clichés, orthography and euphony, sentence and paragraph, dialogue, scene and chapter structure, audit of a finished text. Also works for checking text that is already written, your own or generated. Book-specific rules (characters, glossary, lore, tone) are not part of the skill; they should come from a book profile |

## What it can do

The matching skill activates on its own when a request resembles one of these. The
skills expect Ukrainian requests; the English in brackets is for orientation
only.

### ukrainian-tech-docs

The package has six skills, each doing one job. A request covering several
jobs at once («підготуй документ для Замовника», *prepare the document for
the customer*) goes to the dispatcher, which names the skills and their order.

| Task | How to ask | Skill |
|---|---|---|
| Write a document of a given genre | «Напиши ADR про вибір …» *(write an ADR on choosing …)*, «покрокова інструкція для …» *(step-by-step guide for …)*, «ТЗ на …» *(specification for …)* | `write` |
| Rewrite a document, turn notes into a note | «Перепиши документ» *(rewrite the document)*, «оформи як нотатку» *(format as a note)* | `write` |
| Translate technical text | «Переклади українською» *(translate into Ukrainian)* | `write` |
| Draft questions to an adjacent team | «Сформулюй питання до мережевиків про …» *(draft questions to the network team about …)* | `write` |
| Clean text of AI clichés, bureaucratese and calques without touching the meaning | «Почисти текст» *(clean up the text)*, «прибери воду» *(cut the fluff)* | `language` |
| Find calques without editing | «Діагностика кальок» *(calque diagnostics)*, «перевір переклад» *(check the translation)* | `language` |
| Check a finished specification | «Перевір ТЗ» *(check the spec)* | `language` |
| Check claims against documentation | «Фактчекінг» *(fact-check)*, «перевір факти» *(check the facts)*, «звір із документацією» *(verify against the docs)* | `factcheck` |
| Build a file for readers outside the team | «Збери docx» *(build a docx)*, «оформи як лист» *(format as an email)* | `export` |
| Draft a work plan | «Спершу план» *(plan first)*, «склади план» *(make a plan)* | `plan` |
| Independent review of a plan or document | «План готовий» *(the plan is ready)*, «перевір незалежно» *(check independently)*, «рецензія HLD» *(HLD review)* | `review` |
| Check that it reads without the author | «Тест читача» *(reader test)*, «чи зрозуміло це без мене» *(is it clear without me)* | `review` |

`review` hands a plan or document to several narrow reviewer agents:
coherence, feasibility, a decision adversary, security, architecture, network
and others. A separate coordinator agent picks the reviewers, and each sees
only the subject, not the conversation that produced it. Findings on a
document also go through an adversary pass, and the main session checks each
one against its source. Where subagents are unavailable, the review runs in
one session and is marked as not independent.

**Genres.** Each has its own structure rules and checklist.

| Genre | What goes in it |
|---|---|
| HLD | Concepts, decisions, trade-offs; no values of a specific build |
| LLD | Values, addresses, parameters and step order following from HLD decisions |
| ADR | One architecture decision with options and the trade-off |
| Specification (ТЗ) | What is needed and how it is accepted: executable items only, no open questions |
| How-to, runbook, procedure | Steps with verification and rollback |
| Step-by-step guide | Actions only, for a reader doing them for the first time: verified prerequisites, step by step |
| Concept | How a component works |
| Reference | Tables, data schemas, codes; no prose |
| Troubleshooting | A case record, symptom first |
| Postmortem | Closing an incident after service is restored |
| Security document | How the system is protected: access, secrets, network surface, data, supply chain |
| Diagram | Topology and mechanism, legible in print |
| Plan | Only when asked: «спершу план» *(plan first)*, «склади план» *(make a plan)* |
| Email, message, note, README | General rules: one document, one task; an email is a slice of the working document for one recipient |

Each genre in detail and how to ask for it (in Ukrainian):
[docs/ukrainian-tech-docs-genres.md](docs/ukrainian-tech-docs-genres.md).

### ukrainian-fiction

| Task | How to ask |
|---|---|
| Write a scene or a chapter | «Напиши сцену …» *(write a scene …)*, «для наступної глави …» *(for the next chapter …)* |
| Clean a chapter of AI clichés | «Почисти главу» *(clean up the chapter)*, «прибери ШІ з тексту» *(remove the AI from the text)* |
| Check a text, your own or generated | «Чи звучить це як ШІ?» *(does this sound like AI?)*, «перевір мій текст» *(check my text)*, «перевір згенерований текст» *(check the generated text)* |
| Find calques | «Діагностика кальок у главі» *(calque diagnostics in the chapter)* |
| Check one level only | «Перевір будову глави» *(check the chapter structure)*, «перевір тільки діалоги» *(check the dialogue only)* |
| Read a chapter as a reader would | «Тест читача» *(reader test)*, «прожени главу очима читача» *(run the chapter past a reader)* |

The audit returns a table of findings, not a rewritten text: the author
decides what to change.

## Skills in detail

What each skill does, what it returns and what it does not do. The skills
answer in Ukrainian, so the request-and-answer examples are in the Ukrainian
README, section «Скіли докладно» ([README.md](README.md#скіли-докладно)); each
item below says what its example shows. The examples come from runs on
02.11.2026 over synthetic texts (a made-up product «Ліхтар», invented notes).

### Dispatcher — `ukrainian-tech-docs`

Takes over when a request covers several jobs at once or it is unclear which
skill fits. It names the skills needed, their order and why; the work itself
is done by those skills. Ambiguous requests are settled by a table: "rewrite
the document" is writing, "clean up the text" is language, "check the spec" is
a specification audit, an unnamed text type gets one question to the owner.
*Example:* "prepare a docx for the customer from a two-sentence HLD draft" —
write, then fact-check only if vendor claims appear, review offered but not
started, export with a full language pass first; plus a question whether to
list open questions before writing.

### Writing — `write`

Writes and edits a document of any genre: HLD, LLD, ADR, specification,
runbook, step-by-step guide, postmortem, email, note, translation, diagram,
questions to an adjacent team.

- **Contract** — seven lines before the first line of text: genre, reader,
  whether the document leaves the team, depth boundary (what stays in the HLD
  and what goes to the LLD), sources, what is out of scope, which stages the
  work goes through. An objection changes a line.
- **Project profile** — one file in your project that gives the glossary, code
  register, source ladder and where the question register lives. No profile —
  the skill says so and invents nothing.
- **Sources** — every platform claim carries a source address where it stands.
  What the sources lack is not in the text: an uncertainty marker or a question
  goes there instead.
- **Forks and questions** — when a decision is not the writer's, the skill
  gives options with the cost of each, an addressee and a recommendation.
- **Self-check** — the genre checklist, a final language pass, a list of claims
  without a source, a marker summary and a stages line.

Writing never offers a plan; planning starts only when you ask.
*Example:* an HLD fragment from a decision record — the contract table with
an explicit depth exception, the fragment, two questions with options and a
recommendation, and the stages line.

### Language check — `language`

Checks a finished text and does not edit it unless asked. Modes:

| Mode | Returns |
|---|---|
| Language audit | A findings table: where, quote, rule number, level (S1 fixed on first occurrence, S2 when it clusters, S3 only in a cleanup), suggested replacement |
| Cleanup ("clean up the text", "cut the fluff") | The cleaned text, a table of what was done and a check that no meaning was lost or added |
| Whole-document audit | An extra table for completeness, genre boundary, security |
| Calque diagnostics | A table of suspects: word, calque type, English original, replacement, confidence; the verdict is yours |
| Specification audit | A table "spec line · what is wrong · suggested fix · source" |
| Final pass | A pass over a finished text before it goes out; writing and export require it |

It does not check facts (`factcheck`) or judge decisions (`review`). A cleanup
that touches a claim or the meaning is writing.
*Example:* "cut the fluff, add no facts" on a three-sentence note — the
evaluative sentence is removed, the table names rule 1.4 (S1 and S2), the
meaning check says nothing was added, and a question asks for a number if
"fast processing" is a real requirement.

### Fact-checking — `factcheck`

Checks claims in a finished text against vendor documentation and project
sources: is the claim true today, for which version and edition. Capabilities,
limits, requirements, compatibility, versions, command parameters; claims with
"always", "only", "automatically", "supported" go first. Returns a table of
claims with status, evidence, source address and the cost of an error; you fill
in the verdict column. It does not edit the text: a fix is a separate writing
job. The exception is a step-by-step guide, where an obvious fix from a source
is made and listed.
*Example:* three claims about «Ліхтар» 2.0 — one confirmed, two refuted with
quotes from the source, verdict column left empty.

### Export — `export`

Prepares a document for a reader outside the team: `.docx`, `.xlsx`, `.pdf`,
email or message. Removes working traces from the final text, formats links,
tables and diagrams, resolves markers. The last step before the build is a
full language pass over the final text; a pass made before later edits does
not count. If the export changes meaning, it is also writing. The plugin hook
stops a turn that built the file without that pass.
*Example:* building `note.docx` — the hook caught that the language pass came
before the text was written to `note.md`; the pass was repeated, and the file
was not rebuilt because the text had not changed.

### Planning — `plan`

Starts only when you ask ("plan first", "make a plan"); no skill offers it. A
plan records the task verbatim and completion criteria that can be checked by
observation. Before full work comes a short "plan for the plan": what to read,
what to extract, what to check against, what the result looks like, what not
to do; at this checkpoint you say "yes" or "skip". Steps take the form
"step · output · state", and a step closes only with evidence. A change of
the task is added as a delta, not a rewrite. When you say the plan is ready,
review checks it.
*Example:* moving a queue service from one VM to two to survive a node
failure — criteria, reconnaissance, eight steps, and five questions with
recommendations (is a "node" a host or a VM?).

### Review — `review`

An independent check of a plan or a document by several agents that did not
see the conversation that produced it. A separate coordinator agent picks
narrow reviewers: coherence, feasibility, scope, decision adversary, security,
operations, architecture, network, platform, capacity, requirements, diagrams,
reality check. A plan has a ceiling: up to five reviewers for a short plan, up
to seven for a larger one. For a document, a separate adversary agent checks
every finding (is the quote verbatim, is the severity inflated, is it already
known). A large document is split among reviewers. The main session checks
each finding against its source, rejects false ones with a reason and builds
the report. It does not edit the text: fixes go through writing.

A separate light mode is the **reader test**: one fresh agent reads the
document without context and says what the named reader would not understand.
*Examples:* a four-step plan to move backups to Azure Backup — three blockers
(no trial restore before switching the old script off, no Recovery Services
vault, no passphrase owner) and one finding rejected against Microsoft Learn;
a reader test of a four-step runbook — the document answers one of eight
reader questions.

### ukrainian-fiction

One skill for all fiction work. It holds no book-specific rules: the book
profile gives them (voice canon, reference passages, glossary, fact canon).
No profile — the skill says what is missing and invents nothing. Plot, turns
and the characters' behaviour are the author's: the skill offers options with
a mechanism and a consequence, not a ready paragraph instead of a question.

| Function | What it does |
|---|---|
| Structure | Analyses or plans a scene, episode or chapter at plot level |
| Writing | A new scene or an edit in the book's voice; reads the reference passages and the end of the previous chapter first |
| Audit | A findings table with rule, option and confidence; the author decides what to fix. "Clean up" is an audit with language edits |
| Calque diagnostics | A table of suspects with the norm; edits nothing |
| Reader test | How a reader without context will read the text; never starts on its own, edits nothing |

*Example:* "does this sound like AI?" on a three-sentence passage — a ready
image, a paired abstraction, a filter word and a Russian calque, each with a
rule number and an option. The full example is in
[docs/examples.md](docs/examples.md).

## What it looks like

> **Before:** Варто зазначити, що резервне копіювання відіграє ключову роль
> у забезпеченні надійності інфраструктури. Здійснення резервного копіювання
> відбувається щоночі за допомогою скрипта `backup.ps1`, що дозволяє мінімізувати
> ризики втрати даних. Таким чином, наше рішення є надійним, масштабованим
> і гнучким.
>
> *("It is worth noting that backup plays a key role in ensuring infrastructure
> reliability. The performing of backup takes place nightly by means of the
> `backup.ps1` script, which allows minimising the risks of data loss. Thus, our
> solution is reliable, scalable and flexible.")*
>
> **After:** Резервну копію щоночі знімає скрипт `backup.ps1`.
> *("The `backup.ps1` script takes a backup every night.")*
>
> **Question to the author:** how much data can this scheme lose (RPO), and how
> long does a restore take? The reliability sentence was removed because it
> stated no fact.

Every finding cites a rule number: `1.1 · S1` is an empty opener, `1.2 · S2` a
verbal noun, `1.9 · S2` a forced triad. The full breakdown and a fiction audit
example (in Ukrainian): [docs/examples.md](docs/examples.md).

## What makes it different

- **Asks instead of inventing.** Whatever the text lacks (a number, a name, a
  scene detail) becomes a question to the author, not a plausible insertion.
- **Meaning over style.** After a cleanup the skill compares the result with
  the original: no lost fact, condition, constraint or uncertainty marker.
- **Weighted signs.** Not every sign is a defect: some are fixed on first
  occurrence, others only when they cluster. This keeps the skill from
  scrubbing a living author's voice.
- **Calques in a separate pass.** A table of suspects with the norm and a
  confidence level; the verdict is the author's. Disputed pairs were checked
  against dictionaries.
- **No step gets lost.** Every skill ends with a stages line listing the
  files it actually read, so a skipped stage shows. If a turn built a .docx,
  .xlsx or .pdf without a language pass over the final text, a plugin hook
  stops the turn and asks for that pass.
- **Two genres, two plugins.** Technical text and fiction follow different
  rules: a character's colloquial line or a deliberate repetition in prose is
  a device, not a defect.

## How it is tested

Test sets live in [tests/](tests/). The technical plugin has 24 synthetic
cases: language editing and audit, sources and fact-checking, genres and
export, plus texts that need no edits. Fiction has 6 human-written passages
the skill must not "fix". Criteria were fixed before the first run, and the
executor never sees them.

Did the skill flag something that is not a defect? Open an issue with the
"False positive" template: a confirmed case becomes a counterexample in the
rule itself.

## Installation

### Claude Code

```
/plugin marketplace add alexgorby/claude-skills
/plugin install ukrainian-tech-docs@alexgorby-skills
/plugin install ukrainian-fiction@alexgorby-skills
```

The skills activate on their own when you ask to write, review or clean up
Ukrainian text of the matching genre.

### Claude Desktop and claude.ai

With a chat open (not the Code tab), go to Customize → Plugins, choose Add →
add marketplace and enter `alexgorby/claude-skills` or
`https://github.com/alexgorby/claude-skills` as the URL. Both plugins then
appear on the Browse tab; Add installs the one you need.

Where you add it from matters. A marketplace added from chat is saved to your
claude.ai account, and the plugins work in chat, Claude Code and Cowork (where available). Added
while the Code tab is active, it stays on that computer and chat won't see it.

Updates are manual: Plugins → "⋮" next to the plugin → check for updates → Update.

When you add or update the technical plugin, Claude Desktop warns that it
"contains components that run code". This is the hook
`hooks/check_language_pass.py`. At the end of every Claude turn in sessions on
your computer it reads the current session's transcript. If the turn built a
`.docx`, `.xlsx` or `.pdf` and there was no language pass after the last text
change, the hook sends Claude a request to run one; otherwise it does nothing.
The hook changes no files and makes no network calls. It runs via the `python`
command, so Python must be on `PATH`.

Review agents and the language-pass hook work in both Claude Code and Claude
Desktop chat: a test on 02.11.2026 showed this, although Anthropic's
compatibility table lists them as ignored in chat. claude.ai chat in a browser
has not been tested separately.

Alternatively, upload the skills as archives: Customize → Skills → add custom
skill. `pwsh ./build.ps1` builds them into `dist/`: seven archives for the
technical package, one per skill, each with its own copy of the shared rules.
Archives carry no agents and no hook: the review runs without subagents, and
only the stages line guards the language pass before export. Uploading the
archives has not been tested: a claude.ai support article gives a 200-character
limit for a skill description, and the package's descriptions are longer. Don't
keep the plugin and an uploaded copy of the same skill at once: Claude would see
two identical skills.

### Codex

Codex reads the same marketplace; there is no separate edition for it:

```
codex plugin marketplace add alexgorby/claude-skills
codex plugin add ukrainian-tech-docs@alexgorby-skills
codex plugin add ukrainian-fiction@alexgorby-skills
```

`codex plugin marketplace upgrade` refreshes the marketplace snapshot.

Tested 27.10.2026, Codex 0.164, on the earlier single-skill layout: the skill
activates and reads its rules, but the report follows them only partly. The
six-skill layout has not been tested in Codex as a plugin yet; agents and the
hook likely don't work there.

### Other agents

A skill is a plain folder with `SKILL.md`. The technical skills read the
plugin's shared `shared/` folder, so outside the plugin take the folder from an
archive built by `build.ps1`, which already has `shared/` inside.

## Repository layout

```
.claude-plugin/marketplace.json     plugin catalog
plugins/
  ukrainian-tech-docs/
    .claude-plugin/plugin.json
    skills/ukrainian-tech-docs/     dispatcher: which skill, in what order
    skills/write/                   writing: contract, project profile, stages
    skills/language/                language check and audit
    skills/factcheck/               fact-checking
    skills/export/                  export to .docx, .xlsx, .pdf, email
    skills/plan/                    planning
    skills/review/                  multi-agent review
    shared/                         language.md, evidence.md, genres/, profile template
    agents/                         reviewers for review
    hooks/                          language-pass check before export
  ukrainian-fiction/
    .claude-plugin/plugin.json
    skills/ukrainian-fiction/       SKILL.md, references/, templates/
build.ps1                           builds zips for manual upload, one per skill
```

## Sources

The rules are written from scratch in Ukrainian. Some ideas come from research
and other people's skills; English-specific rules were carried over only where
they work for Ukrainian. The full list with links is in the technical plugin's `SOURCES.md` (for the
review, also the "Джерела" section of `skills/review/SKILL.md`) and in the
"Джерела пакета" (Sources) section of the fiction skill's `SKILL.md`.

## License

[MIT](LICENSE): free to use, modify and distribute, keeping the copyright notice.

## Author

[alexgorby](https://github.com/alexgorby). Maintenance notes (in Ukrainian): [MAINTAINING.md](MAINTAINING.md).
