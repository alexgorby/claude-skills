# Packs each skill folder into dist\<skill>.zip for upload in Claude Desktop
# (Settings -> Skills -> add custom skill). The zip holds the skill folder at its root.
param(
    [string[]]$Skill = @('ukrainian-tech-docs', 'ukrainian-fiction')
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$dist = Join-Path $root 'dist'
New-Item -ItemType Directory -Force $dist | Out-Null

foreach ($name in $Skill) {
    $src = Join-Path $root $name
    if (-not (Test-Path (Join-Path $src 'SKILL.md'))) { throw "No SKILL.md in $src" }
    # Only committed state goes to Claude
    if (git -C $root status --porcelain -- $name) { throw "$name has uncommitted changes; commit first" }
    $zip = Join-Path $dist "$name.zip"
    if (Test-Path $zip) { Remove-Item $zip -Confirm:$false }
    Compress-Archive -Path $src -DestinationPath $zip
    Write-Output $zip
}
