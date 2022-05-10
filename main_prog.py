from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from deep_translator import GoogleTranslator
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from flask import Flask, request, url_for
from data import db_session
from data.users import User
import random
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def start(update, context):
    m = "Привет! Я бот-2022 от valeronk04! Заполни форму по ссылке"
    p = "%s (работает на компьютере): http://127.0.0.1:8080/form" % (m)
    reply_keyboard = [['/ok']]
    x = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(p, reply_markup=x)


def echo(update, context):
    global fl1, fl2, name, db_sess
    if fl1:
        if update.message.text.isdigit():
            reply_keyboard = [["/info", "/back"],
                              ["/trivia", "/math", "/random_"]]
            url = 'http://numbersapi.com/%s/math' % (update.message.text)
            re = requests.get(url)
            p = GoogleTranslator(source='en', target='ru').translate(re.text)
            k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(p, reply_markup=k)
            fl1, fl2 = False, False
            user = User()
            user.name = name
            user.req = "beautiful_numbers"
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
        else:
            update.message.reply_text("Вы ввели не число!")
    elif fl2:
        if update.message.text.isdigit():
            reply_keyboard = [["/info", "/back"],
                              ["/trivia", "/math", "/random_"]]
            url = 'http://numbersapi.com/%s/trivia' % (update.message.text)
            re = requests.get(url)
            p = GoogleTranslator(source='en', target='ru').translate(re.text)
            k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(p, reply_markup=k)
            fl1, fl2 = False, False
            user = User()
            user.name = name
            user.req = "beautiful_numbers"
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
        else:
            update.message.reply_text("Вы ввели не число!")
    else:
        reply_keyboard = [["/beautiful_numbers", "/photo_from_space"],
                          ['/quote_of_the_Day', '/all_info'], ['/close']]
        p = "Отлично, %s! Что хотите посмотреть?" % (name)
        x = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(p, reply_markup=x)


def photo_from_space(update, context):
    global updater, picture, translated, inf, db_sess
    reply_keyboard = [["/back"]]
    # https://api.nasa.gov/
    j = "https://api.nasa.gov/planetary/apod?"
    url = f"{j}api_key=S2FgLdbFtPe25RTfDbzqof0g4fvM6kPkvBbgbo80"
    r = requests.get(url)
    x = r.json()
    p = x['title']
    picture = x['hdurl']
    translated = GoogleTranslator(source='en', target='ru').translate(p)
    t = "Вы попали в космическое пространство."
    update.message.reply_text("%s Сейчас вы увидите уникальный снимок." % (t))
    update.message.reply_text(translated)
    updater.bot.send_photo(chat_id=update.message.chat_id, photo=x['hdurl'])
    k = x['explanation']
    inf = GoogleTranslator(source='en', target='ru').translate(k)
    st = "А вот подробное описание(ссылка работает с компьютера):"
    update.message.reply_text(st)
    kk = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('http://127.0.0.1:8080/im',
                              reply_markup=kk)
    user = User()
    user.name = name
    user.req = "photo_from_space"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


@app.route('/im')
def im():
    global picture, translated, inf
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>{translated}</title>
                  </head>
                  <body>
                    <h3>{inf}</h3>
                    <img src="{picture}"
                     alt="здесь должна была быть картинка, но не нашлась">
                  </body>
                </html>"""


def all_info(update, context):
    global db_sess
    reply_keyboard = [["/back"]]
    x = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    for i in db_sess.query(User).all():
        p = '%s - запрос: %s %s' % (i.name, i.req, i.created_date)
        update.message.reply_text(p)
    update.message.reply_text("Это все пользователи и их запросы",
                              reply_markup=x)


@app.route('/form', methods=['POST', 'GET'])
def form():
    global name
    if request.method == 'GET':
        d = "bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
        n = "HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
        return f'''<!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, /
            shrink-to-fit=no">
            <link rel="stylesheet" /
            href="https://cdn.jsdelivr.net/npm/{d}" /
            integrity="sha384-giJF6kkoqNQ00vy+{n}"
                    crossorigin="anonymous">
            <link rel="stylesheet"type="text/css" /
            href="{url_for('static', filename='css/style.css')}" />
            <title>Пример формы</title>
             </head>
                <body>
                 <h1><center>Привет! Давай знакомиться!</center></h1>
                  <div>
                   <form class="login_form" method="post">
    <input type="text" class="form-control" id="email" /
    aria-describedby="emailHelp" placeholder="Введите своё имя" name="email">
                 <div class="form-group">
                     <label for="classSelect">Какое у вас образование?</label>
                <select class="form-control" id="classSelect" name="class">
                        <option>Начальное</option>
                         <option>Среднее</option>
                        <option>Высшее</option>
                         </select>
                 </div>
                 <div class="form-group">
                  <label for="form-check">Укажите пол</label>
                    <div class="form-check">
                      <input class="form-check-input" /
                      type="radio" name="sex" id="male" value="male" checked>
                     <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                  <input class="form-check-input" /
                        type="radio" name="sex" id="female" value="female">
                        <label class="form-check-label" for="female">
                                          Женский
                          </label>
                        </div>
                     </div>
                    <div class="form-group">
                     <label for="photo">Приложите фотографию</label>
        <input type="file" class="form-control-file" id="photo" name="file">
                        </div>
                            <br>
            <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        name = request.form['email']
        return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>OK</title>
                  </head>
                  <body>
                    <h3>OK</h3>
                  </body>
                </html>"""


def ok(update, context):
    global name
    reply_keyboard = [["/beautiful_numbers", "/photo_from_space"],
                      ['/quote_of_the_Day', '/all_info'], ['/close']]
    p = "Отлично, %s! Что хотите посмотреть?" % (name)
    x = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(p, reply_markup=x)


def beautiful_numbers(update, context):
    reply_keyboard = [["/info", "/random_"], ["/trivia", "/math"]]
    k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Раздел фактов о цифрах", reply_markup=k)


def info(update, context):
    reply_keyboard = [["/back", "/random_"], ["/trivia", "/math"]]
    k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("1) /math - математический факт")
    update.message.reply_text("2) /trivia - факт из жизни")
    update.message.reply_text("3) /random - рандомный факт", reply_markup=k)


def trivia(update, context):
    global fl2, fl1
    fl2 = True
    update.message.reply_text("Введите число,факт о котором хотите посмотреть")


def random_(update, context):
    reply_keyboard = [["/info", "/back"], ["/trivia", "/math", "/random_"]]
    a = ['math', 'trivia']
    m = random.randint(0, 10000)
    url = 'http://numbersapi.com/%s/%s' % (m, random.choice(a))
    re = requests.get(url)
    p = GoogleTranslator(source='en', target='ru').translate(re.text)
    k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(p, reply_markup=k)


def math(update, context):
    global fl2, fl1
    fl1 = True
    update.message.reply_text("Введите число,факт о котором хотите посмотреть")


def quote_of_the_Day(update, context):
    global name, db_sess
    reply_keyboard = [["/go"], ["/back"]]
    k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Цитата дня!", reply_markup=k)
    user = User()
    user.name = name
    user.req = "quote_of_the_Day"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def go(update, context):
    reply_keyboard = [["/back"], ["/go"]]
    url = "https://favqs.com/api/qotd"
    re = requests.get(url)
    x = re.json()["quote"]["body"]
    p = GoogleTranslator(source='en', target='ru').translate(x)
    k = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text(p, reply_markup=k)


def back(update, context):
    reply_keyboard = [["/beautiful_numbers", "/photo_from_space"],
                      ['/quote_of_the_Day', '/all_info'], ['/close']]
    x = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Что хотите посмотреть?", reply_markup=x)


def close(update, context):
    update.message.reply_text(
        "Пока!)))",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    global updater, fl1, fl2, db_sess
    updater = Updater("5205454801:AAHKmMQ0_Q2FEetEpWCPS4_C9IBCAeLBHRY",
                      use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("photo_from_space", photo_from_space))
    dp.add_handler(CommandHandler("beautiful_numbers", beautiful_numbers))
    dp.add_handler(CommandHandler("quote_of_the_Day", quote_of_the_Day))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("all_info", all_info))
    dp.add_handler(CommandHandler("go", go))
    dp.add_handler(CommandHandler("trivia", trivia))
    dp.add_handler(CommandHandler("math", math))
    dp.add_handler(CommandHandler("back", back))
    dp.add_handler(CommandHandler("random_", random_))
    dp.add_handler(CommandHandler("close", close))
    dp.add_handler(CommandHandler("ok", ok))
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    updater.start_polling()
    db_session.global_init("db/person_info.db")
    db_sess = db_session.create_session()
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    fl1, fl2, name, inf = False, False, '', ''
    main()
