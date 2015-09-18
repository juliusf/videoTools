#!/usr/bin/env python

__author__ = 'jules'

import argparse
import sys
import os
import csv
import Cdf
import Pmf
import numpy as np

import matplotlib.pylab as plt

def main():
    arg_parser = argparse.ArgumentParser(description='extracts statistical information from a given CSV video file created with video2csv')
    arg_parser.add_argument("--csvFile", help="the movie file to convert with ffmpeg")
    args = arg_parser.parse_args()

    if args.csvFile is None:
        print("no CSV file specified!")
    if not os.path.isfile(args.csvFile):
        print("No CSV file given or file does not exist")
        sys.exit(127)

    iframes = []
    pframes = []

    with open(args.csvFile) as csvfile:
        video_reader = csv.reader(csvfile, delimiter=";")
        video_reader.next() #skip first line comment
        for row in video_reader:
            if "I" in row[1]:

                iframes.append(float(row[3]))
            else:

                pframes.append(float(row[3]))

        print("Number of I-frames: %s" % (len(iframes)))
        print("Average I-frame size: %s" % ( np.average(iframes)))
        print("Number of P-frames: %s" % (len(pframes)))
        print("Average P-frame size: %s" % ( np.average(pframes)))

        x1, y1 = list_to_ccdf(iframes)
        x2, y2 = list_to_ccdf(pframes)
        fig =  plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.plot(x1,y1, label="IFrames")
        ax.plot(x2,y2, label="PFrames")
        plt.xscale('log')
        plt.xlabel("coded picture size in bytes")
        plt.ylabel(("P"))
        plt.grid()
        plt.legend()
        plt.show()

def list_to_cdf(list):
    array_hist = Pmf.MakeHistFromList(list)
    array_cdf = Cdf.MakeCdfFromHist(array_hist)
    array_x_axis, array_y_axis = array_cdf.Render()
    return [array_x_axis, array_y_axis]

def list_to_ccdf(list):
    array_x_axis, array_y_axis = list_to_cdf(list)
    return [array_x_axis, cdf_to_ccdf(array_y_axis)]

def cdf_to_ccdf(p):
    ccdf = []
    for x in p:
        ccdf.append(1-x)
    return ccdf
if __name__ == "__main__":
    main()