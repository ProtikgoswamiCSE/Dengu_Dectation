# 🔧 Fix Database Migration Error

## Problem
You're seeing this error:
```
⚠️ সতর্কতা: Database table does not exist. Please run migrations first: python manage.py migrate
```

## ✅ Solution - Run Migrations

### Method 1: Double-Click Script (Easiest)
1. Go to the root directory: `E:\update Ai\Dengu_Dectation`
2. Double-click **`run_migrations.bat`**
3. Wait for it to complete
4. Refresh your browser

### Method 2: Manual Command
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project:
   ```bash
   cd "E:\update Ai\Dengu_Dectation\disease_analyzer"
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Run migrations:
   ```bash
   python manage.py migrate analyzer
   ```
5. You should see:
   ```
   Operations to perform:
     Apply all migrations: analyzer
   Running migrations:
     Applying analyzer.0003_signswarning... OK
     Applying analyzer.0004_signswarning_symptoms... OK
   ```

## What This Does
- Creates the `SignsWarning` database table
- Adds all 12 symptom fields to store symptom data
- Enables data saving from the "See Warning" button

## After Migration
1. ✅ The error will disappear
2. ✅ You can save data from the awareness card
3. ✅ Data will appear in the signs-warnings page table
4. ✅ All symptoms will be displayed correctly

## Troubleshooting

### If "venv\Scripts\activate" doesn't work:
Try:
```bash
venv\Scripts\Activate.ps1
```

### If Django is not found:
Make sure you're in the `disease_analyzer` directory and the virtual environment is activated.

### If migration says "No changes detected":
The migrations might already be applied. Check the database or try:
```bash
python manage.py showmigrations analyzer
```

## Need Help?
Check the console/terminal output for specific error messages.

