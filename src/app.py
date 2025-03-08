"""
Gradio-based LLM testing dialogue platform
"""

import gradio as gr
import os
from typing import List, Tuple
import traceback

from .key_generator import KeyGenerator
from .llm_proxy import LLMProxy
from .models import LLMConfig


class LLMChatApp:
    """LLM chat application"""
    
    def __init__(self):
        self.llm_proxy = None
        self.chat_history = []
        self.config = None
    
    def validate_config(self, encrypted_key: str) -> str:
        """Validate the encrypted configuration key"""
        try:
            # Try to decrypt the configuration
            self.config = KeyGenerator.decrypt_config(encrypted_key)
            
            # Create LLM proxy
            self.llm_proxy = LLMProxy(encrypted_key)
            
            return f"✅ Configuration successful! Provider: {self.config.provider}, Model: {self.config.model}"
        except Exception as e:
            traceback.print_exc()
            return f"❌ Configuration failed: {str(e)}"
    
    def chat(self, message: str) -> Tuple[str, List[Tuple[str, str]], str]:
        """Process user message and update chat history"""
        if not self.llm_proxy:
            return "", self.chat_history, "Please configure LLM API first"
        
        try:
            # Send message and get response
            response = self.llm_proxy.send_message(message)
            
            # Update chat history
            self.chat_history.append((message, response))
            
            return "", self.chat_history, ""
        except Exception as e:
            traceback.print_exc()
            error_message = f"Error: {str(e)}"
            return "", self.chat_history, error_message
    
    def clear_history(self) -> List[Tuple[str, str]]:
        """Clear chat history"""
        self.chat_history = []
        return self.chat_history


def create_demo():
    """Create Gradio demo interface"""
    app = LLMChatApp()
    
    with gr.Blocks(title="LLM Proxy Platform") as demo:
        gr.Markdown("# LLM Proxy Platform - Testing Dialogue Interface")
        
        with gr.Row():
            with gr.Column(scale=4):
                encrypted_key = gr.Textbox(
                    label="Encrypted Configuration Key", 
                    placeholder="Paste encrypted configuration key...",
                    type="password"
                )
            
            with gr.Column(scale=1):
                validate_btn = gr.Button("Validate and Configure")
                
        config_status = gr.Markdown("*Please enter encrypted configuration key and click validate button*")
        
        chatbot = gr.Chatbot(label="Conversation")
        
        with gr.Row():
            with gr.Column(scale=4):
                msg = gr.Textbox(
                    label="Message", 
                    placeholder="Enter message...",
                    show_label=False
                )
            
            with gr.Column(scale=1):
                submit_btn = gr.Button("Send")
                clear_btn = gr.Button("Clear History")
        
        error_box = gr.Textbox(label="Error Messages", visible=True)
        
        # Bind events
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
    """Main function"""
    demo = create_demo()
    demo.launch(share=False)


if __name__ == "__main__":
    main() 