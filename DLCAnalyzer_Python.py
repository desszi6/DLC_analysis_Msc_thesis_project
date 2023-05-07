import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

def IsTrackingData(t):
    if t.object_type is not None:
        if t.object_type == "TrackingData":
            return True
    return False


def PlotPointData(t, points=None, from_=None, to=None, unit="frame", type_=None):
    if not IsTrackingData(t):
        raise ValueError("Object is not of type TrackingData")

    if points is None and type_ is None:
        points = list(t.data.keys())

    if unit == "second":
        if from_ is not None:
            from_ = t.frames[np.where(t.seconds >= from_)[0][0]]
        if to is not None:
            to = t.frames[np.where(t.seconds >= to)[0][0]]

    if from_ is None:
        from_ = min(t.frames)
    if to is None:
        to = max(t.frames)

    if type_ is not None:
        points = t.point_info[t.point_info["PointType"] == type_]["PointName"]

    range_ = np.arange(from_, to+1)

    p = None
    dim = math.ceil(math.sqrt(len(points)))
    nplot = 0

    for i in points:
        plot_data = t.data[i][t.data[i]["frame"].isin(range_)]
        plot_title = i
        x_label = "x / {}".format(t.distance_units)
        y_label = "y / {}".format(t.distance_units)
        plot = plot_data.plot(x="x", y="y", color="likelihood")
        plot.set_title(plot_title)
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        plot.set_aspect("equal")
        plot.figure.set_size_inches(6, 6)
        plot.figure.tight_layout()
        plot_figure = plot.get_figure()

        plot_axes = plot_figure.get_axes()[0]
        plot_position = plot_axes.get_position()
        plot_width = plot_position.width
        plot_height = plot_position.height

        plot_figure.clf()

        if p is None:
            p = plot_axes.figure.add_subplot(111)
        else:
            p = plot_figure.add_subplot(111)

        p.axis("off")
        p.set_position([nplot % dim / dim, (dim - 1) / dim - math.floor(nplot / dim) / dim, plot_width, plot_height])
        p.imshow(plot_axes.get_figure().canvas.buffer_rgba(), interpolation="nearest", aspect="auto")
        nplot += 1

    return p

def RunPipeline(files, path, FUN):
    out = {}
    for j in files:
        out[j] = FUN(path+j)
    return out
