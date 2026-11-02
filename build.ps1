# Packs each skill into dist\<skill>.zip for manual upload in Claude Desktop
# (Settings -> Skills -> add custom skill). The zip holds the skill folder at its root.
# Skills live at plugins\<plugin>\skills\<skill>\ (marketplace layout).
#
# A plugin with a shared\ folder holds several skills that read it through
# ../../shared/. An uploaded skill has no plugin around it, so each skill gets
# its own zip with a copy of shared\ inside, the paths rewritten to shared/,
# and the plugin name as a prefix of the skill name (no plugin namespace there).
# Agents and hooks do not travel in a zip: the review skill falls back to its
# mode without subagents, and the language-pass hook is not there.
param(
    [string[]]$Plugin = @('ukrainian-tech-docs', 'ukrainian-fiction')
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$dist = Join-Path $root 'dist'
New-Item -ItemType Directory -Force $dist | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)

foreach ($name in $Plugin) {
    $rel = "plugins/$name"
    $src = Join-Path $root $rel
    if (-not (Test-Path (Join-Path $src 'skills'))) { throw "No skills\ in $src" }
    # Only committed state goes to Claude; a failed git call is not a clean tree
    $dirty = git -C $root status --porcelain -- $rel
    if ($LASTEXITCODE -ne 0) { throw "git status failed in $root; build needs a git checkout" }
    if ($dirty) { throw "$name has uncommitted changes; commit first" }
    $shared = Join-Path $src 'shared'

    foreach ($skillDir in Get-ChildItem (Join-Path $src 'skills') -Directory) {
        if (-not (Test-Path (Join-Path $skillDir.FullName 'SKILL.md'))) { throw "No SKILL.md in $($skillDir.FullName)" }
        $skill = if ($skillDir.Name -eq $name) { $name } else { "$name-$($skillDir.Name)" }
        $zip = Join-Path $dist "$skill.zip"
        if (Test-Path $zip) { Remove-Item $zip -Confirm:$false }
        $stage = Join-Path ([IO.Path]::GetTempPath()) "skill-build-$skill"
        if (Test-Path $stage) { Remove-Item $stage -Recurse -Confirm:$false }
        $dst = Join-Path $stage $skill
        New-Item -ItemType Directory $stage | Out-Null
        Copy-Item $skillDir.FullName -Destination $dst -Recurse
        if (Test-Path $shared) {
            Copy-Item $shared -Destination (Join-Path $dst 'shared') -Recurse
            foreach ($md in Get-ChildItem $dst -Recurse -Filter *.md) {
                $text = [IO.File]::ReadAllText($md.FullName, $utf8)
                $new = $text.Replace('../../shared/', 'shared/')
                if ($md.Name -eq 'SKILL.md' -and $md.Directory.FullName -eq $dst) {
                    $new = $new -replace '(?m)^name:\s*\S+\s*$', "name: $skill"
                }
                if ($new -ne $text) { [IO.File]::WriteAllText($md.FullName, $new, $utf8) }
            }
        }
        # The licence lives at the repo root; each archive carries its own copy
        Copy-Item (Join-Path $root 'LICENSE') -Destination $dst
        Compress-Archive -Path $dst -DestinationPath $zip
        Remove-Item $stage -Recurse -Confirm:$false
        Write-Output $zip
    }
}
