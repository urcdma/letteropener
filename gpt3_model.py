import openai

class GPT3Model:
    def __init__(self, api_key: str = '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'):
        openai.api_key = api_key

    def describe_code(self, code: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"This is a Python code: \n{code}\nWhat does this code do?",
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def evaluate_code(self, code: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"This is a Python code: \n{code}\nWhat are the main functions and structures of this code?",
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def list_knowledge_points(self, code: str) -> str:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"This is a Python code: \n{code}\nWhat are the technical knowledge points related to this code's function and structure?",
            temperature=0.5,
            max_tokens=100
        )
        return response.choices[0].text.strip()
