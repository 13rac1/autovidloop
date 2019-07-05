# Auto Video Looper

Attempt to automatically trim a video to create a loop by finding the video
frame least different from the first frame. The method is bruteforce, so can
take significant processing time on large source files.

Works well enough for my needs. YMMV. ¯\_(ツ)_/¯

## Install

```bash
pip3 install https://github.com/13rac1/autovidloop/archive/master.zip
# TODO: Upload to pip?
```

## Usage

```bash
$ autovidloop -h
usage: autovidloop [-h] [--output FILENAME] [--skip N] FILENAME

Attempt to automatically trim a video to create a loop by finding the frame
least different from the first frame.

positional arguments:
  FILENAME           a video file readable by FFMPEG

optional arguments:
  -h, --help         show this help message and exit
  --output FILENAME  an output filename (default is "loop.mp4")
  --skip N           number of frames to skip after the first for diff
                     calculations (default: 30)
```

## Notes

```bash
# Trim a video with ffmpeg
ffmpeg -i input.mp4 -vf select="between(n\,0\,200),setpts=PTS-STARTPTS" \
-c:v libx264 -strict -2 -r 30 -pix_fmt yuv420p output.mp4
```
