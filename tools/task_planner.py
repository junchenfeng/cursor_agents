from mcp import types
from utils import o3_mini_chat_completion


tool = types.Tool(
    name="task_planner",
    description="将产品文档转化为技术任务拆解",
    inputSchema={
        "type": "object",
        "required": ["product_doc"],
        "properties": {
            "product_doc": {
                "type": "string",
            },
            "test_cases": {
                "type": "string",
            },
            "tech_stack": {
                "type": "string",
            },
            "project_structure": {
                "type": "string",
            },
        },
    },
)


async def function(
    product_doc: str,
    test_cases: str,
    tech_stack: str,
    project_structure: str,
) -> list[types.TextContent]:
    tech_tasks = await plan_task(product_doc, test_cases, tech_stack, project_structure)
    return [types.TextContent(type="text", text=tech_tasks)]


async def plan_task(product_doc: str, test_cases: str, tech_stack: str, project_structure: str) -> str:
    prompt = f"""
    你是一个资深研发工程师，请以下面的产品文档和测试用例为基础，进行任务拆解，并给出每个任务的详细描述
    
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

    在进行任务拆解时，一个模块应该基本对应一个测试用例的完成，一个模块可以有多个子任务组成

    请按照以下内容输出
    ```markdown
# TASK-XXX: 任务标题 [状态]

# 1. 前端任务
## 1.1 前端子任务1名称
**状态**：[未开始, 进行中, 已完成]
**任务要求**: 描述该前端任务需要实现的功能
...

# 2. 后端任务
## 2.1 后端子任务1名称
**状态**：[未开始, 进行中, 已完成]
**任务要求**: 描述该后端任务需要实现的功能
**技术组件选型**（如果需要）： 如果为实现这个任务有技术组件不在项目技术栈中，需要增加技术组件选型的内容。如果已经存在，则可以忽略。对于技术组件选型，描述具体的组件名称和调用方式，对于每个选择的优缺点进行简单描述。
...

# 3. 任务模块
## 3.1 模块1
**对应测试用例**
**关联前端任务**
**关联后端任务**

# 4. 前后端接口设计（如果需要）
## 4.1 接口1
**接口名称**
**请求方式**
**请求路径**
**请求参数**
**返回结果**
**CORS设置**（如果需要）如何设置跨域请求以确保前后端畅通

# 5. 数据模型设计（如果需要）
## 5.1 数据模型1
**db类型**：[mysql, postgresql, sqlite, mongodb]
**数据库名称**
**数据表名称**
**数据表结构**
...




# 关联文档
 - 关联产品文档：PRD-XXX
 - 关联测试文档：TEST-XXX
```
    """
    return o3_mini_chat_completion(prompt)
