import json
from io import TextIOWrapper, BytesIO
from flask import render_template, redirect, url_for, session, request, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from genskew.web import app
from genskew.web.model import Tab, Settings, PlotData
from genskew.input import SeqLoader
from genskew import utils


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', navitems=__get_nav_items())


@app.route('/new', methods=['POST'])
def new_tab():

    file = request.files.get('file')
    tab = Tab(file.filename)
    if request.form.get('title'):
        tab.title = request.form.get('title')

    seqlen = 0
    for seq in SeqLoader.parse(TextIOWrapper(file)):
        seqlen += seq.len
        tab.sequences.append(seq.__dict__)

    # TODO: proper error handling
    if seqlen == 0:
        return redirect(url_for('index'))

    tab.settings = Settings(seqlen).__dict__
    session[tab.id] = json.dumps(tab.__dict__)

    return redirect(url_for('show_tab', id=tab.id))


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
            plot.contig_start_pos.append(len(seq_recs[i]) + 1)
        else:
            plot.contig_start_pos.append(plot.contig_start_pos[i - 1] + len(seq_recs[i]) + 1)

    plot.total_len = len(pseudo_contig)
    plot.gc_content = round(utils.compute_gc_content(pseudo_contig), 1)
    plot.x_seq_position, plot.y_skew_normal, plot.y_skew_cumulative = \
        utils.compute_skew_data(pseudo_contig, tab['settings']['n1'], tab['settings']['n2'],
                          tab['settings']['windowsize'], tab['settings']['stepsize'])

    tab['plot'] = plot.__dict__
    session[id] = json.dumps(tab)
    return render_template('tab.html', navitems=__get_nav_items(), tab=tab, plot=json.dumps(plot.get_plot_data()), origin=plot.get_pos_for_origin())


@app.route('/tab/<id>/plot', methods=['GET'])
def download_plot(id):
    data = session.get(id, None)
    if data is None:
        # TODO: show error (session expired?)
        return redirect(url_for('index'))

    tab = json.loads(data)

    fig = Figure(dpi=150)
    utils.draw_figure(fig, tab['plot']['x_seq_position'], tab['plot']['y_skew_normal'], tab['plot']['y_skew_cumulative'],
                      tab['plot']['contig_start_pos'])

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
