# 🌿 Herb Helper Bot

Herb Helper Bot is a Telegram bot that helps users distinguish between Coriander and Parsley by analyzing photos sent via chat. It utilizes OpenAI's image recognition capabilities to classify the plant based on your image.

## ✨ Features

- Upload a photo of either Coriander or Parsley, and the bot will tell you which plant it is.
- If the photo doesn't contain either plant, it will respond with "Invalid."
- Built using Python, `python-telegram-bot`, OpenAI API, and Pillow for image processing.

## 🛠️ Prerequisites

Before running the bot, make sure you have:

- **Python 3.8** or higher installed.
- A **Telegram Bot token** (see the setup steps below).
- An **OpenAI API key**.

## 🛠️ Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/herb-helper-bot.git
    cd herb-helper-bot
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

    On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Add your Telegram Bot Token and OpenAI API Key:**

    Create a file called `tokens.txt` in the project directory and add your tokens like this:

    ```txt
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
    OPENAI_API_KEY=your_openai_api_key_here
    ```

5. **Run the bot:**

    Once everything is set up, start the bot by running:

    ```bash
    python bot.py
    ```

    If everything is working correctly, you will see messages like "Bot started" in your terminal.

## 🤖 How to Create a Telegram Bot

1. **Talk to BotFather**:

    Open Telegram and search for [BotFather](https://telegram.me/BotFather). Start a conversation and send `/newbot`.

2. **Name Your Bot**:

    Follow the instructions and give your bot a name like "Herb Helper Bot."

3. **Choose a Username**:

    BotFather will ask for a username that must end in `bot` (e.g., `HerbHelperBot`).

4. **Get Your Token**:

    After creating the bot, BotFather will give you an API token. Copy it.

5. **Add the Token to `tokens.txt`:**

    Open your `tokens.txt` file and replace `your_telegram_bot_token_here` with the token provided by BotFather.

6. **Set Bot Commands (Optional):**

    You can set commands using `/setcommands` in BotFather to make the bot more user-friendly:

    ```txt
    start - Start the bot
    ```

## 🚀 Usage

1. **Start the Bot**:

    Ensure the bot is running with:

    ```bash
    python bot.py
    ```

2. **Interact with the Bot**:

    - Open Telegram and search for your bot by username (e.g., `HerbHelperBot`).
    - Send the `/start` command.
    - Send a picture of a Coriander or Parsley plant, and the bot will classify it for you.

## 📦 Dependencies

- **`python-telegram-bot`**: A wrapper for Telegram Bot API.
- **`openai`**: OpenAI API for image recognition.
- **`Pillow`**: Python library for image processing.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Omar Wahba
