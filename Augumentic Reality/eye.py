# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# image = cv2.imread('image.jpg')
# image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
# gray = cv2.cvtColor(image , cv2.COLOR_BGR2GRAY)
# eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
# eyes = eye_cascade.detectMultiScale(gray)
# filter = cv2.cvtColor(cv2.imread('blue.png') , cv2.COLOR_BGR2RGB)
# for x, y, w, h in eyes:
#     centre_x = x+w/2 
#     centre_y = y + h/2
#     filter = cv2.resize(filter , (int( w / 4)  ,int( h /4) ))
#     print(filter.shape) 
#     if max(filter.shape) == max(image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)):int(centre_x+(w/8))].shape):
#         filter = cv2.resize(filter , (int( w / 4)  ,int( h /4) ))
#     elif max(filter.shape) > max(image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)):int(centre_x+(w/8))].shape):
#         n = max(filter.shape) - max(image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)):int(centre_x+(w/8))].shape)
#         filter = cv2.resize(filter , (int( w / 4) +n ,int( h /4) + n))
#     elif max(filter.shape) < max(image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)):int(centre_x+(w/8))].shape):
#         n = max(image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)):int(centre_x+(w/8))].shape) - max(filter.shape) 
#         filter = cv2.resize(filter , (int( w / 4) +n ,int( h /4) + n))
#     alpha_filter =   filter[:,:,2] / 255
#     alpha_back =  1 - alpha_filter
#     for c in range(0,3):
#         image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)+4):int(centre_x+(w/8)+4),c]=(alpha_back*image[int(centre_y-(h/8)):int(centre_y+(h/8)),int(centre_x-(w/8)+4):int(centre_x+(w/8)+4),c]+alpha_filter*filter[:,:,c])
#     plt.imshow(image)
#     plt.imsave('filter1.png' , image)





























import cv2
import numpy as np

# Load the video
video = cv2.VideoCapture(0)

# Load the eye cascade classifier
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load the filter image
filter = cv2.cvtColor(cv2.imread('blue.png'), cv2.COLOR_BGR2RGB)

# Output video file configuration
output_file = 'output_video.mp4'
fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

while True:
    # Read the next frame from the video
    ret, frame = video.read()

    # Break if no frame is read
    if not ret:
        break

    # Convert the frame to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray)

    for x, y, w, h in eyes:
        # Calculate the center coordinates of the detected eye
        center_x = x + w // 2
        center_y = y + h // 2

        # Calculate the size of the filter based on the size of the detected eye region
        filter_size = max(w, h)
        filter_resized = cv2.resize(filter, (filter_size, filter_size))

        # Calculate the region of the frame to apply the filter
        region_x = center_x - filter_size // 2
        region_y = center_y - filter_size // 2
        region = frame[region_y:region_y + filter_size, region_x:region_x + filter_size]

        # Calculate the alpha values for blending the filter with the frame
        alpha_filter = filter_resized[:, :, 2] / 255
        alpha_back = 1 - alpha_filter

        # Apply the filter to the region of the frame
        for c in range(0, 3):
            region[:, :, c] = (alpha_back * region[:, :, c] + alpha_filter * filter_resized[:, :, c])

    # Convert the frame back to BGR for writing to the output video
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Write the frame to the output video file
    out.write(frame)

    # Display the processed frame
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and writer objects
video.release()
out.release()

# Close all windows
cv2.destroyAllWindows()
