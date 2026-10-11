# claude-skills

Головна редакція власних скілів Claude, оформлена як маркетплейс плагінів:
кожен скіл — окремий плагін, тож їх можна ставити й публікувати незалежно.

| Плагін | Скіл | Шлях |
|---|---|---|
| `ukrainian-tech-docs` | Письмо технічної документації українською | `plugins/ukrainian-tech-docs/skills/ukrainian-tech-docs/` |
| `ukrainian-fiction` | Письмо художньої прози українською | `plugins/ukrainian-fiction/skills/ukrainian-fiction/` |

Маркетплейс — `.claude-plugin/marketplace.json`, назва `alexgorby-skills`.
Поле `version` свідомо не задано: встановлені копії оновлюються за комітами.

## Встановлення

Claude Code:

```
/plugin marketplace add alexgorby/claude-skills
/plugin install ukrainian-tech-docs@alexgorby-skills
/plugin install ukrainian-fiction@alexgorby-skills
```

Поки репозиторій приватний, git на машині має вже мати збережений доступ до
GitHub (SSH-ключ в `ssh-agent` або Git Credential Manager).

Claude Desktop без маркетплейсу: `pwsh .\build.ps1` → `dist\<скіл>.zip` →
налаштування → Skills → додати власний скіл.

## Порядок зміни

1. Правка в теці скіла — лише після погодження власника.
2. Коміт; повідомлення каже, що змінено й навіщо.
3. `claude plugin validate .` — без помилок (попередження про `version` очікуване).
4. Push — на слово власника. Для ручного завантаження — `build.ps1`; архів
   збирається лише з закоміченого стану.

`dist/` у git не входить.

## Вихідний стан

Перший коміт — версії, що були завантажені в Claude на 2026-10-11
(`ukrainian-tech-docs` v10 від 24.09, `ukrainian-fiction` від 07.10), узяті з
синхронізованої копії `~/.claude/skills/synced/…`. Синхронізована копія
`ukrainian-tech-docs` новіша за останній архів у `Downloads`
(`ukrainian-tech-docs_10.zip`): у `references/genres/hld.md` додано групу
«Експлуатація й нефункціональні вимоги». У `ukrainian-fiction/SKILL.md` поле
`description` взято з архіву: Claude при завантаженні переписав його в один
рядок, зміст той самий.

Джерела ідей — розділ «Джерела пакета» в `SKILL.md` кожного скіла. Ідеї для
наступних правок — нота волту
`00 Inbox/Доповнення скілів — ідеї з чужих скілів — 2026-10-11.md`.
