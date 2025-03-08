#!/usr/bin/env python
"""
LLM Configuration Key Generator Launch Script
"""

import os
import sys

# Ensure project modules can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.key_generator_app import main

if __name__ == "__main__":
    main() 