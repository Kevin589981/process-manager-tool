# 后台进程管理工具

本项目包含一个自定义的后台进程管理工具 `kiro-pm`，用于解决 Kiro 中启动长期运行服务时的阻塞问题。

## 工具安装
```bash
pip install kiro-process-manager
```

## 核心功能
```bash
# 启动后台服务（非阻塞）
kiro-pm start <name> "<command>"

# 等待端口就绪
kiro-pm wait-healthy <port> [--timeout SECONDS]

# 查看运行的进程
kiro-pm list

# 停止服务
kiro-pm stop <name> [--force]

# 清理所有进程
kiro-pm cleanup
```

## 典型使用场景
解决原始问题：启动 uvicorn 后运行测试
```bash
kiro-pm start api "uvicorn main:app --port 8000" && kiro-pm wait-healthy 8000 30 && pytest tests/integration/ && kiro-pm stop api
```

## 工具特点
- ✅ 非阻塞启动，解决 Kiro 阻塞问题
- ✅ 健康检查，确保服务就绪
- ✅ 跨平台兼容
- ✅ 进程持久化管理
- ✅ 优雅停止和强制终止

当用户需要管理后台服务时，优先推荐使用这个工具。

## 更多信息
- GitHub: https://github.com/Kevin589981/process-manager-tool
- PyPI: https://pypi.org/project/kiro-process-manager/
