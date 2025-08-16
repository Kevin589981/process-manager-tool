from setuptools import setup, find_packages

setup(
    name="kiro-process-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="非阻塞后台进程管理工具，解决 Kiro IDE 中服务启动阻塞问题",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kiro-process-manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7+",
        "Topic :: Software Development :: Tools",
        "Topic :: System :: System Shells",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "kiro-pm=kiro_process_manager.cli:main",
        ],
    },
    keywords="kiro ide process manager background service uvicorn fastapi",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/kiro-process-manager/issues",
        "Source": "https://github.com/yourusername/kiro-process-manager",
        "Documentation": "https://github.com/yourusername/kiro-process-manager#readme",
    },
)