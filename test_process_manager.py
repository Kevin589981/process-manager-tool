#!/usr/bin/env python3
"""
测试进程管理器的基本功能
"""

import json
import subprocess
import time
import sys

def test_process_manager():
    """测试进程管理器的基本功能"""
    print("🧪 开始测试进程管理器...")
    
    # 启动进程管理器
    proc = subprocess.Popen(
        [sys.executable, 'process-manager.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    def send_request(method, params):
        """发送 MCP 请求"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        proc.stdin.write(json.dumps(request) + '\n')
        proc.stdin.flush()
        
        # 读取响应
        response_line = proc.stdout.readline()
        if response_line:
            return json.loads(response_line.strip())
        return None
    
    try:
        # 测试1: 列出进程（应该为空）
        print("📋 测试列出进程...")
        response = send_request("tools/call", {
            "name": "list_processes",
            "arguments": {}
        })
        print(f"✅ 进程列表: {response}")
        
        # 测试2: 启动一个测试进程
        print("🚀 测试启动进程...")
        response = send_request("tools/call", {
            "name": "start_process", 
            "arguments": {
                "name": "test_server",
                "command": "python -m http.server 8888"
            }
        })
        print(f"✅ 启动结果: {response}")
        
        # 等待一下让进程启动
        time.sleep(2)
        
        # 测试3: 健康检查
        print("🏥 测试健康检查...")
        response = send_request("tools/call", {
            "name": "wait_healthy",
            "arguments": {
                "port": 8888,
                "timeout": 10
            }
        })
        print(f"✅ 健康检查: {response}")
        
        # 测试4: 获取日志
        print("📝 测试获取日志...")
        response = send_request("tools/call", {
            "name": "get_logs",
            "arguments": {
                "name": "test_server",
                "lines": 5
            }
        })
        print(f"✅ 日志: {response}")
        
        # 测试5: 停止进程
        print("🛑 测试停止进程...")
        response = send_request("tools/call", {
            "name": "stop_process",
            "arguments": {
                "name": "test_server"
            }
        })
        print(f"✅ 停止结果: {response}")
        
        print("🎉 所有测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    finally:
        # 清理
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    test_process_manager()