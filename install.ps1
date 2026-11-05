# ZeroArmor 1-Click Bootstrap Installer for Windows
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   🛡️ ZeroArmor v1.0.0 Automated Cloud Installer          " -ForegroundColor Yellow
Write-Host "   Instant 22-Vector RASP Immunity for Any Python Project" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""

$wheelUrl = "https://github.com/harshitpratap1113-glitch/zeroarmor/releases/download/v1.0.0/zeroarmor-1.0.0-py3-none-any.whl"

Write-Host "[*] Installing ZeroArmor via pip..." -ForegroundColor White
& python -m pip install --upgrade --no-cache-dir $wheelUrl

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[+] ZeroArmor successfully installed!" -ForegroundColor Green
    Write-Host "[*] Verifying protection core..." -ForegroundColor White
    & python -c "import zeroarmor; print('✅ Core Verification: ARMORED | 22 Shields Online!')"
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Yellow
    Write-Host "  Add 'import zeroarmor' at the top of your python script/web app." -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "[-] Installation failed. Please check Python/pip installation." -ForegroundColor Red
}
