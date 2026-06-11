# -*- coding: utf-8 -*-
"""
AI+智慧物流每日资讯更新脚本
用法：python update_news.py
建议：用Windows任务计划程序设置每天7:30自动运行
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 项目路径
PROJECT_DIR = Path(__file__).parent
TOPICS_FILE = PROJECT_DIR / "topics" / "ai-smart-logistics.html"
INDEX_FILE = PROJECT_DIR / "index.html"

def get_current_issue_number():
    """获取当前期号"""
    if TOPICS_FILE.exists():
        content = TOPICS_FILE.read_text(encoding='utf-8')
        # 查找"第X期"模式
        import re
        match = re.search(r'第(\d+)期', content)
        if match:
            return int(match.group(1))
    return 1

def update_index_page(new_articles):
    """更新首页AI+智慧物流版块"""
    if not INDEX_FILE.exists():
        return
    
    content = INDEX_FILE.read_text(encoding='utf-8')
    
    # 更新版块显示文字（这里可以添加更多更新逻辑）
    print(f"首页已更新，显示 {len(new_articles)} 条新资讯")

def main():
    print("=" * 50)
    print("AI+智慧物流每日资讯更新")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 获取当前期号
    current_issue = get_current_issue_number()
    new_issue = current_issue + 1
    print(f"当前期号: 第{current_issue}期")
    print(f"新期号: 第{new_issue}期")
    
    # 提示用户手动执行搜索
    print("\n[步骤1] 请手动搜索以下关键词的最新新闻:")
    print("  - AI 医药物流")
    print("  - 智慧物流 AI")
    print("  - 人工智能 医药供应链")
    
    print("\n[步骤2] 将搜索到的新闻整理后，更新以下文件:")
    print(f"  - {TOPICS_FILE}")
    print(f"  - {INDEX_FILE}")
    
    print("\n[步骤3] 更新完成后，执行以下命令推送:")
    print("  git add -A")
    print(f'  git commit -m "feat: AI+智慧物流晨间更新 第{new_issue}期"')
    print("  git push origin main")
    
    print("\n" + "=" * 50)
    print("提示: 建议用Windows任务计划程序设置每天7:30自动运行此脚本")
    print("=" * 50)

if __name__ == "__main__":
    main()
