import os

EXTENSIONS = [".py", ".js", ".java", ".cpp", ".ts", ".ipynb", ".html", ".css"]

def load_code_files(root_folder):
    code_data = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if any(file.endswith(ext) for ext in EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        code_data.append({"file": file_path, "content": content})
                except Exception as e:
                    print(f"Skipping file {file_path}: {e}")
    return code_data

def chunk_code(code_files, max_length=500):
    chunks = []
    for item in code_files:
        content = item["content"]
        file_path = item["file"]
        lines = content.splitlines()
        for i in range(0, len(lines), max_length):
            chunk = "\n".join(lines[i:i+max_length])
            chunks.append({"file": file_path, "content": chunk})
    return chunks
