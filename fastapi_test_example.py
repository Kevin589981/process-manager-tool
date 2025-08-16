#!/usr/bin/env python3
"""
FastAPI + 集成测试的完整示例
演示如何解决原始 Issue 中的问题
"""

import subprocess
import sys
import time

def run_command(cmd, check_success=True):
    """运行命令并显示结果"""
    print(f"[CMD] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(f"[OUT] {result.stdout.strip()}")
    if result.stderr:
        print(f"[ERR] {result.stderr.strip()}")
    
    if check_success and result.returncode != 0:
        print(f"[FAIL] 命令执行失败，退出码: {result.returncode}")
        sys.exit(1)
    
    return result.returncode == 0

def main():
    print("=" * 60)
    print("FastAPI 后台服务 + 集成测试完整工作流演示")
    print("解决 Issue: Kiro 启动 uvicorn 后阻塞的问题")
    print("=" * 60)
    
    # 这就是原始问题中用户想要的工作流：
    # "Start the app with uvicorn main:app --host 0.0.0.0 --port 8000 and then run pytest tests/integration/"
    
    print("\n[STEP 1] 启动 FastAPI 应用 (非阻塞)")
    # 原来的问题：uvicorn 会阻塞，导致后续命令无法执行
    # 现在的解决方案：使用进程管理器非阻塞启动
    run_command("python simple_process_manager.py start fastapi \"uvicorn main:app --host 0.0.0.0 --port 8000\"")
    
    print("\n[STEP 2] 等待 API 服务就绪")
    # 确保服务真正启动并可以接受连接
    run_command("python simple_process_manager.py wait-healthy 8000 30")
    
    print("\n[STEP 3] 查看运行状态")
    run_command("python simple_process_manager.py list")
    
    print("\n[STEP 4] 运行集成测试")
    # 现在可以正常运行测试了，因为 uvicorn 在后台运行
    print("[INFO] 模拟运行: pytest tests/integration/")
    print("[INFO] 在实际项目中，这里会运行真正的集成测试")
    
    # 如果你有实际的测试，可以取消注释下面的行：
    # run_command("pytest tests/integration/ -v", check_success=False)
    
    # 模拟测试运行
    time.sleep(2)
    print("[OK] 集成测试完成")
    
    print("\n[STEP 5] 清理后台服务")
    run_command("python simple_process_manager.py stop fastapi")
    
    print("\n" + "=" * 60)
    print("✅ 工作流完成！")
    print("现在你可以在 Kiro 中使用这个模式：")
    print("1. 启动服务：python simple_process_manager.py start api \"uvicorn main:app --port 8000\"")
    print("2. 等待就绪：python simple_process_manager.py wait-healthy 8000")
    print("3. 运行测试：pytest tests/integration/")
    print("4. 清理服务：python simple_process_manager.py stop api")
    print("=" * 60)

if __name__ == '__main__':
    main()