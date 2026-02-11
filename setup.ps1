# PowerShell script to start the application locally
# Autonomous Learning Agent - Local Development Setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Autonomous Learning Agent - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists in backend
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  Backend .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ Created backend\.env" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Please edit backend\.env and add:" -ForegroundColor Yellow
    Write-Host "   - GROQ_API_KEY (get from https://console.groq.com/)" -ForegroundColor Yellow
    Write-Host "   - SECRET_KEY (generate with: python -c 'import secrets; print(secrets.token_hex(32))')" -ForegroundColor Yellow
    Write-Host "   - MONGODB_URL (if using MongoDB Atlas)" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Press Enter after updating .env file, or type 'exit' to quit"
    if ($continue -eq "exit") {
        exit
    }
}

# Check if frontend .env exists
if (-not (Test-Path "frontend\.env")) {
    Write-Host "Creating frontend .env file..." -ForegroundColor Yellow
    if (Test-Path "frontend\.env.example") {
        Copy-Item "frontend\.env.example" "frontend\.env"
    } else {
        "VITE_API_URL=http://localhost:8000" | Out-File -FilePath "frontend\.env" -Encoding utf8
    }
    Write-Host "✅ Created frontend\.env" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting setup process..." -ForegroundColor Cyan
Write-Host ""

# Backend Setup
Write-Host "📦 Setting up Backend..." -ForegroundColor Green
Write-Host "---------------------------------------" -ForegroundColor Gray

# Check if virtual environment exists
if (-not (Test-Path "backend\.venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv backend\.venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
$activateScript = "backend\.venv\Scripts\Activate.ps1"
& $activateScript
pip install -r backend\requirements.txt
Write-Host "✅ Backend dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "📦 Setting up Frontend..." -ForegroundColor Green
Write-Host "---------------------------------------" -ForegroundColor Gray

# Frontend Setup
Set-Location frontend
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
    npm install
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✅ Frontend dependencies already installed" -ForegroundColor Green
}
Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Ensure MongoDB is running (locally or MongoDB Atlas)" -ForegroundColor White
Write-Host "2. Open TWO terminal windows:" -ForegroundColor White
Write-Host ""
Write-Host "   Terminal 1 (Backend):" -ForegroundColor Cyan
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "   Terminal 2 (Frontend):" -ForegroundColor Cyan
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open your browser at http://localhost:5173" -ForegroundColor White
Write-Host ""

$startNow = Read-Host "Would you like to start the servers now? (y/n)"
if ($startNow -eq "y") {
    Write-Host ""
    Write-Host "🚀 Starting servers..." -ForegroundColor Green
    Write-Host ""
    
    # Start backend in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\.venv\Scripts\Activate.ps1; uvicorn main:app --reload --port 8000"
    
    Start-Sleep -Seconds 2
    
    # Start frontend in new window
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"
    
    Write-Host "✅ Servers started in separate windows!" -ForegroundColor Green
    Write-Host "Frontend should be available at http://localhost:5173" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Happy Learning! 🎓" -ForegroundColor Magenta
