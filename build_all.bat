@echo off
title UW External - Build All
echo.
echo  [1/3] Building rbx-external (C++)...
echo.
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
msbuild rbx-external.sln /p:Configuration=Release /p:Platform=x64 /v:minimal
if %errorlevel% neq 0 (
    echo  [-] rbx-external build FAILED
    pause
    exit /b 1
)
echo  [+] rbx-external.exe built successfully

echo.
echo  [2/3] Checking .NET 6 SDK...
dotnet --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] .NET SDK not found. Installing .NET 6 SDK...
    powershell -Command "Invoke-WebRequest -Uri 'https://download.visualstudio.microsoft.com/download/pr/b6723010-3764-4b3d-b307-83715e3b8dc6/a0fc5c31bd6f461a5d99af1c92e8a023/dotnet-sdk-6.0.421-win-x64.exe' -OutFile '%TEMP%\dotnet-sdk.exe'; Start-Process '%TEMP%\dotnet-sdk.exe' -ArgumentList '/quiet /norestart' -Wait"
    echo  [+] .NET SDK installed
)

echo.
echo  [3/3] Building UWLoader (C# WinForms)...
echo.
cd UWLoader_CS
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true -o ..\Build\Loader
if %errorlevel% neq 0 (
    echo  [-] UWLoader build FAILED
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo  [+] All builds succeeded!
echo.
echo      rbx-external.exe  --^>  Build\rbx-external.exe
echo      UWLoader.exe       --^>  Build\Loader\UWLoader.exe
echo.
echo  Run UWLoader.exe to launch.
echo.
pause
