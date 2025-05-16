import json
from googletrans import LANGUAGES


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
def get_lang_text() -> tuple[str, str]:
    lang_list1 = ""
    lang_list2 = ""
    for lang in LANGUAGES.keys():
        if len(lang_list1) < 1900:
            lang_list1 += f"{LANGUAGES[lang].title()} - {lang}\n"
        else:
            lang_list2 += f"{LANGUAGES[lang].title()} - {lang}\n"
    return lang_list1, lang_list2


### Supported languages as a list
def get_lang_list() -> list:
    return [lang for lang in LANGUAGES.keys()]


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
