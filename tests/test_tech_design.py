"""
测试技术设计部分agent的功能
"""

import pytest
from pathlib import Path
from tools.task_planner import function as task_planner_function
from tools.task_reviewer import function as task_reviewer_function

@pytest.fixture
def test_files():
    # Create necessary directories if they don't exist
    base_dir = Path("data/test")
    src_dir = base_dir / "case_1"
    output_dir = base_dir / "output"
    
    src_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return {
        "prd_path": src_dir / "prd.md",
        "test_path": src_dir / "test.md",
        "tech_stack_path": src_dir / "tech_stack.md",
        "proj_structure_path": src_dir / "proj_structure.md",
        "task_plan_path": src_dir / "task_plan.md",
        "output_path": output_dir / "task_breakdown.md",
        "review_output_path": output_dir / "task_review.md"
    }

@pytest.mark.asyncio
async def test_propose_solution_options(test_files):
    # Check if input files exist
    assert test_files["prd_path"].exists(), f"PRD file not found at {test_files['prd_path']}"
    assert test_files["test_path"].exists(), f"Test file not found at {test_files['test_path']}"
    assert test_files["tech_stack_path"].exists(), f"Tech stack file not found at {test_files['tech_stack_path']}"
    assert test_files["proj_structure_path"].exists(), f"Project structure file not found at {test_files['proj_structure_path']}"
    
    # Read input files
    with open(test_files["prd_path"], "r", encoding="utf-8") as f:
        prd_content = f.read()
    with open(test_files["test_path"], "r", encoding="utf-8") as f:
        test_content = f.read()
    with open(test_files["tech_stack_path"], "r", encoding="utf-8") as f:
        tech_stack_content = f.read()
    with open(test_files["proj_structure_path"], "r", encoding="utf-8") as f:
        proj_structure_content = f.read()
    
    # Call task planner function
    task_breakdown = await task_planner_function(
        product_doc=prd_content,
        test_cases=test_content,
        tech_stack=tech_stack_content,
        project_structure=proj_structure_content
    )
    
    # Verify task breakdown output
    assert task_breakdown is not None, "Task breakdown should not be None"
    assert len(task_breakdown) > 0, "Task breakdown should not be empty"
    assert task_breakdown[0].text is not None, "Task breakdown text should not be None"
    
    # Write output to file
    with open(test_files["output_path"], "w", encoding="utf-8") as f:
        f.write(task_breakdown[0].text)
    
    # Verify output file was created
    assert test_files["output_path"].exists(), "Output file should be created"
    
    # Verify output file content
    with open(test_files["output_path"], "r", encoding="utf-8") as f:
        output_content = f.read()
    assert len(output_content) > 0, "Output file should not be empty"

@pytest.mark.asyncio
async def test_task_reviewer(test_files):
    # Check if input files exist
    assert test_files["prd_path"].exists(), f"PRD file not found at {test_files['prd_path']}"
    assert test_files["test_path"].exists(), f"Test file not found at {test_files['test_path']}"
    assert test_files["tech_stack_path"].exists(), f"Tech stack file not found at {test_files['tech_stack_path']}"
    assert test_files["proj_structure_path"].exists(), f"Project structure file not found at {test_files['proj_structure_path']}"
    assert test_files["task_plan_path"].exists(), f"Task plan file not found at {test_files['task_plan_path']}"
    
    # Read input files
    with open(test_files["prd_path"], "r", encoding="utf-8") as f:
        prd_content = f.read()
    with open(test_files["test_path"], "r", encoding="utf-8") as f:
        test_content = f.read()
    with open(test_files["tech_stack_path"], "r", encoding="utf-8") as f:
        tech_stack_content = f.read()
    with open(test_files["proj_structure_path"], "r", encoding="utf-8") as f:
        proj_structure_content = f.read()
    with open(test_files["task_plan_path"], "r", encoding="utf-8") as f:
        task_plan_content = f.read()
    
    # Call task reviewer function
    review_result = await task_reviewer_function(
        product_doc=prd_content,
        test_cases=test_content,
        tech_stack=tech_stack_content,
        project_structure=proj_structure_content,
        task_plan=task_plan_content
    )
    
    # Verify review result
    assert review_result is not None, "Review result should not be None"
    assert len(review_result) > 0, "Review result should not be empty"
    assert review_result[0].text is not None, "Review result text should not be None"
    
    # Write review result to file
    with open(test_files["review_output_path"], "w", encoding="utf-8") as f:
        f.write(review_result[0].text)
    
    # Verify review output file was created
    assert test_files["review_output_path"].exists(), "Review output file should be created"
    
    # Verify review output file content
    with open(test_files["review_output_path"], "r", encoding="utf-8") as f:
        review_content = f.read()
    assert len(review_content) > 0, "Review output file should not be empty"