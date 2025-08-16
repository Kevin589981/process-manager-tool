# Kiro Background Process Management Solution

## License

![MIT](https://img.shields.io/badge/License-MIT-blue.svg) MIT License

# Fast Usage
You can now start using it directly with `pip install kiro-process-manager`.
```bash
# Initialize the current directory for Kiro to use
# This will add a md under .kiro/steering in the current directory for Kiro to automatically use
kiro-pm init
# Start a process
kiro-pm start <name> <command>

# Stop a process
kiro-pm stop <name> [--force]

# List all processes
kiro-pm list

# Wait for a port to be ready
kiro-pm wait-healthy <port> [timeout]

# Clean up all processes
kiro-pm cleanup
```

## Problem Description

When using Kiro to start long-running background services (such as uvicorn, redis-server, etc.) and then run tests, Kiro will block indefinitely while synchronously waiting for the process to exit, preventing subsequent commands from being executed.

Of course, you can also integrate this project into your own.

## Solution

This project provides a simple and effective process management script `simple_process_manager.py` to achieve non-blocking background service management in Kiro.

## Core Files

- `simple_process_manager.py` - The main process management script
- `demo_workflow.py` - Basic functionality demonstration
- `fastapi_test_example.py` - A complete solution for the original problem
- `solution.md` - Detailed technical solution documentation

## Quick Start

### 1. Basic Usage

```bash
# Start a background service
python simple_process_manager.py start myapp "uvicorn main:app --port 8000"

# Wait for the service to be ready
python simple_process_manager.py wait-healthy 8000

# View running processes
python simple_process_manager.py list

# Stop the service
python simple_process_manager.py stop myapp
```

### 2. Complete Workflow (Solving the Original Problem)

Execute in Kiro:

```bash
python simple_process_manager.py start api "uvicorn main:app --host 0.0.0.0 --port 8000" && python simple_process_manager.py wait-healthy 8000 30 && pytest tests/integration/ && python simple_process_manager.py stop api
```

### 3. Running the Demonstration

```bash
# Basic functionality demonstration
python demo_workflow.py

# FastAPI test scenario demonstration
python fastapi_test_example.py
```

## Features

- ✅ **Non-blocking Start**: Background services will not block subsequent commands
- ✅ **Health Check**: Wait for the port to be ready before running tests
- ✅ **Process Management**: Start, stop, list, and clean up functions
- ✅ **Cross-platform**: Supports Windows/Linux/macOS
- ✅ **Persistence**: Process information is saved to a file, supporting session recovery
- ✅ **Error Handling**: Comprehensive exception handling and timeout mechanisms

## Command Reference

```bash
# Start a process
python simple_process_manager.py start <name> <command>

# Stop a process
python simple_process_manager.py stop <name> [--force]

# List all processes
python simple_process_manager.py list

# Wait for a port to be ready
python simple_process_manager.py wait-healthy <port> [timeout]

# Clean up all processes
python simple_process_manager.py cleanup
```

## Use Cases

1. **Web Application Testing**: Start FastAPI/Django applications and run integration tests
2. **Microservices Testing**: Start multiple services simultaneously and run end-to-end tests
3. **Database Testing**: Start Redis/PostgreSQL and run data-related tests
4. **Front-end Development**: Start both front-end and back-end services simultaneously for development and debugging

## Technical Principles

- Use `subprocess.Popen` to start processes non-blocking
- Persist process information to a JSON file
- Check port health status via socket connections
- Support graceful shutdown and forced termination
- Cross-platform process management (Windows uses taskkill, Unix uses signal)

## Contribution

Contributions are welcome through Issues and Pull Requests to improve this solution.

