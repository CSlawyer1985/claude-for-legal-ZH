<#
.SYNOPSIS
  Appends a "-cn" suffix to every plugin name in the claude-for-legal-ZH repo so the
  China-law plugins can run in parallel with the US-law claude-for-legal plugins without
  name collisions (commercial-legal-cn vs commercial-legal, etc.).

  Idempotent: running twice is safe. Re-run this after `git pull` updates the repo,
  because autoUpdate is disabled for this marketplace to preserve the rename.

  Only the plugin *name* fields are changed. Directory names and "source" paths are
  left untouched, the top-level marketplace name (claude-for-legal-zh) is left untouched,
  and author names are left untouched.
#>

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot   # repo root (parent of scripts/)

$plugins = @(
  'ai-governance-legal','commercial-legal','corporate-legal','employment-legal',
  'ip-legal','law-student','legal-builder-hub','legal-clinic','litigation-legal',
  'privacy-legal','product-legal','regulatory-legal'
)

function Set-NameSuffix {
  param([string]$Path, [string]$Plain)
  if (-not (Test-Path $Path)) { Write-Warning "missing: $Path"; return }
  $text = Get-Content -Raw -Encoding UTF8 $Path
  $from = '"name": "' + $Plain + '"'
  $to   = '"name": "' + $Plain + '-cn"'
  if ($text -match [regex]::Escape($to)) {
    Write-Host "  already suffixed: $Plain"
    return
  }
  if ($text -match [regex]::Escape($from)) {
    $text = $text -replace [regex]::Escape($from), $to
    # write without BOM so Claude Code parses cleanly
    [System.IO.File]::WriteAllText($Path, $text, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "  -> $Plain-cn  ($Path)"
  } else {
    Write-Warning "  pattern not found for $Plain in $Path"
  }
}

Write-Host "Applying -cn suffix in $repo"

# 1) marketplace.json: every plugin name entry
$mkt = Join-Path $repo '.claude-plugin\marketplace.json'
Write-Host "marketplace.json:"
foreach ($p in $plugins) { Set-NameSuffix -Path $mkt -Plain $p }

# 2) each plugin's plugin.json
Write-Host "plugin.json files:"
foreach ($p in $plugins) {
  Set-NameSuffix -Path (Join-Path $repo "$p\.claude-plugin\plugin.json") -Plain $p
}

# 3) Redirect the practice-profile config path so the China plugins read/write their OWN
#    config tree (claude-for-legal-zh) instead of colliding with the US plugins'
#    config tree (claude-for-legal). Upstream skill bodies hardcode the US path even
#    though the README documents the -zh path; this reconciles them.
#    Idempotent: "claude-for-legal-zh/" is not re-matched by "claude-for-legal/".
Write-Host "config-path references (md files):"
$enc = New-Object System.Text.UTF8Encoding($false)
$changed = 0
Get-ChildItem -Path $repo -Recurse -Filter *.md -File |
  Where-Object { $_.FullName -notmatch '\\\.git\\' } |
  ForEach-Object {
    $t = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
    $orig = $t
    $t = $t -replace 'plugins/config/claude-for-legal/', 'plugins/config/claude-for-legal-zh/'
    $t = $t -replace 'plugins\\config\\claude-for-legal\\', 'plugins\config\claude-for-legal-zh\'
    if ($t -ne $orig) {
      [System.IO.File]::WriteAllText($_.FullName, $t, $enc)
      $changed++
    }
  }
Write-Host "  rewrote config path in $changed file(s)"

Write-Host "Done. Restart Claude Code (or /plugin reload) for changes to take effect."
