Set-Location "disease_analyzer"
python manage.py migrate analyzer
Write-Host "Migration completed! Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

