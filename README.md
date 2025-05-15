# 🌐 Discord Translate Bot

🚀 **Demo Available:** You can test a live [demo](https://discord.com/oauth2/authorize?client_id=1370851504289873920) of this project

A Discord bot that detects and translates messages into 133 supported languages using slash commands and context menu options. User language preferences are saved automatically — even after restarts. 

Works anywhere — you can use it in all channels or DMs, and only you will see the translated messages!

---

## 🛠 Setup

To start the bot:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set an environment variable named `Discord_API` with your Discord Bot token:
   ```python
   TOKEN = os.getenv("Discord_API")
   ```

**Or** hardcode the token (not recommended for production):
```python
TOKEN = "YOUR_API_HERE"
```

---

## ➕ Adding Bot to Apps

To make the bot available in your server:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application.
3. Navigate to the **"Installation"** tab.
4. Copy your **"Install Link"** and open it in your browser.

![image](https://github.com/user-attachments/assets/6131bd7b-5776-409a-8de9-a00ed8e2597e)

In the Discord popup, click **"Add to My Apps"**  
![image](https://github.com/user-attachments/assets/4582cae6-5461-43ef-9ddf-1d72f852fbbf)

Once added, the bot's commands will be available in chat commands.

---

## 📦 Bot Commands

### `/languages`  
Sends a list of 133 supported languages  
![languages](https://github.com/user-attachments/assets/a3b28214-8915-4e83-bff6-7a95a81d518c)

---

### `/set_language`  
Sets your chosen language as the default.  
🛈 *Used for context menu translation*
>Supported languages must be provided in ISO 639-1 format (e.g., `en`, `es`, `de`, `ru`, `ja`)

```bash
/set_language <your language>
```

- User language preferences are stored in a `.json` file in the format:  
  ```json
  { "user_id": "language" }
  ```
- Language settings persist after bot restarts — user data is not lost.
  
![set_language](https://github.com/user-attachments/assets/70250853-e407-448c-986c-b8d1556d9d2e)

#### 🖱️ How to Use via Context Menu:
Right-click a message → **Apps** → **Translate**

![context_1](https://github.com/user-attachments/assets/a138d8bc-f069-43ae-9162-a7d7549a5041)  
![context_2](https://github.com/user-attachments/assets/98940bc3-3a63-426a-b646-54985688a92d)

---

### `/translate`  
Translates text to the selected language.
>Supported languages must be provided in ISO 639-1 format (e.g., `en`, `es`, `de`, `ru`, `ja`)

#### ➤ Auto-detect input language:
```bash
/translate <target language> <your text>
```

#### ➤ Manually specify source language (optional):
```bash
/translate <target language> <your text> <source language>
```

![translate](https://github.com/user-attachments/assets/8ef3b382-3efe-4b07-a3f9-cf54e8399685)
