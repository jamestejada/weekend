@ECHO OFF

if NOT EXIST "%cd%\venv\" (
    ECHO Virtual Environment not found....
    ECHO Creating...
    python -m venv venv
)

ECHO Starting Virtual Environment
"%cd%\venv\Scripts\activate.bat"