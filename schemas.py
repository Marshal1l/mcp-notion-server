# schemas.py

from mcp.types import Tool

# 导入上面定义的通用组件
from common import (
    common_id_description,
    format_parameter,
    rich_text_object_schema,
    block_object_schema,
)

# --- Blocks Tools ---

append_block_children_tool = Tool(
    name="notion_append_block_children",
    description="Append new children blocks to a specified parent block in Notion. Requires insert content capabilities. You can optionally specify the 'after' parameter to append after a certain block.",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the parent block." + common_id_description,
            },
            "children": {
                "type": "array",
                "description": "Array of block objects to append. Each block must follow the Notion block schema.",
                "items": block_object_schema,
            },
            "after": {
                "type": "string",
                "description": "The ID of the existing block that the new block should be appended after."
                + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["block_id", "children"],
    },
)

retrieve_block_tool = Tool(
    name="notion_retrieve_block",
    description="Retrieve a block from Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the block to retrieve."
                + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["block_id"],
    },
)

retrieve_block_children_tool = Tool(
    name="notion_retrieve_block_children",
    description="Retrieve the children of a block",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the block." + common_id_description,
            },
            "start_cursor": {
                "type": "string",
                "description": "Pagination cursor for next page of results",
            },
            "page_size": {
                "type": "number",
                "description": "Number of results per page (max 100)",
            },
            "format": format_parameter,
        },
        "required": ["block_id"],
    },
)

delete_block_tool = Tool(
    name="notion_delete_block",
    description="Delete a block in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the block to delete." + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["block_id"],
    },
)

update_block_tool = Tool(
    name="notion_update_block",
    description="Update the content of a block in Notion based on its type. The update replaces the entire value for a given field.",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the block to update." + common_id_description,
            },
            "block": {
                "type": "object",
                "description": "The updated content for the block. Must match the block's type schema.",
            },
            "format": format_parameter,
        },
        "required": ["block_id", "block"],
    },
)

# --- Pages Tools ---

retrieve_page_tool = Tool(
    name="notion_retrieve_page",
    description="Retrieve a page from Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "The ID of the page to retrieve."
                + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["page_id"],
    },
)

update_page_properties_tool = Tool(
    name="notion_update_page_properties",
    description="Update properties of a page or an item in a Notion database",
    inputSchema={
        "type": "object",
        "properties": {
            "page_id": {
                "type": "string",
                "description": "The ID of the page or database item to update."
                + common_id_description,
            },
            "properties": {
                "type": "object",
                "description": "Properties to update. These correspond to the columns or fields in the database.",
            },
            "format": format_parameter,
        },
        "required": ["page_id", "properties"],
    },
)

# --- Users Tools ---

list_all_users_tool = Tool(
    name="notion_list_all_users",
    description="List all users in the Notion workspace. **Note:** This function requires upgrading to the Notion Enterprise plan and using an Organization API key to avoid permission errors.",
    inputSchema={
        "type": "object",
        "properties": {
            "start_cursor": {
                "type": "string",
                "description": "Pagination start cursor for listing users",
            },
            "page_size": {
                "type": "number",
                "description": "Number of users to retrieve (max 100)",
            },
            "format": format_parameter,
        },
    },
)

retrieve_user_tool = Tool(
    name="notion_retrieve_user",
    description="Retrieve a specific user by user_id in Notion. **Note:** This function requires upgrading to the Notion Enterprise plan and using an Organization API key to avoid permission errors.",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The ID of the user to retrieve."
                + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["user_id"],
    },
)

retrieve_bot_user_tool = Tool(
    name="notion_retrieve_bot_user",
    description="Retrieve the bot user associated with the current token in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "random_string": {
                "type": "string",
                "description": "Dummy parameter for no-parameter tools",
            },
            "format": format_parameter,
        },
        # 即使不需要参数，有些客户端也需要 required 不为空，这里设个 dummy 是个常见做法
        "required": ["random_string"],
    },
)

# --- Databases Tools ---

create_database_tool = Tool(
    name="notion_create_database",
    description="Create a database in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "parent": {
                "type": "object",
                "description": "Parent object of the database",
            },
            "title": {
                "type": "array",
                "description": "Title of database as it appears in Notion. An array of rich text objects.",
                "items": rich_text_object_schema,
            },
            "properties": {
                "type": "object",
                "description": "Property schema of database. The keys are the names of properties as they appear in Notion and the values are property schema objects.",
            },
            "format": format_parameter,
        },
        "required": ["parent", "properties"],
    },
)

query_database_tool = Tool(
    name="notion_query_database",
    description="Query a database in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "database_id": {
                "type": "string",
                "description": "The ID of the database to query."
                + common_id_description,
            },
            "filter": {
                "type": "object",
                "description": "Filter conditions",
            },
            "sorts": {
                "type": "array",
                "description": "Sort conditions",
                "items": {
                    "type": "object",
                    "properties": {
                        "property": {"type": "string"},
                        "timestamp": {"type": "string"},
                        "direction": {
                            "type": "string",
                            "enum": ["ascending", "descending"],
                        },
                    },
                    "required": ["direction"],
                },
            },
            "start_cursor": {
                "type": "string",
                "description": "Pagination cursor for next page of results",
            },
            "page_size": {
                "type": "number",
                "description": "Number of results per page (max 100)",
            },
            "format": format_parameter,
        },
        "required": ["database_id"],
    },
)

retrieve_database_tool = Tool(
    name="notion_retrieve_database",
    description="Retrieve a database in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "database_id": {
                "type": "string",
                "description": "The ID of the database to retrieve."
                + common_id_description,
            },
            "format": format_parameter,
        },
        "required": ["database_id"],
    },
)

update_database_tool = Tool(
    name="notion_update_database",
    description="Update a database in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "database_id": {
                "type": "string",
                "description": "The ID of the database to update."
                + common_id_description,
            },
            "title": {
                "type": "array",
                "description": "An array of rich text objects that represents the title of the database that is displayed in the Notion UI.",
                "items": rich_text_object_schema,
            },
            "description": {
                "type": "array",
                "description": "An array of rich text objects that represents the description of the database that is displayed in the Notion UI.",
                "items": rich_text_object_schema,
            },
            "properties": {
                "type": "object",
                "description": "The properties of a database to be changed in the request, in the form of a JSON object.",
            },
            "format": format_parameter,
        },
        "required": ["database_id"],
    },
)

create_database_item_tool = Tool(
    name="notion_create_database_item",
    description="Create a new item (page) in a Notion database",
    inputSchema={
        "type": "object",
        "properties": {
            "database_id": {
                "type": "string",
                "description": "The ID of the database to add the item to."
                + common_id_description,
            },
            "properties": {
                "type": "object",
                "description": "Properties of the new database item. These should match the database schema.",
            },
            "format": format_parameter,
        },
        "required": ["database_id", "properties"],
    },
)

# --- Comments Tools ---

create_comment_tool = Tool(
    name="notion_create_comment",
    description="Create a comment in Notion. This requires the integration to have 'insert comment' capabilities. You can either specify a page parent or a discussion_id, but not both.",
    inputSchema={
        "type": "object",
        "properties": {
            "parent": {
                "type": "object",
                "description": "Parent object that specifies the page to comment on. Must include a page_id if used.",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "The ID of the page to comment on."
                        + common_id_description,
                    },
                },
            },
            "discussion_id": {
                "type": "string",
                "description": "The ID of an existing discussion thread to add a comment to."
                + common_id_description,
            },
            "rich_text": {
                "type": "array",
                "description": "Array of rich text objects representing the comment content.",
                "items": rich_text_object_schema,
            },
            "format": format_parameter,
        },
        "required": ["rich_text"],
    },
)

retrieve_comments_tool = Tool(
    name="notion_retrieve_comments",
    description="Retrieve a list of unresolved comments from a Notion page or block. Requires the integration to have 'read comment' capabilities.",
    inputSchema={
        "type": "object",
        "properties": {
            "block_id": {
                "type": "string",
                "description": "The ID of the block or page whose comments you want to retrieve."
                + common_id_description,
            },
            "start_cursor": {
                "type": "string",
                "description": "If supplied, returns a page of results starting after the cursor.",
            },
            "page_size": {
                "type": "number",
                "description": "Number of comments to retrieve (max 100).",
            },
            "format": format_parameter,
        },
        "required": ["block_id"],
    },
)

# --- Search Tool ---

search_tool = Tool(
    name="notion_search",
    description="Search pages or databases by title in Notion",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Text to search for in page or database titles",
            },
            "filter": {
                "type": "object",
                "description": "Filter results by object type (page or database)",
                "properties": {
                    "property": {
                        "type": "string",
                        "description": "Must be 'object'",
                    },
                    "value": {
                        "type": "string",
                        "description": "Either 'page' or 'database'",
                    },
                },
            },
            "sort": {
                "type": "object",
                "description": "Sort order of results",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["ascending", "descending"],
                    },
                    "timestamp": {
                        "type": "string",
                        "enum": ["last_edited_time"],
                    },
                },
            },
            "start_cursor": {
                "type": "string",
                "description": "Pagination start cursor",
            },
            "page_size": {
                "type": "number",
                "description": "Number of results to return (max 100). ",
            },
            "format": format_parameter,
        },
    },
)
