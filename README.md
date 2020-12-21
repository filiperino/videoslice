# videoslice

A single .py version of http://www.lofibucket.com/articles/video_slicing.html by Pekka Väänänen.

Excerpt from the widerscreen.fi article: 

"An orthogonal projection gives an interesting perspective of the demo as you can clearly see changes of settings and transformations in relation to time and space. The orthogonal XZ-view uses one horizontal (X) slice from the centre of each image and adds every line underneath the last one in a chronological order along the Y-axis (Z). The YZ-view uses vertical lines (Y) from the source images to display the time (Z) along the X-axis."

More on the topic: 

http://widerscreen.fi/numerot/2014-1-2/demo-age-new-views/ 

archive.org mirror: https://web.archive.org/web/20201021052343/http://widerscreen.fi/numerot/2014-1-2/demo-age-new-views/

Requirements:
- Python 3.5 or later (https://www.python.org/downloads/)
- Windows 7 or later

Usage:
1. Place process.py into any directory
2. Run process.py in the terminal by using: 
    ```
    usage: process.py [-h] [-H] [-j] [-m 1/2] videofile        

    positional arguments:
    videofile           path to the video file.

    optional arguments:
    -h, --help          show this help message and exit      
    -H, --half          whether to half the framerate or not.
    -j, --jpeg          whether to output as .jpeg (outputs a .png by default)
    -m 1/2, --mode 1/2  projection mode (YZ/XZ)
    ```

    NOTE: On first launch download and extraction of FFmpeg happens, which depending on your internet download speed and proximity to mirror host, takes ~15 minutes. The projection process is generally around 1.2x faster than real-time playback, but that can go up drastically .

To-do:
- Variable slice width (X)
- Add a XZ projection mode (V)
- Linux support (X)

Known Issues:
- N/A
