$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$PaperDir = Join-Path $Root "paper"
$DataDir = Join-Path $Root "data"
$CanonicalPdf = Join-Path $env:USERPROFILE "Downloads\60.pdf"
$LocalPdf = Join-Path $PaperDir "main.pdf"

Push-Location $PaperDir
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

if (-not (Test-Path $LocalPdf)) {
    throw "Expected local PDF was not produced: $LocalPdf"
}

Copy-Item -LiteralPath $LocalPdf -Destination $CanonicalPdf -Force
$CanonicalItem = Get-Item -LiteralPath $CanonicalPdf
Remove-Item -LiteralPath $LocalPdf -Force

New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
$status = [ordered]@{
    paper = 60
    decision = "workshop-only"
    hardening_version = "v2"
    canonical_pdf = $CanonicalPdf
    canonical_pdf_bytes = $CanonicalItem.Length
    local_pdf_removed = -not (Test-Path $LocalPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}
$status | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $DataDir "build_status.json") -Encoding UTF8

Write-Host "canonical_pdf=$CanonicalPdf"
Write-Host "canonical_pdf_bytes=$($CanonicalItem.Length)"
Write-Host "local_pdf_removed=$(-not (Test-Path $LocalPdf))"
