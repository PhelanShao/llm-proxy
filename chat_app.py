#!/usr/bin/env python
"""
LLM Chat Testing Application Launch Script
"""

import os
import sys

# Ensure project modules can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import main

if __name__ == "__main__":
    main() 