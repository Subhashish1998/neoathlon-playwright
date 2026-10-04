# Record a new test with codegen. BASE_URL is read from .env.
# Usage: .\scripts\record.ps1 <test_name> [url_path]
#   .\scripts\record.ps1 signup /signup   ->  tests\recorded\test_signup.py
param(
    [Parameter(Mandatory=$true)][string]$Name,
    [string]$Path = "/"
)
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
if (-not (Test-Path $envFile)) { Write-Error ".env not found. Copy .env.example to .env and fill it in."; exit 1 }
$line = Select-String -Path $envFile -Pattern '^\s*BASE_URL\s*=\s*(.+)$' | Select-Object -First 1
if (-not $line) { Write-Error "BASE_URL missing in .env"; exit 1 }
$baseUrl = $line.Matches[0].Groups[1].Value.Trim().TrimEnd('/')

$out = Join-Path $root "tests\recorded\test_$Name.py"
$state = Join-Path $root "auth\state.json"
$cgArgs = @("codegen", "--target", "python-pytest", "--viewport-size", "1440,900", "-o", $out)
if (Test-Path $state) { $cgArgs += @("--load-storage", $state) }
$cgArgs += "$baseUrl$Path"
Write-Host "Recording to $out"
playwright @cgArgs
python (Join-Path $root "scripts\clean_recording.py") $out
