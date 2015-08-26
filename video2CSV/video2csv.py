#!/usr/bin/env python

__author__ = 'jules'

from ffvideo import VideoStream
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

    number_of_streams = math.ceil((r_max - r_min) / step_length)

    for bitrate in range(r_min, r_max, step_length):
        convert_with_ffmpeg(args.movieFile, bitrate)

def convert_with_ffmpeg(file, bitrate):

    out_file = '/tmp/%s_%sk.mov' % (file, bitrate)
    if os.path.isfile(out_file):
        print("file %s exists. skipping" % (out_file))
    else:
        print("converting %s as %s kBit/s" % (file, bitrate))
        subprocess.call(["ffmpeg", "-i", file, "-b:v", str(bitrate) +"k", "-bufsize", str(bitrate) +"k", '/tmp/%s_%sk.mov' % (file, bitrate)])


if __name__ == "__main__":
    main()