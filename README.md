# LLM代理平台

这是一个安全的LLM代理平台，允许用户加密和使用不同LLM服务提供商的API配置。

## 功能

- 将多种LLM供应商的API配置（base URL, model, API key等）加密成一个字符串
- 使用加密的配置字符串自动设置环境变量，用于LLM服务访问
- 基于Gradio的测试对话平台，用于验证配置和测试LLM交互
- 基于Gradio的密钥生成界面，方便生成加密的配置密钥

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 或者安装为包（开发模式）
pip install -e .
```

## 使用方法

### 使用GUI生成加密配置

```bash
# 启动密钥生成界面
python generate_key.py
```

或者直接运行：

```bash
python -m src.key_generator_app
```

### 通过代码生成加密配置

```python
from src.key_generator import generate_encrypted_key

# 生成加密的配置密钥
encrypted_key = generate_encrypted_key(
    provider="openai",
    base_url="https://api.openai.com/v1",
    api_key="your-api-key",
    model="gpt-3.5-turbo"
)
print(f"加密的配置密钥: {encrypted_key}")
```

### 使用加密配置访问LLM

```python
from src.llm_proxy import LLMProxy

# 初始化代理
proxy = LLMProxy(encrypted_key="your-encrypted-key")

# 发送消息
response = proxy.send_message("你好，世界！")
print(response)
```

### 启动对话测试界面

```bash
# 启动对话测试界面
python chat_app.py
```

或者直接运行：

```bash
python -m src.app
```

## 开发

### 运行测试

```bash
python -m unittest discover tests
```

### 使用命令行工具生成密钥

```bash
python examples/generate_key.py --provider openai --base-url https://api.openai.com/v1 --api-key your-api-key --model gpt-3.5-turbo
```

## 许可证

MIT 