import discord, os, json
from discord.ext import commands
from deep_translator import GoogleTranslator

TOKEN = os.getenv("Discord_API")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


### Database initialization
def database_init():
    try:
        with open("userdata.json"):
            print("Database successfully loaded")
    except FileNotFoundError:
        with open("userdata.json", "w") as f:
            json.dump([], f)


### Database read and write
async def read_database():
    with open("userdata.json") as f:
        return json.load(f)


async def write_database(data):
    with open("userdata.json", "w") as f:
        json.dump(data, f)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


### Supported languages as text
def get_lang_text():
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    lang_list = ""
    for lang in supported_languages:
        lang_list += f"{lang} - {supported_languages[lang]}\n"
    return lang_list


supported_languages_formated = get_lang_text()


### Supported languages as a list
def get_lang_list():
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    return [lang for lang in supported_languages.values()]


supported_languages_list = get_lang_list()

def length_check(text):
    if len(text) <= 1500:
        return True
    else:
        return False


### Command /languages
@bot.tree.command(name='languages', description='List of supported languages')
async def languages(interaction: discord.Interaction):
    await interaction.response.send_message(f'Languages supported: \n{supported_languages_formated}', ephemeral=True)


### Command /translate
@bot.tree.command(name='translate',
                  description='Autodetect language and translate to chosen language, or manually input language')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format',
                               text='The text to translate',
                               from_lang='Manual source language input')
async def translate(interaction: discord.Interaction, destination: str, text: str, from_lang: str = None):
    if length_check(text): # Checking if the text is too long
        ### Translate text
        if from_lang is None:  ### Detecting manual language input
            translation = GoogleTranslator(target=destination).translate(text=text)
        else:
            translation = GoogleTranslator(source=from_lang, target=destination).translate(text=text)

        ### Constructing a message to send
        await interaction.response.send_message(f"Translation: {translation}", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Context menu button Translate
@bot.tree.context_menu(name='Translate')
async def translate_context(interaction: discord.Interaction, message: discord.Message):
    if length_check(message.content): # Checking if the text is too long
        dest_lang = await get_user_language(str(interaction.user.id))
        if dest_lang:
            translation = GoogleTranslator(target=f"{dest_lang}").translate(text=message.content)
            await interaction.response.send_message(f"Translation:\n{translation}", ephemeral=True)
        else:
            await interaction.response.send_message("You have not set a default language yet\n"
                                                    "Please use /set_language command for it", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Get default language for context menu button Translate from database
async def get_user_language(interaction_user_id: str):
    users_db = await read_database()
    for user in users_db:
        if interaction_user_id in user:
            return user[interaction_user_id]
    return None


@bot.tree.command(name='set_language',
                  description='Sets your default language this will be used ONLY for Translate context menu button')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format, for more detail use /languages command')
async def set_language(interaction: discord.Interaction, destination: str):
    ### Checking if the language is supported
    if destination not in supported_languages_list:
        await interaction.response.send_message("This language is not supported\n"
                                                "Try again", ephemeral=True)

    ### Checking if the user is already in the database
    else:
        ### Updating database
        user_id = str(interaction.user.id)  # converting user_id to string
        users_db = await read_database()
        ### If the user is already in a database, update his language
        for user in users_db:
            if user_id in user:
                user[user_id] = destination
                await write_database(users_db)
                await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)
                break
        else:
            ### If the user is not in a database, add him
            users_db.append({user_id: destination})
            await write_database(users_db)
            await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)


if __name__ == '__main__':
    database_init()
    bot.run(TOKEN)
