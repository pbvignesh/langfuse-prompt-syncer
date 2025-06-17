from langfuse import Langfuse
import os
import requests
import base64
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

# Initialize Langfuse clients for source and destination projects
def initialize_langfuse_client(public_key, secret_key, host=None):
    # Use provided host or get from environment variable with default fallback
    host = host or os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
    langfuse = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host
    )
    if not langfuse.auth_check():
        raise Exception(f"Authentication failed for Langfuse client with public key {public_key}")
    return langfuse

# Function to fetch all production prompts from the source project
def fetch_prompts(langfuse_client):
    try:
        # Get all prompts from the API
        all_prompts = langfuse_client.api.get_prompts()
        print("Printing the prompts")
        print(all_prompts)
        
        # Filter to get only prompts with production label
        production_prompts = []
        for prompt in all_prompts:
            try:
                # Get the production version of each prompt
                prod_prompt = langfuse_client.get_prompt(prompt.name, label="production")
                production_prompts.append(prod_prompt)
            except Exception as e:
                print(f"Failed to fetch production version of prompt {prompt.name}: {e}")
        
        return production_prompts
    except Exception as e:
        raise Exception(f"Failed to fetch prompts: {e}")

# Function to check if a prompt exists in the destination project
def prompt_exists(langfuse_client, prompt_name):
    try:
        langfuse_client.get_prompt(prompt_name, label="production")
        return True
    except Exception:
        return False

# Function to update or create prompts in the destination project
def sync_prompts(prompts, dest_langfuse):
    for prompt in prompts:
        try:
            if prompt_exists(dest_langfuse, prompt.name):
                # Update existing prompt
                dest_langfuse.create_prompt(
                    name=prompt.name,
                    prompt=prompt.prompt,
                    type=prompt.type,
                    config=prompt.config,
                    labels=["production"]
                )
                print(f"Updated prompt {prompt.name}")
            else:
                # Create new prompt with version 1
                dest_langfuse.create_prompt(
                    name=prompt.name,
                    prompt=prompt.prompt,
                    type=prompt.type,
                    config=prompt.config,
                    labels=["production"],
                    version=1
                )
                print(f"Created prompt {prompt.name} with version 1")
        except Exception as e:
            print(f"Failed to sync prompt {prompt.name}: {e}")

# Function to get destination environment choice from user
def get_destination_choice():
    while True:
        print("\nSelect destination environment:")
        print("1. TEST")
        print("2. UAT")
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            return "TEST"
        elif choice == "2":
            return "UAT"
        else:
            print("Invalid choice. Please enter 1 for TEST or 2 for UAT.")

# Main execution
def main():
    # Initialize LOCAL Langfuse client (source)
    local_langfuse = initialize_langfuse_client(
        os.environ.get("LOCAL_LANGFUSE_PUBLIC_KEY"),
        os.environ.get("LOCAL_LANGFUSE_SECRET_KEY")
    )

    # Get destination environment choice from user
    dest_env = get_destination_choice()

    # Initialize destination Langfuse client based on user choice
    if dest_env == "TEST":
        dest_langfuse = initialize_langfuse_client(
            os.environ.get("TEST_LANGFUSE_PUBLIC_KEY"),
            os.environ.get("TEST_LANGFUSE_SECRET_KEY")
        )
        print("\nSelected TEST as destination environment")
    else:  # UAT
        dest_langfuse = initialize_langfuse_client(
            os.environ.get("UAT_LANGFUSE_PUBLIC_KEY"),
            os.environ.get("UAT_LANGFUSE_SECRET_KEY")
        )
        print("\nSelected UAT as destination environment")

    # Fetch prompts from LOCAL project
    print("\nFetching prompt names from LOCAL environment...")
    prompts = fetch_prompts(local_langfuse)
    print(f"Fetched {len(prompts)} prompts: {[p.name for p in prompts]}")

    # Sync prompts to destination project
    print(f"\nSyncing prompts to {dest_env} environment...")
    # sync_prompts(prompts, dest_langfuse)
    print(f"Prompt migration from LOCAL to {dest_env} completed")

if __name__ == "__main__":
    main()
