
from .parse_python_ast import parse_python_ast


def parsed_data(all_files : list) -> list : 
    for file_data in all_files : 
        if file_data.get("file_path", "").endswith(".py"):
            content = file_data.get("content")
            if content:
                metadata = parse_python_ast(content)
                if metadata : 
                    file_data["ast_metadata"] = metadata

    
    return all_files