import ast
import networkx as nx
from contextlib import contextmanager
import jsonschema
import chardet
import sys
import json


#  定义 read_file_as_utf8 函数
def read_file_as_utf8(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    detected_encoding = result['encoding']
    with open(file_path, 'r', encoding=detected_encoding) as file:
        content = file.read()
    return content.encode('utf-8').decode('utf-8')
# DependencyAnalyzer Class
class DependencyAnalyzer(ast.NodeVisitor):
    def __init__(self):
        
        self.graph = nx.DiGraph()
        self.current_scope = ['global']
    
    def analyze_dependencies(self, ast_tree: ast.AST):
        self.visit(ast_tree)
        return self.graph.edges(data=True)

    def visit_FunctionDef(self, node):
        self.current_scope.append(node.name)
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_ClassDef(self, node):
        self.current_scope.append(node.name)
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.graph.add_edge(node.name, base.id, type='inherit')
        self.generic_visit(node)
        self.current_scope.pop()

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.graph.add_edge(node.func.id, self.current_scope[-1], type='call')
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.graph.add_edge(target.id, self.current_scope[-1], type='assign')
        self.generic_visit(node)

    def get_most_dependent_node(self):
        in_degrees = self.graph.in_degree()
        most_dependent_node = max(in_degrees, key=lambda x: x[1])[0]
        return most_dependent_node


# AstParser Class
class AstParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.global_vars = set()
        self.local_vars = set()
        self.parents = []

    @contextmanager
    def push_parent(self, node):
        self.parents.append(node)
        yield
        self.parents.pop()

    def parse_code(self, code: str):
        tree = ast.parse(code)
        self.visit(tree)
        return tree, {
            "functions": list(self.functions),
            "classes": list(self.classes),
            "global_vars": list(self.global_vars),
            "local_vars": list(self.local_vars)
        }
        

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.local_vars.update({arg.arg for arg in node.args.args})
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if any(isinstance(parent, (ast.FunctionDef, ast.ClassDef, ast.For, ast.While, ast.If)) for parent in self.parents):
                    self.local_vars.add(target.id)
                else:
                    self.global_vars.add(target.id)
        self.generic_visit(node)

    def visit(self, node):
        with self.push_parent(node):
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)
# 定义数据验证器
class DataValidator:
    # 初始化方法
    def __init__(self):
        # 定义验证的JSON模式
        self.schema = {
            "type": "object",
            "properties": {
                "functions": {"type": "array", "items": {"type": "string"}},
                "classes": {"type": "array", "items": {"type": "string"}},
                "global_vars": {"type": "array", "items": {"type": "string"}},
                "local_vars": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["functions", "classes", "global_vars", "local_vars"],
        }

    # 验证数据的方法
    def validate_data(self, data: dict) -> bool:
        try:
            # 验证数据是否符合模式
            jsonschema.validate(data, self.schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            sys.stderr.write(f"Data validation error: {e}\n")
            return False
        
# DataValidator Class remains unchanged as it seemed well-structured already.
class SimpleView:
    def addItem(self, message):
        print(message)
if __name__ == "__main__":
    
    validator = DataValidator()
    # 从标准输入读取原始字节数据
    input_data = sys.stdin.buffer.read()

    # 检测编码并将其转换为UTF-8
    detected_encoding = chardet.detect(input_data)['encoding']
    code = input_data.decode(detected_encoding).encode('utf-8').decode('utf-8')

    # 使用 AstParser 解析代码
    parser = AstParser()
    _, data = parser.parse_code(code)

    response = {}

    # 使用 DataValidator 验证解析结果
    if validator.validate_data(data):
        response["status"] = "success"
        response["data"] = data
    else:
        response["status"] = "failure"
        response["message"] = "Validation failed!"

    print(json.dumps(response))