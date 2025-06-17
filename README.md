# Langfuse Prompt Syncer

A utility script to synchronize prompts from LOCAL to either TEST or UAT Langfuse environments.

## Description

This tool allows you to easily copy all prompts from your LOCAL Langfuse environment to either a TEST or UAT environment. It's useful for maintaining consistency across different environments and for testing prompt changes before they go into production.

## Prerequisites

- Python 3.6+
- Langfuse API keys for both source and destination projects

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/langfuse-prompt-syncer.git
   cd langfuse-prompt-syncer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the example environment file to create your own `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Langfuse API keys for all environments:
   ```
   # Langfuse host URL (default is cloud.langfuse.com)
   LANGFUSE_HOST=https://cloud.langfuse.com

   # LOCAL environment credentials (source)
   LOCAL_LANGFUSE_PUBLIC_KEY=your_prod_public_key
   LOCAL_LANGFUSE_SECRET_KEY=your_prod_secret_key

   # TEST environment credentials
   TEST_LANGFUSE_PUBLIC_KEY=your_test_public_key
   TEST_LANGFUSE_SECRET_KEY=your_test_secret_key

   # UAT environment credentials
   UAT_LANGFUSE_PUBLIC_KEY=your_uat_public_key
   UAT_LANGFUSE_SECRET_KEY=your_uat_secret_key
   ```

   You can find your API keys in your Langfuse project settings.

## Usage

Run the script with:

```bash
python main.py
```

The script will:
1. Ask you to select a destination environment (TEST or UAT)
2. Fetch all prompts from the LOCAL environment
3. For each prompt, check if it exists in the selected destination environment
4. If the prompt exists, update it with the latest version from LOCAL
5. If the prompt doesn't exist, create it in the destination environment

## Notes

- The script only syncs prompts with the "production" label
- For new prompts in the destination environment, the version starts at 1
- When updating existing prompts in the destination, the script lets Langfuse handle version numbering automatically
- LOCAL is always used as the source environment
- You can choose between TEST and UAT as the destination environment
