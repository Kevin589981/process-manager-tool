# Kiro Process Manager 使用指南

## 🚀 快速开始

### 1. 安装

```bash
pip install kiro-process-manager
```

### 2. 初始化 Kiro 项目

在你的 Kiro 项目根目录中运行：

```bash
kiro-pm init
```

这会创建 `.kiro/steering/process-manager-tool.md` 文件，让 Kiro 自动识别这个工具。

### 3. 重启 Kiro

重启 Kiro IDE 以加载新的 Steering 配置。

## 📋 命令参考

### `kiro-pm init`
初始化 Kiro 项目的 Steering 配置

```bash
kiro-pm init
```

### `kiro-pm start`
启动后台进程

```bash
kiro-pm start <进程名> "<命令>"
kiro-pm start --cwd <工作目录> <进程名> "<命令>"
```

示例：
```bash
kiro-pm start api "uvicorn main:app --port 8000"
kiro-pm start --cwd ./backend api "uvicorn main:app --port 8000"
```

### `kiro-pm wait-healthy`
等待端口就绪（健康检查）

```bash
kiro-pm wait-healthy <端口> [--timeout <秒数>] [--host <主机>]
```

示例：
```bash
kiro-pm wait-healthy 8000
kiro-pm wait-healthy 8000 --timeout 60
kiro-pm wait-healthy 8000 --host 127.0.0.1
```

### `kiro-pm list`
列出所有管理的进程

```bash
kiro-pm list
```

### `kiro-pm stop`
停止进程

```bash
kiro-pm stop <进程名> [--force]
```

示例：
```bash
kiro-pm stop api
kiro-pm stop api --force  # 强制终止
```

### `kiro-pm cleanup`
清理所有进程

```bash
kiro-pm cleanup
```

## 🎯 典型使用场景

### 场景1: FastAPI + 集成测试

```bash
# 在 Kiro 中执行这个完整的工作流
kiro-pm start api "uvicorn main:app --port 8000" && kiro-pm wait-healthy 8000 30 && pytest tests/integration/ && kiro-pm stop api
```

### 场景2: 微服务测试环境

```bash
# 启动多个服务
kiro-pm start auth "uvicorn auth.main:app --port 8001"
kiro-pm start user "uvicorn user.main:app --port 8002"
kiro-pm start redis "redis-server --port 6379"

# 等待所有服务就绪
kiro-pm wait-healthy 8001
kiro-pm wait-healthy 8002
kiro-pm wait-healthy 6379

# 运行测试
pytest tests/e2e/

# 清理
kiro-pm cleanup
```

### 场景3: 前端 + 后端开发

```bash
# 启动前后端服务
kiro-pm start frontend "npm run dev"
kiro-pm start backend "python manage.py runserver 8000"

# 等待服务就绪
kiro-pm wait-healthy 3000
kiro-pm wait-healthy 8000

# 运行 E2E 测试
npm run test:e2e

# 停止服务
kiro-pm stop frontend
kiro-pm stop backend
```

## 🔧 高级用法

### 工作目录设置

```bash
# 在特定目录中启动服务
kiro-pm start --cwd ./backend api "uvicorn main:app --port 8000"
```

### 超时设置

```bash
# 设置更长的健康检查超时
kiro-pm wait-healthy 8000 --timeout 120
```

### 强制终止

```bash
# 如果进程无响应，强制终止
kiro-pm stop api --force
```

## 🐛 故障排除

### 进程启动失败

1. 检查命令是否正确
2. 确认端口没有被占用
3. 查看进程列表：`kiro-pm list`

### 端口健康检查失败

1. 确认服务确实在指定端口启动
2. 增加超时时间：`--timeout 60`
3. 检查防火墙设置

### 进程无法停止

1. 使用强制停止：`kiro-pm stop <name> --force`
2. 如果仍然无法停止，使用系统工具手动终止

### 清理残留进程

```bash
# 清理所有管理的进程
kiro-pm cleanup
```

## 💡 最佳实践

1. **使用描述性的进程名称**: 便于管理和调试
2. **总是等待健康检查**: 确保服务真正就绪后再执行测试
3. **及时清理进程**: 避免端口冲突和资源浪费
4. **使用 init 命令**: 在 Kiro 项目中使用 `kiro-pm init` 获得更好的集成体验
5. **设置合理的超时**: 根据服务启动时间设置合适的超时值

## 🔗 相关链接

- [GitHub 仓库](https://github.com/yourusername/kiro-process-manager)
- [PyPI 页面](https://pypi.org/project/kiro-process-manager/)
- [问题反馈](https://github.com/yourusername/kiro-process-manager/issues)