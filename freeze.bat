call venv\Scripts\activate.bat
fbs freeze
if not exist "target\Health-weather correlation\docx" mkdir "target\Health-weather correlation\docx"
xcopy /s src\docx "target\Health-weather correlation\docx"
if not exist "target\Health-weather correlation\samples" mkdir "target\Health-weather correlation\samples"
xcopy /s "src\main\python\science\samples" "target\Health-weather correlation\samples"