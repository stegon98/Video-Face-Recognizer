<h1>Video-Face-Recognizer</h1>

✅ It's reguired **python3**

✅ install cmake **apt install cmake**

✅ install the pip requirements **pip install --no-cache-dir -r requirements.txt**

Before running the program you need to edit set the following environment variable **$VIDEO_DIR** and **$IMG_DIR**

If there are more images with the same name but with a different extension, the matches will be added together, for greater precision it would be better to have more images per actor

<h1>Docker</h1>

Build image **docker build . -t vfr2**

Run container with this command:

>docker run -v /video_path:/app/video -v /image_path:/app/img -v /output_cmd_list:/app/output -it vfr2