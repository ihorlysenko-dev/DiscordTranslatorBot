import discord, os
from discord.ext import commands
from deep_translator import GoogleTranslator
from usersdata import users_database

TOKEN = os.getenv("Discord_API")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())



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


### Generate random hash for file name
async def gen_hash():
    return os.urandom(16).hex()


### Command /languages
@bot.tree.command(name='languages', description='List of supported languages')
async def languages(interaction: discord.Interaction):
    await interaction.response.send_message(f'Languages supported: \n{supported_languages_formated}', ephemeral=True)


### Command /translate
@bot.tree.command(name='translate', description='Autodetect language and translate to chosen language,'
                                                ' or manually input language')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format', text='The text to translate',
                               from_lang='Manual source language input')
async def translate(interaction: discord.Interaction, destination: str, text: str, from_lang: str = None):
    ### Translate text
    if from_lang is None:  ### Detecting manual language input
        translation = GoogleTranslator(target=destination).translate(text=text)
    else:
        translation = GoogleTranslator(source=from_lang, target=destination).translate(text=text)

    ### Constructing a message to send
    await interaction.response.send_message(f"Translation: {translation}", ephemeral=True)


### Context menu button Translate
@bot.tree.context_menu(name='Translate')
async def translate_context(interaction: discord.Interaction, message: discord.Message):
    dest_lang = await get_user_language(interaction.user.id)
    if dest_lang:
        translation = GoogleTranslator(target=f"{dest_lang}").translate(text=message.content)
        await interaction.response.send_message(f"Translation:\n{translation}", ephemeral=True)
    else:
        await interaction.response.send_message("You have not set a default language yet\n"
                                                "Please use /set_language command for it", ephemeral=True)


### Get default language for context menu button Translate from database
async def get_user_language(interaction_user_id: int):
    for user in users_database:
        if interaction_user_id in user:
            return user[interaction_user_id]
    return None


@bot.tree.command(name='set_language', description='Sets your default language this will be used ONLY for Translate'
                                                   ' context menu button')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format, for more detail use /languages command')
async def set_language(interaction: discord.Interaction, destination: str):
    if destination not in supported_languages_list:
        await interaction.response.send_message("This language is not supported", ephemeral=True)

    else:
        user_id = interaction.user.id
        for user in users_database:
            if user_id in user:
                user[user_id] = destination
                await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)
        users_database.append({user_id: destination})
        await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)


if __name__ == '__main__':
    bot.run(TOKEN)
