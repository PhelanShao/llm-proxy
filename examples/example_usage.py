"""
示例脚本 - 演示LLM代理的使用
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import generate_encrypted_key
from src.llm_proxy import LLMProxy


def main():
    """演示LLM代理的使用流程"""
    print("1. 生成加密的配置密钥")
    # 注意: 在实际使用中，应该使用真实的API密钥
    encrypted_key = generate_encrypted_key(
        provider="openai",
        base_url="https://api.openai.com/v1",
        api_key="sk-your-openai-api-key",
        model="gpt-3.5-turbo"
    )
    print(f"加密的配置密钥: {encrypted_key}")
    
    # 实际应用中，加密的密钥会通过安全渠道传输给应用开发者
    # 开发者无需知道原始API密钥
    
    print("\n2. 使用加密的密钥初始化LLM代理")
    try:
        # 在实际使用中，这里应该使用上面生成的密钥
        # 但由于我们使用的是示例API密钥，这里会失败
        proxy = LLMProxy(encrypted_key)
        print("LLM代理初始化成功")
        
        print("\n3. 发送消息到LLM")
        response = proxy.send_message("Hello, world!")
        print(f"LLM响应: {response}")
    except Exception as e:
        print(f"错误: {str(e)}")
        print("注意: 由于使用了示例API密钥，这个错误是预期的。在实际应用中，使用有效的API密钥不会出现此问题。")
    
    print("\n示例说明:")
    print("1. 在实际应用中，配置密钥的生成通常由服务管理员完成")
    print("2. 生成的加密密钥可以安全地分享给应用开发者")
    print("3. 应用开发者使用加密密钥，而无需知道原始API配置")
    print("4. 这种方式保护了API密钥和其他敏感配置信息")


if __name__ == "__main__":
    main() 