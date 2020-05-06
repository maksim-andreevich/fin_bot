from tests import table, exceptions
import re
from typing import NamedTuple, List


# Структура категории
class Newcat(NamedTuple):
    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


# Добавление категории
def add_category(raw_message: str) -> Newcat:
    try:
        parsed_message = _parse_message(raw_message)
        inserted_row_id = table.insert_category("category", {
            "codename": parsed_message.codename,
            "name": parsed_message.name,
            "is_base_expense": parsed_message.is_base_expense,
            "aliases": parsed_message.aliases})
        return Newcat(codename=parsed_message.codename,
                      name=parsed_message.name,
                      is_base_expense=parsed_message.is_base_expense,
                      aliases=parsed_message.aliases)
    except:
        raise exceptions.DubleCategory("Такая категория уже есть или введен некорректный формат\n"
                                       "Формат категории:\nеда eat 1\n\n"
                                       "Выйти: /exit")


# Парсинг сообщения с категорией
def _parse_message(raw_message: str) -> Newcat:
    regexp_result = re.split(r' ', raw_message)
    name = regexp_result[0]
    codename = regexp_result[1]
    is_base_expense = regexp_result[2]
    aliases = regexp_result[0]
    return Newcat(codename=codename, name=name, is_base_expense=is_base_expense, aliases=aliases)


# Удаляет категорию по ее названию
def delete_category(row_id: str) -> None:
    table.delete_category("category", row_id)

