# imports


try:
    import pytube.exceptions
    import math
    import os
    import pickle
    import time
    import urllib.request
    import re
    import timeit
    import shutil
    import datetime as dt
    import youtube_dl
    import sys
    import shutil
    import traceback
    import integv

    from wrapt_timeout_decorator import *
    from pymediainfo import MediaInfo
    from pathvalidate import sanitize_filename
    from datetime import datetime
    from pytube import Playlist
    from pytube import YouTube
    import pytube.request
    from Youtbedef import Y_dlall
    from Youtbedef import Livetest

except Exception as e:

    print(e)





def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def Download(Playlists, Name, SaveLocation, numbersafe):
    # getting urls
    print("getting Video Urls")
    playlist = Playlist(Playlists).video_urls

    # Setting all used Varibels to its standarts


    fielexist = True
    vidinpl = 0
    vindnum = 0
    LoadingbarCons = ""
    vidinplc = 0
    timelaps = 0
    fnum = -1
    donevids = False
    Titleselist = []
    Livestream = False
    viddone = False

    # code starts
    for video_link in playlist:
        vidinpl = vidinpl + 1

    # Loding
    LoadingTen = vidinpl / 50

    LoadingTen = math.ceil(LoadingTen)


    # deleting files if programm needed a restart
    try:
        os.remove(SaveLocation + str(Name) + '/vid.mp4.part')
    except Exception as e:
        pass
    try:
        os.remove(SaveLocation + str(Name) + '/vid.mp4')
    except Exception as e:
        pass
    try:
        os.remove(SaveLocation + str(Name) + '/pic.jpg')
    except Exception as e:
        pass
    try:
        os.remove(SaveLocation + str(Name) + '/vidl.mp4')
    except Exception as e:
        pass

    for video_link in playlist:
        start = datetime.now()

        # Loading
        print(video_link)
        vindnum = vindnum + 1

        vidinplc = vidinplc + 1

        if vindnum == LoadingTen:
            LoadingbarCons = LoadingbarCons.replace("[", "").replace("]", "")

            LoadingbarCons = "[" + LoadingbarCons + "#" + "]"

            vindnum = 0

        Loadingbar = LoadingbarCons + " [" + str(vidinplc) + "/" + str(vidinpl) + "] [" + str(timelaps) + "|" + str(
            timelaps * (vidinpl - vidinplc)) + "] [Time: %s:%s" % (
                     datetime.now().hour, datetime.now().minute) + "] [" + str(numbersafe) + "]"

        print(Loadingbar)

        lasthree = str(" (" + str(video_link[(int(len(video_link) - 3)):]) + "[Copy])")



        while True:


            try:

                Title = YouTube(video_link).title
                print("Title got")
                Titlese = sanitize_filename(Title)
                try:
                    open(SaveLocation + str(Name) + "/" + str(Titlese) + ".mp4")

                    if integv.verify(open(SaveLocation + Name + '/' + str(Titlese) + ".mp4", 'rb'), file_type="mp4") == False:
                        os.remove(SaveLocation + Name + '/' + str(Titlese))
                        raise Exception("Error in file")


                    vidlen = ""
                    while str(vidlen).isnumeric() == False:
                        try:
                            vidlen = round(MediaInfo.parse(SaveLocation + str(Name) + "/" + str(Titlese) + ".mp4").tracks[0].duration / 1000)
                            print(vidlen)
                        except Exception as e:
                            print(e)
                            print(str(traceback.format_exc()))
                            print(numbersafe)
                            print(SaveLocation + str(Name) + "/" + str(Titlese) + ".mp4")
                            continue

                    Length = ""
                    while str(Length).isnumeric() == False:
                        try:
                            Length = str(YouTube(video_link).length)
                            print(Length)
                        except Exception as e:
                            print(e)
                            print(numbersafe)
                            continue


                    if int(vidlen) == int(Length) or int(vidlen) == int(Length) + 1 or int(vidlen) + 1 == int(Length):
                        donevids = True
                    else:
                        donevids = False

                    if donevids == False:
                        try:
                            open(SaveLocation + str(Name) + "/" + Titlese + lasthree + ".mp4")

                            if integv.verify(open(SaveLocation + Name + '/' + str(Titlese) + lasthree + ".mp4", 'rb'),file_type="mp4") == False:
                                os.remove(SaveLocation + Name + '/' + str(Titlese) + lasthree + ".mp4")
                                raise Exception("Error in file")
                            donevids = True
                        except Exception as e:
                            print(e)
                            donevids = False


                except Exception as e:
                    donevids = False
                    print(e)

                if donevids == False:

                    for i in range(20):
                        try:
                            Date = str(YouTube(video_link).publish_date)
                        except Exception as e:
                            print(e)
                            continue
                        break
                    try:
                        try:
                            os.remove(SaveLocation + str(Name) + '/vid.jpg')
                        except Exception as e:
                            pass
                        try:
                            os.remove(SaveLocation + str(Name) + '/pic.jpg')
                        except Exception as e:
                            pass
                        try:
                            os.remove(SaveLocation + str(Name) + '/vidl.mp4')
                        except Exception as e:
                            pass



                        #download video
                        Y_dlall(SaveLocation, Name, video_link)


                    except Exception as e:
                        print(str(e))
                        break
                    if Livetest(video_link) == False:
                        for i in range(20):
                            try:
                                Thumbnail = YouTube(video_link).thumbnail_url
                                Description = sanitize_filename(YouTube(video_link).description)
                            except Exception as e:
                                print(e)
                                continue
                            break

                        print(Thumbnail)
                        while True:

                            try:
                                for i in range(20):
                                    try:
                                        urllib.request.urlretrieve(Thumbnail, SaveLocation + str(Name) + '/pic.jpg')
                                    except Exception as e:
                                        print(e)
                                        continue
                                    break

                                try:
                                    open(SaveLocation + str(Name) + '/pic.jpg')
                                except:
                                    shutil.copy(SaveLocation + "hqdefault.jpg", SaveLocation + str(Name) + '/pic.jpg')
                                for i in range(20):
                                    try:
                                        os.system(
                                            'ffmpeg -i ' + '"' + SaveLocation + str(
                                                Name) + '/vid.mp4" -i ' + '"' + SaveLocation + str(
                                                Name) + '/pic.jpg" -map 1 -map 0 -c copy -disposition:0 attached_pic -metadata title="' + str(
                                                video_link) + '" -metadata comment="' + str(
                                                Description) + '" -metadata genre="' + str(
                                                Date) + ' " "' + SaveLocation + str(
                                                Name) + '/vidl.mp4"')
                                        os.remove(SaveLocation+ str(Name) + '/vid.mp4')
                                        os.remove(SaveLocation + str(Name) + '/pic.jpg')
                                    except Exception as e:
                                        print(e)
                                        continue
                                    break
                            except Exception as e:
                                print(e)
                                print(numbersafe)
                                print(video_link)
                                continue
                            break
                        try:
                            open(SaveLocation + str(Name) + "/" + Titlese + ".mp4")

                            os.rename(SaveLocation + str(Name) + '/vidl.mp4',
                                      SaveLocation  + str(Name) + '/' + str(Titlese) + lasthree + '.mp4')
                        except:
                            pass
                        try:
                            os.rename(SaveLocation + str(Name) + '/vidl.mp4',
                                      SaveLocation + str(Name) + '/' + str(Titlese) + '.mp4')
                        except:
                            pass






            except Exception as e:
                print(e)

                continue
            break


        timelaps = datetime.now() - start


# Start of Programm
if __name__ == "__main__":
    Manuel = False
    SaveLoc = (os.path.dirname(__file__))

    try:
        ort = open("Ort.txt", "r").read()
        SaveLoc = ort
    except:
        pass


    try:
        Channelmanuel = open(SaveLoc + "Channel.txt", "r").read().split(" ")
        Manuel = True
        Channelmanuel = input().split(" ")
    except:
        pass


    # with open(SaveLoc + "NumberSafe.dat", "wb") as pickle_files:
    #    pickle.dump(0, pickle_files)
    #    pickle_files.close
    numbersafe = 0


    with open(SaveLoc + "UrlofChannel.dat", "rb") as pickle_files:
        youtubeURL = pickle.load(pickle_files)
        pickle_files.close()

    with open(SaveLoc + "NameofChannel.dat", "rb") as pickle_files:
        youtubeNamelist = pickle.load(pickle_files)
        pickle_files.close()




    try:
        os.remove(SaveLoc + "data.test")
    except:
        pass
    if Manuel == False:
        numbersafe = 0
        while True:


            youtubeName = (youtubeNamelist[numbersafe])
            playlistURL = (youtubeURL[numbersafe])

            print(playlistURL)
            Download(playlistURL, youtubeName, SaveLoc, numbersafe)

            numbersafe = numbersafe + 1
            print(numbersafe)

    else:
        num = 0
        while True:
            numbersafe = int(Channelmanuel[num])
            youtubeName = (youtubeNamelist[numbersafe])
            playlistURL = (youtubeURL[numbersafe])

            print(playlistURL)
            Download(playlistURL, youtubeName, SaveLoc, numbersafe)

            num = num + 1
            print(numbersafe)



