import os
import shutil
import time

from icrawler.builtin import GoogleImageCrawler
import face_recognition

file = open('../list.txt', 'r')
Lines = file.readlines()
path="../IMMAGINI_TMP"
new_path="../IMMAGINI"
google_crawler = GoogleImageCrawler(storage={'root_dir': path})
for row in Lines:
    time.sleep(1)
    google_crawler.crawl(keyword=row.strip().replace("_"," ")+" "+ os.environ["OTHERS_TAG"], max_num=1)
    counter=1
    for download in os.listdir(path):
        downloaded_file_name=path+"/"+download
        #if counter==1:
        #    counter += 1
        #    os.remove(downloaded_file_name)
        #    continue
        try:
            image = face_recognition.load_image_file(downloaded_file_name)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations)==0:
                counter += 1
                os.remove(downloaded_file_name)
                continue
        except:
            counter += 1
            os.remove(downloaded_file_name)
            continue

        new_file_name=row.strip().replace(" ","_")+".00"+str(counter)
        os.rename(downloaded_file_name,path+"/"+new_file_name)
        counter+=1
        shutil.move(path+"/"+new_file_name,new_path+"/"+new_file_name)

