# videoslice

A single .py version of http://www.lofibucket.com/articles/video_slicing.html by Pekka Väänänen.

More on the topic: 

http://widerscreen.fi/numerot/2014-1-2/demo-age-new-views/ (archive.org mirror: https://web.archive.org/web/20201021052343/http://widerscreen.fi/numerot/2014-1-2/demo-age-new-views/)

Excerpt from the widerscreen.fi article: 

"An orthogonal projection gives an interesting perspective of the demo as you can clearly see changes of settings and transformations in relation to time and space. The orthogonal XZ-view uses one horizontal (X) slice from the centre of each image and adds every line underneath the last one in a chronological order along the Y-axis (Z). The YZ-view uses vertical lines (Y) from the source images to display the time (Z) along the X-axis."

Requirements:
- Python 3.x (https://www.python.org/downloads/)
- Windows 7 or later

Usage:
1. Place process_local_compact.py into any directory
2. Run process.py in the terminal by using: 
```python process.py path_to_video_file```

    NOTE: First Usually the process is around 1.2x faster than real-time playback, so for eg a 10 minute video finished in ~8 minutes.

To-do:
- Variable slice width
- Add a XZ projection mode
- Linux support

Known Issues: