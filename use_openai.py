from openai import OpenAI
import subprocess

print("Welcome to Nadav's ChatGPT Bot. When you need to stop just write stop.")

# Initialize the OpenAI client
client = OpenAI()

# Initialize the messages list with a system message
messages = [
    {"role": "system", "content": "You are a ChatGPT bot inside a Linux bash shell, in AlmaLinux. Just give the answ>
]

while True:
    # Get the user input prompt
    prompt = input("Prompt: ")

    # Check if the user wants to stop
    if prompt == "stop":
        print("Exiting...")
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

    # Print the message content
    print(assistant_message)

    # Append the assistant's message to the messages list
    messages.append({"role": "assistant", "content": assistant_message})

 # Check if the assistant's message looks like a command
    if "bash -c" in assistant_message:
        # Ask the user if they want to execute the content
        execute = input("Do you want to execute this content? (yes/no): ")
        if execute == "yes":
            # Execute the content
            subprocess.run(assistant_message, shell=True)
            break

   
    if "/bin/bash" in assistant_message:
        # Ask the user if  they to make a bash script out of it
        execute = input("Do you want to make a bash script out of it? (yes/no): ")
        if execute == "yes":
            # Add the result to a new script file 
            escaped_message = assistant_message.replace('"', '\\"').replace('$', '\\$')
            subprocess.run(f'echo "{escaped_message}" > ai.sh', shell=True)
            print("The script has been written to 'ai.sh'.")
            break


