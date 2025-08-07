Write-Host "Starting frontend in debug mode..." -ForegroundColor Green
Set-Location frontend_vite
$env:VITE_MAIN_JS="src/main_debug.jsx"
npm run dev
