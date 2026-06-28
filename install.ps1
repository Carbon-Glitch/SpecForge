param(
  [ValidateSet("codex", "universal", "claude", "cursor", "antigravity", "all")]
  [string]$Platform = "codex"
)

$SkillName = "specforge-skill"
$Source = Split-Path -Parent $MyInvocation.MyCommand.Path

function Copy-Skill {
  param([string]$Destination)
  $Parent = Split-Path -Parent $Destination
  New-Item -ItemType Directory -Force -Path $Parent | Out-Null
  if (Test-Path -LiteralPath $Destination) {
    Remove-Item -LiteralPath $Destination -Recurse -Force
  }
  Copy-Item -LiteralPath $Source -Destination $Destination -Recurse
  Write-Host "Installed $SkillName to $Destination"
}

if ($Platform -eq "codex" -or $Platform -eq "universal" -or $Platform -eq "all") {
  Copy-Skill (Join-Path $env:USERPROFILE ".agents\skills\$SkillName")
}
if ($Platform -eq "claude" -or $Platform -eq "all") {
  Copy-Skill (Join-Path $env:USERPROFILE ".claude\skills\$SkillName")
}
if ($Platform -eq "cursor" -or $Platform -eq "all") {
  Copy-Skill (Join-Path (Get-Location) ".cursor\skills\$SkillName")
}
if ($Platform -eq "antigravity" -or $Platform -eq "all") {
  Copy-Skill (Join-Path (Get-Location) ".agent\skills\$SkillName")
}

Write-Host "Invoke with: /specforge <product idea>"
