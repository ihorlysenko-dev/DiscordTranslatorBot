# 🌐 Discord Translate Bot

🚀 **Demo Available:** You can test a live [demo](https://discord.com/oauth2/authorize?client_id=1370851504289873920) of this project.

A Discord bot that detects and translates messages into 245 supported languages using slash commands and context menu options. User language preferences are saved automatically — even after restarts. 

Works everywhere — you can even use it in other channels or in DMs, and only you will see the translated messages!

---

## ➕ Adding Bot to Apps

### In the Discord popup click **"Add to My Apps/Server"**
```
Add to My Apps: Available Everywhere ONLY for you
Add to Server: Available ONLY on Server
```

![image](https://github.com/user-attachments/assets/4582cae6-5461-43ef-9ddf-1d72f852fbbf)

Once added, the bot's commands will be available in chat commands.

---

## 📦 Bot Commands

### `/help`  
Info about functionality

---

### `/languages`  
Sends a list of 245 supported languages  
![languages](https://github.com/user-attachments/assets/a3b28214-8915-4e83-bff6-7a95a81d518c)

---

### `/my`  
Sets your chosen language as the default.  
🛈 *Used for context menu translation*
>Supported languages must be provided in ISO 639-1 format (e.g., `en`, `es`, `de`, `ru`, `ja`)

```bash
/my <language>
```

- User language preferences are stored in the PostgreSQL database  


- Language settings persist after bot restarts — user data is not lost.
  
![image](https://github.com/user-attachments/assets/ef66ce38-43d8-4e41-a41a-c46bec6b7341)

#### 🖱️ How to Use via Context Menu:
Right-click a message → **Apps** → **Translate**

![image](https://github.com/user-attachments/assets/0607d32e-a98b-4a60-842f-af9539685f56)
![context_2](https://github.com/user-attachments/assets/98940bc3-3a63-426a-b646-54985688a92d)

---

### `/translate`  
Translates text to the selected language.
>Supported languages must be provided in ISO 639-1 format (e.g., `en`, `es`, `de`, `ru`, `ja`)

#### ➤ Auto-detect input language:
```bash
/translate <to_lang> <text>
```

#### ➤ Manually specify source language (optional):
```bash
/translate <to_lang> <text> <from_lange>
```

![image](https://github.com/user-attachments/assets/6e1021a8-1f3d-44e2-81f9-bd664ae2ae40)

---

### Detect message language via context menu
Right-click a message → **Apps** → **Detect language**

![image](https://github.com/user-attachments/assets/cf05cb0d-6173-4bf5-8384-2010f056a616)
![image](https://github.com/user-attachments/assets/a0260a73-8bb0-46d6-b0e6-2fbfa53cc3bc)


