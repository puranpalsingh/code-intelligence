import os
import git

def clone_repo(repo_url : str, repo_id: str) -> dict | None : 

    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')

    repo_dir = os.path.join("repos", f"{repo_id}_{repo_name}")

    if os.path.exists(repo_dir):
        return {
            "repo_id": repo_id,
            "repo_path": repo_dir,
            "repo_name": repo_name
        }

    if not os.path.exists(os.path.dirname(repo_dir)):
        os.makedirs(os.path.dirname(repo_dir), exist_ok=True)
    
    try : 
        repo = git.Repo.clone_from(repo_url, repo_dir, depth = 1 )
        return {"repo_id" : repo_id, "repo_path" : repo_dir, "repo_name" : repo_name}

    except Exception : 
        return None


def scan_repo(repo_path : str) -> list : 
    all_file = []

    for root,_,files in os.walk(repo_path) :
        for file in files : 
            fullpath = os.path.join(root, file)

            all_file.append(fullpath)

    return all_file




def is_valid_file(file_path : str) -> bool : 

    allowed_exts= {
        ".py", ".ts", ".js", ".java", ".cpp", ".c", ".h", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".md", ".go", ".txt", ".jsx", ".tsx", ".prisma"
    }

    not_allowed_dir = {
        "dist", "node_modules", "build", "bin", "obj", "out", ".git", ".svn", ".hg", "__pycache__", ".tox", ".venv", ".idea", ".vscode", ".DS_Store", ".pytest_cache"
    }

    for path in file_path.split(os.sep) :
        if path in not_allowed_dir : 
            return False
        
    
    _,ext = os.path.splitext(file_path)

    return ext.lower() in allowed_exts


def extract_file(repo_path : str) -> list : 
    all_files = scan_repo(repo_path=repo_path)

    sourced_file = []

    for file in all_files : 
        if is_valid_file(file) : 
            sourced_file.append(file)
    

    return sourced_file


def read_file_data(file_path : str, max_size = 50000) : 
    try : 
        if os.path.getsize(file_path) > max_size :
            return None
        
        
        with open(file_path, "r", encoding = "utf-8", errors = "ignore") as f:
            return f.read()
    
    except Exception :
        return None
    


def extract_data(repo_path : str, repo_id :str) -> list :
    sourced_file = extract_file(repo_path=repo_path)
    
    extracted_data  = []
    for file in sourced_file :

        content = read_file_data(file_path=file)

        if content : 
            extracted_data.append({
                "file_path" : file,
                "content" : content,
                "repo_id" : repo_id
            })

        
    return extracted_data


def get_data(repo_url : str, repo_id : str) -> list : 
    cloned = clone_repo(repo_url=repo_url, repo_id = repo_id)
    repo_path = cloned["repo_path"] if isinstance(cloned, dict) else getattr(cloned, "repo_path", None)

    data = extract_data(repo_path=repo_path, repo_id=repo_id)

    return data
