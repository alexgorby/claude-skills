# Packs each skill into dist\<skill>.zip for manual upload in Claude Desktop
# (Settings -> Skills -> add custom skill). The zip holds the skill folder at its root.
# Skills live at plugins\<skill>\skills\<skill>\ (marketplace layout).
param(
    [string[]]$Skill = @('ukrainian-tech-docs', 'ukrainian-fiction')
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$dist = Join-Path $root 'dist'
New-Item -ItemType Directory -Force $dist | Out-Null

foreach ($name in $Skill) {
    $rel = "plugins/$name/skills/$name"
    $src = Join-Path $root $rel
    if (-not (Test-Path (Join-Path $src 'SKILL.md'))) { throw "No SKILL.md in $src" }
    # Only committed state goes to Claude; a failed git call is not a clean tree
    $dirty = git -C $root status --porcelain -- $rel
    if ($LASTEXITCODE -ne 0) { throw "git status failed in $root; build needs a git checkout" }
    if ($dirty) { throw "$name has uncommitted changes; commit first" }
    $zip = Join-Path $dist "$name.zip"
    if (Test-Path $zip) { Remove-Item $zip -Confirm:$false }
    # The licence lives at the repo root; each archive carries its own copy
    $stage = Join-Path ([IO.Path]::GetTempPath()) "skill-build-$name"
    if (Test-Path $stage) { Remove-Item $stage -Recurse -Confirm:$false }
    New-Item -ItemType Directory $stage | Out-Null
    Copy-Item $src -Destination $stage -Recurse
    Copy-Item (Join-Path $root 'LICENSE') -Destination (Join-Path $stage $name)
    Compress-Archive -Path (Join-Path $stage $name) -DestinationPath $zip
    Remove-Item $stage -Recurse -Confirm:$false
    Write-Output $zip
}
