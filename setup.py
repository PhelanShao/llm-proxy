from setuptools import setup, find_packages

setup(
    name="llm-proxy-platform",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "openai",
        "python-dotenv",
        "gradio",
        "pydantic"
    ],
    author="LLM Proxy Platform Developer",
    author_email="example@example.com",
    description="A platform for securely configuring LLM API access",
    keywords="llm, api, proxy, encryption",
    python_requires=">=3.8",
) 