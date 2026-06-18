$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PaperDir = Join-Path $Root "paper"
$DataDir = Join-Path $Root "data"
$ValidationPath = Join-Path $Root "results\full_scale\experiment_validation.json"
$CanonicalPdf = Join-Path $env:USERPROFILE "Downloads\60.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"
$MinPages = 25

function Assert-Equal {
    param(
        [string]$Name,
        $Actual,
        $Expected
    )
    if ($Actual -ne $Expected) {
        throw "$Name expected $Expected but found $Actual"
    }
}

if (-not (Test-Path -LiteralPath $ValidationPath)) {
    throw "Missing full-scale validation file: $ValidationPath"
}

$validation = Get-Content -LiteralPath $ValidationPath -Raw | ConvertFrom-Json
Assert-Equal "paper" ([int64]$validation.paper) 60
Assert-Equal "condition_rows" ([int64]$validation.condition_rows) 414720
Assert-Equal "expected_condition_rows" ([int64]$validation.expected_condition_rows) 414720
Assert-Equal "represented_evaluations" ([int64]$validation.represented_evaluations) 108716359680
Assert-Equal "represented_planning_tick_decisions" ([int64]$validation.represented_planning_tick_decisions) 6957847019520
Assert-Equal "best_non_oracle_strategy" ([string]$validation.best_non_oracle_strategy) "safety_gated_probe_policy"
Assert-Equal "high_cost_best_deployable_strategy" ([string]$validation.high_cost_best_deployable_strategy) "abstain"
if (-not [bool]$validation.row_count_ok) {
    throw "row_count_ok is false"
}
if (-not [bool]$validation.full_scale_ok) {
    throw "full_scale_ok is false"
}

Remove-Item -LiteralPath $LocalPdf -ErrorAction SilentlyContinue

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $LocalPdf)) {
    throw "Expected local PDF was not produced: $LocalPdf"
}

$pdfInfo = & pdfinfo $LocalPdf
$pageLine = $pdfInfo | Select-String -Pattern "^Pages:\s+(\d+)"
if (-not $pageLine) {
    throw "Could not read page count from $LocalPdf"
}
$Pages = [int]$pageLine.Matches[0].Groups[1].Value
if ($Pages -lt $MinPages) {
    throw "Final PDF has $Pages pages; required at least $MinPages"
}

Copy-Item -LiteralPath $LocalPdf -Destination $CanonicalPdf -Force
$CanonicalItem = Get-Item -LiteralPath $CanonicalPdf
$CanonicalHash = (Get-FileHash -LiteralPath $CanonicalPdf -Algorithm SHA256).Hash
Remove-Item -LiteralPath $LocalPdf -Force

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
$status = [ordered]@{
    paper = 60
    decision = "final full-scale submission candidate"
    hardening_version = "v3_full_scale"
    canonical_pdf = $CanonicalPdf
    canonical_pdf_pages = $Pages
    canonical_pdf_bytes = $CanonicalItem.Length
    canonical_pdf_sha256 = $CanonicalHash
    minimum_pages_required = $MinPages
    local_pdf_removed = -not (Test-Path -LiteralPath $LocalPdf)
    condition_rows = [int64]$validation.condition_rows
    represented_evaluations = [int64]$validation.represented_evaluations
    represented_planning_tick_decisions = [int64]$validation.represented_planning_tick_decisions
    best_non_oracle_strategy = [string]$validation.best_non_oracle_strategy
    high_cost_best_deployable_strategy = [string]$validation.high_cost_best_deployable_strategy
    full_scale_ok = [bool]$validation.full_scale_ok
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $DataDir "build_status.json") -Encoding ASCII

Write-Host "canonical_pdf=$CanonicalPdf"
Write-Host "canonical_pdf_pages=$Pages"
Write-Host "canonical_pdf_bytes=$($CanonicalItem.Length)"
Write-Host "canonical_pdf_sha256=$CanonicalHash"
Write-Host "local_pdf_removed=$(-not (Test-Path -LiteralPath $LocalPdf))"
