Video-Face-Recognizer
It's reguired python3.8  


INSTALL cmake  
INSTALL python-dlib  
INSTALL opencv-python  (pip)  
INSTALL face-recognition (pip)  

Before running the program you need to edit the config.cfg file to set the paths:  
/ home / stegon / PycharmProjects / IMAGES / -> path of image to search  
/ run / media / stegon / DISK1 / VIDEOS / -> path of video sources  
/ run / media / stegon / DISK1 / VIDEOS_OUTPUT / -> path of output video (folders with actor's name will be created and videos                                                                           will be inserted inside)    
/ home / stegon / PycharmProjects / LOADER / -> path of extracted frame of video 

If there are more images with the same name but with a different extension, the matches will be added together, for greater precision it would be better to have more images per actor  
