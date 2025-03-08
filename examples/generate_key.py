"""
示例脚本 - 生成加密的LLM配置密钥
"""

import os
import sys
import argparse

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import generate_encrypted_key


def main():
    """解析命令行参数并生成加密的LLM配置密钥"""
    parser = argparse.ArgumentParser(description='生成加密的LLM配置密钥')
    
    parser.add_argument('--provider', required=True, choices=['openai', 'anthropic', 'google', 'openrouter', 'custom'],
                      help='LLM提供商 (openai, anthropic, google, openrouter, custom)')
    parser.add_argument('--base-url', required=True, help='API基础URL')
    parser.add_argument('--api-key', required=True, help='API密钥')
    parser.add_argument('--model', required=True, help='模型名称')
    parser.add_argument('--header', action='append', help='可选的HTTP头信息 (格式: 键=值)')
    parser.add_argument('--extra-body', action='append', help='可选的额外请求体参数 (格式: 键=值)')
    
    args = parser.parse_args()
    
    # 处理头信息
    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split('=', 1)
            headers[key] = value
    
    # 处理额外请求体参数
    extra_body = {}
    if args.extra_body:
        for param in args.extra_body:
            key, value = param.split('=', 1)
            # 尝试转换为合适的类型
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            extra_body[key] = value
    
    # 生成加密的配置密钥
    encrypted_key = generate_encrypted_key(
        provider=args.provider,
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        headers=headers,
        extra_body=extra_body
    )
    
    print(f"加密的配置密钥: {encrypted_key}")


if __name__ == "__main__":
    main() 