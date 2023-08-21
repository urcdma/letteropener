import openai
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gpt3_model.log', filemode='w')

class GPT3Model:
    def __init__(self, api_key: str = 'key'):
        openai.api_key = api_key

    def describe_code(self, code: str) -> str:
        logging.info("Describing code using GPT-3 model.")
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"这是一个Python代码：\n{code}\n这段代码的功能是什么？",
            temperature=0.5,
            max_tokens=100
        )
        logging.info("Code description completed.")
        return response.choices[0].text.strip()

    def evaluate_code(self, code: str) -> str:
        logging.info("Evaluating code using GPT-3 model.")
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"这是一个Python代码：\n{code}\n这段代码的主要功能和结构是什么？",
            temperature=0.5,
            max_tokens=100
        )
        logging.info("Code evaluation completed.")
        return response.choices[0].text.strip()

    def list_knowledge_points(self, code: str) -> str:
        logging.info("Listing knowledge points using GPT-3 model.")
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"这是一个Python代码：\n{code}\n与这段代码的功能和结构相关的技术知识点是什么？",
            temperature=0.5,
            max_tokens=100
        )
        logging.info("Knowledge points listing completed.")
        return response.choices[0].text.strip()

    def get_knowledge_point_description(self, point: str) -> Tuple[str, str]:
        logging.info(f"Getting description for knowledge point: {point} using GPT-3 model.")
        
        # 获取中文描述
        response_cn = openai.Completion.create(
            engine="davinci",
            prompt=f"为初学者简单地用中文解释概念'{point}'。",
            temperature=0.5,
            max_tokens=100
        )
        description_cn = response_cn.choices[0].text.strip()

        # 获取英文描述
        response_en = openai.Completion.create(
            engine="davinci",
            prompt=f"为初学者简单地用英文解释概念'{point}'。",
            temperature=0.5,
            max_tokens=100
        )
        description_en = response_en.choices[0].text.strip()

        logging.info(f"Please provide a beginner-friendly explanation in English for the concept: '{point}'.")
        return description_cn, description_en
