import json
from deep_translator import GoogleTranslator


### Database initialization
def database_init() -> None:
    try:
        with open("userdata.json"):
            print("Database successfully loaded")
    except FileNotFoundError:
        with open("userdata.json", "w") as f:
            json.dump([], f)


### Database read
async def read_database() -> list:
    with open("userdata.json") as f:
        return json.load(f)


### Database write
async def write_database(data) -> None:
    with open("userdata.json", "w") as f:
        json.dump(data, f)


### Supported languages as text
def get_lang_text() -> str:
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    lang_list = ""
    for lang in supported_languages:
        lang_list += f"{lang} - {supported_languages[lang]}\n"
    return lang_list


### Supported languages as a list
def get_lang_list() -> list:
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)
    return [lang for lang in supported_languages.values()]


### Checking length of text
async def length_check(text) -> bool:
    if len(text) <= 1500:
        return True
    else:
        return False


### Get default language for context menu button Translate from database
async def get_user_language(interaction_user_id: str) -> str | None:
    users_db = await read_database()
    for user in users_db:
        if interaction_user_id in user:
            return user[interaction_user_id]
    return None
