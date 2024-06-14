from openai import OpenAI
import subprocess

# Color definitions
PROMPT_COLOR = "\033[1;36m"
ANSWER_COLOR = "\033[1;32m"
RESET_COLOR = "\033[0m"

print(PROMPT_COLOR + "Welcome to Nadav's ChatGPT Bot. When you need to stop just write stop." + RESET_COLOR)

# Initialize the OpenAI client
client = OpenAI()

# Initialize the messages list with a system message
messages = [
    {"role": "system", "content": "You are a ChatGPT bot inside a Linux bash shell, in AlmaLinux. Just give the answer without any additional text. not even ``` and bash. if you get a couple of commands put semicolon in between for exection. if your answer is a shell command (not a general answer) add bash -c before it so i can execute it later. if you are asked for a bash script just write with /bin/bash format"}
]

while True:
    # Get the user input prompt
    prompt = input(PROMPT_COLOR + "Prompt:" + RESET_COLOR + " ")

    # Check if the user wants to stop
    if prompt.lower() == "stop":
        print(ANSWER_COLOR + "Exiting..." + RESET_COLOR)
        break

    # Append the user's message to the messages list
    messages.append({"role": "user", "content": prompt})

    # Create the chat completion
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    # Extract the message content
    assistant_message = completion.choices[0].message.content

    # Print the message content in green
    print(ANSWER_COLOR + assistant_message + RESET_COLOR)

    # Append the assistant's message to the messages list
    messages.append({"role": "assistant", "content": assistant_message})

    # Check if the assistant's message looks like a command
    if "bash -c" in assistant_message:
        # Ask the user if they want to execute the content
        execute = input(PROMPT_COLOR + "Do you want to execute this content? (yes/no):" + RESET_COLOR + " ")
        if execute.lower() == "yes":
            # Execute the content
            subprocess.run(assistant_message, shell=True)

    if "/bin/bash" in assistant_message:
        # Ask the user if they want to make a bash script out of it
        execute = input(PROMPT_COLOR + "Do you want to make a bash script out of it? (yes/no):" + RESET_COLOR + " ")
        if execute.lower() == "yes":
            # Add the result to a new script file
            escaped_message = assistant_message.replace('"', '\\"').replace('$', '\\$')
            subprocess.run(f'echo "{escaped_message}" > ai.sh', shell=True)
            print(ANSWER_COLOR + "The script has been written to 'ai.sh'." + RESET_COLOR)
