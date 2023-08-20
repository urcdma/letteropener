import ast

class CodeAnalyzer:
    def __init__(self):
        self.tree = None

    def analyze_code(self, code: str):
        self.tree = ast.parse(code)

    def get_functions(self):
        return [node.name for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]

    def get_imports(self):
        return [node.names[0].name for node in ast.walk(self.tree) if isinstance(node, ast.Import)]

    def get_variables(self):
        return [node.targets[0].id for node in ast.walk(self.tree) if isinstance(node, ast.Assign)]
