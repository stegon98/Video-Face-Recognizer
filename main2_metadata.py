import multiprocessing

import face_recognition
import cv2
import os
import subprocess
from multiprocessing import Process, Queue
from multiprocessing import Pool
import time
import pickle
import time
from shlex import quote

TOT_THREAD=4

# I thread sono stati accantonati in quanto in python non sono gestiti in maniera corretta, abbiamo quindi optato per l'utilizzo di piu' processi
# https://stackoverflow.com/questions/10789042/python-multi-threading-slower-than-serial


def generateLinkCommand(image_base, video, int,server_video):
    print(f"processo {int} - la funzione generateLinkCommand e stata richiamata con i seguenti parametri")
    print(f"processo {int} - image_base-> {image_base}")
    print(f"processo {int} - video-> {video}")
    # print(f"processo {int} -  y-> {y}")

    basename = os.path.basename(
        image_base).replace(".jpg", "").replace(".JPG", "").replace(".png", "").replace(".PNG", "")

    video_name = os.path.basename(video)

    comando="mv  '{0}'  '{1}'" .format("'"+server_video+"'", "'"+server_video+"_bk'")

    print(f"processo {int} -  lancio comando  {comando}")
    output = subprocess.check_output("echo {0} >>comandi.txt".format(comando), shell=True).decode("utf-8").replace("\n", "")

    print(f"processo {int} - il comando ha restituito {output}")
    if (output == "0"):
        comando = " mkdir " + OUTPUT_DIR + basename
        print("processo {int} -  lancio comando {comando}")
        output = subprocess.check_output(comando, shell=True)
    #comando="ln -s  {0}  {1}" .format("'"+server_video+"'", "'"+OUTPUT_DIR +  basename+"/" + video_name + "'")
    comando="ffmpeg -i '{0}' -metadata artist={1} -codec copy '{2}'".format("'"+server_video+"_bk'",basename, "'"+OUTPUT_DIR+"/" + video_name+"'")

    print(f"processo {int} - lancio comando {comando}")

    try:
        output = subprocess.check_output("echo {0} >>comandi.txt".format(comando), shell=True).decode("utf-8").replace("\n", "")
    except Exception as e:
        print(f"processo {int} - non ho spostato il file per il seguente motivo")
        print(f"processo {int} - {str(e)}")
        try:
            subprocess.check_output("echo " + comando_ls + " >>comandiInErrore", shell=True)
        except:
            print(f"errore salvataggio comando in errore {int} - {str(e)}")


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
                print(f"aggiunta immagine {LISTA_IMMAGINI_PATH}{i}")
            except:
                print(f"nessun immagine {LISTA_IMMAGINI_PATH + i}")
                output = subprocess.check_output("rm " + LISTA_IMMAGINI_PATH + i , shell=True)
    filehandler=open("immagini_encoded.dump","wb")
    pickle.dump(image,filehandler)
    filehandler.close()
    return image

def imageEncodeList_file():
    filehandler = open("immagini_encoded.dump","rb")
    return pickle.load(filehandler)

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


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


def function(proc_id):
    start = time.time()
    tn=[ ]
    for i in range(TOT_THREAD):
        tn.append([])
    copia = []
    cnt = num_lines_video_num_parsed + 1
    idx_th = 0

    while cnt > 1:
        tn[idx_th%TOT_THREAD].append(idx_th)
        idx_th += 1
        cnt -= 1
        if cnt < 1:
            break

    copia = tn[proc_id-1]

    for k in copia:
        check = False
        #server_video=lista_video[k].rstrip()
        video = lista_video[k].rstrip()
        print(video)
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 400
        count_matches = [0] * num_lines_valori_num_parsed
        count_matches_unique = [0] * len(image_unique_list)
        try:
            tot_frame_video = count_frames(video)
            print(f"durata video-> {tot_frame_video}")
            frame_to_skip = round(tot_frame_video / 250)
            print(f"skip ogni {frame_to_skip}")
        except:
            print(f"durata video-> errore ")
            frame_to_skip = 50

        while success == True and check == False:
            success, image = vidcap.read()

            if (count % frame_to_skip == 0 and count > 1):
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
                        molt=0
                        exit_attempt=True
                        try:
                            #res = face_recognition.compare_faces([image_encoded[y]], image_frame_encode)
                            dis = face_recognition.face_distance([image_encoded[y]], image_frame_encode)
                            if dis<= 0.45:
                                molt=4
                            elif dis<=0.48:
                                molt=3
                            elif dis<=0.53:
                                molt=2
                            elif dis<=0.58:
                                molt=1
                            else:
                                molt=0
                                exit_attempt = False
                            # print(f"diff image {dis}")

                        except:
                            #print(f"nessun match tra le immagini {video}")
                            # print(f"immagine encoded {[image_encoded[y]]} - frame encoded {image_frame_encode}")
                            exit_attempt=False


                        if exit_attempt == True:
                            count_matches[y] = count_matches[y] + (1*molt)
                            for n in range(len(image_unique_list)):
                                if (image_base[y].lower()[:-4]) == image_unique_list[n]:
                                    count_matches_unique[n] = count_matches_unique[n] + (1*molt)
                                if count_matches_unique[n] >= int(MATCH_REQUIRED):
                                    generateLinkCommand(image_unique_list[n], video, y,video)
                                    check = True
                                    for prova in range(len(count_matches_unique)):
                                        print(f"processo {proc_id} - {image_unique_list[prova]} -  {count_matches_unique[prova]}")

                            # for row in range(len(count_matches_unique)):
                            #    print(f"processo {int} - {image_unique_list[row]} -  {count_matches_unique[row]}")
                    if (check == True):
                        break
            if success == False:
                print(f"processo {proc_id} - non ho trovato nessun match ")
                #generateLinkCommand("ALTRO", video, y,video)
                for prova in range(len(count_matches_unique)):
                    print(f"processo {proc_id} - {image_unique_list[prova]} -  {count_matches_unique[prova]}")

            count += 1
    end = time.time()

    print(f"processo {proc_id} - trascorso {end - start}")


print("inizio")

out = subprocess.check_output("ls | grep config.cfg | wc -l", shell=True).rstrip()

fileCfg = open('config.cfg', 'r')

LISTA_IMMAGINI_PATH = fileCfg.readline().rstrip()
LISTA_VIDEO_PATH = fileCfg.readline().rstrip()
OUTPUT_DIR = fileCfg.readline().rstrip()
MATCH_REQUIRED= fileCfg.readline().rstrip()
fileCfg.close()

subprocess.call("find " + LISTA_IMMAGINI_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " "lista_image.txt \\;",shell=True)  # sum(1 for line in open('VALORI.txt'))
subprocess.call("find " + LISTA_VIDEO_PATH + " -maxdepth 1 -type f  >  lista_video.txt ",shell=True)  # sum(1 for line in open('VALORI.txt'))

num_lines_valori_num = subprocess.check_output(['wc', '-l', "lista_image.txt"]).decode("utf-8")
num_lines_video_num = subprocess.check_output(['wc', '-l', "lista_video.txt"]).decode("utf-8")

print(f"sono presenti %s valori nel file valori " % (num_lines_valori_num[:3]))
print(f"sono presenti %s valori nel file lista video  " % (num_lines_video_num[:3]))

fileVal = open('lista_image.txt', 'r')
fileVal_lista = open('lista_video.txt', 'r')
image_base = []
lista_video = []
check = False


num_lines_valori_num_parsed = file_len("lista_image.txt")
num_lines_video_num_parsed = file_len("lista_video.txt")

lista_video = caricaDaFile(num_lines_video_num_parsed, fileVal_lista)
image_base = caricaDaFile(num_lines_valori_num_parsed, fileVal)

image_aus = []
for i in range(num_lines_valori_num_parsed):
    image_aus.append(image_base[i].lower()[:-4])

image_unique_list = getUniqueValueList(image_aus)
print(image_unique_list)


leggiDaFile = subprocess.check_output("ls | grep immagini_encoded.dump | wc -l", shell=True).rstrip()

if(int(leggiDaFile)==0):
    image_encoded = imageEncodeList()

else:
    image_encoded = imageEncodeList_file()

"""with Pool(8) as p:
    print(p.map(function, [1, 2, 3, 4, 5, 6, 7 ,8]))"""

processParameter=[]
for i in range(TOT_THREAD):
    processParameter.append(i)

with Pool(TOT_THREAD) as p:
    print(p.map(function, processParameter))