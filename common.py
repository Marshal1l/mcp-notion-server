# common.py

# 通用的 ID 描述后缀
common_id_description = " (uuidv4)"

# 通用的 format 参数定义
format_parameter = {
    "type": "string",
    "description": "Format of the response. Use 'markdown' for converted content or 'json' for raw API response.",
    "enum": ["markdown", "json"],
    "default": "markdown",
}

# 简化的 Rich Text Schema (对应 Notion API)
rich_text_object_schema = {
    "type": "object",
    "description": "A Notion rich text object",
    "properties": {
        "type": {"type": "string", "enum": ["text", "mention", "equation"]},
        "text": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "link": {"type": ["object", "null"]},
            },
        },
        "annotations": {"type": "object"},
        "plain_text": {"type": "string"},
        "href": {"type": ["string", "null"]},
    },
}

# 简化的 Block Schema (这是一个非常基础的定义，实际 Notion Block 结构很复杂)
# 在实际 MCP 使用中，通常只需要声明它是 "object" 或 "dict" 即可
block_object_schema = {
    "type": "object",
    "description": "A Notion block object",
    "properties": {
        "object": {"type": "string", "enum": ["block"]},
        "type": {"type": "string"},
        # 实际属性取决于 type，这里不再展开以免 Schema 过大
    },
    "required": ["type"],
}
