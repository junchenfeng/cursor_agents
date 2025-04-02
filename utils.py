import os
from typing import List, Tuple
from dotenv import load_dotenv
from openai import BadRequestError, AzureOpenAI, OpenAI

import logging
import json
import re


logger = logging.getLogger(name=__name__)

load_dotenv()

azure_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
deepseek_base_url = os.getenv("DEEPSEEK_BASE_URL", "")

openai_instance = AzureOpenAI(
    api_key=azure_api_key,
    api_version=azure_api_version,
    azure_endpoint=azure_endpoint,
)
deepseek_instance = OpenAI(
    api_key=deepseek_api_key,
    base_url=deepseek_base_url,
)

def _o_chat_completion(prompt: str, model: str, history: List[str] = [], max_completion_tokens=16384) -> str:
    messages = [{"role": "user", "content": msg} for msg in history]
    messages.append({"role": "user", "content": prompt})

    params = {
        "model": model,
        "messages": messages,
        "stream": False,
        "max_completion_tokens": max_completion_tokens # 支持最大16ktoken，以生成足够长的paper
    }

    try:
        response = openai_instance.chat.completions.create(**params)
    except BadRequestError as bad_request_error:
        logger.warning(
            f"o_chat_completion failed: {str(bad_request_error)} prompt:{prompt}",
            exc_info=bad_request_error,
        )
        raise Exception("系统异常，请稍后再试")
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}", exc_info=e)
        raise

    return response.choices[0].message.content

def o3_mini_chat_completion(prompt: str, history: List[str] = [], max_completion_tokens=16384) -> str:
    return _o_chat_completion(prompt, "advisor-o3mini-1", history, max_completion_tokens)



def _reasoning_chat_completion(prompt: str, model: str, history: List[str] = []) -> Tuple[str, str]:
    """Shared chat completion logic."""
    messages = [{"role": "user", "content": msg} for msg in history]
    messages.append({"role": "user", "content": prompt})

    params = {
        "model": model,
        "messages": messages,
        "stream": False,
        "max_tokens": 8000,  # 支持最大8ktoken，以生成足够长的paper
    }

    try:
        response = deepseek_instance.chat.completions.create(**params)
    except BadRequestError as bad_request_error:
        logger.warning(
            f"_reasoning_chat_completion failed: {str(bad_request_error)} prompt:{prompt}",
            exc_info=bad_request_error,
        )
        raise Exception("系统异常，请稍后再试")
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}", exc_info=e)
        raise

    return (
        response.choices[0].message.reasoning_content,
        response.choices[0].message.content,
    )

def ds_r1_chat_completions(prompt: str, history: List[str] = []) -> Tuple[str, str]:
    """
    使用DeepSeek R1模型进行推理聊天

    Args:
        prompt: 提示词
        history: 历史消息列表

    Returns:
        包含推理内容和最终内容的元组
    """
    try:
        return _reasoning_chat_completion(prompt, "deepseek-r1-250120", history)
    except json.JSONDecodeError as json_error:
        logger.error(
            f"Reasoning chat completion failed: {str(json_error)} doc:{json_error.doc}",
            exc_info=json_error,
        )
        raise
    except BadRequestError as bad_request_error:
        logger.warning(
            f"ds_r1_chat_completions failed: {str(bad_request_error)} prompt:{prompt}",
            exc_info=bad_request_error,
        )
        raise Exception("系统异常，请稍后再试")
    except Exception as e:
        logger.error(f"Reasoning chat completion failed: {str(e)}", exc_info=e)
        raise