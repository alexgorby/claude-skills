# Джерела пакета

Дослідження і готові скіли, на основі яких укладено правила пакета
`ukrainian-fiction`.
Посилання на скіли закріплено на коміті, щоб текст за адресою не змінився.

- Russell та ін., «StoryScope: Investigating idiosyncrasies in AI fiction»,
  [arXiv 2604.03136v6](https://arxiv.org/html/2604.03136v6).
  Розмір тестового набору стаття подає по-різному: у §3 — 1 377 запитів
  (8 262 оповідання), у дод. D — 1 384 (8 301). Дод. H і табл. 13 узгоджені
  з §3. У правила пакета це число не входить.
- Sepia, прохід будови оповіді й прохід стилю, MIT:
  [narrative-pass.md](https://github.com/Nanako0129/sepia/blob/d6cc9cb/skills/sepia/references/narrative-pass.md),
  [discourse-pass.md](https://github.com/Nanako0129/sepia/blob/d6cc9cb/skills/sepia/references/discourse-pass.md),
  [style-pass.md](https://github.com/Nanako0129/sepia/blob/d6cc9cb/skills/sepia/references/style-pass.md),
  [model-fingerprints.md](https://github.com/Nanako0129/sepia/blob/d6cc9cb/skills/sepia/references/model-fingerprints.md).
- creative-writing-skills, Apache 2.0:
  [prose-writing.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/creative-writing-craft/resources/prose-writing.md),
  [scene-construction.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/creative-writing-craft/resources/scene-construction.md),
  [fantasy.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/creative-writing-craft/resources/genre/fantasy.md),
  [editor.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/agents/editor.md).
- stop-slop, MIT: [SKILL.md](https://github.com/hardikpandya/stop-slop/blob/8da1f03/SKILL.md),
  [structures.md](https://github.com/hardikpandya/stop-slop/blob/8da1f03/references/structures.md).
- deslop, MIT: [SKILL.md](https://github.com/stephenturner/skill-deslop/blob/a906154/SKILL.md).
- humanizer, MIT: [SKILL.md](https://github.com/blader/humanizer/blob/225a6f3/SKILL.md),
  §22, §24, §25 — залишки чату й текст про текст (`language.md`, Л11).
- beautiful-prose: [SKILL.md](https://github.com/shadowpr0/beautiful_prose/blob/bf44efb/SKILL.md)
  (узято лише для переліку того, що не переноситься, Р9).
- author-toolkit, MIT: [fiction-workshop/SKILL.md, Stage 3](https://github.com/rhavekost/author-toolkit/blob/b782870/skills/fiction-workshop/SKILL.md) —
  читацький тест субагентом без Біблії книги (`reader-test.md`, А6);
  [fiction-workshop/references/continuity-tracking.md](https://github.com/rhavekost/author-toolkit/blob/b782870/skills/fiction-workshop/references/continuity-tracking.md) —
  категорії безперервності (знання, тіло й речі, час, правила світу), «хто
  кому що сказав», обидва місця розбіжності з главами й наслідки далі
  (`continuity/SKILL.md`, Б1–Б6).
- chinese-novelist-skill, MIT:
  [phase2-planning.md](https://github.com/penglonghuang/chinese-novelist-skill/blob/6a64a04/references/flows/phase2-planning.md),
  [phase3-writing.md](https://github.com/penglonghuang/chinese-novelist-skill/blob/6a64a04/references/flows/phase3-writing.md) —
  еталонні абзаци голосу, які читаються останніми перед письмом глави разом
  із кінцем попередньої, і заміна еталона абзацом із готової глави (слот
  «Еталонні уривки», `shared/profile.md`). Довжину уривків у знаках із
  джерела не взято.
- Українські адаптації humanizer, усі MIT, узято лише ідеї, текст власний:
  [iosipov27/ukrainian-humanizer](https://github.com/iosipov27/ukrainian-humanizer) —
  що шукати в еталонному уривку (`shared/profile.md`);
  [asaulyuk/humanizer-ukr](https://github.com/asaulyuk/humanizer-ukr) — активні
  дієприкметники й кальки (`calques.md`, К1), канцелярит (Л13), кличний відмінок
  (`orthography.md`, О8), регіональна норма (Р8);
  [tatet-ua/tatet-humanizer](https://github.com/tatet-ua/tatet-humanizer) —
  службові мітки чату (Л11), хвостове заперечення (Р3), ознаки живого тексту
  (Р8), прийоми самої чистки (`shared/findings.md`, А4);
  [majlovskij-cmd/humanizer-ua](https://github.com/majlovskij-cmd/humanizer-ua) —
  приклади кальок із російської. Заборону тире, «додавай голос» і автозаміни
  не перенесено (Р9).
- Поглиблення сцени й проміжні сцени (`scene-chapter.md`, С18), узято лише ідеї,
  текст власний; огляд — нота проєкту «поглиблення сцен і проміжні сцени —
  чужі підходи», 2026-11-07:
  creative-writing-skills, Apache 2.0, [chapter-and-scene.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/story-planning/resources/story-architecture/chapter-and-scene.md)
  і `scene-construction.md` (вище) — вага переходу, відомість — у наявну сцену;
  chinese-novelist-skill, MIT, [content-expansion.md](https://github.com/penglonghuang/chinese-novelist-skill/blob/6a64a04/references/guides/content-expansion.md) —
  причина тонкої сцени перед розширенням, місце в паузі, тест «чи гірше без
  нього» (числову норму знаків не взято);
  author-toolkit, MIT, [developmental-editing.md](https://github.com/rhavekost/author-toolkit/blob/b782870/skills/fiction-workshop/references/developmental-editing.md) —
  прапорці пропущеного переходу й осмислення;
  jwynia/agent-skills, MIT, [scene-sequencing](https://github.com/jwynia/agent-skills/blob/e02ec7e226a6e4f8419fd3b88a1d8e472d421b32/skills/creative/fiction/structure/scene-sequencing/SKILL.md) —
  «сцена — відгук» як одна з оптик;
  danjdewhurst/story-skills, `scene-craft`, [try-fail.md](https://github.com/danjdewhurst/story-skills/blob/main/skills/scene-craft/references/try-fail.md)
  (за відповіддю Perplexity, посилання на гілку `main`, ліцензію не перевірено) —
  місток не вигадує конфлікту заради драматургії;
  [блог Sudowrite про Expand](https://sudowrite.com/blog/how-to-write-longer-scenes-expand-feature/) —
  слабкий сюжетний такт лагодять будовою, а не прикрасами.
- Повтори між главами (`audit.md`, А8; `scene-chapter.md`, С19, С20) і
  складники читацького інтересу (`reader-test.md`, А6, п. 3 і п. 9), узято
  лише ідеї, текст власний; огляд — нота проєкту «повтори між главами й
  складники читацького інтересу — чужі підходи», 2026-11-07:
  K. M. Weiland, [шість питань проти однакових сцен](https://www.goodreads.com/author_blog_posts/21853881-6-questions-to-help-you-avoid-repetitive-scenes)
  (передрук із блогу Helping Writers Become Authors) — питання про повтор
  сцени (С19), без обов'язкового списку;
  ProWritingAid ([Echoes](https://prowritingaid.com/art/345/How-to-use----The-Repeats-Check.aspx),
  [All Repeats](https://help.prowritingaid.com/article/48-how-to-use-the-repeats-check))
  і AutoCrit ([Repeated phrases](https://www.autocrit.com/editing/support/repeated-phrases-how-autocrit-can-help/),
  [Phrase Frequency](https://www.autocrit.com/support/repetition/)) —
  два масштаби повтору, близький і на весь рукопис, і частота зворотів із
  кількох слів як джерело кандидатів (скрипт А8); лише ідеї з публічних
  сторінок, як працюють самі інструменти, не перевірено;
  creative-writing-skills, Apache 2.0, [reader-sim](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/reader-sim/SKILL.md) —
  читач описує досвід, а не оцінює за переліком (А6, п. 3), і
  [developmental-edit.md](https://github.com/haowjy/creative-writing-skills/blob/0d5bf7f/cw/skills/story-review/resources/developmental-edit.md) —
  жанрова обіцянка, рівна напруга без перепадів притуплює (С20);
  анкети бета-читачів ([authority.pub](https://authority.pub/?p=6061),
  [thepromptindex](https://www.thepromptindex.com/prompt/1758-beta-reader-questionnaire-for-your-book)) —
  «де пробігав очима», «що чекаєш далі», правдоподібність вчинків;
  stop-slop, MIT, [structures.md](https://github.com/hardikpandya/stop-slop/blob/8da1f03/references/structures.md) —
  та сама формула іншими словами: повтор видно за будовою, а не за рядками
  (А8). Окремої поради про паузу посеред загрози (С20) у джерелах не
  знайдено: пункт сформульовано в пакеті.
- Український правопис 2019, офіційний текст МОН:
  [ukr.pravopys-2019.pdf](https://mon.gov.ua/static-objects/mon/sites/1/zagalna%20serednya/Pravopys.2019/ukr.pravopys-2019.pdf).

Англомовні скіли писано для англійської; stop-slop, deslop і beautiful-prose —
ще й для нехудожніх текстів. З них узято тільки те, що переноситься на
українську художню прозу; що свідомо не взято й чому — у кінці
`shared/sentence.md`, розділ Р9.
