import asyncio
import json
import logging
import os
from typing import Dict, Any, List, Optional, Set
from mcp.server.lowlevel import Server
from mcp.types import Tool, TextContent, CallToolRequest, ListToolsRequest
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.types import Receive, Scope, Send
from contextlib import asynccontextmanager

# 导入你之前转换好的 Notion 客户端
from notionClient import NotionClientWrapper

# 假设你有一个 schemas.py 文件定义了工具结构，或者在这里定义
import schemas

# 配置日志
logging.basicConfig(level=logging.INFO)


async def create_mcp_app(
    notion_token: str, enabled_tools_set: Set[str], enable_markdown_conversion: bool
):
    # 1. 初始化 Server
    server = Server("Notion MCP Server")

    # 2. 初始化 Notion 客户端
    notion_client = NotionClientWrapper(notion_token)

    # 3. 注册：列出工具 (List Tools)
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        # 这里列出所有可用的工具定义 (对应 TS 中的 schemas.*)
        all_tools = [
            schemas.append_block_children_tool,
            schemas.retrieve_block_tool,
            schemas.retrieve_block_children_tool,
            schemas.delete_block_tool,
            schemas.update_block_tool,
            schemas.retrieve_page_tool,
            schemas.update_page_properties_tool,
            schemas.list_all_users_tool,
            schemas.retrieve_user_tool,
            schemas.retrieve_bot_user_tool,
            schemas.create_database_tool,
            schemas.query_database_tool,
            schemas.retrieve_database_tool,
            schemas.update_database_tool,
            schemas.create_database_item_tool,
            schemas.create_comment_tool,
            schemas.retrieve_comments_tool,
            schemas.search_tool,
        ]

        # 过滤工具
        return [tool for tool in all_tools if tool.name in enabled_tools_set]

    # 4. 注册：调用工具 (Call Tool)
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
        logging.info(f"Received CallToolRequest: {name}")
        try:
            if not arguments:
                raise ValueError("No arguments provided")

            response: Any = None

            # --- 辅助函数：安全获取必填字符串参数 ---
            def get_required_str(key: str) -> str:
                val = arguments.get(key)
                if not val or not isinstance(val, str):
                    raise ValueError(f"Missing required string argument: {key}")
                return val

            # --- 工具路由逻辑 ---
            if name == "notion_append_block_children":
                block_id = get_required_str("block_id")
                children = arguments.get("children")
                if not children:
                    raise ValueError("Missing required argument: children")
                response = notion_client.append_block_children(block_id, children)

            elif name == "notion_retrieve_block":
                block_id = get_required_str("block_id")
                response = notion_client.retrieve_block(block_id)

            elif name == "notion_retrieve_block_children":
                block_id = get_required_str("block_id")
                response = notion_client.retrieve_block_children(
                    block_id, arguments.get("start_cursor"), arguments.get("page_size")
                )

            elif name == "notion_delete_block":
                block_id = get_required_str("block_id")
                response = notion_client.delete_block(block_id)

            elif name == "notion_update_block":
                block_id = get_required_str("block_id")
                block = arguments.get("block")
                if not block:
                    raise ValueError("Missing required argument: block")
                response = notion_client.update_block(block_id, block)

            elif name == "notion_retrieve_page":
                page_id = get_required_str("page_id")
                response = notion_client.retrieve_page(page_id)

            elif name == "notion_update_page_properties":
                page_id = get_required_str("page_id")
                properties = arguments.get("properties")
                if not properties:
                    raise ValueError("Missing required argument: properties")
                response = notion_client.update_page_properties(page_id, properties)

            elif name == "notion_list_all_users":
                response = notion_client.list_all_users(
                    arguments.get("start_cursor"), arguments.get("page_size")
                )

            elif name == "notion_retrieve_user":
                user_id = get_required_str("user_id")
                response = notion_client.retrieve_user(user_id)

            elif name == "notion_retrieve_bot_user":
                response = notion_client.retrieve_bot_user()

            elif name == "notion_query_database":
                database_id = get_required_str("database_id")
                response = notion_client.query_database(
                    database_id,
                    arguments.get("filter"),
                    arguments.get("sorts"),
                    arguments.get("start_cursor"),
                    arguments.get("page_size"),
                )

            elif name == "notion_create_database":
                parent = arguments.get("parent")
                properties = arguments.get("properties")
                if not parent or not properties:
                    raise ValueError("Missing required arguments: parent, properties")

                response = notion_client.create_database(
                    parent, properties, arguments.get("title")
                )

            elif name == "notion_retrieve_database":
                database_id = get_required_str("database_id")
                response = notion_client.retrieve_database(database_id)

            elif name == "notion_update_database":
                # 【你报错的地方在这里】
                # 我们先提取并检查 database_id，确保它是 str
                database_id = get_required_str("database_id")

                response = notion_client.update_database(
                    database_id,
                    arguments.get("title"),
                    arguments.get("description"),
                    arguments.get("properties"),
                )

            elif name == "notion_create_database_item":
                database_id = get_required_str("database_id")
                properties = arguments.get("properties")
                if not properties:
                    raise ValueError("Missing required argument: properties")
                response = notion_client.create_database_item(database_id, properties)

            elif name == "notion_create_comment":
                response = notion_client.create_comment(
                    arguments.get("parent"),
                    arguments.get("discussion_id"),
                    arguments.get("rich_text"),
                )

            elif name == "notion_retrieve_comments":
                block_id = get_required_str("block_id")
                response = notion_client.retrieve_comments(
                    block_id, arguments.get("start_cursor"), arguments.get("page_size")
                )

            elif name == "notion_search":
                response = notion_client.search(
                    arguments.get("query"),
                    arguments.get("filter"),
                    arguments.get("sort"),
                    arguments.get("start_cursor"),
                    arguments.get("page_size"),
                )

            else:
                raise ValueError(f"Unknown tool: {name}")

            # --- 响应格式处理 ---
            requested_format = arguments.get("format", "markdown")
            if enable_markdown_conversion and requested_format == "markdown":
                markdown_text = notion_client.to_markdown(response)
                return [TextContent(type="text", text=markdown_text)]
            else:
                json_text = json.dumps(response, indent=2, ensure_ascii=False)
                return [TextContent(type="text", text=json_text)]

        except Exception as e:
            logging.error(f"Error executing tool: {e}")
            error_json = json.dumps({"error": str(e)}, ensure_ascii=False)
            return [TextContent(type="text", text=error_json)]

    # 5. 设置 Streamable HTTP 传输管理器
    session_manager = StreamableHTTPSessionManager(app=server)

    # 6. 定义 Lifespan (修正点)
    # 必须调用 session_manager.run()，它会返回一个 Context Manager 用于初始化后台任务组
    @asynccontextmanager
    async def lifespan(app):
        async with session_manager.run():
            yield

    # 7. 定义处理 Streamable HTTP 请求的 ASGI 应用
    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    # 8. 创建 Starlette 应用
    starlette_app = Starlette(
        routes=[
            Mount("/mcp", app=handle_streamable_http),
        ],
        lifespan=lifespan,  # 确保传入了 lifespan
        debug=True,
    )
    return starlette_app


# 简单的入口点示例
if __name__ == "__main__":
    # 从环境变量获取配置
    TOKEN = os.environ.get("NOTION_API_TOKEN")
    # 如果你想默认关闭 Markdown 转换，把 "true" 改成 "false" 即可。
    ENABLE_MD = os.environ.get("ENABLE_MARKDOWN", "true").lower() == "true"

    # 默认启用所有工具 (实际使用中你可以根据需求定义)
    ALL_TOOLS = {
        "notion_append_block_children",
        "notion_retrieve_block",
        "notion_retrieve_block_children",
        "notion_delete_block",
        "notion_update_block",
        "notion_retrieve_page",
        "notion_update_page_properties",
        "notion_list_all_users",
        "notion_retrieve_user",
        "notion_retrieve_bot_user",
        "notion_query_database",
        "notion_create_database",
        "notion_retrieve_database",
        "notion_update_database",
        "notion_create_database_item",
        "notion_create_comment",
        "notion_retrieve_comments",
        "notion_search",
    }

    if not TOKEN:
        print("Error: NOTION_API_TOKEN environment variable not set.")
    else:
        # 创建 ASGI 应用
        app = asyncio.run(create_mcp_app(TOKEN, ALL_TOOLS, ENABLE_MD))

        # 使用 uvicorn 运行 HTTP 服务器（需安装 uvicorn: pip install uvicorn）
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
