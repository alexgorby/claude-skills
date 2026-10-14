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
