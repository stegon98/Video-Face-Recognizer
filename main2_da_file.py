import multiprocessing

import face_recognition
import cv2
import os
import subprocess
import threading
from threading import Thread
from multiprocessing import Process, Queue
from multiprocessing import Pool
import time
import pickle
import hashlib
import time


# import tkinter as tk


# I thread sono stati accantonati in quanto in python non sono gestiti in maniera corretta, abbiamo quindi optato per l'utilizzo di piu' processi
# https://stackoverflow.com/questions/10789042/python-multi-threading-slower-than-serial

# class IlMioThread (Thread):
#   def __init__(self, num):
#      threading.Thread.__init__(self)
#      self.num = num
#   def run(self):
#      print ("Thr avviato")
#      function(self.num)

# def disegna():
#    window = tk.Tk()
#    window.geometry("600x600")
#    window.title("Hello TkInter!")
#    window.mainloop()


def spostaFile(image_base, video, int):
    print(f"processo {int} - la funzione spostaFile e stata richiamata con i seguenti parametri")
    print(f"processo {int} - image_base-> {image_base}")
    print(f"processo {int} - video-> {video}")
    # print(f"processo {int} -  y-> {y}")

    basename = os.path.basename(
        image_base).replace(".jpg", "").replace(".JPG", "").replace(".png", "").replace(".PNG", "")

    video_name = os.path.basename(video)

    comando = "ls -l " + OUTPUT_DIR + " | egrep \"^d\" | grep -i " + basename + " | wc -l"
    print(f"processo {int} -  lancio comando  {comando}")
    output = subprocess.check_output(comando, shell=True).decode("utf-8").replace("\n", "")

    print(f"processo {int} - il comando ha restituito {output}")
    if (output == "0"):
        comando = "mkdir " + OUTPUT_DIR + basename
        print("processo {int} -  lancio comando {comando}")
        output = subprocess.check_output(comando, shell=True)

    comando = "cp '" + video + "' '" + OUTPUT_DIR + basename + "/" + video_name.replace("'", "") + "' "
    print(f"processo {int} - lancio comando {comando}")

    try:

        output = subprocess.check_output(comando, shell=True)
    except Exception as e:
        print(f"processo {int} - non ho spostato il file per il seguente motivo")
        print(f"processo {int} - str(e)")


####################################################################

def caricaDaFile(num_val, file):
    list = []
    for v in range(int(num_val)):  ## carico all'interno dell'array

        list.append(file.readline().rstrip())

    file.close()

    return list


def imageEncodeList():
    image = []
    for i in os.listdir(LISTA_IMMAGINI_PATH):
        if not i.endswith(".txt"):
            try:

                image_frame = face_recognition.load_image_file(LISTA_IMMAGINI_PATH + i)
                cod = face_recognition.face_encodings(image_frame)[0]
                image.append(cod)
                print(f"aggiunta immagine {LISTA_IMMAGINI_PATH}/{i}")
            except:
                print(f"nessun immagine {LISTA_IMMAGINI_PATH + i}")
                output = subprocess.check_output("mv " + LISTA_IMMAGINI_PATH + i + " ../LOADER/", shell=True)
    filehandler=open("immagini_encoded.dump","wb")
    pickle.dump(image,filehandler)
    filehandler.close()

    return image

def imageEncodeList_file():
    filehandler = open("immagini_encoded.dump","rb")

    return pickle.load(filehandler)


def load_from_file_mp(who, start, end):
    image = []
    count = 1
    enable_read = False
    for i in os.listdir(LISTA_IMMAGINI_PATH):
        if count > start:
            if not i.endswith(".txt"):
                try:

                    image_frame = face_recognition.load_image_file(LISTA_IMMAGINI_PATH + i)
                    cod = face_recognition.face_encodings(image_frame)[0]
                    image.append(cod)



                except:
                    print(f"nessun immagine {LISTA_IMMAGINI_PATH + i}")
                    output = subprocess.check_output(
                        "mv " + LISTA_IMMAGINI_PATH + i + " /run/media/stegon/131ac7e7-32e9-457b-92e0-7068ecf6c2d7/LOADER/",
                        shell=True)

        if count >= end:
            break
        count = count + 1

    if who == 1:
        save_to_file_encode(image, "load1.dump")
    if who == 2:
        save_to_file_encode(image, "load2.dump")
    if who == 3:
        save_to_file_encode(image, "load3.dump")
    if who == 4:
        save_to_file_encode(image, "load4.dump")


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def save_to_file_encode(encoded_array, filename):
    try:

        with open(filename, "wb") as f:
            pickle.dump(encoded_array, f)
        return 0
    except:
        print("errore salvataggio del file dump")
        return -1


def load_from_file(filename):
    try:
        with open(filename, "rb") as f:
            var = pickle.load(f)
        return var
        # return -1#temporaneo
    except:
        print("errore caricamento del file dump")
        return -1


def getUniqueValueList(image_list):
    myset = set(image_list)
    unique = []
    unique = [item for item in myset if item not in unique]
    # print(unique)
    return unique


def count_frames(path, override=False):
    # grab a pointer to the video file and initialize the total
    # number of frames read
    video = cv2.VideoCapture(path)
    total = 0
    # if the override flag is passed in, revert to the manual
    # method of counting frames
    if override:
        total = count_frames_manual(video)
    # otherwise, let's try the fast way first
    else:
        # lets try to determine the number of frames in a video
        # via video properties; this method can be very buggy
        # and might throw an error based on your OpenCV version
        # or may fail entirely based on your which video codecs
        # you have installed
        try:
            total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        # uh-oh, we got an error -- revert to counting manually
        except:
            total = count_frames_manual(video)
    # release the video file pointer
    video.release()
    # return the total number of frames in the video
    return total


def count_frames_manual(video):
    # initialize the total number of frames read
    total = 0
    # loop over the frames of the video
    while True:
        # grab the current frame
        (grabbed, frame) = video.read()

        # check to see if we have reached the end of the
        # video
        if not grabbed:
            break
        # increment the total number of frames read
        total += 1
    # return the total number of frames in the video file
    return total


def function(int):
    start = time.time()
    t1 = []
    t2 = []
    t3 = []
    t4 = []
    t5 = []
    t6 = []
    t7 = []
    t8 = []
    copia = []
    cnt = num_lines_video_num_parsed + 1
    idx_th = 0

    #   for i in range(num_lines_video_num_parsed):
    #       if (i%2==0):
    #           even.append(i)
    #       else if (i%3==0):
    #           odd.append(i)

    #   if(int%2==0):
    #       copia=even
    #   else:
    #       copia=odd

    while cnt > 1:
        t1.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t2.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t3.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t4.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t5.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t6.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t7.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break
        t8.append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break

    if int == 1:
        copia = t1
    if int == 2:
        copia = t2
    if int == 3:
        copia = t3
    if int == 4:
        copia = t4
    if int == 5:
        copia = t5
    if int == 6:
        copia = t6
    if int == 7:
        copia = t7
    if int == 8:
        copia = t8

    for k in copia:

        check = False
        video = LISTA_VIDEO_PATH + lista_video[k].rstrip()
        print(video)
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 500
        count_matches = [0] * num_lines_valori_num_parsed
        count_matches_unique = [0] * len(image_unique_list)
        try:
            tot_frame_video = count_frames(video)
            print(f"durata video-> {tot_frame_video}")
            frame_to_skip = round(tot_frame_video / 1000)
            print(f"skip ogni {frame_to_skip}")
        except:
            print(f"durata video-> errore ")
            frame_to_skip = 50

        while success == True and check == False:

            success, image = vidcap.read()

            if (count % frame_to_skip == 0 and count > 1):

                filename = LOADER_FRAME_DIR + "frame" + str(count) + ".jpg"
                # print(filename)

                # rgb_small = cv2.cvtColor(image, 4)

                doCheck = 0
                try:
                    image_frame_encode = face_recognition.face_encodings(image)[0]


                except:
                    #print("non ci sono volti nell'immagine frame")
                    image_frame_encode = None
                    doCheck = 1
                for y in range(num_lines_valori_num_parsed):  ##
                    if doCheck == 0:
                        res = []

                        try:
                            res = face_recognition.compare_faces([image_encoded[y]], image_frame_encode)
                            # dis = face_recognition.face_distance([image_encoded[y]], image_frame_encode)
                            # print(f"diff image {dis}")


                        except:
                            #print(f"nessun match tra le immagini {video}")
                            # print(f"immagine encoded {[image_encoded[y]]} - frame encoded {image_frame_encode}")
                            None

                        # print(res[0])
                        try:
                            exit_attempt = res[0]
                        except:
                            exit_attempt = False
                        if exit_attempt == True:
                            count_matches[y] = count_matches[y] + 1
                            for n in range(len(image_unique_list)):
                                if (image_base[y].lower()[:-4]) == image_unique_list[n]:
                                    count_matches_unique[n] = count_matches_unique[n] + 1
                                #  print(f"LA PERSONA E LA STESSA STONKS ,attualmente sono {count_matches[y]} - trovato match con {image_unique_list[n]}")
                                if count_matches_unique[n] >= 25:
                                    spostaFile(LISTA_IMMAGINI_PATH + image_unique_list[n], video, y)
                                    check = True
                                    for prova in range(len(count_matches_unique)):
                                        print(f"processo {int} - {image_unique_list[prova]} -  {count_matches_unique[prova]}")

                            # for row in range(len(count_matches_unique)):
                            #    print(f"processo {int} - {image_unique_list[row]} -  {count_matches_unique[row]}")
                    if (check == True):
                        break
            if success == False:
                print(f"processo {int} - non ho trovato nessun match sposto in altro")
                spostaFile("ALTRO", video, y)
                max_match = 0
                for row in range(len(count_matches_unique)):
                    if count_matches_unique[row] > count_matches_unique[max_match]:
                        print(f"{count_matches_unique[row]} > {count_matches_unique[max_match]}")
                        print(
                            f"processo {int} - {image_unique_list[row]} -  {count_matches_unique[row]}  > {image_unique_list[max_match]} -  {count_matches_unique[max_match]} ")
                        max_match = row

                spostaFile(LISTA_IMMAGINI_PATH + image_unique_list[max_match], video, int)

                for row in range(len(count_matches_unique)):
                    print(f"processo {int} - {image_unique_list[row]} -  {count_matches_unique[row]}")
            count += 1
    end = time.time()

    print(f"processo {int} - trascorso {end - start}")


print("inizio")
# disegna()

# thread1 = IlMioThread(1)
# thread2 = IlMioThread(2)
# thread3 = IlMioThread(3)
# thread4 = IlMioThread(4)
# thread5 = IlMioThread(5)
# thread6 = IlMioThread(6)
# thread7 = IlMioThread(7)
# thread8 = IlMioThread(8)


p1 = Process(target=function, args=(1,))
p2 = Process(target=function, args=(2,))
p3 = Process(target=function, args=(3,))
p4 = Process(target=function, args=(4,))
p5 = Process(target=function, args=(5,))
p6 = Process(target=function, args=(6,))
p7 = Process(target=function, args=(7,))
p8 = Process(target=function, args=(8,))

out = subprocess.check_output("ls | grep config.cfg | wc -l", shell=True).rstrip()

if int(out) == 0:
    subprocess.check_output("echo '/home/stegon/PycharmProjects/IMMAGINI/' >>config.cfg ", shell=True).rstrip()
    subprocess.check_output("echo '/run/media/stegon/131ac7e7-32e9-457b-92e0-7068ecf6c2d7/MEGA2/' >>config.cfg ",
                            shell=True).rstrip()
    subprocess.check_output("echo '/run/media/stegon/131ac7e7-32e9-457b-92e0-7068ecf6c2d7/MEGA2/' >>config.cfg ",
                            shell=True).rstrip()
    subprocess.check_output("echo '/home/stegon/PycharmProjects/LOADER/' >>config.cfg ", shell=True).rstrip()

fileCfg = open('config.cfg', 'r')

LISTA_IMMAGINI_PATH = fileCfg.readline().rstrip()
LISTA_VIDEO_PATH = fileCfg.readline().rstrip()
OUTPUT_DIR = fileCfg.readline().rstrip()
LOADER_FRAME_DIR = fileCfg.readline().rstrip()

fileCfg.close()

subprocess.call("find " + LISTA_IMMAGINI_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " "lista_image.txt \\;",shell=True)  # sum(1 for line in open('VALORI.txt'))
subprocess.call("find " + LISTA_VIDEO_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " "lista_video.txt \\;",shell=True)  # sum(1 for line in open('VALORI.txt'))

num_lines_valori_num = subprocess.check_output(['wc', '-l', "lista_image.txt"]).decode("utf-8")
num_lines_video_num = subprocess.check_output(['wc', '-l', "lista_video.txt"]).decode("utf-8")

print(f"sono presenti %s valori nel file valori " % (num_lines_valori_num[:3]))
print(f"sono presenti %s valori nel file lista video  " % (num_lines_video_num[:3]))

fileVal = open('lista_image.txt', 'r')
fileVal_lista = open('lista_video.txt', 'r')
# lista_video=[]
# lista_video.append(fileVal_lista.readline())
image_base = []
lista_video = []
check = False

# num_lines_video_num_parsed=int(num_lines_video_num[:2])
# num_lines_valori_num_parsed=int(num_lines_valori_num[:2])

num_lines_valori_num_parsed = file_len("lista_image.txt")
num_lines_video_num_parsed = file_len("lista_video.txt")

lista_video = caricaDaFile(num_lines_video_num_parsed, fileVal_lista)
image_base = caricaDaFile(num_lines_valori_num_parsed, fileVal)

image_aus = []
for i in range(num_lines_valori_num_parsed):
    image_aus.append(image_base[i].lower()[:-4])

image_unique_list = getUniqueValueList(image_aus)
print(image_unique_list)

# image_encoded=imageEncodeList()
#   save_to_file_encode(image_encoded)
leggiDaFile = subprocess.check_output("ls | grep immagini_encoded.dump | wc -l", shell=True).rstrip()

if(int(leggiDaFile)==0):
    image_encoded = imageEncodeList()

else:
    image_encoded = imageEncodeList_file()

p1.start()
p2.start()
p3.start()
p4.start()
p5.start()
p6.start()
p7.start()
p8.start()
