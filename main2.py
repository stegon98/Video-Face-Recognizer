import face_recognition
import cv2
import os
import subprocess
import timeit


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


print("inizio")

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




for k in range(num_lines_video_num_parsed):

    # vidcap = cv2.VideoCapture(lista_video[k])
    check = False
    video = LISTA_VIDEO_PATH+lista_video[k].rstrip()
    print(video)
    vidcap = cv2.VideoCapture(video)
    success, image = vidcap.read()
    #success=True
    count = 1000
    count_matches=[0]*num_lines_valori_num_parsed
    count_matches_unique=[0]*len(image_unique_list)

    #while count < 150001 and check == False and video!=LISTA_VIDEO_PATH+"lista.txt":
    while success ==True and check == False :
        ##TO DO impostare un triplo check per essere sicuri del match
        ##success, image = vidcap.read()
        ##vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
        success, image = vidcap.read()

        #success, image = vidcap.read()

        if (count % 250 == 0 and count > 1):

            #print(LOADER_FRAME_DIR+"frame%d.jpg" % count)
            filename = LOADER_FRAME_DIR+"frame" + str(count) + ".jpg"
            print(filename)
            #cv2.imwrite(filename, image)  # save frame as JPEG file
            rgb_small=cv2.cvtColor(image,4)
            # confronto immagini
            #image_frame = face_recognition.load_image_file(filename)
            #image_frame = face_recognition.load_image_file(rgb_small)
            doCheck=0

            try:

            #    image_frame_encode = face_recognition.face_encodings(image_frame)[0]
                image_frame_encode = face_recognition.face_encodings(rgb_small)[0]

            except:
                print("non ci sono volti nell'immagine frame")
                image_frame_encode = None
                doCheck=1


            for y in range(num_lines_valori_num_parsed):  ##

                if  doCheck==0 :
                    res = []
                    # res[0]=False
                #    print("utilizzo l'immagine %s" %(LISTA_IMMAGINI_PATH+image_base[y]))
                   # image_conf = face_recognition.load_image_file(LISTA_IMMAGINI_PATH+image_base[y])
                   # image_conf_encode = face_recognition.face_encodings(image_conf)[0]


                    #print(image_frame_encode)

                    try:
                       # res = face_recognition.compare_faces([image_conf_encode], image_frame_encode)
                       res = face_recognition.compare_faces([image_encoded[y]], image_frame_encode)
                       #correct = face_recognition.face_distance([image_encoded[y]], image_frame_encode)
                       #print(correct[0])
                       #if correct[0]<=0.6:
                       #    res[0]=True

                    except:
                        print("nessun match tra le immagini")

                    try:
                        exit_attempt = res[0]
                    except:
                        exit_attempt = False

                    if exit_attempt == True:
                        count_matches[y]=count_matches[y]+1
                        for n in range(len(image_unique_list)):
                            if (image_base[y].lower()[:-4]) ==image_unique_list[n]:
                                count_matches_unique[n]=count_matches_unique[n]+1
                                print(f"LA PERSONA E LA STESSA STONKS ,attualmente sono {count_matches[y]} - trovato match con {image_unique_list[n]}")
                            if count_matches_unique[n]>=10 :
                                spostaFile(LISTA_IMMAGINI_PATH+image_unique_list[n], video, y)
                                check = True
                                for prova in range(len(image_unique_list)):
                                    print(f"{image_unique_list[prova]} -  {count_matches_unique[prova]}")
                                break



        if success==False:
            print("non ho trovato nessun match sposto in altro")
            spostaFile("ALTRO",video,y)
        count += 1


