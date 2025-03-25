import os
from typing import List
from dotenv import load_dotenv
from openai import BadRequestError,AzureOpenAI

import logging
logger = logging.getLogger(name=__name__)

load_dotenv()

azure_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION", "")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")

openai_instance = AzureOpenAI(
    api_key=azure_api_key,
    api_version=azure_api_version,
    azure_endpoint=azure_endpoint,
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