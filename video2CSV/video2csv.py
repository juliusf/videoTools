#!/usr/bin/env python

__author__ = 'jules'

import argparse
import os.path
import subprocess
import sys
import math

def main():
    arg_parser = argparse.ArgumentParser(description='converts a video file to a series of differently encoded video sequences with different bitrate and then converts the metadata to CSV')
    arg_parser.add_argument("--movieFile", help="the movie file to convert with ffmpeg")
    arg_parser.add_argument("--R_min", help="minimum data rate of csv stream in kBit/s")
    arg_parser.add_argument("--R_max", help="maximum data rate of csv stream in kBit/s")
    arg_parser.add_argument("--stepLength", help="length of steps between R_min and R_max in kBit/s", default=200)
    args = arg_parser.parse_args()

    if args.movieFile is None:
        print("No movie File given")
    if not os.path.isfile(args.movieFile):
        print("No movieFile given or file does not exist")
        sys.exit(127)

    if args.R_min is None or args.R_max is None:
        print("R_min or R_max not given")
        sys.exit(127)

    r_min = int(args.R_min)
    r_max = int(args.R_max)

    step_length = int(args.stepLength)

    #number_of_streams = math.ceil((r_max - r_min) / step_length)

    for bitrate in range(r_min, r_max, step_length):
        out_file = '/tmp/%sk_%s' % (bitrate, args.movieFile)
        convert_with_ffmpeg(args.movieFile, bitrate, out_file)
        csv_file = '%s.csv' % (out_file)
        create_csv_from_video(out_file, csv_file)

def convert_with_ffmpeg(file, bitrate, out_file):
    tolerance = int(int(bitrate) * 0.05)
    if os.path.isfile(out_file):
        print("file %s exists. skipping" % (out_file))
    else:
        print("converting %s as %s kBit/s" % (file, bitrate))
        print("ffmpeg -i "+ file + " -b:v "+ str(bitrate) + "k" + " -minrate %sk" % str(int(bitrate) - tolerance) + " -maxrate %sk" % str(int(bitrate) + tolerance) +" -bufsize " + str(bitrate) +"k "+ out_file)
        #subprocess.call(["ffmpeg", "-i", file, "-b:v", str(bitrate) +"k", "-minrate %sk" % str(int(bitrate) - tolerance), "-maxrate %sk" % str(int(bitrate) + tolerance),"-bufsize", str(bitrate) +"k ", out_file])
        subprocess.call("ffmpeg -i "+ file + " -b:v "+ str(bitrate) + "k" + " -minrate %sk" % str(int(bitrate) - tolerance) + " -maxrate %sk" % str(int(bitrate) + tolerance) +" -bufsize " + str(bitrate) +"k "+ out_file, shell=True)
def create_csv_from_video(video_file, csv_file):
        print("creating CSV for file: %s") % (video_file)
        subprocess.call(["./extract_video_info %s > %s" % (video_file, csv_file)], shell=True)

if __name__ == "__main__":
    main()