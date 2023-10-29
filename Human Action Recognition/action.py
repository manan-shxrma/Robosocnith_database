import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import cv2
from collections import deque
import numpy as np
import pandas as pd


SEQUENCE_LENGTH = 20
IMAGE_HEIGHT = 64
IMAGE_WIDTH = 64
NUM_CHANNELS = 3
NUM_CLASSES = 4
DATASET_DIR = "UCF50"

CLASSES_LIST = ["BenchPress", "Biking", "Swing", "HorseRace"]

path_to_model = "model.h5"

LRCN_model = load_model(path_to_model)
# Make the Output directory if it does not exist
test_videos_directory = 'test_videos'
os.makedirs(test_videos_directory, exist_ok = True)

# Download a YouTube Video.
# video_title = download_youtube_videos('/content/Benchpress.mp4', test_videos_directory)

# Get the YouTube Video's path we just downloaded.
input_video_file_path = f'video.mp4'

def predict_on_video(video_file_path, output_file_path, SEQUENCE_LENGTH):
    video_reader = cv2.VideoCapture(video_file_path)

    original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), 
                                   video_reader.get(cv2.CAP_PROP_FPS), (original_video_width, original_video_height))

    frames_queue = deque(maxlen = SEQUENCE_LENGTH)

    predicted_class_name = ''

    while video_reader.isOpened():

        ok, frame = video_reader.read() 
        
        if not ok:
            break

        resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
        
        normalized_frame = resized_frame / 255

        frames_queue.append(normalized_frame)

        if len(frames_queue) == SEQUENCE_LENGTH:

            predicted_labels_probabilities = LRCN_model.predict(np.expand_dims(frames_queue, axis = 0))[0]

            predicted_label = np.argmax(predicted_labels_probabilities)

            predicted_class_name = CLASSES_LIST[predicted_label]

        cv2.putText(frame, predicted_class_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        video_writer.write(frame)
        
    # Release the VideoCapture and VideoWriter objects.
    video_reader.release()
    video_writer.release()



import time
start = time.time()

output_video_file_path = f'{test_videos_directory}/{"Video"}-Output-SeqLen{10}.mp4'

predict_on_video(input_video_file_path, output_video_file_path, SEQUENCE_LENGTH)
end = time.time()

print(end-start)
# Display the output video.
VideoFileClip(output_video_file_path, audio=False, target_resolution=(300,None)).ipython_display()


# import time
# start = time.time()

# output_video_file_path = f'{test_videos_directory}/{"biking"}-Output-SeqLen{10}.mp4'

# predict_on_video(input_video_file_path, output_video_file_path, SEQUENCE_LENGTH)
# end = time.time()

# print(end-start)
# # Display the output video.
# VideoFileClip(output_video_file_path, audio=False, target_resolution=(300,None)).ipython_display()