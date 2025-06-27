from googletrans import LANGUAGES
import psycopg


### Database initialization
def database_init(DB_CONFIG) -> None:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS userdata
                       (   id           serial,
                           user_id      TEXT PRIMARY KEY,
                           name         TEXT,
                           language     TEXT,
                           translations integer DEFAULT 0
                        )""")

            conn.commit()


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
async def get_user_language(DB_CONFIG, user_id: str) -> str | None:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT language FROM userdata
                           WHERE user_id = %s""", (user_id,))
            user_language = cur.fetchone()
            if user_language is None:
                return None
            else:
                return user_language[0]

async def set_user_language(DB_CONFIG, user_id: str, language: str) -> None:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE userdata
                           SET language = %s
                           WHERE user_id = %s""", (language, user_id))
            conn.commit()


async def add_user_to_db(DB_CONFIG, user_id, user_name, language) -> None:
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO userdata (user_id, name, language)
                           VALUES (%s, %s, %s)
                           ON CONFLICT (user_id) DO UPDATE SET name = %s, language = %s""", (user_id, user_name, language, user_name, language))
            conn.commit()


async def update_counter(DB_CONFIG, user_id):
    with psycopg.connect(DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""UPDATE userdata
                           SET translations = translations + 1
                           WHERE user_id = %s""", (user_id,))
            conn.commit()