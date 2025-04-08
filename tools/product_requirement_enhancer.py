from mcp import types
from utils import ds_r1_chat_completions
import logging

logger = logging.getLogger(__name__)

tool = types.Tool(
    name="product_requirement_enhancer",
    description="扩写产品文档，提高需求质量",
    inputSchema={
        "type": "object",
        "required": ["product_doc"],
        "properties": {
            "product_doc": {
                "type": "string",
            }
        },
    },
)


async def function(
    product_doc: str,
) -> list[types.TextContent]:
    logger.info("Task planner input parameters:")
    logger.info(f"Product doc length: {len(product_doc)}")
    
    tech_tasks = await enhance_product_requirement(product_doc)
    return [types.TextContent(type="text", text=tech_tasks)]


async def enhance_product_requirement(product_doc: str) -> str:
    prompt = f"""
    你是一个资深产品经理，特别擅长做UI设计和用户交互设计。下面有一个产品文档，请扩写这个产品文档，为技术团队尽可能详细描述交互流程和交互细节
    
    # 产品文档：
    ```markdown
    {product_doc}
    ```

    输出的文档格式和输入的产品文档相同
    """
    _, resp= ds_r1_chat_completions(prompt)
    return resp