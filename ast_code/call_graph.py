import ast
from collections import defaultdict

class CallGraphVisitor(ast.NodeVisitor):
    def __init__(self):
        # caller -> set(callees)
        self.call_graph = defaultdict(set)
        self.current_scope = None
        self.current_class = None
        self.imports = {}

    def visit_ClassDef(self, node):
        prev_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = prev_class

    def visit_FunctionDef(self, node):
        if self.current_class:
            scope_name = f"{self.current_class}.{node.name}"
        else:
            scope_name = node.name

        prev_scope = self.current_scope
        self.current_scope = scope_name

        self.generic_visit(node)

        self.current_scope = prev_scope

    def visit_Call(self, node):
    if self.current_scope is None:
        return

    callee = self._get_call_name(node.func)
    if callee:
        resolved = self.imports.get(callee, callee)
        self.call_graph[self.current_scope].add(resolved)

    self.generic_visit(node)

        
    def visit_Import(self, node):
    for alias in node.names:
        name = alias.asname or alias.name
        self.imports[name] = alias.name

   def visit_ImportFrom(self, node):
    module = node.module
    for alias in node.names:
        local = alias.asname or alias.name
        self.imports[local] = f"{module}.{alias.name}"


    def _get_call_name(self, node):
        """
        Extract function name from:
        - foo()
        - module.foo()
        - obj.method()
        """
        if isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Attribute):
            # obj.method -> method
            return node.attr

        elif isinstance(node, ast.Call):
            return self._get_call_name(node.func)

        return None


def build_call_graph(content: str) -> dict | None:
    try:
        tree = ast.parse(content)
        visitor = CallGraphVisitor()
        visitor.visit(tree)

        return {
            caller: sorted(callees)
            for caller, callees in visitor.call_graph.items()
        }

    except Exception:
        return None
