import discord, os
from discord.ext import commands
from discord import app_commands
from googletrans import Translator, LANGUAGES
from bot_functions import (database_init, get_lang_text, get_lang_list, length_check,
                           get_user_language, add_user_to_db, update_counter, set_user_language)
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = os.getenv("DB_CONFIG")
TOKEN = os.getenv("DISCORD_API")
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


### Command /languages
@bot.tree.command(name='languages', description='List of supported languages')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def languages(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f'Languages supported:\n{supported_languages_text1}', ephemeral=True)
    await interaction.followup.send(f'{supported_languages_text2}', ephemeral=True)


### Command /translate
@bot.tree.command(name='translate',
                  description='Autodetect language and translate to chosen language'
                              '(or you can manually input your language')
@discord.app_commands.describe(to_lang='The language in "en/ja/ru" format',
                               text='The text to translate',
                               from_lang='Manual source language input')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def translate(interaction: discord.Interaction, to_lang: str, text: str, from_lang: str = None) -> None:
    if await length_check(text):  # Checking if the text is too long
        ### Translate text
        if from_lang:  ### Detecting manual language input if is not None
            async with Translator() as translator:
                translation = await translator.translate(dest=to_lang, text=text, src=from_lang)
        else:
            async with Translator() as translator:
                translation = await translator.translate(dest=to_lang, text=text)

        ### Constructing a message to send
        await interaction.response.send_message(f"Translation:\n{translation.text}", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Context menu button Translate
@bot.tree.context_menu(name='Translate')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def translate_context(interaction: discord.Interaction, message: discord.Message) -> None:
    if await length_check(message.content):  # Checking if the text is too long
        user_language = await get_user_language(DB_CONFIG, str(interaction.user.id))  # Getting user language from a database or None
        if user_language:
            async with Translator() as translator:
                translation = await translator.translate(text=message.content, dest=user_language)
                await interaction.response.send_message(f"Translation:\n{translation.text}", ephemeral=True)
                await update_counter(DB_CONFIG, str(interaction.user.id))
        else:
            await interaction.response.send_message("You have not set a default language yet\n"
                                                    "Please use /my command for it", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Setting user language
@bot.tree.command(name='my',
                  description='Sets your default language for: Right click on message -> Apps -> Translate')
@discord.app_commands.describe(language='The language in "en/ja/ru" format, for more detail use /languages command')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def my(interaction: discord.Interaction, language: str) -> None:
    if language in supported_languages_list:
        user_id = str(interaction.user.id)  # converting user_id to string
        user_name = str(interaction.user.name)
        if await set_user_language(DB_CONFIG, user_id, language):
            await interaction.response.send_message(f"Language set to {language}", ephemeral=True)
        else:  # If the user is not in a database, add him
            await add_user_to_db(DB_CONFIG, user_id, user_name, language)
            await interaction.response.send_message(f"Language set to {language}", ephemeral=True)

    else:
        ### Sending a message about not supported language or language format
        await interaction.response.send_message("This language is not supported\n"
                                                "Try again", ephemeral=True)


### Detect language context menu
@bot.tree.context_menu(name='Detect language')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def translate_context(interaction: discord.Interaction, message: discord.Message) -> None:
    async with Translator() as translator:
        result = await translator.detect(message.content)
        try:
            await interaction.response.send_message(
                f"Detected language: {LANGUAGES[result.lang.lower()].title()} - {result.lang.lower()}", ephemeral=True)
        except KeyError:
            await interaction.response.send_message(f"Detected language: {result.lang.lower()}", ephemeral=True)


### Help command
@bot.tree.command(name='help', description='Info about functionality')
@app_commands.allowed_contexts(guilds=True,  # usable in servers
                               dms=True,  # usable in 1-to-1 DMs <- dm_permission=True
                               private_channels=True  # usable in group-DMs
                               )
async def help(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f'Commands:\n'
                                            f'/languages - List of supported languages\n\n'
                                            f'/translate - Autodetect language and translate to chosen language\n'
                                            f'(or you can manually input your language)\n\n'
                                            f'/my - Sets your default language. Used for: Right click on message -> Apps -> Translate\n\n'
                                            f'Detect message language: Right click on message -> Apps -> Detect language',
                                            ephemeral=True,
                                            )


def main() -> None:
    database_init(DB_CONFIG)
    bot.run(TOKEN)


if __name__ == '__main__':
    supported_languages_text1, supported_languages_text2 = get_lang_text()
    supported_languages_list = get_lang_list()
    main()
