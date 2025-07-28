import os

files = [
    "requirements.txt",
    "README.md",
    "main.py",
    "src/config/config.py",
    "src/agents/master_agent.py",
    "src/agents/code_suggestion_agent.py",
    "src/agents/code_review_agents/mulesoft_code_review_agent.py",
    "src/agents/code_review_agents/general_code_review_agent.py",
    "src/api/server.py",
    "src/api/routes.py",
    "src/utils/logger.py",
    "src/dashboard/app.py",
    ".env",
    "setup.py",
]

for file in files:
    folder = os.path.dirname(file)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created directory: {folder}")

    if not os.path.exists(file):
        with open(file, 'w') as f:
            f.write("# Placeholder for " + file)
        print(f"Created: {file}")
    else:
        print(f"File already exists: {file}")