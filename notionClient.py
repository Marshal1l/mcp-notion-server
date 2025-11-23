import requests
import json
from typing import Optional, List, Dict, Any, Union
import sys
import io

# 强制将标准输出流设置为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# 模拟外部导入的 markdown 转换函数
# 实际使用时你需要实现这个逻辑或导入对应的 Python 库
def convert_to_markdown(response: Dict[str, Any]) -> str:
    # 这是一个占位符，实际逻辑取决于原项目的 markdown/index.js
    return json.dumps(response, indent=2, ensure_ascii=False)


class NotionClientWrapper:
    def __init__(self, token: str):
        self.notion_token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """内部通用请求处理方法"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method, url=url, headers=self.headers, json=body, params=params
            )
            # 如果响应状态码是 4xx 或 5xx，抛出异常
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # 打印错误详情以便调试
            print(f"Notion API Error: {e.response.text}")
            raise e

    def append_block_children(
        self, block_id: str, children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"children": children}
        return self._request("PATCH", f"/blocks/{block_id}/children", body=body)

    def retrieve_block(self, block_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/blocks/{block_id}")

    def retrieve_block_children(
        self,
        block_id: str,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start_cursor:
            params["start_cursor"] = start_cursor
        if page_size:
            params["page_size"] = page_size

        return self._request("GET", f"/blocks/{block_id}/children", params=params)

    def delete_block(self, block_id: str) -> Dict[str, Any]:
        return self._request("DELETE", f"/blocks/{block_id}")

    def update_block(self, block_id: str, block: Dict[str, Any]) -> Dict[str, Any]:
        # block 本身就是一个字典，直接作为 body
        return self._request("PATCH", f"/blocks/{block_id}", body=block)

    def retrieve_page(self, page_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/pages/{page_id}")

    def update_page_properties(
        self, page_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {"properties": properties}
        return self._request("PATCH", f"/pages/{page_id}", body=body)

    def list_all_users(
        self, start_cursor: Optional[str] = None, page_size: Optional[int] = None
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if start_cursor:
            params["start_cursor"] = start_cursor
        if page_size:
            params["page_size"] = page_size

        return self._request("GET", "/users", params=params)

    def retrieve_user(self, user_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/users/{user_id}")

    def retrieve_bot_user(self) -> Dict[str, Any]:
        return self._request("GET", "/users/me")

    def create_database(
        self,
        parent: Dict[str, Any],
        properties: Dict[str, Any],
        title: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        # 显式标注类型，允许混合 List 和 Dict
        body: Dict[str, Any] = {"parent": parent, "properties": properties}
        if title:
            body["title"] = title

        return self._request("POST", "/databases", body=body)

    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        # 显式标注类型
        body: Dict[str, Any] = {}
        if filter:
            body["filter"] = filter
        if sorts:
            body["sorts"] = sorts
        if start_cursor:
            body["start_cursor"] = start_cursor
        if page_size:
            body["page_size"] = page_size

        return self._request("POST", f"/databases/{database_id}/query", body=body)

    def retrieve_database(self, database_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/databases/{database_id}")

    def update_database(
        self,
        database_id: str,
        title: Optional[List[Dict[str, Any]]] = None,
        description: Optional[List[Dict[str, Any]]] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        # 显式标注类型
        body: Dict[str, Any] = {}
        if title:
            body["title"] = title
        if description:
            body["description"] = description
        if properties:
            body["properties"] = properties

        return self._request("PATCH", f"/databases/{database_id}", body=body)

    def create_database_item(
        self, database_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }
        return self._request("POST", "/pages", body=body)

    def create_comment(
        self,
        parent: Optional[Dict[str, str]] = None,
        discussion_id: Optional[str] = None,
        rich_text: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        # 显式标注类型
        body: Dict[str, Any] = {}
        if rich_text:
            body["rich_text"] = rich_text
        if parent:
            body["parent"] = parent
        if discussion_id:
            body["discussion_id"] = discussion_id

        return self._request("POST", "/comments", body=body)

    def retrieve_comments(
        self,
        block_id: str,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"block_id": block_id}
        if start_cursor:
            params["start_cursor"] = start_cursor
        if page_size:
            params["page_size"] = page_size

        return self._request("GET", "/comments", params=params)

    def search(
        self,
        query: Optional[str] = None,
        filter: Optional[Dict[str, str]] = None,
        sort: Optional[Dict[str, str]] = None,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> Dict[str, Any]:
        # 显式标注类型
        body: Dict[str, Any] = {}
        if query:
            body["query"] = query
        if filter:
            body["filter"] = filter
        if sort:
            body["sort"] = sort
        if start_cursor:
            body["start_cursor"] = start_cursor
        if page_size:
            body["page_size"] = page_size

        return self._request("POST", "/search", body=body)

    def to_markdown(self, response: Dict[str, Any]) -> str:
        return convert_to_markdown(response)


# if __name__ == "__main__":
#     # Note: In a real project, avoid hardcoding the token; use environment variables instead.
#     token = os.environ.get("NOTION_API_TOKEN")
#     client = NotionClientWrapper(token)
#     print("--- 1. Testing Connection (Get Bot Info) ---")
#     try:
#         bot_user = client.retrieve_bot_user()
#         print(f"Connection successful! Bot name: {bot_user.get('name')}")
#         # print(json.dumps(bot_user, indent=2, ensure_ascii=False)) # Print detailed info
#     except Exception as e:
#         print(f"Connection failed: {e}")
#         exit(1)
#     print("\n--- 2. Testing Search (To get a valid Page ID) ---")
#     # Search for any page, limit to 1 result
#     search_result = client.search(
#         filter={"property": "object", "value": "page"}, page_size=1
#     )
#     results = search_result.get("results", [])
#     if not results:
#         print(
#             "No pages found. Please ensure you have added this bot via '...' -> 'Connections' at the top right of a Notion page."
#         )
#     else:
#         first_page = results[0]
#         page_id = first_page["id"]
#         page_title = "Untitled"
#         # Attempt to extract title
#         try:
#             props = first_page.get("properties", {})
#             for key, val in props.items():
#                 if val.get("type") == "title":
#                     title_obj = val.get("title", [])
#                     if title_obj:
#                         page_title = title_obj[0].get("plain_text", "Untitled")
#                     break
#         except:
#             pass
#         print(f"Found page: {page_title} (ID: {page_id})")
#         print(f"\n--- 3. Testing Retrieve Specific Page (Retrieve Page: {page_id}) ---")
#         page_detail = client.retrieve_page(page_id)
#         print("Page retrieved successfully! Metadata:")
#         print(f"Created time: {page_detail.get('created_time')}")
#         print(f"URL: {page_detail.get('url')}")
#         # Uncomment to see full JSON response
#         # print(json.dumps(page_detail, indent=2, ensure_ascii=False))
#         print(
#             f"\n--- 4. Testing Retrieve Page Content Blocks (Retrieve Block Children: {page_id}) ---"
#         )
#         # Read page content (first 3 blocks)
#         block_children = client.retrieve_block_children(page_id, page_size=3)
#         blocks = block_children.get("results", [])
#         print(f"Successfully retrieved {len(blocks)} content blocks.")
#         for block in blocks:
#             b_type = block.get("type")
#             print(f"- Block type: {b_type} (ID: {block.get('id')})")
