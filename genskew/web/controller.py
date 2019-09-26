import json
from io import TextIOWrapper, BytesIO
from flask import render_template, redirect, url_for, session, request, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from genskew.web import app
from genskew.web.model import Tab, Settings, PlotData
from genskew.web.forms import NewTabForm
from genskew.input import SeqLoader
from genskew import utils


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

        seqlen = 0
        for seq in SeqLoader.parse(TextIOWrapper(file)):
            #tab.sequences[seq.id] = seq.__dict__
            seqlen += seq.len
            tab.sequences.append(seq.__dict__)

        tab.settings = Settings(seqlen).__dict__
        session[tab.id] = json.dumps(tab.__dict__)
        return redirect(url_for('show_tab', id=tab.id))

    return redirect(url_for('index', navitems=__get_nav_items(), newTabForm=form))


# TODO: code refactoring
@app.route('/tab/<id>', methods=['GET', 'POST'])
def show_tab(id):
    data = session.get(id, None)
    if data is None:
        # TODO: show error (session expired?)
        return redirect(url_for('index'))

    tab = json.loads(data)

    if request.method == 'POST':
        for seq in tab['sequences']:
            if request.form.get(seq['id']):
                seq['enabled'] = True
            else:
                seq['enabled'] = False

        tab['settings']['n1'] = request.form.get('n1')
        tab['settings']['n2'] = request.form.get('n2')

        if request.form.get('windowsize'):
            tab['settings']['windowsize'] = int(request.form.get('windowsize'))

        if request.form.get('stepsize'):
            tab['settings']['stepsize'] = int(request.form.get('stepsize'))

    seq_recs = [seq['data'] for seq in tab['sequences']]
    pseudo_contig = ''.join(seq_recs)

    plot = PlotData()
    for i in range(0, len(seq_recs[1:])):
        if i == 0:
            plot.contig_separators.append(len(seq_recs[i]) + 1)
        else:
            plot.contig_separators.append(plot.contig_separators[i - 1] + len(seq_recs[i]) + 1)

    plot.seq_position, plot.skew_normal, plot.skew_cumulative = \
        utils.compute_skew_data(pseudo_contig, tab['settings']['n1'], tab['settings']['n2'],
                          tab['settings']['windowsize'], tab['settings']['stepsize'])

    tab['plot'] = plot.__dict__
    session[id] = json.dumps(tab)
    return render_template('tab.html', navitems=__get_nav_items(), tab=tab, newTabForm=NewTabForm(), plot=json.dumps(plot.get_plot_data()))


@app.route('/tab/<id>/plot.png', methods=['GET'])
def plot_data(id):
    data = session.get(id, None)
    if data is None:
        # TODO: show error (session expired?)
        return redirect(url_for('index'))

    tab = json.loads(data)

    fig = Figure()
    utils.draw_figure(fig, tab['plot']['seq_position'], tab['plot']['skew_normal'], tab['plot']['skew_cumulative'],
                      tab['plot']['contig_separators'])

    out = BytesIO()
    FigureCanvasAgg(fig).print_png(out)

    return Response(out.getvalue(), mimetype='image/png')


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
