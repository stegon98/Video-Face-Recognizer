import face_recognition
import cv2
import os
import subprocess
import threading
from threading import Thread
import time

class IlMioThread (Thread):
   def __init__(self, num):
      threading.Thread.__init__(self)
      self.num = num
   def run(self):
      print ("Thr avviato")
      function(self.num)

def spostaFile(image_base, video, y):

    print("la funzione spostaFile e stata richiamata con i seguenti parametri")
    print("image_base-> %s"%(image_base))
    print("video-> %s"%(video))
    print("y-> %s"%(y))

    basename = os.path.basename(
        image_base).replace(".jpg","").replace(".JPG","").replace(".png","").replace(".PNG","")

    video_name=os.path.basename(video)

    comando = "ls -l "+OUTPUT_DIR+" | egrep \"^d\" | grep -i " + basename + " | wc -l"
    print("lancio comando %s" % comando)
    output = subprocess.check_output(comando, shell=True).decode("utf-8").replace("\n","")

    print("il comando ha restituito %s" %(output))
    if (output == "0"):
        comando = "mkdir "+OUTPUT_DIR + basename
        print("lancio comando %s" % comando)
        output = subprocess.check_output(comando, shell=True)

    comando = "mv '" + video + "' '"+ OUTPUT_DIR + basename + "/"+video_name+"' 2>/dev/null"
    print("lancio comando %s" % comando)

    try:

        output = subprocess.check_output(comando, shell=True)
    except Exception as e :
        print("non ho spostato il file per il seguente motivo")
        print(str(e))

####################################################################

def caricaDaFile(num_val,file):
    list=[]
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
            except:
                print(f"nessun immagine {LISTA_IMMAGINI_PATH + i}")

    return image

def getUniqueValueList(image_list):
    myset = set(image_list)
    unique=[]
    unique=[item for item in myset if item not in unique]
    print(unique)
    return unique

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
    copia=[]
    cnt=num_lines_video_num_parsed+1
    idx_th=0

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

    if int==1:
        copia=t1
    if int==2:
        copia=t2
    if int==3:
        copia=t3
    if int==4:
        copia=t4
    if int==5:
        copia=t5
    if int==6:
        copia=t6
    if int==7:
        copia=t7
    if int==8:
        copia=t8


    for k in copia:

        check = False
        video = LISTA_VIDEO_PATH + lista_video[k].rstrip()
        print(video)
        vidcap = cv2.VideoCapture(video)
        success, image = vidcap.read()
        count = 1000
        count_matches = [0] * num_lines_valori_num_parsed
        count_matches_unique = [0] * len(image_unique_list)
        while success == True and check == False:

            success, image = vidcap.read()

            if (count % 250 == 0 and count > 1):

                filename = LOADER_FRAME_DIR + "frame" + str(count) + ".jpg"
                print(filename)

                rgb_small = cv2.cvtColor(image, 4)

                doCheck = 0
                try:
                    image_frame_encode = face_recognition.face_encodings(rgb_small)[0]
                except:
                    print("non ci sono volti nell'immagine frame")
                    image_frame_encode = None
                    doCheck = 1
                for y in range(num_lines_valori_num_parsed):  ##
                    if doCheck == 0:
                        res = []


                        try:
                            res = face_recognition.compare_faces([image_encoded[y]], image_frame_encode)


                        except:
                            print("nessun match tra le immagini")
                        try:
                            exit_attempt = res[0]
                        except:
                            exit_attempt = False
                        if exit_attempt == True:
                            count_matches[y] = count_matches[y] + 1
                            for n in range(len(image_unique_list)):
                                if (image_base[y].lower()[:-4]) == image_unique_list[n]:
                                    count_matches_unique[n] = count_matches_unique[n] + 1
                                    print(
                                        f"LA PERSONA E LA STESSA STONKS ,attualmente sono {count_matches[y]} - trovato match con {image_unique_list[n]}")
                                if count_matches_unique[n] >= 10:
                                    spostaFile(LISTA_IMMAGINI_PATH + image_unique_list[n], video, y)
                                    check = True
                                    for prova in range(len(image_unique_list)):
                                        print(f"{image_unique_list[prova]} -  {count_matches_unique[prova]}")
                                    break
            if success == False:
                print("non ho trovato nessun match sposto in altro")
                spostaFile("ALTRO", video, y)
            count += 1
    end = time.time()

    print(f"trascorso {end - start}")


print("inizio")


thread1 = IlMioThread(1)
thread2 = IlMioThread(2)
thread3 = IlMioThread(3)
thread4 = IlMioThread(4)
thread5 = IlMioThread(5)
thread6 = IlMioThread(6)
thread7 = IlMioThread(7)
thread8 = IlMioThread(8)

out = subprocess.check_output("ls | grep config.cfg | wc -l", shell=True).rstrip()

if int(out)==0 :
    subprocess.check_output("echo '/home/stegon/PycharmProjects/IMMAGINI/' >>config.cfg ", shell=True).rstrip()
    subprocess.check_output("echo '/run/media/stegon/131ac7e7-32e9-457b-92e0-7068ecf6c2d7/MEGA2/' >>config.cfg ", shell=True).rstrip()
    subprocess.check_output("echo '/run/media/stegon/131ac7e7-32e9-457b-92e0-7068ecf6c2d7/MEGA2/' >>config.cfg ", shell=True).rstrip()
    subprocess.check_output("echo '/home/stegon/PycharmProjects/LOADER/' >>config.cfg ", shell=True).rstrip()

fileCfg = open('config.cfg', 'r')

LISTA_IMMAGINI_PATH=fileCfg.readline().rstrip()
LISTA_VIDEO_PATH=fileCfg.readline().rstrip()
OUTPUT_DIR=fileCfg.readline().rstrip()
LOADER_FRAME_DIR=fileCfg.readline().rstrip()

fileCfg.close()




subprocess.call("find " + LISTA_IMMAGINI_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " "lista_image.txt \\;", shell=True)# sum(1 for line in open('VALORI.txt'))
subprocess.call("find " + LISTA_VIDEO_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " "lista_video.txt \\;", shell=True)# sum(1 for line in open('VALORI.txt'))



num_lines_valori_num=subprocess.check_output(['wc', '-l', "lista_image.txt"]).decode("utf-8")
num_lines_video_num=subprocess.check_output(['wc', '-l', "lista_video.txt"]).decode("utf-8")

print(f"sono presenti %s valori nel file valori " % (num_lines_valori_num[:3]))
print(f"sono presenti %s valori nel file lista video  " % (num_lines_video_num[:3]))

fileVal = open('lista_image.txt', 'r')
fileVal_lista = open('lista_video.txt', 'r')
# lista_video=[]
# lista_video.append(fileVal_lista.readline())
image_base = []
lista_video = []
check = False

num_lines_video_num_parsed=int(num_lines_video_num[:2])
num_lines_valori_num_parsed=int(num_lines_valori_num[:2])

lista_video=caricaDaFile(num_lines_video_num_parsed,fileVal_lista)
image_base=caricaDaFile(num_lines_valori_num_parsed,fileVal)

image_aus=[]
for i in range(num_lines_valori_num_parsed):
    image_aus.append(image_base[i].lower()[:-4])

image_unique_list=getUniqueValueList(image_aus)
print(image_unique_list)


image_encoded=imageEncodeList()

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()

