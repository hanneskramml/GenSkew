import json
from io import TextIOWrapper
from flask import render_template, redirect, url_for, session, request
from genskew.web import app
from genskew.web.model import Tab
from genskew.web.forms import NewTabForm
from genskew.input import SeqLoader


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', navitems=__get_nav_items(), newTabForm=NewTabForm())


@app.route('/new', methods=['POST'])
def new_tab():
    form = NewTabForm()

    if form.validate_on_submit():
        file = request.files.get('file')
        tab = Tab(file.filename)
        if form.title.data:
            tab.title = form.title.data

        for seq in SeqLoader.parse(TextIOWrapper(file)):
            tab.sequences[seq.id] = seq.__dict__

        session[tab.id] = json.dumps(tab.__dict__)
        return redirect(url_for('show_tab', id=tab.id))

    return redirect(url_for('index', navitems=__get_nav_items(), newTabForm=form))


@app.route('/tab/<id>', methods=['GET'])
def show_tab(id):
    data = session.get(id, None)
    if data is not None:
        return render_template('tab.html', navitems=__get_nav_items(), tab=json.loads(data), newTabForm=NewTabForm())
    else:
        return redirect(url_for('index'))


@app.route('/tab/<id>/delete', methods=['GET'])
def delete_tab(id):
    session.pop(id)
    return redirect(url_for('index'))


@app.route('/clear', methods=['GET'])
def clear_session():
    session.clear()
    return redirect(url_for('index'))


def __get_nav_items():
    navitems = []

    #listOfKeys = [{key: value['title']} for (key, value) in session.items() if key.startswith('tab_')]
    #print(listOfKeys)

    # TODO: improve to O(1)
    for key in session.keys():
        if key.startswith('tab_'):
            tab = json.loads(session.get(key))
            navitems.append({'id': tab['id'], 'title': tab['title']})

    return navitems
