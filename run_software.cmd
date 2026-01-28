@echo off
setlocal

:: Check if GEMINI_API_KEY is set in environment
if "%GEMINI_API_KEY%"=="" (
    echo GEMINI_API_KEY is not set.
    set /p API_KEY="Please enter your Gemini API Key: "
) else (
    set API_KEY=%GEMINI_API_KEY%
)

echo.
echo Starting Genesis System with Gemini...
echo Mode: CREATE_CAMPAIGN
echo Input: inputs_example.json
echo Model: gemini-3-pro-preview (Default)
echo.

python main.py --mode CREATE_CAMPAIGN --input_file inputs_example.json --llm_provider gemini --gemini_api_key "%API_KEY%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Software failed with error code %ERRORLEVEL%.
) else (
    echo.
    echo Software finished successfully. Check 'output' directory.
)

pause
