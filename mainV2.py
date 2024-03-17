import os
import face_recognition
import cv2
import pickle
from collections import defaultdict
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import Pool

pos_progres_bar=0

def encode_faces_in_folder(actor_image_folder):
    print("Encoding faces in actor images...")
    actor_encodings = {}
    actor_files = [actor_file for actor_file in os.listdir(actor_image_folder) ]

    with Pool(processes=os.cpu_count()) as pool:
        for actor_name, encoding in pool.imap_unordered(encode_actor, [(actor_image_folder, actor_file) for actor_file in actor_files]):
            actor_encodings[actor_name] = encoding

    print("Encoding faces complete.")
    return actor_encodings

def encode_actor(args):
    actor_image_folder, actor_file = args
    actor_name, _ = os.path.splitext(actor_file)
    actor_path = os.path.join(actor_image_folder, actor_file)
    img = face_recognition.load_image_file(actor_path)
    encoding = face_recognition.face_encodings(img)[0]
    return actor_name, encoding

def count_faces_in_video(video_path, actor_encodings):
    #print(f"Processing video: {video_path}")
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    actor_face_counts = defaultdict(int)

    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    #progress_bar = tqdm(total=total_frames, position=++pos_progres_bar, desc=os.path.basename(video_path))

    while True:
        # Esci se si è raggiunto il limite di match
        if any(count >= 100 for count in actor_face_counts.values()):
            break
        # Skip 60 frames
        for _ in range(30):
            video_capture.grab()

        ret, frame = video_capture.retrieve()
        if not ret:
            break

        frame_count += 30  # Increment frame count by 10
        #progress_bar.update(60)  # Increment progress bar by 10 frames
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            for actor_name, actor_encoding in actor_encodings.items():
                #match = face_recognition.compare_faces([actor_encoding], face_encoding,tolerance=0.4)
                #if match[0]:
                #    actor_face_counts[actor_name] += 1
                dis = face_recognition.face_distance([actor_encoding], face_encoding)
                if dis<= 0.43:
                    molt=4
                elif dis<=0.45:
                    molt=3
                elif dis<=0.48:
                    molt=2
                elif dis<=0.50:
                    molt=1
                else:
                    molt=0

                actor_face_counts[actor_name] += molt

    video_actor = max(actor_face_counts, key=actor_face_counts.get)
    #progress_bar.close()
    print(f"Video {video_path} processed. Most recurrent actor: {video_actor}")


    output_filename = os.path.splitext(os.path.basename(video_path))[0] + "_modified.mp4"
    ffmpeg_command = f"ffmpeg -i \"{video_path}\" -metadata artist=\"{video_actor}\" -codec copy \"{output_filename}\""

    f = open("/app/output/comandiffmpeg.txt", "a")
    f.write(ffmpeg_command)
    f.close()

    #return video_actor
    return ffmpeg_command

def process_video(video_folder, actor_image_folder):
    actor_encodings = encode_faces_in_folder(actor_image_folder)
    video_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder)]
    ffmpeg_commands = []

    count_faces_partial = partial(count_faces_in_video, actor_encodings=actor_encodings)

    with ProcessPoolExecutor(max_workers=len(video_files)) as executor:
        results = list(tqdm(executor.map(count_faces_partial, video_files), total=len(video_files), desc="Videos processed"))

    print("All videos processed. Results:")
    for video_path, most_recurrent_actor in zip(video_files, results):
        print(f"Video {video_path} - Most recurrent actor: {most_recurrent_actor}")
        ffmpeg_commands.append(count_faces_in_video(video_path, actor_encodings))


if __name__ == "__main__":
    video_folder = os.environ.get("VIDEO_DIR") #input("Enter the path to the folder containing videos: ")
    actor_image_folder = os.environ.get("IMG_DIR") #input("Enter the path to the folder containing actor images: ")
    process_video(video_folder, actor_image_folder)
