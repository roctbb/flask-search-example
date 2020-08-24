from flask import Flask, render_template, request
import vk

session = vk.Session(access_token='TOKEN_HERE')
api = vk.API(session)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    # валидация
    query = request.args.get('anek', '')
    if not query:
        return "введите текст анекдота"

    likes = request.args.get('likes', '')
    if not likes:
        likes = 0
    else:
        likes = int(likes)

    aneks = api.wall.search(domain='baneks', query=query, v=5.211, count=100, owners_only=1)

    good_aneks = []
    for anek in aneks['items']:
        if anek['likes']['count'] > likes:
            anek['text'] = anek['text'].replace('\n', '<br>')
            good_aneks.append(anek)

    return render_template('search.html', query=query, likes=likes, aneks=good_aneks)

app.run(debug=True)