from tests import table, exceptions


# Обновляет лимит
def up_limit(raw_message: int) -> None:
    try:
        table.update_budget("budget", raw_message)
    except:
        raise exceptions.NotCorrectCategory("Некорректный формат")
