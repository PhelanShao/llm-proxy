"""
Gradio-based LLM configuration key generator application
"""

import gradio as gr
import os
import sys
import json
from typing import Dict, Any, List, Tuple

# Ensure project modules can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.key_generator import generate_encrypted_key
from src.models import LLMProvider


def parse_key_value_pairs(text: str) -> Dict[str, Any]:
    """
    Parse key-value pair text into dictionary
    
    Format: One key-value pair per line, format is "key=value"
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
        
        # Try to convert to appropriate type
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
    """Generate encrypted configuration key"""
    try:
        # Parse headers and extra request body parameters
        headers = parse_key_value_pairs(headers_text)
        extra_body = parse_key_value_pairs(extra_body_text)
        
        # Generate encrypted key
        encrypted_key = generate_encrypted_key(
            provider=provider,
            base_url=base_url,
            api_key=api_key,
            model=model,
            headers=headers,
            extra_body=extra_body
        )
        
        return f"""### Generation successful!

Encrypted configuration key: 
```
{encrypted_key}
```

Please save this key securely and provide it to applications that need to access LLM services."""
        
    except Exception as e:
        return f"❌ Generation failed: {str(e)}"


def create_demo():
    """Create Gradio demo interface"""
    
    with gr.Blocks(title="LLM Configuration Key Generator") as demo:
        gr.Markdown("# LLM Configuration Key Generator")
        gr.Markdown("Generate encrypted LLM configuration keys that can be safely shared with application developers without exposing the original API keys")
        
        with gr.Row():
            with gr.Column():
                provider = gr.Dropdown(
                    label="LLM Provider",
                    choices=[p.value for p in LLMProvider],
                    value="openai"
                )
                
                base_url = gr.Textbox(
                    label="API Base URL",
                    placeholder="https://api.openai.com/v1",
                    value="https://api.openai.com/v1"
                )
                
                api_key = gr.Textbox(
                    label="API Key",
                    placeholder="sk-...",
                    type="password"
                )
                
                model = gr.Textbox(
                    label="Model Name",
                    placeholder="gpt-3.5-turbo",
                    value="gpt-3.5-turbo"
                )
                
            with gr.Column():
                headers = gr.Textbox(
                    label="HTTP Headers (Optional, one key-value pair per line, e.g., HTTP-Referer=https://example.com)",
                    placeholder="HTTP-Referer=https://example.com\nX-Title=MyApp",
                    lines=5
                )
                
                extra_body = gr.Textbox(
                    label="Extra Request Body Parameters (Optional, one key-value pair per line)",
                    placeholder="temperature=0.7\nmax_tokens=2000",
                    lines=5
                )
        
        generate_btn = gr.Button("Generate Encrypted Configuration Key", variant="primary")
        
        result = gr.Markdown("*Fill out the form and click the generate button*")
        
        # Bind events
        generate_btn.click(
            fn=generate_key,
            inputs=[provider, base_url, api_key, model, headers, extra_body],
            outputs=[result]
        )
        
    return demo


def main():
    """Main function"""
    demo = create_demo()
    demo.launch(share=False)


if __name__ == "__main__":
    main() 