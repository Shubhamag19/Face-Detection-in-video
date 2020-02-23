import cv2
import face_recognition

input_movie = cv2.VideoCapture("sample_video.mp4")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

image = face_recognition.load_image_file("sample_image.jpeg")
face_encoding = face_recognition.face_encodings(image)[0]

known_faces = [
		face_encoding,
		]
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grabinga single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Converting image from BGR to RGB color
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        name = None
        if match[0]:
            name = "SUSPECT"
            import mail
            exec('mail.py')

        face_names.append(name)

    # Labeling the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue
        
        # Drawing a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Drawing a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
    # Writing resulting image to the output video file
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(input_movie.get(cv2.CAP_PROP_FPS))
    frame_width = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_movie = cv2.VideoWriter("output.mp4", codec, fps, (frame_width,frame_height))
    print("Writing frame {} / {}".format(frame_number, length))
    output_movie.write(frame)

input_movie.release()
output_movie.release()
cv2.destroyAllWindows()
