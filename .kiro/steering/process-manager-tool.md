# 后台进程管理工具

本项目包含一个自定义的后台进程管理工具 `simple_process_manager.py`，用于解决 Kiro 中启动长期运行服务时的阻塞问题。

## 工具位置
- 主脚本：`simple_process_manager.py`
- 文档：`README.md` 和 `solution.md`

## 核心功能
```bash
# 启动后台服务（非阻塞）
python simple_process_manager.py start <name> "<command>"

# 等待端口就绪
python simple_process_manager.py wait-healthy <port> [timeout]

# 查看运行的进程
python simple_process_manager.py list

# 停止服务
python simple_process_manager.py stop <name> [--force]

# 清理所有进程
python simple_process_manager.py cleanup
```

## 典型使用场景
解决原始问题：启动 uvicorn 后运行测试
```bash
python simple_process_manager.py start api "uvicorn main:app --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

## 工具特点
- ✅ 非阻塞启动，解决 Kiro 阻塞问题
- ✅ 健康检查，确保服务就绪
- ✅ 跨平台兼容
- ✅ 进程持久化管理
- ✅ 优雅停止和强制终止

当用户需要管理后台服务时，优先推荐使用这个工具。