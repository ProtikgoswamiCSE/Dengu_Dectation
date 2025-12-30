# Database Migration Instructions

## Problem
The SignsWarning database table doesn't exist, so data cannot be saved.

## Solution: Run Migration

### Step 1: Open Terminal/Command Prompt
Navigate to the project directory:
```
cd "E:\update Ai\Dengu_Dectation\disease_analyzer"
```

### Step 2: Activate Virtual Environment
**For Windows PowerShell:**
```
.\venv\Scripts\Activate.ps1
```

**For Windows Command Prompt:**
```
venv\Scripts\activate.bat
```

**For Git Bash:**
```
source venv/Scripts/activate
```

### Step 3: Run Migration
```
python manage.py migrate analyzer
```

### Step 4: Verify Migration
You should see output like:
```
Operations to perform:
  Apply all migrations: analyzer
Running migrations:
  Applying analyzer.0003_signswarning... OK
  Applying analyzer.0004_signswarning_symptoms... OK
```

**Note:** If you already ran migration 0003, you only need to run it again to apply 0004 (symptom fields).

## Alternative: Use the Script Files

I've created two script files in the root directory:
- `run_migration.bat` - Double-click to run (Windows)
- `run_migration.ps1` - Run in PowerShell

## After Migration

Once the migration is complete:
1. The SignsWarning table will be created in the database
2. Data from "See Warning" button will be saved properly
3. The signs-warnings page will display all saved data

## Troubleshooting

If you get "no such table" error:
- Make sure you activated the virtual environment
- Run: `python manage.py migrate analyzer`
- Check that migration file exists: `analyzer/migrations/0003_signswarning.py`

