import matplotlib as mpl
import matplotlib.pyplot as plt

default_options = {
        'font_size': 16, # pt
        'plot_size': (4.8, 4.8 * 3/4),
        'line_width': 3.25,
        'xtick_size': 13.5,
        'ytick_size': 13.5,
        }

__dc_options = {}

def init_plots_for_paper(options=default_options):
    global __dc_options
    __dc_options.update(options)
    mpl.rcParams.update({'font.size': options['font_size'], 'figure.figsize': options['plot_size'], 'lines.linewidth': options['line_width'], 'xtick.labelsize': options['xtick_size'], 'ytick.labelsize': options['ytick_size'], })
    mpl.interactive(False)

def init_plot():
    global __dc_options
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    return fig, ax

