"""
基于Gradio的LLM测试对话平台
"""

import gradio as gr
import os
from typing import List, Tuple
import traceback

from .key_generator import KeyGenerator
from .llm_proxy import LLMProxy
from .models import LLMConfig


class LLMChatApp:
    """LLM聊天应用"""
    
    def __init__(self):
        self.llm_proxy = None
        self.chat_history = []
        self.config = None
    
    def validate_config(self, encrypted_key: str) -> str:
        """验证加密的配置密钥"""
        try:
            # 尝试解密配置
            self.config = KeyGenerator.decrypt_config(encrypted_key)
            
            # 创建LLM代理
            self.llm_proxy = LLMProxy(encrypted_key)
            
            return f"✅ 配置成功！提供商: {self.config.provider}, 模型: {self.config.model}"
        except Exception as e:
            traceback.print_exc()
            return f"❌ 配置失败: {str(e)}"
    
    def chat(self, message: str) -> Tuple[str, List[Tuple[str, str]], str]:
        """处理用户消息并更新聊天历史"""
        if not self.llm_proxy:
            return "", self.chat_history, "请先配置LLM API"
        
        try:
            # 发送消息并获取响应
            response = self.llm_proxy.send_message(message)
            
            # 更新聊天历史
            self.chat_history.append((message, response))
            
            return "", self.chat_history, ""
        except Exception as e:
            traceback.print_exc()
            error_message = f"出错: {str(e)}"
            return "", self.chat_history, error_message
    
    def clear_history(self) -> List[Tuple[str, str]]:
        """清除聊天历史"""
        self.chat_history = []
        return self.chat_history


def create_demo():
    """创建Gradio演示界面"""
    app = LLMChatApp()
    
    with gr.Blocks(title="LLM代理平台") as demo:
        gr.Markdown("# LLM代理平台 - 测试对话界面")
        
        with gr.Row():
            with gr.Column(scale=4):
                encrypted_key = gr.Textbox(
                    label="加密配置密钥", 
                    placeholder="粘贴加密的配置密钥...",
                    type="password"
                )
            
            with gr.Column(scale=1):
                validate_btn = gr.Button("验证并配置")
                
        config_status = gr.Markdown("*请输入加密配置密钥并点击验证按钮*")
        
        chatbot = gr.Chatbot(label="对话")
        
        with gr.Row():
            with gr.Column(scale=4):
                msg = gr.Textbox(
                    label="消息", 
                    placeholder="输入消息...",
                    show_label=False
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button("发送")
                clear_btn = gr.Button("清除历史")
        
        error_box = gr.Textbox(label="错误信息", visible=True)
        
        # 绑定事件
        validate_btn.click(
            fn=app.validate_config,
            inputs=[encrypted_key],
            outputs=[config_status]
        )
        
        submit_btn.click(
            fn=app.chat,
            inputs=[msg],
            outputs=[msg, chatbot, error_box]
        )
        
        msg.submit(
            fn=app.chat,
            inputs=[msg],
            outputs=[msg, chatbot, error_box]
        )
        
        clear_btn.click(
            fn=app.clear_history,
            inputs=[],
            outputs=[chatbot]
        )
        
    return demo


def main():
    """主函数"""
    demo = create_demo()
    demo.launch(share=False)


if __name__ == "__main__":
    main() 