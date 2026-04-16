@echo off
pip install customtkinter pyinstaller
pyinstaller --noconsole --onefile main.py
echo Compilacao concluida! O arquivo esta na pasta dist.
pause
