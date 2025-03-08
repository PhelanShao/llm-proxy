"""
基于Gradio的LLM配置密钥生成器应用
"""

import gradio as gr
import os
import sys
import json
from typing import Dict, Any, List, Tuple

# 确保能够导入项目模块
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.key_generator import generate_encrypted_key
from src.models import LLMProvider


def parse_key_value_pairs(text: str) -> Dict[str, Any]:
    """
    解析键值对文本为字典
    
    格式: 每行一个键值对，格式为 "key=value"
    """
    result = {}
    if not text.strip():
        return result
        
    for line in text.strip().split("\n"):
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        # 尝试转换为适当的类型
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
        elif value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():
            value = float(value)
            
        result[key] = value
    
    return result


def generate_key(
    provider: str, 
    base_url: str, 
    api_key: str, 
    model: str, 
    headers_text: str,
    extra_body_text: str
) -> str:
    """生成加密的配置密钥"""
    try:
        # 解析头信息和额外请求体参数
        headers = parse_key_value_pairs(headers_text)
        extra_body = parse_key_value_pairs(extra_body_text)
        
        # 生成加密密钥
        encrypted_key = generate_encrypted_key(
            provider=provider,
            base_url=base_url,
            api_key=api_key,
            model=model,
            headers=headers,
            extra_body=extra_body
        )
        
        return f"""### 生成成功！

加密的配置密钥: 
```
{encrypted_key}
```

请安全地保存此密钥，并将其提供给需要访问LLM服务的应用程序。"""
        
    except Exception as e:
        return f"❌ 生成失败: {str(e)}"


def create_demo():
    """创建Gradio演示界面"""
    
    with gr.Blocks(title="LLM配置密钥生成器") as demo:
        gr.Markdown("# LLM配置密钥生成器")
        gr.Markdown("生成加密的LLM配置密钥，可安全分享给应用开发者而不暴露原始API密钥")
        
        with gr.Row():
            with gr.Column():
                provider = gr.Dropdown(
                    label="LLM提供商",
                    choices=[p.value for p in LLMProvider],
                    value="openai"
                )
                
                base_url = gr.Textbox(
                    label="API基础URL",
                    placeholder="https://api.openai.com/v1",
                    value="https://api.openai.com/v1"
                )
                
                api_key = gr.Textbox(
                    label="API密钥",
                    placeholder="sk-...",
                    type="password"
                )
                
                model = gr.Textbox(
                    label="模型名称",
                    placeholder="gpt-3.5-turbo",
                    value="gpt-3.5-turbo"
                )
                
            with gr.Column():
                headers = gr.Textbox(
                    label="HTTP头信息（可选，每行一个键值对，例如：HTTP-Referer=https://example.com）",
                    placeholder="HTTP-Referer=https://example.com\nX-Title=MyApp",
                    lines=5
                )
                
                extra_body = gr.Textbox(
                    label="额外请求体参数（可选，每行一个键值对）",
                    placeholder="temperature=0.7\nmax_tokens=2000",
                    lines=5
                )
        
        generate_btn = gr.Button("生成加密配置密钥", variant="primary")
        
        result = gr.Markdown("*填写表单并点击生成按钮*")
        
        # 绑定事件
        generate_btn.click(
            fn=generate_key,
            inputs=[provider, base_url, api_key, model, headers, extra_body],
            outputs=[result]
        )
        
    return demo


def main():
    """主函数"""
    demo = create_demo()
    demo.launch(share=False)


if __name__ == "__main__":
    main() 