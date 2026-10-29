# Mechanical checks of skill and docs text. Finds, never fixes: every finding is
# a candidate for a human verdict, not an error by itself.
#
# Checks (-Check):
#   Url          broken relative links; with -Online also HTTP status of external URLs
#   Placeholder  unfilled placeholders: TODO, TBD, FIXME, XXX, {{...}}, [...]
#   Euphony      у/в, і/й, з/із/зі against the sounds at the word junction
#                (language.md 1.14; Правопис 2019, § 23-25)
#   Label        service label with a colon at the start of a prose paragraph (language.md 1.12);
#                structural labels the format requires are skipped ($formatLabels)
#   Opening      the same opening in 3+ sibling sections (language.md 1.5); skips templates/
#   Artifact     chat service marks (oaicite, utm_source=chatgpt, 【N†source】, [cite: N]),
#                invisible characters (U+200B, U+200D, U+2060, U+FEFF past the start,
#                U+00AD) and Latin homoglyphs inside a Cyrillic word
#                (language.md 1.13; export.md, розд. 0)
#   Shared      signs shared by both packages (docs/shared-signs.md): each point
#                exists and carries every form marker. Repo-wide, ignores -Path;
#                runs by default only when -Path is not given
#
# Usage:
#   pwsh ./check.ps1                         # docs/, plugins/, tests/ and root docs, all checks, offline
#   pwsh ./check.ps1 -Check Euphony,Label
#   pwsh ./check.ps1 -Check Shared
#   pwsh ./check.ps1 -Path docs -Online
# Exit code 1 when anything is found.
param(
    [string[]]$Path = @('docs', 'plugins', 'tests', 'README.md', 'README.en.md', 'MAINTAINING.md'),
    [ValidateSet('Url', 'Placeholder', 'Euphony', 'Label', 'Opening', 'Artifact', 'Shared')]
    [string[]]$Check = @('Url', 'Placeholder', 'Euphony', 'Label', 'Opening', 'Artifact', 'Shared'),
    [switch]$Online
)
if ($PSBoundParameters.ContainsKey('Path') -and -not $PSBoundParameters.ContainsKey('Check')) {
    $Check = $Check | Where-Object { $_ -ne 'Shared' }
}

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot

# ---------- text model ----------

# Returns blocks of prose: @{ Line; Text; Kind } where Kind is
# heading | para | list | cell. Code blocks and frontmatter are dropped.
function Get-Blocks([string[]]$lines) {
    $blocks = [System.Collections.Generic.List[object]]::new()
    $inCode = $false; $inFront = $false
    $cur = $null
    $flush = { if ($cur) { $blocks.Add($cur) }; Set-Variable cur $null -Scope 1 }
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $l = $lines[$i]; $n = $i + 1
        if ($i -eq 0 -and $l -eq '---') { $inFront = $true; continue }
        if ($inFront) { if ($l -eq '---') { $inFront = $false }; continue }
        if ($l -match '^\s*(```|~~~)') { & $flush; $inCode = -not $inCode; continue }
        if ($inCode) { continue }
        if ($l -match '^\s*$') { & $flush; continue }
        if ($l -match '^(#{1,6})\s+(.*)$') {
            & $flush
            $blocks.Add(@{ Line = $n; Text = $Matches[2]; Kind = 'heading'; Level = $Matches[1].Length })
            continue
        }
        if ($l -match '^\s*\|') {
            & $flush
            if ($l -match '^\s*\|[\s:\-|]+\|\s*$') { continue }
            foreach ($c in ($l.Trim().Trim('|') -split '\|')) {
                $blocks.Add(@{ Line = $n; Text = $c.Trim(); Kind = 'cell' })
            }
            continue
        }
        if ($l -match '^\s*([-*+]|\d+\.)\s+(.*)$') {
            & $flush
            $cur = @{ Line = $n; Text = $Matches[2]; Kind = 'list'; Lines = @($n) }
            continue
        }
        if ($cur) { $cur.Text += ' ' + $l.Trim(); continue }
        $cur = @{ Line = $n; Text = $l.Trim(); Kind = 'para' }
    }
    & $flush
    $blocks
}

# Masks markup that is not prose: inline code, URLs, link targets, emphasis.
function Get-Prose([string]$t) {
    $t = $t -replace '`[^`]*`', ' ¤ '
    $t = $t -replace '\]\([^)]*\)', ']'
    $t = $t -replace 'https?://\S+', ' ¤ '
    $t = $t -replace '«[^»]*»', ' ¤ '      # quoted examples and requests
    $t = $t -replace '[\[\]*_]', ''
    $t
}

# ---------- euphony ----------

$vowel = 'аеиіоу'          # word-initial vowels
$jot = 'яюєї'              # word-initial letters that start with [й]
$endVowel = 'аеиіоуяюєї'   # word-final vowel letters
$sib = 'зсцжчш'

function Get-Expected([string]$tok, [string]$prev, [bool]$pause, [bool]$start, [string]$next) {
    $t = $tok.ToLower(); $n = $next.ToLower()
    $f = $n[0]; $s = if ($n.Length -gt 1) { $n[1] } else { ' ' }
    $nVowel = $vowel.Contains($f); $nJot = $jot.Contains($f) -or $f -eq 'й'
    $sCons = -not ($vowel + $jot + "ь'$([char]0x2019)$([char]0x02BC) ").Contains($s)
    $pVowel = $prev -and $endVowel.Contains($prev.ToLower()[-1])
    switch ($t) {
        { $_ -in 'у', 'в' } {
            if ('вф'.Contains($f) -or $n -match '^(льв|зв|св|дв|тв|гв|хв)') { return @('у') }
            if ($start) { if ($nVowel) { return @('в') } elseif ($nJot) { return @('у') } else { return @('у', 'в') } }
            if ($pause) { if ($nVowel) { return $null } else { return @('у') } }
            if (-not $pVowel) { if ($nVowel) { return @('в') } elseif ($nJot) { return $null } else { return @('у') } }
            if ($nJot) { return $null }
            return @('в')
        }
        { $_ -in 'і', 'й' } {
            if ($nJot) { return @('і') }
            if ($prev -and 'йяюєї'.Contains($prev.ToLower()[-1])) { return @('і') }
            if ($pause -or $start) { if ($nVowel) { return $null } else { return @('і') } }
            if (-not $pVowel -and -not $nVowel) { return @('і') }
            return @('й')
        }
        { $_ -in 'з', 'із', 'зі' } {
            if ($sib.Contains($f)) { if ($sCons) { return @('зі', 'із') } else { return @('із') } }
            if ($nJot) { return $null }
            if ($nVowel) { return @('з') }
            if ($start -or $pause -or $pVowel) { return @('з') }
            return @('із')
        }
    }
    $null
}

function Test-Euphony($file, $blocks) {
    $rx = [regex]'(?<![\p{L}''\u2019\u02BC-])(і|й|у|в|з|із|зі|І|Й|У|В|З|Із|Зі)(?![\p{L}''\u2019\u02BC-])'
    foreach ($b in $blocks) {
        $t = Get-Prose $b.Text
        if ($b.Kind -eq 'cell' -and ($t -split '\s+' | Where-Object { $_ }).Count -le 4) { continue }   # short cells are labels and forms
        foreach ($m in $rx.Matches($t)) {
            $left = $t.Substring(0, $m.Index).TrimEnd()
            $right = $t.Substring($m.Index + $m.Length).TrimStart()
            if ($right -notmatch '^[а-щьюяєіїґА-ЩЬЮЯЄІЇҐ]') { continue }   # Latin, digit, code: no rule
            if ($right -cmatch '^[А-ЩЬЮЯЄІЇҐ]{2,}\b') { continue }        # abbreviation: read by letter names
            $next = ($right -split '[^\p{L}''\u2019\u02BC-]')[0]
            $start = $left -eq '' -or $left -match '[.!?…]$'
            $pause = -not $start -and $left -match '[,;:—–()\-]$'
            $prev = ''
            if (-not $start -and -not $pause) {
                if ($left -notmatch '([а-щьюяєіїґА-ЩЬЮЯЄІЇҐ''\u2019\u02BC]+)$') { continue }  # Latin or symbol before: unknown sound
                $prev = $Matches[1]
            }
            $exp = Get-Expected $m.Value $prev $pause $start $next
            if (-not $exp -or $exp -contains $m.Value.ToLower()) { continue }
            $hint = "очікується: $($exp -join ' / ')"
            if ($m.Value.ToLower() -eq 'і' -and $exp -contains 'й') { $hint += ' (і — якщо зіставлення понять)' }
            $ctx = ("$($left -replace '^.*?(\S+\s+\S+)$','$1') [$($m.Value)] $next").Trim()
            [pscustomobject]@{ Check = 'Euphony'; File = $file; Line = $b.Line; Text = $ctx; Hint = $hint }
        }
    }
}

# ---------- labels ----------

# Labels the format itself requires: rule weight, request lists, navigation,
# source lines, wrong/right pairs in examples. 1.12 targets explanatory labels.
$formatLabels = @('Вага', 'Запити', 'Приклади запитів', 'Поруч читати', 'Межа', 'Джерело',
    'Жанрова примітка', "Ім'я файлу", 'Хибно', 'Правильно')
# Sentences that end in a colon before a list: 1.12 exempts them, the regex cannot tell.
$sentenceLeads = @('Автор просить', 'Автор питає', 'HLD тримає концепції', 'LLD тримає значення',
    'Порядок такий', 'Нотатка атомарна', 'Порушень чотири', 'Третього немає', 'Четвертого виходу немає',
    'Повністю виключи', 'Рішення не видаляються', "Обов'язкові розділи")

function Test-Label($file, $blocks) {
    if ($file -match '(^|/)templates/|\.en\.md$') { return }   # template fields; English text
    foreach ($b in $blocks) {
        if ($b.Kind -ne 'para') { continue }
        $t = $b.Text
        if ($t -match '^(\*\*)?([\p{Lu}][\p{Ll}''\u2019\u02BC-]*(?:\s+[\p{L}''\u2019\u02BC-]+){0,2}):(\*\*)?\s+\S') {
            $label = $Matches[2]
            if ($label -in $formatLabels -or $label -in $sentenceLeads) { continue }
            [pscustomobject]@{ Check = 'Label'; File = $file; Line = $b.Line; Text = "${label}:"; Hint = 'роль ярлика — у саме речення (1.12)' }
        }
    }
}

# ---------- same opening ----------

function Test-Opening($file, $blocks) {
    if ($file -match '(^|/)templates/') { return }   # template fields repeat by design
    $sections = [System.Collections.Generic.List[object]]::new()
    $stack = @()
    for ($i = 0; $i -lt $blocks.Count; $i++) {
        $b = $blocks[$i]
        if ($b.Kind -ne 'heading') { continue }
        $stack = @($stack | Where-Object { $_.Level -lt $b.Level })
        $parent = if ($stack) { $stack[-1].Line } else { 0 }
        $stack += $b
        $first = $blocks[$i + 1]
        if (-not $first -or $first.Kind -ne 'para') { continue }
        $words = @((Get-Prose $first.Text).ToLower() -split '[^\p{L}\p{N}''\u2019\u02BC-]+' | Where-Object { $_ })
        if ($words.Count -lt 2) { continue }
        $sections.Add(@{ Key = "$parent/$($b.Level)"; Line = $first.Line; Words = $words; Head = $b.Text })
    }
    $hit = @{}
    foreach ($g in ($sections | Group-Object { $_.Key })) {
        foreach ($p in 1..3) {
            $sub = $g.Group | Where-Object { $_.Words.Count -gt $p } |
                Group-Object { "$($_.Words[0]) @$p $($_.Words[$p])" } | Where-Object Count -ge 3
            foreach ($s in $sub) { foreach ($x in $s.Group) { $hit[$x.Line] = @($x, $s.Count) } }
        }
    }
    foreach ($k in ($hit.Keys | Sort-Object)) {
        $x, $count = $hit[$k]
        $open = ($x.Words[0..([Math]::Min(4, $x.Words.Count - 1))] -join ' ')
        [pscustomobject]@{ Check = 'Opening'; File = $file; Line = $x.Line; Text = "$($x.Head): «$open…»"; Hint = "однаковий зачин у $count сусідніх розділах (1.5)" }
    }
}

# ---------- placeholders ----------

function Test-Placeholder($file, [string[]]$lines) {
    if ($file -match '(^|/)templates/') { return }   # templates hold placeholders by design
    $rx = '\b(TODO|TBD|FIXME|XXX)\b|\{\{[^}]*\}\}|\[\s*(\.\.\.|…)\s*\]|(?i:lorem ipsum)'
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if (($lines[$i] -replace '`[^`]*`|«[^»]*»', '') -match $rx) {
            [pscustomobject]@{ Check = 'Placeholder'; File = $file; Line = $i + 1; Text = $Matches[0]; Hint = 'незаповнена заготовка' }
        }
    }
}

# ---------- chat marks, invisible characters, homoglyphs ----------

function Test-Artifact($file, [string[]]$lines) {
    $marks = 'oaicite|contentReference\[|utm_source=chatgpt|【[^】]*†[^】]*】|\[cite:\s*\d'
    $invisible = @{ 0x200B = 'U+200B'; 0x200D = 'U+200D'; 0x2060 = 'U+2060'; 0xFEFF = 'U+FEFF'; 0x00AD = 'U+00AD' }
    $mixed = [regex]'[\p{L}''\u2019\u02BC]*(?:[а-щьюяєіїґА-ЩЬЮЯЄІЇҐ][a-zA-Z]|[a-zA-Z][а-щьюяєіїґА-ЩЬЮЯЄІЇҐ])[\p{L}''\u2019\u02BC]*'
    $inCode = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $l = $lines[$i]
        foreach ($c in $invisible.Keys) {
            $at = $l.IndexOf([char]$c)
            if ($at -lt 0 -or ($c -eq 0xFEFF -and $i -eq 0 -and $at -eq 0)) { continue }   # BOM at file start is fine
            [pscustomobject]@{ Check = 'Artifact'; File = $file; Line = $i + 1; Text = $invisible[$c]; Hint = 'невидимий символ: показати автору, не видаляти мовчки' }
        }
        if ($l -match '^\s*(```|~~~)') { $inCode = -not $inCode; continue }
        if ($inCode) { continue }
        $t = $l -replace '`[^`]*`', ' '   # examples in inline code are documentation, not residue
        if ($t -match $marks) {
            [pscustomobject]@{ Check = 'Artifact'; File = $file; Line = $i + 1; Text = $Matches[0]; Hint = 'службова мітка чату (1.13)' }
        }
        foreach ($m in $mixed.Matches(($t -replace 'https?://\S+', ' '))) {
            [pscustomobject]@{ Check = 'Artifact'; File = $file; Line = $i + 1; Text = $m.Value; Hint = 'латиниця й кирилиця в одному слові: можлива підмінена літера' }
        }
    }
}

# ---------- shared signs ----------

# Text of the section whose heading starts with $prefix, up to the next heading
# of the same or higher level; $null when no such heading.
function Get-Section([string]$full, [string]$prefix) {
    if (-not (Test-Path $full)) { return $null }
    $lines = [IO.File]::ReadAllLines($full, [Text.Encoding]::UTF8)
    $rx = '^(#{1,6})\s+' + [regex]::Escape($prefix) + '(\.|\s|$)'
    $start = -1; $level = 0
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($start -lt 0) {
            if ($lines[$i] -match $rx) { $start = $i; $level = $Matches[1].Length }
        } elseif ($lines[$i] -match '^(#{1,6})\s' -and $Matches[1].Length -le $level) {
            return ($lines[$start..($i - 1)] -join "`n")
        }
    }
    if ($start -ge 0) { return ($lines[$start..($lines.Count - 1)] -join "`n") }
    $null
}

function Test-Shared {
    $reg = 'docs/shared-signs.md'
    $full = Join-Path $root $reg
    if (-not (Test-Path $full)) {
        [pscustomobject]@{ Check = 'Shared'; File = $reg; Line = 0; Text = 'реєстру немає'; Hint = 'перевірку не виконано' }
        return
    }
    $base = @{
        tech    = 'plugins/ukrainian-tech-docs/skills/ukrainian-tech-docs/references'
        fiction = 'plugins/ukrainian-fiction/skills/ukrainian-fiction/references'
    }
    $lines = [IO.File]::ReadAllLines($full, [Text.Encoding]::UTF8)
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $cells = $lines[$i].Trim().Trim('|') -split '\|' | ForEach-Object { $_.Trim() }
        if ($lines[$i] -notmatch '^\s*\|' -or $cells.Count -lt 5) { continue }
        $tech = [regex]::Match($cells[2], '`([^`#]+)#([^`]+)`')
        $fic  = [regex]::Match($cells[3], '`([^`#]+)#([^`]+)`')
        if (-not $tech.Success -or -not $fic.Success) { continue }   # header row
        $key = $cells[0]
        $markers = [regex]::Matches($cells[4], '`([^`]+)`') | ForEach-Object { $_.Groups[1].Value }
        foreach ($side in @(@('tech', $tech), @('fiction', $fic))) {
            $name, $m = $side
            $file = $m.Groups[1].Value; $point = $m.Groups[2].Value
            $text = Get-Section (Join-Path $root "$($base[$name])/$file") $point
            if ($null -eq $text) {
                [pscustomobject]@{ Check = 'Shared'; File = $reg; Line = $i + 1; Text = $key; Hint = "${name}: пункту $file#$point немає" }
                continue
            }
            foreach ($mk in $markers) {
                if ($text.IndexOf($mk, [StringComparison]::OrdinalIgnoreCase) -lt 0) {
                    [pscustomobject]@{ Check = 'Shared'; File = $reg; Line = $i + 1; Text = $key; Hint = "${name}: у $file#$point немає «$mk»" }
                }
            }
        }
    }
}

# ---------- urls ----------

$external = @{}
function Test-Url($file, $full, [string[]]$lines) {
    $dir = Split-Path $full
    $inCode = $false
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $l = $lines[$i]
        if ($l -match '^\s*(```|~~~)') { $inCode = -not $inCode; continue }
        if ($inCode) { continue }
        $l = $l -replace '`[^`]*`', ''
        foreach ($m in [regex]::Matches($l, '\]\(([^)\s]+)\)')) {
            $u = $m.Groups[1].Value
            if ($u -match '^(https?:|mailto:)') { continue }
            if ($u.StartsWith('#')) { continue }
            $target = [uri]::UnescapeDataString(($u -split '#')[0])
            if (-not (Test-Path (Join-Path $dir $target))) {
                [pscustomobject]@{ Check = 'Url'; File = $file; Line = $i + 1; Text = $u; Hint = 'файла немає' }
            }
        }
        foreach ($m in [regex]::Matches($l, 'https?://[^\s)>\]»"`]+')) {
            $u = $m.Value.TrimEnd('.', ',', ';', ':')
            if (-not $external[$u]) { $external[$u] = [System.Collections.Generic.List[string]]::new() }
            $external[$u].Add("${file}:$($i + 1)")
        }
    }
}

function Test-External {
    foreach ($u in ($external.Keys | Sort-Object)) {
        $code = $null; $err = $null; $cf = $false
        foreach ($method in 'Head', 'Get') {
            try {
                $r = Invoke-WebRequest -Uri $u -Method $method -MaximumRedirection 5 -TimeoutSec 20 -SkipHttpErrorCheck -UseBasicParsing
                $code = [int]$r.StatusCode
                $cf = [bool]$r.Headers['cf-mitigated']
            } catch { $err = $_.Exception.Message; $code = $null }
            if ($code -and $code -lt 400) { break }
        }
        if ($code -and $code -lt 400) { continue }
        $where = $external[$u][0] -split ':(?=\d+$)'
        $more = if ($external[$u].Count -gt 1) { " (+$($external[$u].Count - 1))" } else { '' }
        [pscustomobject]@{ Check = 'Url'; File = $where[0]; Line = [int]$where[1]; Text = $u; Hint = $(if ($cf) { "HTTP $code, перевірка Cloudflare: відкрити в браузері$more" } elseif ($code) { "HTTP $code$more" } else { "$err$more" }) }
    }
}

# ---------- run ----------

$files = foreach ($p in $Path) {
    $full = Join-Path $root $p
    if (Test-Path $full -PathType Leaf) { Get-Item $full } else { Get-ChildItem $full -Recurse -Filter *.md }
}

$found = foreach ($f in $files) {
    $rel = [IO.Path]::GetRelativePath($root, $f.FullName) -replace '\\', '/'
    $lines = [IO.File]::ReadAllLines($f.FullName, [Text.Encoding]::UTF8)
    $blocks = Get-Blocks $lines
    if ('Url' -in $Check) { Test-Url $rel $f.FullName $lines }
    if ('Placeholder' -in $Check) { Test-Placeholder $rel $lines }
    if ('Euphony' -in $Check) { Test-Euphony $rel $blocks }
    if ('Label' -in $Check) { Test-Label $rel $blocks }
    if ('Opening' -in $Check) { Test-Opening $rel $blocks }
    if ('Artifact' -in $Check) { Test-Artifact $rel $lines }
}
if ('Url' -in $Check -and $Online) { $found = @($found) + @(Test-External) }
if ('Shared' -in $Check) { $found = @($found) + @(Test-Shared) }

$found = @($found | Where-Object { $_ })
foreach ($g in ($found | Group-Object Check)) {
    Write-Output "== $($g.Name): $($g.Count)"
    foreach ($x in $g.Group) { Write-Output ("{0}:{1}  {2}  — {3}" -f $x.File, $x.Line, $x.Text, $x.Hint) }
    Write-Output ''
}
if ($found.Count) { Write-Output "Знахідок: $($found.Count). Скрипт нічого не правив."; exit 1 }
Write-Output 'Знахідок немає.'
