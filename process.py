import sys
import argparse
import subprocess
from time import time
from os.path import exists, split, splitext
from os import mkdir, remove, environ
from urllib.request import urlretrieve
from zipfile import ZipFile

FFMPEG_URL = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
PREREQUISITES_PATH = environ['TEMP'] + '\\prerequisites'
FFMPEG_FILE_NAME = environ['TEMP'] + '\\prerequisites\\ffmpeg-release-essentials.zip'
FFMPEG_FOLDER_NAME = environ['TEMP'] + '\\prerequisites\\ffmpeg-4.3.1-2020-11-19-essentials_build\\'
FFMPEG_EXE = environ['TEMP'] + '\\prerequisites\\ffmpeg-4.3.1-2020-11-19-essentials_build\\bin\\ffmpeg.exe'
FFPROBE_EXE = environ['TEMP'] + '\\prerequisites\\ffmpeg-4.3.1-2020-11-19-essentials_build\\bin\\ffprobe.exe'

parser = argparse.ArgumentParser()
parser.add_argument(
                    'videofile',
                    help='path to the video file. \
                    ')
parser.add_argument(
                    '-H', '--half',
                    action='store_true',
                    help='whether to half the framerate or not. \
                    ')
parser.add_argument(
                    '-j', '--jpeg',
                    action='store_true',
                    help='whether to output as .jpeg \
                    ')
parser.add_argument(
                    '-m', '--mode',
                    metavar='1/2',
                    type=int,
                    help='projection mode (YZ/XZ)  \
                    ')
args = parser.parse_args()


def saferemove(path: str) -> None:

    if exists(path):
        remove(path)
    else:
        pass


def install_dependencies() -> None:

    def reporthook(blocknum: int, blocksize: int, totalsize: int) -> None:
        bytesread = blocknum * blocksize
        if totalsize > 0:
            percent = bytesread * 1e2 / totalsize
            s = "\r%5.1f%% (%*d / %d bytes)" % (percent, len(str(totalsize)), bytesread, totalsize)
            sys.stderr.write(s)
            if bytesread >= totalsize:
                sys.stderr.write("\n")
        else:
            sys.stderr.write("read %d\n" % (bytesread,))

    if not exists(PREREQUISITES_PATH):
        print('Prerequisites folder not found. Creating the folder...\n')
        mkdir(PREREQUISITES_PATH)
        print('Done!\n')
    else:
        print('Prerequisites folder already exists. Proceeding...\n')

    if not exists(FFMPEG_FILE_NAME):
        print("Downloading FFMPEG from '%s'" % FFMPEG_URL)
        urlretrieve(FFMPEG_URL, FFMPEG_FILE_NAME, reporthook)

        print("Download finished\n")
    else:
        print('FFMPEG already downloaded. Proceeding...\n')

    if not exists(FFMPEG_FOLDER_NAME):
        print("Extracting FFMPEG\n")

        zip = ZipFile(FFMPEG_FILE_NAME, 'r')
        zip.extractall(PREREQUISITES_PATH)
        zip.close()
    else:
        print("FFMPEG already extracted. Proceeding...\n")


def process(path: str, half: bool, jpeg: bool, mode: int) -> None:

    t0 = time()

    duration = float(subprocess.check_output(f'"{FFPROBE_EXE}" \
                                        -hide_banner \
                                        -v error \
                                        -show_entries format=duration \
                                        -of default=noprint_wrappers=1:nokey=1 "{path}" \
                                        '))

    framerate = float(eval(subprocess.check_output(f'"{FFPROBE_EXE}" \
                                        -hide_banner \
                                        -v error \
                                        -select_streams v:0 \
                                        -show_entries stream=avg_frame_rate \
                                        -of csv=s=x:p=0 "{path}" \
                                        ').strip()))

    if half:
        framerate = framerate / 2

    img_height = int(subprocess.check_output(f'"{FFPROBE_EXE}" \
                                        -hide_banner \
                                        -v error \
                                        -select_streams v:0 \
                                        -show_entries stream=height \
                                        -of csv=s=x:p=0 "{path}" \
                                        '))

    qscale = ''

    output = splitext(split(path)[1])[0]

    if jpeg:
        ext = '.jpeg'
        qscale = '-qscale:v 2'
    else:
        ext = '.png'

    # Get the range of frames.
    ilen = round(duration * framerate)

    if mode == 0:
        crop = ':ih:iw/2:0'
        tile = f'{ilen}x1'
        stackmode = 'vstack'
        rotate = ''

    if mode == 1:
        crop = 'iw:1:0:ih/2'
        tile = f'1x{ilen}'
        stackmode = 'hstack'
        rotate = '"transpose=1"'

    print(duration, framerate, ilen)

    # Create the .png file.
    # ffmpeg -i out_%04d.jpg -filter_complex "tile=300x1, format=yuv444p|yuva444p10be|rgb24" output.png
    # -filter_complex "fps=15,format=yuv444p|yuva444p10be|rgb24,crop=1:ih:iw/2:0,tile=5000x1" output.png
    # crop=XSIZE:YSIZE:XPOS:YPOS
    # -loglevel level+debug
    # crop=1:{height}:{width}/2:0
    subprocess.run(f'"{FFMPEG_EXE}" \
        -i "{path}" \
        -hide_banner \
        -filter_complex \
        "fps={framerate}, \
        format=yuv444p|yuva444p10be|rgb24, \
        crop={crop}, \
        tile={tile}" \
        {qscale} \
        "{output}{ext}" \
        ')

    # Extract audio from video file, mux to mono and save as .wav format.
    # ffmpeg -i '.\mercury - the timeless _ Demoscene-Jz3tMVrtOso.mkv' -ac 1 mono.wav
    subprocess.run(f'"{FFMPEG_EXE}" \
        -i "{path}" \
        -hide_banner \
        -ac 1 \
        "{output}_mono.wav" \
        ')

    # Generate a spectrogram from the mono audio file.
    subprocess.run(f'"{FFMPEG_EXE}" \
        -i "{output}_mono.wav" \
        -hide_banner \
        -lavfi \
        showspectrumpic=legend=disabled:s={ilen}x{img_height} \
        wave.png \
        ')

    if mode == 1:
        subprocess.run(f'"{FFMPEG_EXE}" \
            -i wave.png \
            -hide_banner \
            -vf {rotate} \
            wave1.png \
            ')

        # Put the spectrogram .png and video .png together.
        subprocess.run(f'"{FFMPEG_EXE}" \
            -i "{output}{ext}" \
            -i "wave1.png" \
            -hide_banner \
            -filter_complex {stackmode}=inputs=2 \
            "{output}_assembled{ext}" \
            ')

    else:
        # Put the spectrogram .png and video .png together.
        subprocess.run(f'"{FFMPEG_EXE}" \
            -i "{output}{ext}" \
            -i "wave.png" \
            -hide_banner \
            -filter_complex {stackmode}=inputs=2 \
            "{output}_assembled{ext}" \
            ')

    # Create a 25% Y scale version of the video .png file.
    subprocess.run(f'"{FFMPEG_EXE}" \
        -i "{output}.png" \
        -hide_banner \
        -vf scale=iw:ih/4 \
        "{output}_yscale.png" \
        ')

    # Create a 25% Y scale version of the assembled .png file.
    # subprocess.run(f'"{FFMPEG_EXE}" \
    #     -i "{output}_assembled.png" \
    #     -hide_banner \
    #     -vf scale=iw:ih/4 \
    #     "{output}_assembled_yscale.png" \
    #     ')

    # Cleanup.
    saferemove(f"{output}_mono.wav")
    saferemove("wave.png")
    if mode == 1:
        saferemove("wave1.png")

    t1 = time()

    print(f'Finished processing in {t1-t0}s')


def main() -> None:

    install_dependencies()

    if args.videofile:
        process(args.videofile, args.half, args.jpeg, args.mode)


if __name__ == '__main__':
    main()
