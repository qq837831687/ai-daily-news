@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo  AI 每日新闻 - 自动部署到 GitHub
echo ========================================
echo.

cd /d "%~dp0ai-daily-news"

echo [1/6] 检查 Git 配置...
git config user.name >nul 2>&1
if errorlevel 1 (
    echo Git 未配置，正在设置...
    git config --global user.email "ai-daily-news@example.com"
    git config --global user.name "AI Daily News"
)
echo ✓ Git 配置完成
echo.

echo [2/6] 准备 Git 仓库...
if not exist ".git" (
    git init
)
git add .
git commit -m "feat: AI daily news generator" >nul 2>&1
echo ✓ 仓库准备完成
echo.

echo [3/6] 配置远程仓库...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/qq837831687/ai-daily-news.git
echo ✓ 远程仓库配置完成
echo.

echo [4/6] 推送代码到 GitHub...
echo 请输入您的 GitHub Personal Access Token:
echo.
echo 如果还没有 Token，请先创建:
echo 1. 访问 https://github.com/settings/tokens
echo 2. 点击 "Generate new token" - "Generate new token (classic)"
echo 3. 勾选 repo 权限
echo 4. 生成并复制 Token
echo.
set /p GITHUB_TOKEN="Token: "

if "%GITHUB_TOKEN%"=="" (
    echo ✗ Token 不能为空！
    pause
    exit /b 1
)

echo.
echo 正在推送...
git remote set-url origin https://%GITHUB_TOKEN%@github.com/qq837831687/ai-daily-news.git
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ✗ 推送失败！可能的原因:
    echo   - Token 无效或权限不足
    echo   - 网络连接问题
    echo   - 仓库名称不正确
    echo.
    pause
    exit /b 1
)

echo ✓ 代码推送成功！
echo.

echo [5/6] 配置仓库设置...
echo.
echo 接下来需要在 GitHub 网页上完成以下操作:
echo.
echo 1. 添加 OpenAI API Key:
echo    - 访问: https://github.com/qq837831687/ai-daily-news/settings/secrets/actions
echo    - 点击 "New repository secret"
echo    - Name: OPENAI_API_KEY
echo    - Secret: 您的 OpenAI API 密钥
echo.
echo 2. 启用 GitHub Pages:
echo    - 访问: https://github.com/qq837831687/ai-daily-news/settings/pages
echo    - Source: 选择 "GitHub Actions"
echo    - 点击 Save
echo.
echo 3. 手动运行一次工作流:
echo    - 访问: https://github.com/qq837831687/ai-daily-news/actions
echo    - 点击 "Build Daily AI News" workflow
echo    - 点击 "Run workflow" 按钮
echo.
echo [6/6] 完成！
echo.
echo 您的网站将在几分钟内上线:
echo   https://qq837831687.github.io/ai-daily-news/
echo.

pause
