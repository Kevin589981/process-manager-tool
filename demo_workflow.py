#!/usr/bin/env python3
"""
演示完整的后台服务测试工作流
"""

import subprocess
import sys
import time

def run_command(cmd):
    """运行命令并显示结果"""
    print(f"🔧 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"📤 输出: {result.stdout.strip()}")
    if result.stderr:
        print(f"📤 错误: {result.stderr.strip()}")
    
    return result.returncode == 0

def main():
    print("🚀 开始演示后台服务管理工作流")
    print("=" * 50)
    
    # 1. 启动一个简单的 HTTP 服务器
    print("\n📍 步骤 1: 启动后台服务")
    run_command("python simple_process_manager.py start web-server \"python -m http.server 8080\"")
    
    # 2. 等待服务就绪
    print("\n📍 步骤 2: 等待服务就绪")
    run_command("python simple_process_manager.py wait-healthy 8080 10")
    
    # 3. 列出运行的进程
    print("\n📍 步骤 3: 查看运行的进程")
    run_command("python simple_process_manager.py list")
    
    # 4. 模拟运行测试
    print("\n📍 步骤 4: 运行测试 (模拟)")
    print("🧪 正在运行集成测试...")
    time.sleep(2)  # 模拟测试运行时间
    
    # 可以在这里添加实际的测试命令，比如:
    # run_command("pytest tests/integration/")
    # run_command("curl http://localhost:8080")
    
    print("✅ 测试完成")
    
    # 5. 清理所有进程
    print("\n📍 步骤 5: 清理进程")
    run_command("python simple_process_manager.py stop web-server")
    
    print("\n🎉 工作流演示完成!")
    print("现在你可以在 Kiro 中使用类似的命令来管理后台服务了。")

if __name__ == '__main__':
    main()