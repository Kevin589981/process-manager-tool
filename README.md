# Kiro 后台进程管理解决方案

## 问题描述

在使用 Kiro 时，当需要启动长期运行的后台服务（如 uvicorn、redis-server 等）并随后运行测试时，Kiro 会因为同步等待进程退出而无限阻塞，导致后续命令无法执行。


当然，你也可以将这个项目引入自己

## 解决方案

本项目提供了一个简单而有效的进程管理脚本 `simple_process_manager.py`，可以在 Kiro 中实现非阻塞的后台服务管理。

## 核心文件

- `simple_process_manager.py` - 主要的进程管理脚本
- `demo_workflow.py` - 基本功能演示
- `fastapi_test_example.py` - 针对原始问题的完整解决方案
- `solution.md` - 详细的技术方案文档

## 快速开始

### 1. 基本用法

```bash
# 启动后台服务
python simple_process_manager.py start myapp "uvicorn main:app --port 8000"

# 等待服务就绪
python simple_process_manager.py wait-healthy 8000

# 查看运行的进程
python simple_process_manager.py list

# 停止服务
python simple_process_manager.py stop myapp
```

### 2. 完整工作流（解决原始问题）

在 Kiro 中执行：

```bash
python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

### 3. 运行演示

```bash
# 基本功能演示
python demo_workflow.py

# FastAPI 测试场景演示
python fastapi_test_example.py
```

## 功能特性

- ✅ **非阻塞启动**: 后台服务不会阻塞后续命令
- ✅ **健康检查**: 等待端口就绪后再执行测试
- ✅ **进程管理**: 启动、停止、列表、清理功能
- ✅ **跨平台**: 支持 Windows/Linux/macOS
- ✅ **持久化**: 进程信息保存到文件，支持会话恢复
- ✅ **错误处理**: 完善的异常处理和超时机制

## 命令参考

```bash
# 启动进程
python simple_process_manager.py start <name> <command>

# 停止进程
python simple_process_manager.py stop <name> [--force]

# 列出所有进程
python simple_process_manager.py list

# 等待端口就绪
python simple_process_manager.py wait-healthy <port> [timeout]

# 清理所有进程
python simple_process_manager.py cleanup
```

## 使用场景

1. **Web 应用测试**: 启动 FastAPI/Django 应用，运行集成测试
2. **微服务测试**: 同时启动多个服务，运行端到端测试
3. **数据库测试**: 启动 Redis/PostgreSQL，运行数据相关测试
4. **前端开发**: 同时启动前后端服务进行开发调试

## 技术原理

- 使用 `subprocess.Popen` 非阻塞启动进程
- 进程信息持久化到 JSON 文件
- 通过 socket 连接检查端口健康状态
- 支持优雅停止和强制终止
- 跨平台进程管理（Windows 使用 taskkill，Unix 使用 signal）

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个解决方案。

## 许可证

MIT License