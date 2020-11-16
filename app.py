from flask import Flask, request, render_template, redirect
import redis


app = Flask(__name__)
db = redis.Redis(host="redis", port=6379, db=0)     # подключение к БД


@app.route("/", methods=['GET', 'POST'])
def usual():
    if request.method == 'POST':                            # если польз-ль отправил запрос
        if 'publish' in request.form:                       # если была нажата кнопка publish
            title = request.form.get('title')               # сохраняем заголовок
            author = request.form.get('author')             # автора
            story = request.form.get('story')               # и историю
            db.lpush("title_author", f"{title}-{author}")   # добавляем в список аналог ключа
            db.lpush("story", f"{story}".encode('utf-8'))   # запоминаем в БД текст
        else:                                               # была нажата кнопка show
            return redirect("/show")                        # отправить на страницу с записями
    return render_template('base.html', visible=False)      # поля для ввода и кнопка для показа записей


@app.route("/show", methods=['GET', 'POST'])
def show():     # функция для страницы с отображенными записями
    if request.method == 'POST':        # если польз-ль отправил запрос
        if 'hide' in request.form:      # если была нажата кнопка hide
            return redirect("/")        # то отправить на страницу, где записи скрыты
        else:                           # иначе
            title = request.form.get('title')               # сохраняем заголовок
            author = request.form.get('author')             # автора
            story = request.form.get('story')               # и историю
            db.lpush("title_author", f"{title}-{author}")   # добавляем в список аналог ключа
            db.lpush("story", f"{story}".encode('utf-8'))   # запоминаем в БД текст
    # если пол-ль сюда был направлен, то отобразить страницу с кнопкой hide и записями из бд
    return render_template('records.html', visible=True, ans=get_records())


def get_records():  # функция для получения всех записей из БД
    records = [db.lindex("title_author", i).decode('utf-8') + ": " + db.lindex("story", i).decode('utf-8')
               for i in range(0, db.llen("story"))]
    return records


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
