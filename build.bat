pyinstaller --noconfirm --clean .\config\main.spec
Xcopy /Y /E /I .\model .\dist\NLP-API\model
copy /Y ".\script\run.bat" ".\dist\NLP-API\run.bat"