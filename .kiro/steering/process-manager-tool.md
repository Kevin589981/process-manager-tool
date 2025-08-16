# 后台进程管理工具

本项目包含一个自定义的后台进程管理工具，用于解决 Kiro 中启动长期运行服务时的阻塞问题。安装后，可以通过 `kiro-pm` 命令直接使用，未安装时也可以通过原始方式运行。

## 工具位置
- 主脚本：`simple_process_manager.py`
- 文档：`README.md` 和 `solution.md`
## 初始化
```bash
kiro-pm init
```


## 核心功能
安装后，使用 `kiro-pm` 命令：
```bash
# 启动后台服务（非阻塞）
kiro-pm start <name> "<command>"

# 等待端口就绪
kiro-pm wait-healthy <port> [timeout]

# 查看运行的进程
kiro-pm list

# 停止服务
kiro-pm stop <name> [--force]

# 清理所有进程
kiro-pm cleanup
```

未安装时，使用原始方式：
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
安装后：
```bash
kiro-pm start api "uvicorn main:app --port 8000" && kiro-pm wait-healthy 8000 30 && pytest tests/integration/ && kiro-pm stop api
```

未安装时：
```bash
python simple_process_manager.py start api "uvicorn main:app --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

## 安装方法
通过 pip 安装：
```bash
pip install kiro_process_manager
```

安装后，即可直接使用 `kiro-pm` 命令。

## 工具特点
- ✅ 非阻塞启动，解决 Kiro 阻塞问题
- ✅ 健康检查，确保服务就绪
- ✅ 跨平台兼容
- ✅ 进程持久化管理
- ✅ 优雅停止和强制终止

当用户需要管理后台服务时，优先推荐使用这个工具。安装后使用 `kiro-pm` 命令更加便捷，未安装时也可以通过原始方式运行。

