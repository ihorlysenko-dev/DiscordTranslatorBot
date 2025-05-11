import discord, os
from discord.ext import commands
from googletrans import Translator, LANGUAGES

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


def lang_list():
    text1_len = 0
    text1 = ""
    text2 = ""
    for lang in LANGUAGES:
        structure = f"{lang} - {LANGUAGES[lang]}\n"
        if text1_len <= 1900:
            text1 += structure
            text1_len += len(structure)
        else:
            text2 += structure
    return text1, text2
text1, text2 = lang_list()

@bot.tree.command(name='languages', description='List of supported languages')
async def languages(interaction: discord.Interaction):
    await interaction.response.send_message(f'Languages supported: {text1}', ephemeral=True)
    await interaction.followup.send(f'Languages supported: {text2}', ephemeral=True)


@bot.tree.command(name='translate', description='Autodetect language and translate to chosen language,'
                                                ' or manually input language')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format', text='The text to translate',
                               from_lang='Manual source language input')
async def translate(interaction: discord.Interaction, destination: str, text: str, from_lang: str = None):
    translator = Translator()
    if from_lang is None:
        translation = await translator.translate(text, dest=destination)
    else:
        translation = await translator.translate(text, dest=destination, src=from_lang)

    text_to_send = (f"From {translation.src.upper()} to {translation.dest.upper()}\n"
                    f"Text: {text}\n"
                    f"Translation: {translation.text}\n"
                    f"Pronunciation: {translation.pronunciation}")
    await interaction.response.send_message(text_to_send, ephemeral=True)


if __name__ == '__main__':
    bot.run(TOKEN)
