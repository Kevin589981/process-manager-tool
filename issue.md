GitHub Issue (EN)
Title: Kiro blocks forever when asked to start a long-running backend service and then run tests in the same session
Description
When I ask Kiro to start a backend service (e.g., uvicorn main:app --host 0.0.0.0 --port 8000) and then immediately execute integration tests against that service, Kiro never proceeds past the service-start step. The agent synchronously waits for the child process to exit, but the service is designed to stay alive, so Kiro hangs indefinitely and no further commands are executed.
Steps to reproduce
1.  Open a Kiro session in a workspace that contains both a FastAPI application and its pytest-based integration tests.
2.  Send the prompt:
Start the app with uvicorn main:app --host 0.0.0.0 --port 8000 and then run pytest tests/integration/.

3.  Observe that Kiro launches uvicorn, attaches to stdout/stderr, and never returns control because uvicorn does not terminate.
Expected behavior
Kiro should be able to (a) start the service in the background, (b) continue executing subsequent commands, and (c) eventually shut the service down when the session ends.
Actual behavior
Kiro hangs forever on step 2, making it impossible to automate the full “start → test → stop” workflow in a single session.
Proposed fix
Introduce a Managed Child Process (MCP) tool that:
•  Starts a command non-blocking and immediately returns {pid, status}
•  Provides mcp.list(), mcp.stop(name), mcp.restart(name), mcp.logs(name) for lifecycle and log access
•  Automatically terminates all MCP processes when the Kiro session ends
This would allow a single prompt such as:
mcp.start uvicorn main:app --host 0.0.0.0 --port 8000
mcp.waitHealthy --port 8000 --timeout 30
pytest tests/integration/
mcp.stop uvicorn