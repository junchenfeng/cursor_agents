from mcp import types
from utils import ds_r1_chat_completions


tool = types.Tool(
    name="task_reviewer",
    description="评审技术任务拆解是否合理，并向人类给出进一步思考的建议",
    inputSchema={
        "type": "object",
        "required": ["product_doc", "test_cases", "task_plan", "tech_stack", "project_structure"],
        "properties": {
            "product_doc": {
                "type": "string",
            },
            "test_cases": {
                "type": "string",
            },
            "task_plan": {
                "type": "string",
            },
            "tech_stack": {
                "type": "string",
            },
            "project_structure": {
                "type": "string",
            }
        },
    },
)


async def function(
    product_doc: str,
    test_cases: str,
    tech_stack: str,
    project_structure: str,
    task_plan: str,
) -> list[types.TextContent]:
    review_result = await review_task(product_doc, test_cases, tech_stack, project_structure, task_plan)
    return [types.TextContent(type="text", text=review_result)]


async def review_task(
    product_doc: str,
    test_cases: str,
    tech_stack: str,
    project_structure: str,
    task_plan: str,
) -> str:
    prompt = f"""
    你是一个资深研发工程师，请对以下任务拆解进行评审，主要从以下几个方面进行分析：

    1. 任务完整性：是否覆盖了所有产品需求
    2. 测试合理性：测试是否覆盖了主要产品需求，并且是可执行的测试
    3. 任务合理性：任务拆解是否合理，每个任务是否可以在300行代码内完成

    此外，针对这个设计方案的可能缺陷和遗漏进行批评，供人类程序员参考。

    # 产品文档：
    ```markdown
    {product_doc}
    ```
    # 测试用例：
    ```markdown
    {test_cases}
    ```
    # 技术栈：
    ```markdown
    {tech_stack}
    ```
    # 项目结构
    ```markdown
    {project_structure}
    ```
    # 任务拆解
    ```markdown
    {task_plan}
    ```

    请按照以下格式输出评审结果：

    ```markdown
    # 任务拆解评审报告

    ## 1. 意见1
    xxx
    ## 2. 意见2
    xxx
    ...
    ```
    """
    _, response = ds_r1_chat_completions(prompt) 
    return response