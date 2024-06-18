from openai import OpenAI
import os
import platform
import shutil
import subprocess

PROMPT_COLOR = "\033[1;36m"
ANSWER_COLOR = "\033[1;32m"
RESET_COLOR = "\033[0m"

print(PROMPT_COLOR + "Welcome to Nadav's ChatGPT Bot. When you need to stop just write stop." + RESET_COLOR)

def get_username():
    return os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown_user'

system_info = {
    'os': platform.system(),
    'os_version': platform.version(),
    'machine': platform.machine(),
    'processor': platform.processor(),
    'python_version': platform.python_version(),
    'user': get_username(),
    'home_directory': os.path.expanduser("~")
}

filesystem_info = {
    'disk_usage': shutil.disk_usage("/"),
    'home_directory_contents': [f for f in os.listdir(os.path.expanduser("~")) if not f.startswith('.')],
    'current_directory': os.getcwd(),
    'filesystem_structure': {}
}

for root, dirs, files in os.walk(os.path.expanduser("~"), topdown=True):
    level = root.replace(os.path.expanduser("~"), "").count(os.sep)
    if level < 2:
        filesystem_info['filesystem_structure'][root] = {
            'dirs': [d for d in dirs if not d.startswith('.')],
            'files': [f for f in files if not f.startswith('.')]
        }

disk_usage = filesystem_info['disk_usage']
formatted_filesystem_info = (
    f"Disk usage: Total - {disk_usage.total // (2**30)} GB, "
    f"Used - {disk_usage.used // (2**30)} GB, "
    f"Free - {disk_usage.free // (2**30)} GB\n"
    f"Home directory contents: {filesystem_info['home_directory_contents']}\n"
    f"Current directory: {filesystem_info['current_directory']}\n"
    f"Filesystem structure (depth 2):\n"
)
for root, content in filesystem_info['filesystem_structure'].items():
    formatted_filesystem_info += f"{root}:\n"
    formatted_filesystem_info += f"    Directories: {content['dirs']}\n"
    formatted_filesystem_info += f"    Files: {content['files']}\n"

system_context = (
    f"System information:\n"
    f"OS: {system_info['os']}\n"
    f"OS Version: {system_info['os_version']}\n"
    f"Machine: {system_info['machine']}\n"
    f"Processor: {system_info['processor']}\n"
    f"Python Version: {system_info['python_version']}\n"
    f"User: {system_info['user']}\n"
    f"Home Directory: {system_info['home_directory']}\n\n"
)

full_context = system_context + formatted_filesystem_info

client = OpenAI()

messages = [
    {"role": "system", "content": "You are a ChatGPT bot inside a Linux bash shell, in AlmaLinux. First try to give a regular answer if it's a regular question not related to the next things. Just give the answer without any additional text, not even ``` and bash. If you get a couple of commands, put semicolon in between for execution. If your answer is a shell command (not a general answer), add bash -c before it so I can execute it later. If you are asked for a bash script, just write with /bin/bash format. If your answer is an Ansible Script, show it without ``` and /bin/bash.\n\n. if i ask about files and directories in the system but don't ask for command just look for them with the system info you have, and don't show the . files just regular ones" + full_context}
]

while True:
    prompt = input(PROMPT_COLOR + "Prompt:" + RESET_COLOR + " ")

    if prompt == "stop":
        print(ANSWER_COLOR + "Exiting..." + RESET_COLOR)
        break

    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    assistant_message = completion.choices[0].message.content

    print(ANSWER_COLOR + assistant_message + RESET_COLOR)

    messages.append({"role": "assistant", "content": assistant_message})

    if "bash -c" in assistant_message:
        execute = input(PROMPT_COLOR + "Do you want to execute this command? (yes/no):" + RESET_COLOR + " ")
        if execute.lower() == "yes":
            subprocess.run(assistant_message.split('bash -c ')[1], shell=True)

    if "/bin/bash" in assistant_message:
        execute = input(PROMPT_COLOR + "Do you want to make a bash script out of it? (yes/no):" + RESET_COLOR + " ")
        if execute.lower() == "yes":
            escaped_message = assistant_message.replace('"', '\\"').replace('$', '\\$')
            subprocess.run(f'echo "{escaped_message}" > ai.sh', shell=True)
            print(ANSWER_COLOR + "The script has been written to 'ai.sh'." + RESET_COLOR)

    if "hosts:" in assistant_message:
        execute = input(PROMPT_COLOR + "Do you want to make an ansible playbook out of it? (yes/no):" + RESET_COLOR + " ")
        if execute.lower() == "yes":
            escaped_message = assistant_message.replace('"', '\\"').replace('$', '\\$')
            subprocess.run(f'echo "{escaped_message}" > play.yml', shell=True)
            print(ANSWER_COLOR + "The playbook has been written to 'play.yml'." + RESET_COLOR)
