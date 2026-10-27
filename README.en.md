# Claude skills for writing in Ukrainian

[Українська](README.md) · **English**

Two Claude skills that help write Ukrainian text that doesn't read like a
translation or machine output: no calques, no bureaucratese, no AI clichés.
Each skill is a separate plugin, so you can install one or both.

The skills themselves are written in Ukrainian and are meant for Ukrainian text.

| Plugin | Purpose |
|---|---|
| `ukrainian-tech-docs` | Technical documentation: a work contract before writing, source discipline and uncertainty markers, living language, genre rules (HLD, LLD, ADR, technical specification (ТЗ), how-to and runbook, concept, reference, troubleshooting, postmortem, diagram, plan), questions to adjacent teams, export to .docx, .xlsx, .pdf or email. Inputs to prepare (in Ukrainian): [docs/ukrainian-tech-docs-inputs.md](docs/ukrainian-tech-docs-inputs.md); what each genre is and how to ask for it (in Ukrainian): [docs/ukrainian-tech-docs-genres.md](docs/ukrainian-tech-docs-genres.md) |
| `ukrainian-fiction` | Fiction prose: language without calques and AI clichés, orthography and euphony, sentence and paragraph, dialogue, scene and chapter structure, audit of a finished text. Also works for checking text that is already written, your own or generated. Book-specific rules (characters, glossary, lore, tone) are not part of the skill; they should come from a book profile |

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
- **Two genres, two skills.** Technical text and fiction follow different
  rules: a character's colloquial line or a deliberate repetition in prose is
  a device, not a defect.

## How it is tested

Test sets live in [tests/](tests/). The technical skill has 22 synthetic
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

A skill activates on its own when you ask to write, review or clean up
Ukrainian text of the matching genre.

### Claude Desktop and claude.ai

With a chat open (not the Code tab), go to Settings → Plugins, choose Add →
add marketplace and enter `alexgorby/claude-skills` or
`https://github.com/alexgorby/claude-skills` as the URL. Both plugins then
appear on the Browse tab; Add installs the one you need.

Where you add it from matters. A marketplace added from chat is saved to your
claude.ai account, and the plugins work in chat, Cowork and Claude Code. Added
while the Code tab is active, it stays on that computer and chat won't see it.

Updates are manual: Plugins → "⋮" next to the plugin → check for updates → Update.

Alternatively, upload a skill as an archive: Settings → Skills → add custom
skill. `pwsh ./build.ps1` builds the archives into `dist/`. Don't keep the
plugin and an uploaded copy of the same skill at once: Claude would see two
identical skills.

### Other agents

A skill is a plain folder with `SKILL.md`. Copy it into the skills folder of
any agent that supports this format.

## Repository layout

```
.claude-plugin/marketplace.json     plugin catalog
plugins/
  ukrainian-tech-docs/
    .claude-plugin/plugin.json
    skills/ukrainian-tech-docs/     SKILL.md, references/, templates/
  ukrainian-fiction/
    .claude-plugin/plugin.json
    skills/ukrainian-fiction/       SKILL.md, references/, templates/
build.ps1                           builds zips for manual upload
```

## Sources

The rules are written from scratch in Ukrainian. Some ideas come from research
and other people's skills; English-specific rules were carried over only where
they work for Ukrainian. The full list with links is in the "Джерела пакета"
(Sources) section of each skill's `SKILL.md`.

## License

[MIT](LICENSE): free to use, modify and distribute, keeping the copyright notice.

## Author

[alexgorby](https://github.com/alexgorby). Maintenance notes (in Ukrainian): [MAINTAINING.md](MAINTAINING.md).
