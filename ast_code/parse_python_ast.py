import ast

def parse_python_ast(content : str) -> dict | None :

    try :
        tree = ast.parse(content)

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree) :
            if isinstance(node, ast.FunctionDef) :
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node)
                })

            elif isinstance(node, ast.ClassDef) :
                classes.append({
                    "name" : node.name,
                    "line" : node.lineno,
                    "docstring": ast.get_docstring(node)
                })
                
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom) :
                if isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                else:
                    module = node.module or ""
                    imports.append(module)
            
        
        return {
            "functions" : functions,
            "classes" : classes,
            "imports" : list(set(imports))
        }

    except Exception :
        return None