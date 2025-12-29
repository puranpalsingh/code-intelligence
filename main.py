from get_data import get_data

repo_url = "https://github.com/puranpalsingh/Parllex-Website.git"
repo_id = "puranAbc"


data = get_data(repo_url=repo_url, repo_id=repo_id)

for item in data :
    print(f"File Path : {item['file_path']}")
    print(f"Content : {item['content'][:100]}...")
    print("--------------------------------------------------")