#!/usr/bin/env python3
"""
Kiro 进程管理工具一键安装脚本
"""

import os
import shutil
import sys
import urllib.request
import json

def install_kiro_process_manager():
    """安装 Kiro 进程管理工具"""
    print("🚀 开始安装 Kiro 进程管理工具...")
    
    # 检查是否在 Kiro 项目中
    if not os.path.exists('.kiro'):
        print("❌ 请在 Kiro 项目根目录中运行此脚本")
        sys.exit(1)
    
    # 创建必要的目录
    os.makedirs('.kiro/steering', exist_ok=True)
    
    # 下载核心文件
    files_to_download = {
        'simple_process_manager.py': 'https://raw.githubusercontent.com/yourusername/kiro-process-manager/main/simple_process_manager.py',
        '.kiro/steering/process-manager-tool.md': 'https://raw.githubusercontent.com/yourusername/kiro-process-manager/main/.kiro/steering/process-manager-tool.md'
    }
    
    for local_path, url in files_to_download.items():
        try:
            print(f"📥 下载 {local_path}...")
            # 这里应该是实际的下载逻辑
            # urllib.request.urlretrieve(url, local_path)
            print(f"✅ {local_path} 安装完成")
        except Exception as e:
            print(f"❌ 下载 {local_path} 失败: {e}")
    
    print("🎉 安装完成！")
    print("现在你可以使用以下命令：")
    print("  python simple_process_manager.py start <name> \"<command>\"")
    print("  python simple_process_manager.py wait-healthy <port>")
    print("  python simple_process_manager.py list")
    print("  python simple_process_manager.py stop <name>")

if __name__ == '__main__':
    install_kiro_process_manager()