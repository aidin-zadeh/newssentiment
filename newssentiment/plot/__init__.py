
import numpy as np
import matplotlib.pyplot as plt


class Scatter(object):

    def __init__(self,
                 marker: str = "o",
                 markersize: int = 6,
                 markeredgecolor: str = "black",
                 markeredgewidth: float = 1,
                 markerfacecolor: str = "black",
                 fillstyle: str = "full",
                 linestyle: str = "",
                 alpha: float = .7,
                 xlabel: str = "",
                 ylabel: str = "",
                 label: str = "",
                 title: str = "",
                 xlim: object = None,
                 ylim: object = None,
                 titlefontsize: int = 14,
                 labelfontsize: int = 13,
                 xtickfontsize: int = 12,
                 ytickfontsize: int = 12,
                 figsize: tuple = (7, 5),
                 legend: bool = True,
                 grid: bool = True,
                 ax: object = None, ) -> object:

        """
        :param marker:
        :param markersize:
        :param markeredgecolor:
        :param markeredgewidth:
        :param markerfacecolor:
        :param fillstyle:
        :param linestyle:
        :param alpha:
        :param xlabel:
        :param ylabel:
        :param label:
        :param title:
        :param xlim:
        :param ylim:
        :param titlefontsize:
        :param labelfontsize:
        :param xtickfontsize:
        :param ytickfontsize:
        :param figsize:
        :param legend:
        :param grid:
        :param ax:
        """
        super(Scatter, self).__init__()

        self.marker = marker
        self.markersize = markersize
        self.markeredgecolor = markeredgecolor
        self.markeredgewidth = markeredgewidth
        self.markerfacecolor = markerfacecolor
        self.fillstyle = fillstyle
        self.linestyle = linestyle
        self.alpha = alpha
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.label = label
        self.title = title
        self.xlim = xlim
        self.ylim = ylim
        self.titlefontsize = titlefontsize
        self.labelfontsize = labelfontsize
        self.xtickfontsize = xtickfontsize
        self.ytickfontsize = ytickfontsize
        self.figsize = figsize
        self.legend = legend
        self.grid = grid

        # create figure/axis handler
        if ax is None:
            self.fig = plt.figure(figsize=self.figsize)
            self.ax = self.fig.subplots(1, 1)

    def __call__(self, x: object, y: object, *args, **kwargs):

        # scatter plot
        self.ax.plot(
            x, y,
            marker=self.marker,
            markersize=self.markersize,
            markeredgecolor=self.markeredgecolor,
            markeredgewidth=self.markeredgewidth,
            markerfacecolor=self.markerfacecolor,
            fillstyle=self.fillstyle,
            linestyle=self.linestyle,
            alpha=self.alpha,
            label=self.label,
        )
        # set title
        _ = self.ax.set_title(
            self.title,
            fontsize=self.titlefontsize,
            fontweight="bold"
        )
        # set axis labels
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.xaxis.label.set_size(self.labelfontsize)
        self.ax.yaxis.label.set_size(self.labelfontsize)

        # set axis ticks
        [tick.label.set_fontsize(self.xtickfontsize) for tick in self.ax.xaxis.get_major_ticks()]
        [tick.label.set_fontsize(self.ytickfontsize) for tick in self.ax.yaxis.get_major_ticks()]

        # set axis range limits
        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)

        # set legend
        if self.legend and (self.label is not ""):
            self.ax.legend()

        # set grid
        if self.grid:
            self.ax.grid(
                True,
                color="grey",
                linestyle=":",
                linewidth=1.5,
                alpha=0.5)

        # set tight layout
        plt.tight_layout()


class Bar(object):

    def __init__(self,
                 color="blue",
                 edgecolor="black",
                 linewidth=2,
                 width=1,
                 alpha=0.5,
                 align="center",
                 xlabel="",
                 ylabel="",
                 title="",
                 titlefontsize=12,
                 labelfontsize=10,
                 grid=True,
                 gridcolor="grey",
                 gridlinestyle = ":",
                 gridlineweight=1.5,
                 gridalpha=0.5,
                 ax=None,
                 figsize=(12, 8),
                 label=False):

        self.color = color
        self.edgecolor = edgecolor
        self.linewidth = linewidth
        self.width = width
        self.align = align
        self.alpha = alpha
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.titlefontsize = titlefontsize
        self.labelfontsize = labelfontsize
        self.grid = grid
        self.gridlinestyle = gridlinestyle
        self.gridlineweith = gridlineweight
        self.gridcolor = gridcolor
        self.gridalpha = gridalpha
        self.figsize = figsize
        self.label = label

        # create figure/axis handler
        if ax is None:
            self.fig = plt.figure(figsize=self.figsize)
            self.ax = self.fig.subplots(1, 1)

    def __call__(self, x, y, colors=None):

        if colors is not None:
            self.colors = colors

        self.ax.bar(
            x=x,
            height=y,
            color=self.colors,
            edgecolor=self.edgecolor,
            linewidth=self.linewidth,
            width=self.width,
            align=self.align)

        _ = self.ax.set_title(
                self.title,
                fontsize=self.titlefontsize,
                fontweight="bold")
        self.ax.grid(self.grid,
                     color=self.gridcolor,
                     linestyle=self.gridlinestyle,
                     linewidth=self.gridlineweith,
                     alpha=self.gridalpha)

        self.ax.set_ylabel(self.ylabel)
        self.ax.set_xlabel(self.xlabel)

        self.ax.xaxis.label.set_size(self.labelfontsize)
        self.ax.yaxis.label.set_size(self.labelfontsize)

        if self.label:
            for (xi, yi) in zip(x, y):
                self.ax.text(
                   x=xi, y=yi * 1.2,
                   s="{:2.0f}%".format(yi),
                   color="k",
                   horizontalalignment="center",
                   fontsize=14,
                   fontweight="bold")

            self.ax.set_ylim([min(y)*1.3, max(y)*1.3])
        plt.tight_layout()
