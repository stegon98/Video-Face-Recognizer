import face_recognition
import cv2
import os
import subprocess


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

    #comando = "cp '" + video + "' "+ OUTPUT_DIR + basename + "/ "
    comando = "mv '" + video + "' '"+ OUTPUT_DIR + basename + "/"+video_name+"' 2>/dev/null"
    print("lancio comando %s" % comando)

    try:

        output = subprocess.check_output(comando, shell=True)
    except Exception as e :
        print("non ho spostato il file per il seguente motivo")
        print(str(e))

####################################################################

def caricaDaFile(num_lines_num_parsed,lista_video,file):
    for v in range(num_lines_video_num_parsed):  ## carico all'interno dell'array

        lista_video.append(file.readline().rstrip())

    file.close()



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




subprocess.call("find " + LISTA_IMMAGINI_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " +LISTA_IMMAGINI_PATH+"lista.txt \\;", shell=True)# sum(1 for line in open('VALORI.txt'))
subprocess.call("find " + LISTA_VIDEO_PATH + " -maxdepth 1 -type f -exec basename \"{}\" > " +LISTA_VIDEO_PATH+"lista.txt \\;", shell=True)# sum(1 for line in open('VALORI.txt'))



num_lines_valori_num=subprocess.check_output(['wc', '-l', LISTA_IMMAGINI_PATH+"lista.txt"]).decode("utf-8")
num_lines_video_num=subprocess.check_output(['wc', '-l', LISTA_VIDEO_PATH+"lista.txt"]).decode("utf-8")

print(f"sono presenti %s valori nel file valori " % (num_lines_valori_num[:3]))
print(f"sono presenti %s valori nel file lista video  " % (num_lines_video_num[:3]))

fileVal = open(LISTA_IMMAGINI_PATH+'lista.txt', 'r')
fileVal_lista = open(LISTA_VIDEO_PATH+'lista.txt', 'r')
# lista_video=[]
# lista_video.append(fileVal_lista.readline())
image_base = []
lista_video = []
check = False

num_lines_video_num_parsed=int(num_lines_video_num[:2])
num_lines_valori_num_parsed=int(num_lines_valori_num[:2])

caricaDaFile(num_lines_video_num_parsed,lista_video,fileVal_lista)
caricaDaFile(num_lines_valori_num,image_base,fileVal)



# print(lista_video[v])



for k in range(num_lines_video_num_parsed):

    # vidcap = cv2.VideoCapture(lista_video[k])
    check = False
    video = LISTA_VIDEO_PATH+lista_video[k].rstrip()
    print(video)
    vidcap = cv2.VideoCapture(video)
    #success, image = vidcap.read()
    success=True
    count = 1000
    count_matches=[0]*num_lines_valori_num_parsed

    #while count < 150001 and check == False and video!=LISTA_VIDEO_PATH+"lista.txt":
    while success ==True and check == False and video!=LISTA_VIDEO_PATH+"lista.txt":
        ##TO DO impostare un triplo check per essere sicuri del match
        ##success, image = vidcap.read()
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
        success, image = vidcap.read()
        print("aa")

        #success, image = vidcap.read()

       ## if (count % 1000 == 0 and count > 1):

        print(LOADER_FRAME_DIR+"frame%d.jpg" % count)
        filename = LOADER_FRAME_DIR+"frame" + str(count) + ".jpg"
        print(filename)
        cv2.imwrite(filename, image)  # save frame as JPEG file

        # confronto immagini
        image_frame = face_recognition.load_image_file(filename)
        doCheck=0

        try:

            image_frame_encode = face_recognition.face_encodings(image_frame)[0]

        except:
            print("non ci sono volti nell'immagine frame")
            image_frame_encode = None
            doCheck=1


        for y in range(num_lines_valori_num_parsed):  ##

            if LISTA_IMMAGINI_PATH+image_base[y]!=LISTA_IMMAGINI_PATH+"lista.txt" and doCheck==0 :
                res = []
                # res[0]=False
            #    print("utilizzo l'immagine %s" %(LISTA_IMMAGINI_PATH+image_base[y]))
                image_conf = face_recognition.load_image_file(LISTA_IMMAGINI_PATH+image_base[y])
                image_conf_encode = face_recognition.face_encodings(image_conf)[0]
                #print(image_conf_encode)
                #print(image_frame_encode)

                try:
                    res = face_recognition.compare_faces([image_conf_encode], image_frame_encode)
                except:
                    print("nessun match tra le immagini")

                try:
                    exit_attempt = res[0]
                except:
                    exit_attempt = False

                if exit_attempt == True:
                    count_matches[y]=count_matches[y]+1
                    print("LA PERSONA E LA STESSA STONKS aggiungo un match,attualmente sono %s" % (count_matches[y]))
                    if count_matches[y]>=3 :
                        spostaFile(LISTA_IMMAGINI_PATH+image_base[y], video, y)
                        check = True
                        break



        if success==False:
            print("non ho trovato nessun match sposto in altro")
            spostaFile("ALTRO",video,y)
        count += 1000

# image_know=face_recognition.load_image_file("/home/stegon/PycharmProjects/riconoscitore/enrico1.jpg");
# image2_know=face_recognition.load_image_file("/home/stegon/PycharmProjects/riconoscitore/andreagale.png")
# image_unknow=face_recognition.load_image_file("/home/stegon/PycharmProjects/riconoscitore/andreagale.png")


# print(type(image_know))
# print(f"{image_know}")

# know_encoding=face_recognition.face_encodings(image_know) ##potrebbero tornare piu valori dati da piu volti ATTENZIONE
# unknow_encoding=face_recognition.face_encodings(image2_know); ##potrebbero tornare piu valori dati da piu volti ATTENZIONE

# len(unknow_encoding)
##embedding dell'immagine

# print (know_encoding)

# risultato=face_recognition.compare_faces([know_encoding],unknow_encoding)

# print(risultato)

# if risultato[0] == True :
#   print("LA PERSONA E LA STESSA STONKS")
# else:
#   print("LA PERSONA NON E LA STESSA")
