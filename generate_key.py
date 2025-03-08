#!/usr/bin/env python
"""
LLM配置密钥生成器启动脚本
"""

import os
import sys

# 确保能够导入项目模块
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.key_generator_app import main

if __name__ == "__main__":
    main() 