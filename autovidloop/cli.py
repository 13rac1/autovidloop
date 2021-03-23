#! /usr/bin/env python3

# Brute force search to find the top three video frames least different from the
# first frame in a video.

import imageio
import numpy
import argparse

def main():

  parser = argparse.ArgumentParser(description='Attempt to automatically trim a video to create a loop by finding the frame least different from the first frame.')
  parser.add_argument('input', metavar='FILENAME', type=str,
                      help='a video file readable by FFMPEG')
  parser.add_argument('--output', metavar='FILENAME', type=str,
                      help='an output filename (default is "loop.mp4")')
  parser.add_argument('--start',
                      default=1, metavar='N', type=int,
                      help='frame to start processing (default: 1)')
  parser.add_argument('--skip',
                      default=30, metavar='N', type=int,
                      help='number of frames to skip after the first for diff calculations (default: 30)')

  args = parser.parse_args()
  if not args.output:
    args.output = "loop.mp4"

  print("AutoVideoLoop\n")

  print("input: {}".format(args.input))

  frame_start = args.start
  print("start frame: {}".format(frame_start))

  # How many frames to skip at the start, generally the first few will be highly
  # similar due to lossy compression.
  frame_skip = args.skip + args.start
  print("skip frames (start + skip): {}".format(frame_skip))

  reader = imageio.get_reader(args.input)

  # Array of set(frame number, diff)
  frames = []

  current_frame = 0

  for im in reader:
    current_frame += 1

    # Store the first frame
    if current_frame == frame_start:
      first = im
      #print("frame: 1")
      continue

    # Skip the requested number of frames
    if current_frame < frame_skip:
      #print("frame: {} (skipped)".format(current_frame))
      continue

    # Subtract the current frame array from the first frame and sum the result
    # This is a simple way to find the "least" different frames.
    diff = numpy.sum(first-im)
    frames.append((current_frame, diff))
    print("frame: {} diff: {}".format(current_frame, diff))

  sorted_frames = sorted(frames, key=lambda frame: frame[1])

  print('\ntop three least different frames')
  for frame in sorted_frames[0:3]:
    print("frame: {} diff: {}".format(frame[0], frame[1]))

  # Assuming the first frame is best.
  least_diff_frame_number = sorted_frames[0][0]

  fps = reader.get_meta_data()['fps']

  current_frame = 0

  print("\noutput: {}".format(args.output))
  writer = imageio.get_writer(args.output, fps=fps)
  for im in reader:
    current_frame += 1
    # Skip the requested number of frames
    if current_frame < frame_skip:
      #print("frame: {} (skipped low)".format(current_frame))
      continue

    if current_frame >= least_diff_frame_number:
      #print("frame: {} (skipped high)".format(current_frame))
      continue

    # Save up to, but not including the least different frame.
    writer.append_data(im)
    # Warning: All frames must be read to avoid: Fatal Python error: could not
    # acquire lock for <_io.BufferedReader name=20> at interpreter shutdown,
    # possibly due to daemon threads

  writer.close()
  print("done")

if __name__ == "__main__":
    # execute only if run as a script
    main()
