"""Файл с исключениями (обработка ошибок)"""


class NotCorrectMessage(Exception):
    pass


class NotCorrectCategory(Exception):
    pass


class DubleCategory(Exception):
    pass


class NotCorrectBudget(Exception):
    pass
