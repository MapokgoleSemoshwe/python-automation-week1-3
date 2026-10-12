import os
import re
import sys
 
 
def check_requirements_file(project_path):
    path = os.path.join(project_path, "requirements.txt")
    exists = os.path.exists(path)
    return ("requirements.txt present", exists,
             "Run 'pip freeze > requirements.txt' if missing.")
 
 
def check_gitignore(project_path):
    path = os.path.join(project_path, ".gitignore")
    exists = os.path.exists(path)
    return (".gitignore present", exists,
             "Add one to avoid committing logs, __pycache__, and venvs.")
 
 
def check_hardcoded_windows_paths(project_path):
    """
    Scans .py files for hardcoded backslash paths (e.g. 'C:\\Users\\...')
    which will break on a Linux-based cloud VM. Scripts should use
    os.path.join() or pathlib instead.
    """
    windows_path_pattern = re.compile(r"[A-Za-z]:\\\\")
    offending_files = []
 
    for root, _, files in os.walk(project_path):
        for filename in files:
            if filename.endswith(".py"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    if windows_path_pattern.search(content):
                        offending_files.append(filename)
                except Exception:
                    continue
 
    passed = len(offending_files) == 0
    detail = ("No hardcoded paths found." if passed
              else f"Hardcoded Windows paths found in: {offending_files}")
    return ("No hardcoded OS-specific paths", passed, detail)
 
 
def generate_starter_dockerfile(project_path):
    dockerfile_path = os.path.join(project_path, "Dockerfile")
    if os.path.exists(dockerfile_path):
        return ("Dockerfile present", True, "Already exists — not overwritten.")
 
    content = (
        "FROM python:3.12-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        "CMD [\"python\", \"main.py\"]\n"
    )
    with open(dockerfile_path, "w") as f:
        f.write(content)
    return ("Dockerfile present", True, "Generated a starter Dockerfile for you.")
 
 
def run_all_checks(project_path):
    checks = [
        check_requirements_file(project_path),
        check_gitignore(project_path),
        check_hardcoded_windows_paths(project_path),
        generate_starter_dockerfile(project_path),
    ]
 
    print("=" * 55)
    print("CLOUD / VIRTUAL ENVIRONMENT READINESS CHECK")
    print("=" * 55)
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}")
        print(f"       {detail}")
    print("=" * 55)
 
 
def main():
    if len(sys.argv) != 2:
        print("Usage: python cloud_readiness_check.py <project_folder>")
        sys.exit(1)
 
    project_path = sys.argv[1]
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a valid folder.")
        sys.exit(1)
 
    run_all_checks(project_path)
 
 
if __name__ == "__main__":
    main()
 