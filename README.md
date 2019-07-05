# Auto Video Looper

Attempt to automatically trim a video to create a loop by finding the video
frame least different from the first frame. Uses bruteforce processing and can
take significant processing time on large source files.

## Notes

```bash
# Trim a video with ffmpeg
ffmpeg -i input.mp4 -vf select="between(n\,0\,200),setpts=PTS-STARTPTS" \
-c:v libx264 -strict -2 -r 30 -pix_fmt yuv420p output.mp4
```
