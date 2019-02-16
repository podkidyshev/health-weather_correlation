call venv\Scripts\activate.bat
rmdir /S /Q dist
python cx.py build
echo DONE
pause >nul