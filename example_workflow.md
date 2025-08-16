# Kiro 后台进程管理使用示例

## 快速开始

### 1. 确保 Python 可用
```bash
python --version  # 确保 Python 3.6+
```

### 2. 重启 Kiro
重启 Kiro 以加载新的 MCP 配置。

### 3. 测试基本功能

在 Kiro 中输入以下命令来测试进程管理功能：

```
# 测试列出进程（应该为空）
list_processes

# 启动一个简单的测试进程
start_process {"name": "test", "command": "python -m http.server 8080"}

# 检查进程列表
list_processes

# 等待端口就绪
wait_healthy {"port": 8080, "timeout": 10}

# 查看进程日志
get_logs {"name": "test", "lines": 10}

# 停止进程
stop_process {"name": "test"}
```

## 实际使用场景

### 场景1: FastAPI + 集成测试

```
# 启动 FastAPI 应用
start_process {"name": "api", "command": "uvicorn main:app --host 0.0.0.0 --port 8000"}

# 等待 API 服务就绪
wait_healthy {"port": 8000, "timeout": 30}

# 运行集成测试
pytest tests/integration/ -v

# 查看 API 日志（如果测试失败）
get_logs {"name": "api", "lines": 50}

# 清理
stop_process {"name": "api"}
```

### 场景2: 微服务测试环境

```
# 启动多个服务
start_process {"name": "auth", "command": "uvicorn auth.main:app --port 8001"}
start_process {"name": "user", "command": "uvicorn user.main:app --port 8002"}  
start_process {"name": "redis", "command": "redis-server --port 6379"}

# 等待所有服务就绪
wait_healthy {"port": 8001, "timeout": 30}
wait_healthy {"port": 8002, "timeout": 30}
wait_healthy {"port": 6379, "timeout": 30}

# 运行端到端测试
pytest tests/e2e/ -v

# 批量清理
stop_process {"name": "auth"}
stop_process {"name": "user"}
stop_process {"name": "redis"}
```

### 场景3: 前端开发服务器

```
# 启动前端开发服务器
start_process {"name": "frontend", "command": "npm run dev"}

# 启动后端 API
start_process {"name": "backend", "command": "python manage.py runserver 8000"}

# 等待服务就绪
wait_healthy {"port": 3000, "timeout": 30}
wait_healthy {"port": 8000, "timeout": 30}

# 运行 E2E 测试
npm run test:e2e

# 清理
stop_process {"name": "frontend"}
stop_process {"name": "backend"}
```

## 故障排除

### 进程启动失败
```
# 查看进程列表确认状态
list_processes

# 查看错误日志
get_logs {"name": "your_process_name", "lines": 20}
```

### 端口被占用
```
# 强制停止可能冲突的进程
stop_process {"name": "old_process", "force": true}

# 或者使用不同端口重新启动
start_process {"name": "api", "command": "uvicorn main:app --port 8001"}
```

### 进程卡住无响应
```
# 强制终止
stop_process {"name": "stuck_process", "force": true}
```

## 最佳实践

1. **使用描述性的进程名称**: 便于管理和调试
2. **总是等待健康检查**: 确保服务真正就绪后再执行测试
3. **及时清理进程**: 避免端口冲突和资源浪费
4. **查看日志排错**: 测试失败时先查看服务日志
5. **使用超时设置**: 避免无限等待

## 注意事项

- 进程管理器会在 Kiro 会话结束时自动清理所有进程
- 如果 Python 脚本意外退出，可能需要手动清理残留进程
- 在 Windows 上，某些命令可能需要调整（如使用 `python` 而不是 `python3`）