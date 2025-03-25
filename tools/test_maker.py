from mcp import types
from utils import o3_mini_chat_completion


tool = types.Tool(
    name="test_maker",
    description="将产品文档转化为测试用例",
    inputSchema={
        "type": "object",
        "required": ["product_doc"],
        "properties": {
            "product_doc": {
                "type": "string",
            },
        },
    },
)


async def function(
    product_doc: str,
) -> list[types.TextContent]:
    test_cases = await plan_task(product_doc)
    return [types.TextContent(type="text", text=test_cases)]


async def plan_task(product_doc: str) -> str:
    prompt = f"""
    你是一个资深测试工程师，请把如下产品文档转化为测试用例，并给出每个测试用例的详细描述
    产品文档：
    {product_doc}

    请按照如下格式输出：
    ```markdown
    # TEST-XXX: 测试标题 [状态]
    # 1. 需求解析（Requirement Parsing）
    将文档中的自然语言或半结构化文本转化为可操作的结构化数据。


    # 2. 测试用例
    根据已解析的需求信息，自动生成测试目的、前置条件、测试步骤、预期结果
    ## 2.x 测试用例名称
    **状态**：[未开始, 进行中, 已完成]
    **测试目的**
    **前置条件**
    **测试步骤**
    **预期结果**

    
    # 3.测试数据
    根据上述信息，如果是后端代码生成pytest框架下的mock测试数据

    # 关联内容
    - 关联产品文档：PRD-XXX
    - 关联任务文档：[TASK-XXX, TASK-XXX]
    ```

    
    """
    return o3_mini_chat_completion(prompt)
