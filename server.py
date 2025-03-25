import importlib
import importlib.util
from pathlib import Path

from dotenv import load_dotenv
from mcp import types
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import uvicorn

# 加载.env文件
load_dotenv()

app = Server("tools-server")
sse = SseServerTransport("/messages")

# 用于存储所有工具的字典
_tools = {}
_functions = {}


# 加载所有工具
def load_tools():
    tools_dir = Path(__file__).parent / "tools"
    for file in tools_dir.glob("*.py"):
        if file.name != "__init__.py":
            module_name = f"tools.{file.stem}"
            module = importlib.import_module(module_name)
            if hasattr(module, "tool") and hasattr(module, "function"):
                _tools[module.tool.name] = module.tool
                _functions[module.tool.name] = module.function


# 初始化时加载所有工具
load_tools()


async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())


starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """返回所有已加载的工具列表"""
    return list(_tools.values())


@app.call_tool()
async def call_entry(
    name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """调用指定的工具函数"""
    if name in _functions:
        return await _functions[name](**arguments)
    return [types.TextContent(type="text", text="method not found")]


if __name__ == "__main__":
    uvicorn.run(
        "server:starlette_app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        timeout_graceful_shutdown=1,
    )
