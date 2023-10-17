import cv2

print("For Using any video press : V")
print("For Using webcam press : W")
abx = input()

if abx == 'V':
    video = cv2.VideoCapture('video.mp4')
elif abx == 'W':
    video = cv2.VideoCapture(0)

# Get the video properties
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

ret1, frame1 = video.read()
ret2, frame2 = video.read()

frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

frame1_blur = cv2.GaussianBlur(frame1_gray, (21, 21), 0)
frame2_blur = cv2.GaussianBlur(frame2_gray, (21, 21), 0)

while video.isOpened():
    diff = cv2.absdiff(frame1_blur, frame2_blur)

    _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)

    white_pixels = cv2.countNonZero(thresh)
    rows, cols = thresh.shape
    total_pixels = rows * cols

    if white_pixels > 0.05 * total_pixels:
        cv2.putText(frame1, 'Motion Detected', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    dilate = cv2.dilate(thresh, None, iterations=9)

    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    display = frame2.copy()

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(display, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('Motion Detection', display)

    # Write the frame with motion detection to the output video
    out.write(display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame1 = frame2
    frame1_gray = frame2_gray
    frame1_blur = frame2_blur

    ret, frame2 = video.read()

    if not ret:
        break

    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frame2_blur = cv2.GaussianBlur(frame2_gray, (21, 21), 0)

# Release the video capture, writer, and close windows
video.release()
out.release()
cv2.destroyAllWindows()
