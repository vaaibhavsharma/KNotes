from flask import Flask, request
from flask import render_template as render
import os, re

SOURCE_FOLDER = os.path.abspath('../personal_notes')

if not os.path.exists(SOURCE_FOLDER):
    os.makedirs(SOURCE_FOLDER)

app = Flask(__name__)

def get_notes(query=None):
    res = []
    for i in os.listdir(SOURCE_FOLDER):
        if query and query not in i:
            continue
        pointer = i[:-3]
        tags = []
        if ':' in pointer:
            tags, pointer = pointer.split(':', 1)
            tags = tags.split(',')
        res.append({
            'pointer': pointer,
            'name': re.sub(r'[^a-zA-Z0-9]+', ' ', pointer),
            'tags':tags
        })
    return res

@app.route("/")
def index():
    return render("index.html")

@app.route("/fetch/<note_name>/")
def fetch(note_name):
    return render('preview.html',
        markdown=open(os.path.join(SOURCE_FOLDER, f'{note_name}.md'), 'r').read()
    )

@app.route("/fetch/index/")
def fetch_sidebar():
    search = request.args.get('search', None)
    return render('sidebar.html', notes=get_notes(query=search)) 


@app.route("/fetch/<note_name>/edit/")
def edit_markdown(note_name):
    return render('editor.html',
        markdown=open(os.path.join(SOURCE_FOLDER, f'{note_name}.md'), 'r').read()
    )

# flask --app main:app run --debug
# https://jinja.palletsprojects.com/en/3.1.x/templates/
