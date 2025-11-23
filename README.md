# MCP Notion Server

一个基于 Python 的 MCP (Model Context Protocol) 服务器，用于与 [Notion API](https://developers.notion.com/) 集成，支持通过 MCP 工具调用对 Notion 数据库、页面、块、用户及评论的操作。

---

## 功能

* 通过 MCP 调用 Notion 工具：

  * 增删改查块（block）
  * 查询及更新页面（page）
  * 查询、创建及更新数据库（database）
  * 创建数据库条目（database item）
  * 创建及查询评论（comment）
  * 搜索 Notion 内容
  * 列出及检索用户

* 支持 **Markdown 转换** 输出

* 支持 **Streamable HTTP** 传输，用于与 MCP 客户端集成

---

## 安装

1. 克隆仓库

```bash
git clone https://github.com/Marshal1l/mcp-notion-server.git
cd mcp-notion-server
```

2. 创建虚拟环境（推荐）

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS / Linux
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

> 注意：如果没有 `requirements.txt`，请确保安装：
>
> ```bash
> pip install mcp notion_client starlette uvicorn python-dotenv
> ```

---

## 配置

1. **安全地设置 Notion Token**

不要把 token 写入代码，推荐使用环境变量或 `.env` 文件：

**方法 1：环境变量**

在 PowerShell 设置（只对当前用户有效）：

```powershell
setx NOTION_API_TOKEN "你的_notion_token"
```

然后重启 VSCode 或 PowerShell。

**方法 2：.env 文件**

在项目根目录创建 `.env` 文件：

```
NOTION_API_TOKEN=你的_notion_token
ENABLE_MARKDOWN=true
```

在代码中加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 运行

### 方法 1：通过 PowerShell 或终端

```powershell
python notionMcpServer.py
```

默认监听 `0.0.0.0:8000`，MCP 客户端可以连接 `/mcp` 路径。

### 方法 2：通过 VSCode Debug

1. 在 VSCode 左侧 **Run and Debug** 创建 `launch.json`
2. 配置环境变量：

```json
"env": {
    "NOTION_API_TOKEN": "你的_notion_token",
    "ENABLE_MARKDOWN": "true"
}
```

3. 点击 **Run** 启动服务器

---

## 工具列表

以下 MCP 工具可用（需在 `enabled_tools_set` 中开启）：

* `notion_append_block_children`
* `notion_retrieve_block`
* `notion_retrieve_block_children`
* `notion_delete_block`
* `notion_update_block`
* `notion_retrieve_page`
* `notion_update_page_properties`
* `notion_list_all_users`
* `notion_retrieve_user`
* `notion_retrieve_bot_user`
* `notion_query_database`
* `notion_create_database`
* `notion_retrieve_database`
* `notion_update_database`
* `notion_create_database_item`
* `notion_create_comment`
* `notion_retrieve_comments`
* `notion_search`

---

## 安全提示

* **不要把 Notion API Token 写入代码或提交到 GitHub**
* 将 `__pycache__` 和 `.env` 加入 `.gitignore`
* 如果 Token 已经泄露，请立即在 Notion [Integrations](https://www.notion.so/my-integrations) 页面重置

---

## GitHub 推送注意

如果提交历史包含 Token，GitHub 会阻止 push。
可参考官方方法清理：

```bash
git rm -r --cached __pycache__
# 或使用 git-filter-repo 清理历史 commit
```

---

## 联系

作者：Marshal1l
项目地址：[https://github.com/Marshal1l/mcp-notion-server](https://github.com/Marshal1l/mcp-notion-server)
