#!/usr/bin/env python3
"""
简单的进程管理脚本
不依赖 MCP，直接通过命令行使用
"""

import subprocess
import sys
import time
import json
import socket
import os
import signal
from typing import Dict, Any, Optional

class SimpleProcessManager:
    def __init__(self):
        self.processes_file = "running_processes.json"
        
    def load_processes(self) -> Dict[str, Any]:
        """从文件加载进程信息"""
        try:
            if os.path.exists(self.processes_file):
                with open(self.processes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_processes(self, processes: Dict[str, Any]):
        """保存进程信息到文件"""
        try:
            with open(self.processes_file, 'w', encoding='utf-8') as f:
                json.dump(processes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存进程信息失败: {e}")
    
    def start_process(self, name: str, command: str, cwd: Optional[str] = None):
        """启动进程"""
        processes = self.load_processes()
        
        if name in processes:
            print(f"[ERROR] 进程 '{name}' 已经在运行 (PID: {processes[name]['pid']})")
            return
        
        try:
            # 启动进程
            proc = subprocess.Popen(
                command.split(),
                cwd=cwd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # 保存进程信息
            processes[name] = {
                'pid': proc.pid,
                'command': command,
                'cwd': cwd or os.getcwd(),
                'start_time': time.time()
            }
            
            self.save_processes(processes)
            print(f"[OK] 启动进程 '{name}' (PID: {proc.pid})")
            
        except Exception as e:
            print(f"[ERROR] 启动进程 '{name}' 失败: {e}")
    
    def stop_process(self, name: str, force: bool = False):
        """停止进程"""
        processes = self.load_processes()
        
        if name not in processes:
            print(f"[ERROR] 进程 '{name}' 不存在")
            return
        
        pid = processes[name]['pid']
        
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/F' if force else '/T', '/PID', str(pid)], 
                             check=False, capture_output=True)
            else:  # Unix/Linux
                os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
            
            del processes[name]
            self.save_processes(processes)
            print(f"[OK] 停止进程 '{name}' (PID: {pid})")
            
        except Exception as e:
            print(f"[ERROR] 停止进程 '{name}' 失败: {e}")
    
    def list_processes(self):
        """列出所有进程"""
        processes = self.load_processes()
        
        if not processes:
            print("[INFO] 没有运行的进程")
            return
        
        print("[INFO] 运行中的进程:")
        for name, info in processes.items():
            print(f"  - {name}: PID {info['pid']}, 命令: {info['command']}")
    
    def wait_healthy(self, port: int, timeout: int = 30, host: str = 'localhost'):
        """等待端口就绪"""
        print(f"[INFO] 等待端口 {port} 就绪...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    elapsed = time.time() - start_time
                    print(f"[OK] 端口 {port} 就绪 (耗时 {elapsed:.1f}s)")
                    return
            except:
                pass
            
            time.sleep(1)
        
        print(f"[ERROR] 端口 {port} 在 {timeout} 秒内未就绪")
        sys.exit(1)
    
    def cleanup_all(self):
        """清理所有进程"""
        processes = self.load_processes()
        
        if not processes:
            print("[INFO] 没有需要清理的进程")
            return
        
        print("[INFO] 清理所有进程...")
        for name in list(processes.keys()):
            self.stop_process(name, force=True)

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python simple_process_manager.py start <name> <command>")
        print("  python simple_process_manager.py stop <name> [--force]")
        print("  python simple_process_manager.py list")
        print("  python simple_process_manager.py wait-healthy <port> [timeout]")
        print("  python simple_process_manager.py cleanup")
        sys.exit(1)
    
    manager = SimpleProcessManager()
    command = sys.argv[1]
    
    if command == 'start':
        if len(sys.argv) < 4:
            print("[ERROR] 用法: start <name> <command>")
            sys.exit(1)
        name = sys.argv[2]
        cmd = ' '.join(sys.argv[3:])
        manager.start_process(name, cmd)
        
    elif command == 'stop':
        if len(sys.argv) < 3:
            print("[ERROR] 用法: stop <name> [--force]")
            sys.exit(1)
        name = sys.argv[2]
        force = '--force' in sys.argv
        manager.stop_process(name, force)
        
    elif command == 'list':
        manager.list_processes()
        
    elif command == 'wait-healthy':
        if len(sys.argv) < 3:
            print("[ERROR] 用法: wait-healthy <port> [timeout]")
            sys.exit(1)
        port = int(sys.argv[2])
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        manager.wait_healthy(port, timeout)
        
    elif command == 'cleanup':
        manager.cleanup_all()
        
    else:
        print(f"[ERROR] 未知命令: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()