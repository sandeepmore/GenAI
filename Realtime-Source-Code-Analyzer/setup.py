from setuptools import find_packages, setup 


setup(
    name="realtime-source-code-analyzer",
    version="0.1.0",
    author="Sandeep",
    author_email="sandeep.more97@gmail.com",
    packages= find_packages(),
    install_requires=[
        "openai",
        "tiktoken",
        "chromadb",
        "langchain",
        "flask",
        "GitPython",
        "python-dotenv"
    ]
)