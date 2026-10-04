# Log in manually in the opened browser, then close it. Session is saved to auth\state.json
# BASE_URL and LOGIN_PATH are read from .env.
param([string]$Path = "")
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) { Write-Error ".env not found. Copy .env.example to .env and fill it in."; exit 1 }
function Get-EnvValue($key) {
    $m = Select-String -Path $envFile -Pattern "^\s*$key\s*=\s*(.+)$" | Select-Object -First 1
    if ($m) { return $m.Matches[0].Groups[1].Value.Trim() } else { return "" }
}
$baseUrl = (Get-EnvValue "BASE_URL").TrimEnd('/')
if (-not $baseUrl) { Write-Error "BASE_URL missing in .env"; exit 1 }
if (-not $Path) { $Path = Get-EnvValue "LOGIN_PATH" }
if (-not $Path) { $Path = "/auth" }
New-Item -ItemType Directory -Force -Path (Join-Path $root "auth") | Out-Null
playwright codegen --save-storage (Join-Path $root "auth\state.json") "$baseUrl$Path"
