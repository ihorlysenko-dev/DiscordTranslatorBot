import discord, os
from discord.ext import commands
from deep_translator import GoogleTranslator
from bot_functions import (database_init, read_database, write_database, get_lang_text, get_lang_list, length_check,
                           get_user_language)

TOKEN = os.getenv("Discord_API")
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
async def languages(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f'Languages supported:\n{supported_languages_text}', ephemeral=True)


### Command /translate
@bot.tree.command(name='translate',
                  description='Autodetect language and translate to chosen language, or manually input language')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format',
                               text='The text to translate',
                               from_lang='Manual source language input')
async def translate(interaction: discord.Interaction, destination: str, text: str, from_lang: str = None) -> None:
    if await length_check(text):  # Checking if the text is too long
        ### Translate text
        if from_lang:  ### Detecting manual language input if is not None
            translation = GoogleTranslator(source=from_lang, target=destination).translate(text=text)
        else:
            translation = GoogleTranslator(target=destination).translate(text=text)

        ### Constructing a message to send
        await interaction.response.send_message(f"Translation:\n{translation}", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Context menu button Translate
@bot.tree.context_menu(name='Translate')
async def translate_context(interaction: discord.Interaction, message: discord.Message) -> None:
    if await length_check(message.content):  # Checking if the text is too long
        user_language = await get_user_language(
            str(interaction.user.id))  # Getting user language from a database or None
        if user_language:
            translation = GoogleTranslator(target=f"{user_language}").translate(text=message.content)
            await interaction.response.send_message(f"Translation:\n{translation}", ephemeral=True)
        else:
            await interaction.response.send_message("You have not set a default language yet\n"
                                                    "Please use /set_language command for it", ephemeral=True)
    else:
        await interaction.response.send_message("Text is too long, please try again\n"
                                                "Limit 1500 symbols", ephemeral=True)


### Setting user language
@bot.tree.command(name='set_language',
                  description='Sets your default language this will be used ONLY for Translate context menu button')
@discord.app_commands.describe(destination='The language in "en/ja/ru" format, for more detail use /languages command')
async def set_language(interaction: discord.Interaction, destination: str) -> None:
    if destination in supported_languages_list:
        user_id = str(interaction.user.id)  # converting user_id to string
        users_db = await read_database()  # Reading DB
        ### If the user is already in a database, update his language
        for user in users_db:
            if user_id in user:
                user[user_id] = destination
                await write_database(users_db)
                await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)
                break
        else:  # If the user is not in a database, add him
            users_db.append({user_id: destination})
            await write_database(users_db)
            await interaction.response.send_message(f"Language set to {destination}", ephemeral=True)

    else:
        ### Sending a message about not supported language or language format
        await interaction.response.send_message("This language is not supported\n"
                                                "Try again", ephemeral=True)


def main() -> None:
    database_init()
    bot.run(TOKEN)


if __name__ == '__main__':
    supported_languages_text = get_lang_text()
    supported_languages_list = get_lang_list()
    main()
