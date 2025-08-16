# Kiro 后台进程管理解决方案

## 来源
该解决方案来源于
https://github.com/kirodotdev/Kiro/issues/2017#issue-3318415455

## 问题分析

Issue 中描述的问题是 Kiro 在启动长期运行的后台服务（如 uvicorn）时会同步等待进程退出，导致后续命令无法执行。这是因为 Kiro 的默认命令执行机制是阻塞式的。


## 实现方案

### 第一步：创建
下载源码到你所需要使用的仓库

### 第二步：配置 Kiro

在.kiro\steering中配置process-manager-tool.md以便kiro集成使用


### 第三步：使用示例

通过简单的工具调用实现完整的"启动→测试→停止"工作流

## 具体实现

简单进程管理脚本（推荐）

创建了 `simple_process_manager.py`，这是一个独立的 Python 脚本，可以直接在 Kiro 中使用。

**核心功能：**
- `start`: 非阻塞启动后台进程
- `stop`: 优雅停止或强制终止进程  
- `list`: 列出所有管理的进程
- `wait-healthy`: 端口健康检查，等待服务就绪
- `cleanup`: 清理所有进程

**特性：**
- 进程信息持久化到 JSON 文件
- 跨平台支持（Windows/Linux/macOS）
- 简单易用，无需复杂配置
- 完善的错误处理

### 使用示例

在 Kiro 中可以直接使用以下命令：

```bash
# 启动后台服务
python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000"

# 等待服务就绪
python simple_process_manager.py wait-healthy 8000 30

# 运行集成测试
pytest tests/integration/

# 查看运行的进程
python simple_process_manager.py list

# 停止服务
python simple_process_manager.py stop api
```

### 完整工作流示例

```bash
# 一次性在 Kiro 中执行完整工作流
python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

### 高级用法

**并行运行多个服务：**
```bash
python simple_process_manager.py start api "uvicorn main:app --port 8000"
python simple_process_manager.py start redis "redis-server --port 6379"
python simple_process_manager.py wait-healthy 8000
python simple_process_manager.py wait-healthy 6379
# 运行测试...
python simple_process_manager.py stop api
python simple_process_manager.py stop redis
```

**查看所有进程状态：**
```bash
python simple_process_manager.py list
```

**强制终止卡住的进程：**
```bash
python simple_process_manager.py stop api --force
```

**一键清理所有进程：**
```bash
python simple_process_manager.py cleanup
```


## 优势

1. **非阻塞执行**: 解决了原始问题中 uvicorn 阻塞后续命令的问题
2. **完整生命周期管理**: 启动、监控、日志、停止一应俱全
3. **健康检查**: 内置端口检查，确保服务真正就绪后再执行测试
4. **自动清理**: 会话结束时自动清理所有后台进程，避免僵尸进程
5. **错误处理**: 完善的异常处理和超时机制
6. **易于扩展**: 基于 Kiro MCP 框架，可轻松添加新功能

## 测试验证

已创建完整的演示脚本验证方案可行性：

- `demo_workflow.py`: 基本工作流演示
- `fastapi_test_example.py`: 针对原始问题的完整解决方案演示

测试结果显示，方案完全解决了原始问题中 uvicorn 阻塞后续命令的情况。

## 在 Kiro 中的实际使用

现在你可以在 Kiro 中直接使用以下命令解决原始问题：

```bash
# 原来的问题命令（会阻塞）：
# uvicorn main:app --host 0.0.0.0 --port 8000 && pytest tests/integration/

# 新的解决方案（非阻塞）：
python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

或者分步执行：
1. `python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000"`
2. `python simple_process_manager.py wait-healthy 8000 30`
3. `pytest tests/integration/`
4. `python simple_process_manager.py stop api`

## 结论

通过创建简单的进程管理脚本，我们成功解决了 Kiro 中后台服务管理的问题：

1. **立即可用**: 无需复杂配置，直接运行 Python 脚本
2. **完全解决原问题**: uvicorn 不再阻塞后续命令
3. **跨平台兼容**: 支持 Windows/Linux/macOS
4. **功能完整**: 包含启动、停止、健康检查、进程列表等功能
5. **易于集成**: 可以直接在 Kiro 的命令中使用

这个方案不需要修改 Kiro 源码，也不依赖复杂的 MCP 协议实现，是一个实用且可靠的解决方案。