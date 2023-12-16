
cd %1
dir
if not exist %2 (
    python -m pip freeze >> %2
)
python -m pip install -U -r .\app_modules\settings\requirements.txt
