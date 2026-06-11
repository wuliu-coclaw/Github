@echo off
chcp 65001 >nul
echo ========================================
echo AI+智慧物流每日资讯更新
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 搜索最新AI+医药物流新闻...
echo 请手动搜索以下关键词:
echo   - AI 医药物流
echo   - 智慧物流 AI
echo   - 人工智能 医药供应链
echo.

echo [2/3] 整理新闻并更新网站文件...
echo 更新文件:
echo   - topics\ai-smart-logistics.html
echo   - index.html
echo.

echo [3/3] 推送到GitHub...
git add -A
git commit -m "feat: AI+智慧物流晨间更新 %date:~0,4%-%date:~5,2%-%date:~8,2%"
git push origin main
echo.

echo ========================================
echo 更新完成！
echo ========================================
pause
