import telebot
from telebot import types
import telegram
from tests import exceptions, expenses, budget, cust
from tests.categories import Categories

bot = telebot.TeleBot('Твой токен')


# Кнопка /help
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
help1 = types.KeyboardButton(text='/help')
keyboard.add(help1)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Привествие и вызов кнопки /help"""
    bot.send_message(message.from_user.id, ("Привет, {0}!\n"
                                            "Чтобы начать нажми /help.\n"
                                            "Если есть вопросы или рекомендации, "
                                            "то пиши сюда - @maksimandreevichr").format(message.from_user.first_name),
                                            reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help(message):
    """Отправка всех команд"""
    bot.send_message(message.from_user.id, ("<b>Бот для учёта финансов</b>\n\n"
                                            "<b>Траты</b>\n"
                                            "100 еда - добавить расход\n"
                                            "/today - за текущий день\n"
                                            "/month - за текущий месяц\n"
                                            "/expenses - последние траты (с удалением)\n"
                                            "/categories - категории трат\n\n"
                                            "<b>Настойки</b>\n"
                                            "/add_category - добавить категорию\n"
                                            "/category_del - удалить категорию\n"
                                            "/daily_limit - дневной лимит"), parse_mode=telegram.ParseMode.HTML)


@bot.message_handler(commands=['categories'])
def categories_list(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Достает список всех категорий и поверяет есть ли они вообще.
        categories = Categories().get_all_categories()
        if not categories:
            bot.send_message(message.from_user.id, "Категории ещё не заведены") # Если категорий нет
            return
        answer_message = "Категории трат:\n\n• " +\
            ("\n• ".join([c.name for c in categories])) # Если категории есть
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['month'])
def month_stat(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Отправляет статистику за месяц
        answer = expenses.get_month_statistics()
        bot.send_message(message.from_user.id, answer)


@bot.message_handler(func=lambda message: message.text.startswith('/del_'))
def del_category(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Например, удаляешь категорию eat, боту отправляется /del_eat
        row_id = str(message.text[5:]) # Из /del_eat берутся все буквы после первых 5, то есть после /del_
        cust.delete_category(row_id) # Название отправляется дальше в cust.py и по этому названию удаляется категория eat
        answer_message = "Удалил"
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['category_del'])
def list_del(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Достатет и отправляет список категорий для удаления
        categories = Categories().get_all_categoriesdel()
        if not categories:
            bot.send_message(message.from_user.id, "Категории ещё не заведены")
            return
        list_del_cat = [
            "/del_{0}".format(c.codename)
            for c in categories]
        answer_message = "Нажми для удаления:\n\n• " + "\n\n• ".join(list_del_cat)
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['today'])
def today_stat(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Отправляет статистику за сегодня
        answer_message = expenses.get_today_statistics()
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['expenses'])
def list_exp(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Отправляет последние 10 трат с командами для удаления
        last_expenses = expenses.last()
        if not last_expenses:
            bot.send_message(message.from_user.id, "Расходы ещё не заведены")
            return
        last_expenses_rows = [
            "{0} руб. на {1} — нажми /delete_{2} для удаления".format(expense.amount, expense.category_name, expense.id)
            for expense in last_expenses]
        answer_message = "Последние сохранённые траты:\n\n• " + "\n\n• " \
            .join(last_expenses_rows)
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(func=lambda message: message.text.startswith('/delete_'))
def del_expense(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Анадогично удалению категории, только тут удаление расхода
        row_id = int(message.text[8:])
        expenses.delete_expense(row_id)
        answer_message = "Удалил"
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['daily_limit'])
def update_limit(message):
    # Отправляет текущий лимит и запускает процесс для изменения лимита
    bot.send_message(message.from_user.id, ("Твой текущий дневной лимит: {0}\n"
                                            "Для обновления введи новый лимит, например: 500\n\n"
                                            "Выход: /exit").format(expenses._get_budget_limit()))
    bot.register_next_step_handler(message, raw_budget)


def raw_budget(message):
    # Отмена изменения лимита
    if message.text == "/exit":
        bot.send_message(message.from_user.id, "Вы вышли из настроек.\n"
                                               "/help")

    # Берет число лимита и проверяет на корректность
    else:
        try:
            raw_message = int(message.text)
        except:
            bot.send_message(message.from_user.id, "Некорректный формат\n"
                                                   "Правильный формат: 500")
            return
        budget.up_limit(raw_message) # Отправлет лимит в budget.py
        answer_message = "Обновил"
        bot.send_message(message.from_user.id, answer_message)


@bot.message_handler(commands=['add_category'])
def add_category(message):
    # Отправляет инструкцию и запускает процесс для добавления категорий
    bot.send_message(message.from_user.id, "<b>Ты попал в настройку категорий.</b>\n\n"
                                            "Формат категории:\nкатегория caregory 1\n\n"
                                            "1 - базовая категория\n0 - не базовая категория\n"
                                            "Выйти: /exit", parse_mode=telegram.ParseMode.HTML)
    bot.register_next_step_handler(message, raw_category)


def raw_category(message):
    # Отмена добавления категорий
    if message.text == "/exit":
        bot.send_message(message.from_user.id, "Вы вышли из настроек.\n"
                                               "/help")

    # Берет категорию и проверяет на корректность
    else:
        try:
            name = cust.add_category(message.text.lower())
        except exceptions.DubleCategory as d:
            answer1 = str(d)
            bot.send_message(message.from_user.id, answer1)
            bot.register_next_step_handler(message, raw_category)
            return
        bot.send_message(message.from_user.id, "Категория добавлена.\nТы все еще в настройках. Выйти: /exit")
        bot.register_next_step_handler(message, raw_category)


@bot.message_handler(content_types=['text'])
def add_expense(message):
    # Провека id пользователя
    if message.from_user.id == 467257161:

        # Берет расход, отправляет на парсинг в expenses.py и проверяет на корректность
        try:
            expense = expenses.add_expense(message.text)
        except exceptions.NotCorrectMessage as e:
            answer = str(e)
            bot.send_message(message.from_user.id, answer)
            return
        answer_message = ("Добавлены траты {0} руб на {1}.\n"
                          "/help").format(expense.amount, expense.category_name)
        bot.send_message(message.from_user.id, answer_message)

    def get_id(msg):
        user_id = msg.from_user.id
        return user_id


bot.polling(none_stop=True, interval=0)

