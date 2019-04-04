
# import datetime
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

"""

A module containing some commonly used plotting
functions which tries to avoid constant repetitions
of function definitions and funciton calls.

Support for the addition of metadata is added as well.


Module's attributes:

fontsize: sets the default fontsize for the
          project.

plots_root = ''
The root folder for storing graphs.

Module's methods:

prepare_ax(ax, legend=True, fontsize=fontsize, grid=True,
               whichGrid='major', ncol=1)

Properly formats an axes object.

Module's classes:

plotter()




"""


fontsize = [17, 20, 24]

plots_root = '../Graphs/'


def prepare_ax(ax, legend=True, fontsize=fontsize, grid=True,
               whichGrid='major', ncol=1):
    """
    Prepare axes for plotting

    Parameters
    ----------

    ax - axes object
    plot_mbl_ergodic - whether to plot MBL and ergodic
                                   horizontal lines for orientation
    legend - whether to include legend
    fontsize - which fontsize to use
    grid - whether to show grid or not
    ncol - number of columns in the legend

    """

    ax.tick_params(axis='x', labelsize=fontsize[1], pad=5, direction='out')
    if legend:
        ax.legend(loc='best', prop={
                  'size': fontsize[0]}, fontsize=fontsize[0],
                  framealpha=0.5, ncol=ncol,
                  handlelength=1.,
                  columnspacing=0.6,
                  handletextpad=0.5,
                  frameon=False)

    ax.tick_params(axis='x', labelsize=fontsize[1])
    ax.tick_params(axis='y', labelsize=fontsize[1])
    if grid:
        ax.grid(which=whichGrid)


class Plotter(object):

    def __init__(self, nrows, ncols, figsize=(14, 7), metadata={},
                 sharex=True, sharey=True):
        super(Plotter, self).__init__()

        self.figsize = figsize
        self.create_plot(nrows, ncols, sharex, sharey)
        self.metadata = {}  # an empty dict for the metadata

    # methods

    def create_plot(self, nrows, ncols, sharex=True, sharey=False):
        """
        Creates a figure and axes. Makes sure that the axes object
        can be flattened even if there is only a single subplot.

        """
        plt.close()
        self.fig, axes = plt.subplots(
            nrows, ncols, figsize=self.figsize, sharex=sharex, sharey=sharey)
        self.axes = np.array(axes)

    # prepare axes
    def prepare_plot(self, savename='', plot_type='', desc='', top=0.89,
                     subfolder='', save=False, save_metadata=True,
                     show=True, block=True):
        """
        Prepare plotting layout for plotting and for saving the
        figures - creates
        the savename string and such.

        A note about the storage path for the plots:

        graphs_folder = '../Graphs/plot_type/desc/subfolder'

        Parameters
        ----------
        savename: string
                  Filename of the saved plot.
        plot_type: which quantity are we calculating and plotting
                  (SFF, level ratios, etc.). Defaults to an empty
                  string.
        desc:  job type description which usually tells us where the
               initial numerical data were stored. Defaults
               to an empty string.
        subfolder: string
                   specifies a possible subfolder structure for
                   storing files. Defaults to an empty string.
        top: float
             a parameter in subplots_adjust function specifying
             where the top of the plot should be.
        save: boolean
              whether to save the plot or not. Defaults to False
              to avoid unintentional overwriting of data.
        save_metadata: boolean
                       whether to add metadata to a pdf file
        show - boolean
               If True, a plot is shown after it has been created.
               Defaults to True.

        """
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=top)

        if save:  # save graphs

            graphs_folder = plots_root + plot_type + '/' + \
                desc + '/' + subfolder

            if not os.path.isdir(graphs_folder):
                os.makedirs(graphs_folder)

            savename = graphs_folder + '/' + savename

            pdffig = PdfPages(savename)

            self.fig.savefig(pdffig, format='pdf')

            if save_metadata:
                metadata = pdffig.infodict()

                metadata.update(self.metadata)
                print('prepare_plot info: plot metadata: {}'.format(metadata))

            pdffig.close()

        if show:

            plt.show(block=block)
