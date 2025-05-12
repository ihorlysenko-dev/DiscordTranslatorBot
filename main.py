import discord, os
from discord.ext import commands
from deep_translator import GoogleTranslator
from gtts import gTTS

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


### Languages list, separated into two messages due to discord's message limit of 2000 characters
def get_lang_list():
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    lang_list = ""
    for lang in supported_languages:
        lang_list += f"{lang} - {supported_languages[lang]}\n"
    return lang_list
supported_languages_formated = get_lang_list()


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
        translation = GoogleTranslator(source='auto', target=destination).translate(text=text)
    else:
        translation = GoogleTranslator(source=from_lang, target=destination).translate(text=text)

    ### Constructing a message to send
    await interaction.response.send_message(f"Translation: {translation}", ephemeral=True)




if __name__ == '__main__':
    bot.run(TOKEN)
