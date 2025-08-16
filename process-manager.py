#!/usr/bin/env python3
"""
Kiro 进程管理 MCP Server
提供非阻塞的后台进程管理功能
"""

import json
import logging
import os
import subprocess
import sys
import time
from typing import Dict, Any, Optional
import socket
import atexit

# 配置日志到文件，避免干扰 MCP 通信
logging.basicConfig(
    filename='process-manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProcessManager:
    def __init__(self):
        self.processes: Dict[str, Dict[str, Any]] = {}
        # 注册退出时清理函数
        atexit.register(self.cleanup_all)
        
    def start_process(self, name: str, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """启动一个后台进程"""
        if name in self.processes:
            raise ValueError(f"进程 '{name}' 已经在运行")
        
        try:
            # 分割命令
            cmd_parts = command.split()
            if not cmd_parts:
                raise ValueError("命令不能为空")
            
            # 启动进程
            proc = subprocess.Popen(
                cmd_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 存储进程信息
            self.processes[name] = {
                'process': proc,
                'pid': proc.pid,
                'command': command,
                'start_time': time.time(),
                'cwd': cwd or os.getcwd(),
                'stdout_lines': [],
                'stderr_lines': []
            }
            
            logger.info(f"启动进程 '{name}' (PID: {proc.pid})")
            return {
                'name': name,
                'pid': proc.pid,
                'status': 'started',
                'command': command
            }
            
        except Exception as e:
            logger.error(f"启动进程 '{name}' 失败: {e}")
            raise
    
    def stop_process(self, name: str, force: bool = False) -> Dict[str, Any]:
        """停止一个进程"""
        if name not in self.processes:
            raise ValueError(f"进程 '{name}' 不存在")
        
        proc_info = self.processes[name]
        proc = proc_info['process']
        
        try:
            if proc.poll() is None:  # 进程还在运行
                if force:
                    proc.kill()  # SIGKILL
                    logger.info(f"强制终止进程 '{name}' (PID: {proc.pid})")
                else:
                    proc.terminate()  # SIGTERM
                    logger.info(f"优雅停止进程 '{name}' (PID: {proc.pid})")
                
                # 等待进程结束
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if not force:
                        proc.kill()
                        proc.wait()
                        logger.info(f"进程 '{name}' 超时，已强制终止")
            
            del self.processes[name]
            return {
                'name': name,
                'status': 'stopped'
            }
            
        except Exception as e:
            logger.error(f"停止进程 '{name}' 失败: {e}")
            raise
    
    def list_processes(self) -> Dict[str, Any]:
        """列出所有进程"""
        result = {}
        for name, info in self.processes.items():
            proc = info['process']
            result[name] = {
                'pid': info['pid'],
                'command': info['command'],
                'status': 'running' if proc.poll() is None else 'stopped',
                'start_time': info['start_time'],
                'cwd': info['cwd']
            }
        return result
    
    def get_logs(self, name: str, lines: int = 50) -> Dict[str, Any]:
        """获取进程日志"""
        if name not in self.processes:
            raise ValueError(f"进程 '{name}' 不存在")
        
        proc_info = self.processes[name]
        proc = proc_info['process']
        
        # 读取新的输出（非阻塞）
        try:
            import select
            import fcntl
            
            # 设置非阻塞模式
            if proc.stdout:
                fd = proc.stdout.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                
                try:
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        proc_info['stdout_lines'].append(line.strip())
                except:
                    pass
            
            if proc.stderr:
                fd = proc.stderr.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                
                try:
                    while True:
                        line = proc.stderr.readline()
                        if not line:
                            break
                        proc_info['stderr_lines'].append(line.strip())
                except:
                    pass
                    
        except ImportError:
            # Windows 不支持 fcntl，使用简单的方法
            pass
        
        return {
            'name': name,
            'stdout': proc_info['stdout_lines'][-lines:],
            'stderr': proc_info['stderr_lines'][-lines:],
            'status': 'running' if proc.poll() is None else 'stopped'
        }
    
    def wait_healthy(self, port: int, timeout: int = 30, host: str = 'localhost') -> Dict[str, Any]:
        """等待端口可用（健康检查）"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    return {
                        'status': 'healthy',
                        'port': port,
                        'elapsed': time.time() - start_time
                    }
            except:
                pass
            
            time.sleep(1)
        
        raise TimeoutError(f"端口 {port} 在 {timeout} 秒内未就绪")
    
    def cleanup_all(self):
        """清理所有进程"""
        for name in list(self.processes.keys()):
            try:
                self.stop_process(name, force=True)
            except:
                pass

def main():
    manager = ProcessManager()
    
    # 首先发送初始化响应
    init_response = {
        "jsonrpc": "2.0",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listChanged": True
                }
            },
            "serverInfo": {
                "name": "process-manager",
                "version": "1.0.0"
            }
        }
    }
    
    # 读取请求并处理
    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
                
            try:
                request = json.loads(line.strip())
                logger.info(f"收到请求: {request}")
                
                method = request.get('method')
                params = request.get('params', {})
                request_id = request.get('id')
                
                if method == 'initialize':
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {
                                    "listChanged": True
                                }
                            },
                            "serverInfo": {
                                "name": "process-manager",
                                "version": "1.0.0"
                            }
                        }
                    }
                    
                elif method == 'tools/list':
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "tools": [
                                {
                                    "name": "start_process",
                                    "description": "启动一个后台进程",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "进程名称"},
                                            "command": {"type": "string", "description": "要执行的命令"},
                                            "cwd": {"type": "string", "description": "工作目录（可选）"}
                                        },
                                        "required": ["name", "command"]
                                    }
                                },
                                {
                                    "name": "stop_process",
                                    "description": "停止一个进程",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "进程名称"},
                                            "force": {"type": "boolean", "description": "是否强制终止"}
                                        },
                                        "required": ["name"]
                                    }
                                },
                                {
                                    "name": "list_processes",
                                    "description": "列出所有管理的进程",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {}
                                    }
                                },
                                {
                                    "name": "get_logs",
                                    "description": "获取进程日志",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string", "description": "进程名称"},
                                            "lines": {"type": "integer", "description": "日志行数"}
                                        },
                                        "required": ["name"]
                                    }
                                },
                                {
                                    "name": "wait_healthy",
                                    "description": "等待端口就绪（健康检查）",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "port": {"type": "integer", "description": "端口号"},
                                            "timeout": {"type": "integer", "description": "超时时间（秒）"},
                                            "host": {"type": "string", "description": "主机地址"}
                                        },
                                        "required": ["port"]
                                    }
                                }
                            ]
                        }
                    }
                    
                elif method == 'tools/call':
                    tool_name = params.get('name')
                    arguments = params.get('arguments', {})
                    
                    try:
                        if tool_name == 'start_process':
                            result = manager.start_process(
                                arguments['name'],
                                arguments['command'],
                                arguments.get('cwd')
                            )
                        elif tool_name == 'stop_process':
                            result = manager.stop_process(
                                arguments['name'],
                                arguments.get('force', False)
                            )
                        elif tool_name == 'list_processes':
                            result = manager.list_processes()
                        elif tool_name == 'get_logs':
                            result = manager.get_logs(
                                arguments['name'],
                                arguments.get('lines', 50)
                            )
                        elif tool_name == 'wait_healthy':
                            result = manager.wait_healthy(
                                arguments['port'],
                                arguments.get('timeout', 30),
                                arguments.get('host', 'localhost')
                            )
                        else:
                            raise ValueError(f"未知工具: {tool_name}")
                        
                        response = {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'result': {
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': json.dumps(result, ensure_ascii=False, indent=2)
                                    }
                                ]
                            }
                        }
                        
                    except Exception as e:
                        logger.error(f"工具调用失败: {e}")
                        response = {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'error': {
                                'code': -1,
                                'message': str(e)
                            }
                        }
                
                else:
                    response = {
                        'jsonrpc': '2.0',
                        'id': request_id,
                        'error': {
                            'code': -32601,
                            'message': f'Method not found: {method}'
                        }
                    }
                
                print(json.dumps(response, ensure_ascii=False))
                sys.stdout.flush()
                logger.info(f"发送响应: {response}")
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON 解析错误: {e}")
                continue
            except Exception as e:
                logger.error(f"处理请求时出错: {e}")
                continue
                
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在清理...")
    except Exception as e:
        logger.error(f"主循环出错: {e}")
    finally:
        manager.cleanup_all()

if __name__ == '__main__':
    main()