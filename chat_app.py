#!/usr/bin/env python
"""
LLM对话测试应用启动脚本
"""

import os
import sys

# 确保能够导入项目模块
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import main

if __name__ == "__main__":
    main() 