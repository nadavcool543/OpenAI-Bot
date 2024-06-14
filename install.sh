!/bin/bash

# Prompt the user for their OpenAI API key
read -p "Please enter your OpenAI API key: " openai_api_key

# Get the home directory of the current user
home_dir=$(eval echo ~$USER)

# Install the OpenAI package
echo "Installing OpenAI package..."
pip install openai

# Append the OpenAI API key to .bashrc
echo "Updating .bashrc with OpenAI API key..."
echo "export OPENAI_API_KEY=${openai_api_key}" >> ${home_dir}/.bashrc

# Append the alias to .bashrc
echo "Updating .bashrc with alias for gpt..."
echo "alias gpt='python3 ${home_dir}/use_openai.py'" >> ${home_dir}/.bashrc

# Source the .bashrc file to apply changes
echo "Reloading .bashrc..."
source ${home_dir}/.bashrc

echo "The OpenAI package has been installed, and the .bashrc file has been updated and reloaded."

