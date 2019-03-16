from tkinter import Tk, Text, BOTH, W, N, E, S, messagebox as mbox, filedialog, StringVar, BooleanVar, IntVar
from tkinter.ttk import Frame, Button, Label, Checkbutton
from ffmpy import FFmpeg
from pymediainfo import MediaInfo
from os import listdir
from os.path import isfile, join, dirname, split, splitext
from threading import Thread
import datetime, time

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("Taiwan Number One!")
        self.pack(fill=BOTH, expand=True)

        # video part (left)
        videolbl = Label(self, text="Video list")
        videolbl.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        videobtn = Button(self, text="Add files...", command=self.addvideo)
        videobtn.grid(row=0, column=1, padx=5, pady=5, sticky=E)

        global vlist
        vlist = StringVar()
        videolist = Label(self, text="the list is empty at the moment...", background="orange", textvariable=vlist)
        videolist.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N+W)

        # audio part (middle)
        audiolbl = Label(self, text="Audio folder")
        audiolbl.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        audiobtn = Button(self, text="Assign an audio folder...", command=self.assignfolder)
        audiobtn.grid(row=0, column=3, padx=5, pady=5, sticky=E)

        # try listbox next time
        global aFolder
        aFolder = StringVar()
        audiolist = Label(self, text="the folder hasn't been assigned yet...", background="orange", textvariable=aFolder)
        audiolist.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky=N+W)

        # buttons (right hand side)
        parsebtn = Button(self, text="Extract audio from video files", command=self.run_extractaudio)
        parsebtn.grid(row=0, column=4, padx=5, pady=5, sticky=E)

        replacebtn = Button(self, text="Replace audio in video files", command=self.run_replaceaudio)
        replacebtn.grid(row=1, column=4, padx=5, pady=5, sticky=E+N)

        #global djistatus
        #djistatus = IntVar()
        #djistatus.set(0)
        #djibox = Checkbutton(self, text="apply DJI audio offset (3 @ 29.976 fps)",
        #                     variable="djistatus")
        #djibox.grid(row=2, column=4, padx=5, pady=5, sticky=E+N)

        aboutbtn = Button(self, text="About", command=self.about)
        aboutbtn.grid(row=2, column=4, padx=5, pady=5, sticky=E)

        quitbtn = Button(self, text="Quit", command=self.quit)
        quitbtn.grid(row=3, column=4, padx=5, pady=5, sticky=E)

        # output window (bottom)
        outputlbl = Label(self, text="Program output")
        outputlbl.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = W+N)

        global runninglog
        runninglog = StringVar()
        progresslog = Label(self, background="orange", textvariable=runninglog)
        progresslog.grid(row = 3, column = 0, columnspan = 4, padx = 5, pady = 5, sticky=N+W+S+E)


    def about(selfs):
        mbox.showinfo("About", "BTW, Taiwan Number One!")

    def addvideo(self):
        # ftypes = [('MTS files', '*.mts'), ('MP4 files', '*.mp4'), ('All files', '*')]
        # ftypes = [('All files', '*')]
        # ftype filter is not compatible in macOS
        global selectedVideo, flist, vfolder
        selectedVideo = filedialog.askopenfilenames(title='Select video files...')
        if selectedVideo != '':
            flist = []
            for i in range(len(selectedVideo)):
                tmp = selectedVideo[i]
                if i == 0:
                    vfolder = dirname(tmp)
                flist.append(split(tmp)[1])

            # generate string to be shown on gui
            string2show = "Folder selected: \n" \
                          + vfolder \
                          + "\n\nFiles selected: \n" \
                          + "\n".join(flist)
            # set vlist on gui
            vlist.set(string2show)


    def assignfolder(self):
        global selectedFolder, audioFound, matchedfiles, onlyfiles

        selectedFolder = filedialog.askdirectory(title='Select an audio folder...')
        if selectedFolder != '':

            # get a list of files from the folder specified
            onlyfiles = [f for f in listdir(selectedFolder) if isfile(join(selectedFolder, f))]
            # filter file list, only wav is accepted
            onlyfiles = [fi for fi in onlyfiles if fi.endswith(".wav")]

            # get matched audio files

            tmp1 = []
            for i in range(len(flist)):
                tmp1.append(splitext(flist[i])[0])

            tmp2 = []
            for i in range(len(onlyfiles)):
                tmp2.append(splitext(onlyfiles[i])[0])

            matchedfiles = sorted(list(set(tmp1).intersection(tmp2)))

            if matchedfiles != []:
                audioFound = [x + ".wav" for x in matchedfiles ]
            else:
                audioFound = ["No matched audio file found"]

            string2show = "Folder selected: \n" \
                          + selectedFolder \
                          + "\n\nMatched audio found (.wav only): \n" \
                          + "\n".join(audioFound)
            aFolder.set(string2show)

    def extractaudio(self):

        string2shown = []
        for i in range(len(selectedVideo)):
            vFile = selectedVideo[i]
            audioFile = selectedFolder + "/" + splitext(flist[i])[0]


            string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                                     + " extracting audio from '" + vFile + "' ...")

            # update runninglog
            runninglog.set("\n".join(string2shown))

            # text = ""
            # text.configure(text=time.asctime())
            # root.after(1000, Refresher)

            # extract audio
            ff = FFmpeg(
                inputs={vFile: None},
                outputs={
                    audioFile + ".wav": '-acodec pcm_s16le -ar 48000'
                }
            )
            # ff.cmd
            ff.run()
            string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                                    + " audio file written '" + audioFile + ".wav'")
            # update runninglog
            runninglog.set("\n".join(string2shown))

        # show notice when finish
        string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                            + " Done!")
        # update runninglog
        runninglog.set("\n".join(string2shown))

    def run_extractaudio(self):
        Thread(target=self.extractaudio).start()

    def replaceaudio(self):

        # run only matched files
        string2shown = []
        for i in range(len(matchedfiles)):
            vFile = ''.join([s for s in selectedVideo if matchedfiles[i] in s])
            audioFile = selectedFolder + "/" + ''.join([s for s in onlyfiles if matchedfiles[i] in s])

            # get offset info
            media_info = MediaInfo.parse(vFile)
            itsoffect = 0

            # the if statement needs a fix, it can go wrong if no delay values
            for track in media_info.tracks:
                if track.track_type == 'Audio':
                    if track.delay_relative_to_video:
                        itsoffect = track.delay_relative_to_video / 1000

            # apply DJI offset
            if "DJI" in audioFile:
                itsoffect = -round(1000/29.976*3/1000, 2)

            string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                                + " audio offset relative to video = " + str(itsoffect) + " seconds")
            string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                                + " replacing audio in '" + vFile + "' ...")

            # update runninglog
            runninglog.set("\n".join(string2shown))

            # combine audio and video with offset
            # ff = FFmpeg(
            #     inputs={vFile: None,
            #             audioFile: '-itsoffset ' + str(itsoffect)},  # offset
            #     outputs={
            #         split(vFile)[0] + "/mixed_" + split(vFile)[1]:
            #             '-map 0:0 -map 1:0 -c:v copy -c:a ac3 -b:a 256k'
            #     }
            # )
            ff = FFmpeg(
                inputs={vFile: None,
                        audioFile: '-itsoffset ' + str(itsoffect)},  # offset
                outputs={
                    split(vFile)[0] + "/mixed_" + split(vFile)[1]:
                        '-map 0:0 -map 1:0 -c:v copy -c:a ac3 -b:a 320k'
                }
            )
            print(ff.cmd)
            ff.run()
            string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                                + " new video file generated: '" + split(vFile)[0] + "/mixed_" + split(vFile)[1] + "'")
            # update runninglog
            runninglog.set("\n".join(string2shown))

        # show notice when finish
        string2shown.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') \
                            + " Done!")
        # update runninglog
        runninglog.set("\n".join(string2shown))

    #         overwrite behaviour

    def run_replaceaudio(self):
        Thread(target=self.replaceaudio).start()

def main():
    root = Tk()
    root.geometry("800x600+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()