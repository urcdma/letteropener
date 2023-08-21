import openai
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gpt3_model.log', filemode='w')

class GPT3Model:
    def __init__(self, api_key: str = 'key'):
        openai.api_key = api_key

    def decompose_code_into_steps(self, code: str) -> str:
        prompt = f"请将以下Python代码分解为多个小步骤：\n{code}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def describe_code(self, code: str) -> str:
        prompt = f"请为以下Python代码的每一行或每一块写下注释，解释其功能和原因：\n{code}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].text.strip()

    def generate_memory_card_for_code_analysis(self, concept: str) -> Tuple[str, str]:
        # 正面
        prompt_front = f"请为以下概念提供英文名称和中文名称与简短描述：\n{concept}"
        response_front = openai.Completion.create(
            engine="davinci",
            prompt=prompt_front,
            temperature=0.5,
            max_tokens=100
        )
        card_front = response_front.choices[0].text.strip()

        # 反面
        prompt_back = f"使用费曼技巧为初学者解读以下概念：\n{concept}"
        response_back = openai.Completion.create(
            engine="davinci",
            prompt=prompt_back,
            temperature=0.5,
            max_tokens=200
        )
        card_back = response_back.choices[0].text.strip()

        return card_front, card_back
    
    def organize_code_by_function_or_module(self, code: str) -> str:
        prompt = f"请按功能或模块划分以下Python代码段：\n{code}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].text.strip()

    def describe_code_module(self, code: str) -> str:
        prompt = f"请为以下Python代码模块或功能提供一个简短的描述：\n{code}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def generate_memory_card_for_code_organization(self, concept: str) -> Tuple[str, str]:
        # 正面
        prompt_front = f"请为以下代码组织概念提供英文名称和中文名称：\n{concept}"
        response_front = openai.Completion.create(
            engine="davinci",
            prompt=prompt_front,
            temperature=0.5,
            max_tokens=100
        )
        card_front = response_front.choices[0].text.strip()

        # 反面
        prompt_back = f"使用费曼技巧为初学者解读以下代码组织概念：\n{concept}"
        response_back = openai.Completion.create(
            engine="davinci",
            prompt=prompt_back,
            temperature=0.5,
            max_tokens=200
        )
        card_back = response_back.choices[0].text.strip()

        return card_front, card_back
    
    def prioritize_knowledge_points(self, knowledge_points: str) -> Tuple[str, str]:
        prompt = f"请根据以下Python知识点，指出哪些知识点是初学者应该首先掌握的，哪些可以稍后深入了解：\n{knowledge_points}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.5,
            max_tokens=200
        )
        prioritized_points = response.choices[0].text.strip().split("\n")
        primary_points = prioritized_points[0]
        advanced_points = prioritized_points[1] if len(prioritized_points) > 1 else ""
        return primary_points, advanced_points

    def generate_memory_card_for_knowledge_points(self, concept: str) -> Tuple[str, str]:
        # 正面
        prompt_front = f"请为以下知识点提供英文名称、中文名称和简短描述：\n{concept}"
        response_front = openai.Completion.create(
            engine="davinci",
            prompt=prompt_front,
            temperature=0.5,
            max_tokens=150
        )
        card_front = response_front.choices[0].text.strip()

        # 反面
        prompt_back = f"使用费曼技巧为初学者解读以下知识点：\n{concept}"
        response_back = openai.Completion.create(
            engine="davinci",
            prompt=prompt_back,
            temperature=0.5,
            max_tokens=250
        )
        card_back = response_back.choices[0].text.strip()

        return card_front, card_back


