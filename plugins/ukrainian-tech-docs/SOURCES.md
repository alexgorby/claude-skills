# Джерела пакета

Готові скіли й статті, з яких узято ідеї. Текст пакета написано наново
українською; англомовні правила перенесено лише там, де вони працюють для
української мови.

- humanizer, MIT: [blader/humanizer](https://github.com/blader/humanizer) —
  ознаки ШІ-тексту для частини 1 `language.md` і перевірка «що тут досі звучить
  як ШІ» і питання, що додано чи втрачено після правки; англійську специфіку
  (тире, регістр заголовків, лапки) як ознаки ШІ не перенесено. Регістр заголовків
  і лапки записано окремо, як норму правопису (`genres/general.md`, розд. 1). Залишки чату, заголовок,
  повторений першим реченням, і текст про документ замість предмета —
  [SKILL.md, §22, §24, §25](https://github.com/blader/humanizer/blob/225a6f3/SKILL.md)
  (`language.md`, 1.13).
- humanizer, форк, MIT: [brandonwise/humanizer](https://github.com/brandonwise/humanizer).
- Українські адаптації humanizer, усі MIT, узято лише ідеї, текст власний:
  [iosipov27/ukrainian-humanizer](https://github.com/iosipov27/ukrainian-humanizer) —
  голос автора перед чисткою (`language.md`, «Переписування зберігає зміст»);
  [asaulyuk/humanizer-ukr](https://github.com/asaulyuk/humanizer-ukr) — активні
  дієприкметники (1.7), канцелярит й аналітичний ступінь порівняння (1.4), кличний
  відмінок і типографіка (`genres/general.md`, розд. 1, 3), невидимі символи
  (`export.md`, розд. 0);
  [tatet-ua/tatet-humanizer](https://github.com/tatet-ua/tatet-humanizer) —
  службові мітки чату (1.13), хвостове заперечення (1.9), прийоми самої чистки;
  [majlovskij-cmd/humanizer-ua](https://github.com/majlovskij-cmd/humanizer-ua) —
  приклади кальок із російської («Діагностика кальок»);
  [OpenMindUA/SimpleUkrainian](https://github.com/OpenMindUA/SimpleUkrainian) —
  умова перед дією (`genres/howto.md`, розд. 2), висновок першим
  (`genres/general.md`, розд. 1), слова-порожнеча (1.4). Заборону тире, числові
  пороги, «додавай голос» і автозаміни «слово → слово» не перенесено.
- technical-writer, MIT: [riekelt/technical-writer](https://github.com/riekelt/technical-writer) —
  контрольні питання після переписування: зміст не втрачено, прийом не
  повернувся в іншій формі (`language.md`, «Переписування зберігає зміст»).
- humanizer-zh, MIT: [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh) —
  те саме для китайської; підтвердження, що перевірка змісту після чистки
  потрібна незалежно від мови.
- korean-humanizer з k-skill, MIT:
  [nomadamas/k-skill, `korean-humanizer/instruction.md`](https://github.com/nomadamas/k-skill/blob/50d7bb3/korean-humanizer/instruction.md) —
  рівні ваги ознак S1/S2/S3 і сортування «лише форматування — правити лише
  форматування» (`language.md`, «Вага ознак»). Розкладку пунктів по рівнях
  складено наново для української.
- StoryScope: J. Russell et al., «StoryScope: Investigating idiosyncrasies in AI
  fiction», COLM 2026, [arXiv 2604.03136](https://arxiv.org/abs/2604.03136) —
  підтвердження, що окрема ознака ШІ не доводить, а сигнал дає їх поєднання
  (рівень S3).
- J. Liao et al., «Defensive Writing in GPT Models», препринт, 2026,
  [arXiv 2610.11355](https://arxiv.org/abs/2610.11355v2) — застереження без
  підстави, які модель дописує, коли перевіряє твердження (`language.md`,
  «Переписування зберігає зміст»). Знайдено через
  [Nanako0129/sepia](https://github.com/Nanako0129/sepia), MIT, де на цій основі
  зроблено правило для переписування ділового тексту; текст правила власний.
- Compound Engineering, MIT:
  [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) —
  ідея плану перед роботою (`/ce-plan`).
- Matt Van Horn, «Every Agentic Engineering Hack I Know», 2026 — той самий
  підхід «спершу план», через статтю.
- doc-coauthoring з anthropics/skills, ліцензію в репозиторії не визначено, узято лише ідею:
  [SKILL.md, Stage 3](https://github.com/anthropics/skills/blob/dbd4588/skills/doc-coauthoring/SKILL.md) —
  тест читача свіжим субагентом (`genres/general.md`, розд. 6).
- wai-skill-suite, MIT:
  [woldinius/wai-skill-suite, `wai-requirements-planning`](https://github.com/woldinius/wai-skill-suite/blob/d83acaf/.claude/skills/wai-requirements-planning/SKILL.md)
  і [`grilling-protocol.md`](https://github.com/woldinius/wai-skill-suite/blob/d83acaf/.claude/skills/wai/references/grilling-protocol.md) —
  перелік припущень наприкінці роботи (`write/SKILL.md`, розд. 3, «Підсумок маркерів»), пошук
  фактів у фоні й найменший варіант серед альтернатив (`forks-and-questions.md`,
  розд. 2–3), три виходи знахідки й формат кількох питань із рекомендацією, де залежне
  питання чекає (там само, розд. 8–9), термін із розмови — у словник проєкту
  (`language.md`, 2.1), дельта плану з датою
  (`genres/plan.md`, розд. 3) і поріг для ADR (`genres/adr.md`). Жорсткий стоп
  перед кожним кроком до підтвердження і питання без ліміту не перенесено: вони суперечать правилу
  «маркер замість питання».
- mattpocock/skills, MIT: [`domain-modeling/ADR-FORMAT.md`](https://github.com/mattpocock/skills/blob/49dd158/skills/engineering/domain-modeling/ADR-FORMAT.md) —
  три умови порогу ADR і класи рішень, які варто записувати (`genres/adr.md`);
  [`to-tickets`](https://github.com/mattpocock/skills/blob/49dd158/skills/engineering/to-tickets/SKILL.md) —
  міграція зі співіснуванням у три кроки (`genres/howto.md`, розд. 3).
- knowledge-work-plugins, Apache-2.0:
  [anthropics/knowledge-work-plugins, `engineering`](https://github.com/anthropics/knowledge-work-plugins/tree/main/engineering) —
  розділ «Коли застосовувати» в runbook (`genres/howto.md`, розд. 1) і умова
  перегляду рішення в «Наслідках» ADR (`genres/adr.md`).
- archify, MIT: [tt-a1i/archify, `authoring-contract.md`](https://github.com/tt-a1i/archify/blob/d0c8c7e/archify/references/authoring-contract.md) —
  лінія крізь чужий вузол як помилка, підпис зв'язку не видаляють, порядок
  перевірки, рамка лише для справжньої межі, застарілі ручні маршрути
  (`genres/schema.md`, розд. 3). Сам інструмент не перенесено: він малює HTML
  через Node.js, а правила тут — для будь-якого інструмента.
- Будова жанру ТЗ (`genres/tz.md`) зведена з кількох шаблонів специфікацій, MIT:
  [github/spec-kit](https://github.com/github/spec-kit) — сталі номери вимог,
  вимірювані критерії, граничні випадки;
  [automazeio/ccpm](https://github.com/automazeio/ccpm) — нефункціональні вимоги
  окремим блоком, припущення і обмеження;
  [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) — вимога у формі
  зобов'язання з умовою приймання;
  [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) —
  трасування вимоги до рішення і перевірки;
  [addyosmani/agent-skills, `spec-driven-development`](https://github.com/addyosmani/agent-skills/tree/main/skills/spec-driven-development) —
  межі виконавця в три яруси;
  [mattpocock/skills, `to-spec`](https://github.com/mattpocock/skills/blob/49dd158/skills/engineering/to-spec/SKILL.md) —
  ухвалені рішення Замовника серед обмежень специфікації. Користувацькі історії як
  обов'язкову форму вимог, оцінку трудомісткості й зупинку на погодження перед
  кожною фазою не перенесено. Правило виконуваності — жодного маркера чи
  відкритого питання в ТЗ, переданому в роботу, — власне.
- Окремі ідеї взято з README інших публічних скілів; текст власний.
