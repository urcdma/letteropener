import ast
import sys
import json

def validate_code(code):
    try:
        ast.parse(code)
        return {"isValid": True}
    except:
        return {"isValid": False}

if __name__ == "__main__":
    code = sys.stdin.read()
    result = validate_code(code)
    print(json.dumps(result))
