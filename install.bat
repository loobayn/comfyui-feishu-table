@echo off
echo 正在安装ComfyUI飞书多维表格插件依赖...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo Python版本检查通过
echo.

REM 安装依赖
echo 正在安装requests和urllib3...
pip install requests>=2.25.1 urllib3>=1.26.0

if errorlevel 1 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)

echo.
echo 依赖安装完成！
echo.
echo 请重启ComfyUI以加载插件
echo 插件将在"飞书工具"分类下显示
echo.
pause
