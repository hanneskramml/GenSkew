import jsonpickle
from io import TextIOWrapper, BytesIO
from flask import render_template, redirect, url_for, session, request, Response
from Bio import SeqIO, SeqRecord
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from genskew.web import app
from genskew.web.model import SeqFile, SeqRec, ContigPlot
from genskew import utils


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', nav=__get_nav_tabs())


@app.route('/new', methods=['POST'])
def new_tab():

    file = request.files.get('file')
    tab = SeqFile(file.filename)
    if request.form.get('title'):
        tab.title = request.form.get('title')

    SeqRecord.SeqRecord.__new__ = staticmethod(SeqRec.__new__)
    tab.seqs = [seq for seq in SeqIO.parse(TextIOWrapper(file), 'fasta')]

    # TODO: proper error handling
    if len(tab.seqs) == 0:
        return redirect(url_for('index'))

    tab.plot = ContigPlot(tab.seqs)
    pseudo_contig = tab.plot.get_pseudo_contig()

    tab.plot.gc_content = round(utils.compute_gc_content(pseudo_contig), 1)
    tab.plot.x_position, tab.plot.y_skew_normal, tab.plot.y_skew_cumulative = \
        utils.compute_skew_data(pseudo_contig, tab.plot.settings.n1, tab.plot.settings.n2,
                                tab.plot.settings.windowsize, tab.plot.settings.stepsize)

    session[tab.id] = jsonpickle.encode(tab)
    return redirect(url_for('show_tab', id=tab.id))


# TODO: code refactoring
@app.route('/tab/<id>', methods=['GET', 'POST'])
def show_tab(id):
    data = session.get(id, None)
    if data is None:
        # TODO: show error (session expired?)
        return redirect(url_for('index'))

    tab = jsonpickle.decode(data)

    if request.method == 'POST':

        tab.plot.seqs = [seq for seq in tab.seqs if seq.enabled]

        tab.plot.settings.n1 = request.form.get('n1')
        tab.plot.settings.n2 = request.form.get('n2')

        if request.form.get('windowsize'):
            tab.plot.settings.windowsize = int(request.form.get('windowsize'))
        else:
            tab.plot.settings.set_default_windowsize(tab.plot.get_total_len())

        if request.form.get('stepsize'):
            tab.plot.settings.stepsize = int(request.form.get('stepsize'))
        else:
            tab.plot.settings.set_default_stepsize(tab.plot.get_total_len())

        pseudo_contig = tab.plot.get_pseudo_contig()
        tab.plot.gc_content = round(utils.compute_gc_content(pseudo_contig), 1)
        tab.plot.x_position, tab.plot.y_skew_normal, tab.plot.y_skew_cumulative = \
            utils.compute_skew_data(pseudo_contig, tab.plot.settings.n1, tab.plot.settings.n2,
                                    tab.plot.settings.windowsize, tab.plot.settings.stepsize)

        session[tab.id] = jsonpickle.encode(tab)

    return render_template('tab.html', nav=__get_nav_tabs(), tab=tab)


@app.route('/tab/<id>/plot', methods=['GET'])
def download_plot(id):
    data = session.get(id, None)
    if data is None:
        # TODO: show error (session expired?)
        return redirect(url_for('index'))

    tab = jsonpickle.decode(data)

    fig = Figure(dpi=150)
    utils.draw_figure(
        fig, tab.plot.x_position, tab.plot.y_skew_normal, tab.plot.y_skew_cumulative, tab.plot.get_start_pos()[1:])

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


def __get_nav_tabs():
    navitems = []

    for key in session.keys():
        if key.startswith('file_'):
            tab = jsonpickle.decode(session.get(key))
            navitems.append({'id': tab.id, 'title': tab.title})

    return navitems
