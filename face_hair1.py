import numpy as np
import cv2
import dlib

# Load face cascade and shape predictor
face_cascade_path = "E:\\3RD_TRIMISTER\\FaceShape-master\\haarcascade_frontalface_default.xml"
predictor_path = "E:\\3RD_TRIMISTER\\FaceShape-master\\shape_predictor_68_face_landmarks(1).dat"

faceCascade = cv2.CascadeClassifier(face_cascade_path)
predictor = dlib.shape_predictor(predictor_path)

# Load hairstyle images for each face shape
hairstyle_images = {
    'Heart': cv2.imread("E:\\3RD_TRIMISTER\\FaceShape-master\\png2jpg\\heart.jpg", cv2.IMREAD_UNCHANGED),
    'Oval': cv2.imread("E:\\3RD_TRIMISTER\\FaceShape-master\\png2jpg\\oval.jpg", cv2.IMREAD_UNCHANGED),
    'Long': cv2.imread("E:\\3RD_TRIMISTER\\FaceShape-master\\png2jpg\\long.jpg", cv2.IMREAD_UNCHANGED),
    'Round': cv2.imread("E:\\3RD_TRIMISTER\\FaceShape-master\\png2jpg\\round.jpg", cv2.IMREAD_UNCHANGED),
    'Square': cv2.imread("E:\\3RD_TRIMISTER\\FaceShape-master\\png2jpg\\square.jpg", cv2.IMREAD_UNCHANGED)
}

def detect_face_shape(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        detected_landmarks = predictor(gray, dlib_rect).parts()
        landmarks = np.array([[p.x, p.y] for p in detected_landmarks])

        # Draw landmarks as dots
        for (x, y) in landmarks:
            cv2.circle(image, (x, y), 2, (0, 0, 255), -1)

        # Overlay hairstyle based on face shape
        overlay_hairstyle(image, landmarks, x, y, w, h)

        # Display face shape name
        face_shape = classify_face_shape(landmarks, w, h)
        text = face_shape
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        text_x = max(x - 20, 0)
        text_y = max(y - 20, text_size[1])
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    return image


def overlay_hairstyle(image, landmarks, x, y, w, h):
    # Get the corresponding hairstyle image for the detected face shape
    face_shape = classify_face_shape(landmarks, w, h)
    hairstyle_img = hairstyle_images.get(face_shape)

    if hairstyle_img is not None:
        # Display the hairstyle image in a separate window
        cv2.imshow("Hairstyle Recommendation", hairstyle_img)

def classify_face_shape(landmarks, w, h):
    # Calculate relevant measurements for face shape classification
    chin_roundness = abs((landmarks[8, 0] - landmarks[1, 0]) / (landmarks[15, 0] - landmarks[0, 0]))
    
    # Define thresholds for classification
    heart_threshold = 0.7
    oval_threshold = 0.75
    long_threshold = 1.0
    round_threshold = 0.8
    square_threshold = 1.2
    
    # Classify face shape based on the measurements
    if chin_roundness < heart_threshold:
        return 'Heart'
    elif chin_roundness > oval_threshold:
        return 'Oval'
    elif w / h > long_threshold:
        return 'Long'
    elif chin_roundness < round_threshold:
        return 'Round'
    else:
        return 'Square'


def capture_live_photo():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Press Space to Capture', frame)
        key = cv2.waitKey(1)
        if key == 32:  # Space key
            break
        elif key == 27:  # Escape key
            cap.release()
            cv2.destroyAllWindows()
            return None
    cap.release()
    cv2.destroyAllWindows()
    return frame

def upload_image(image_path):
    image = cv2.imread(image_path)
    return image

def main():
    option = input("Choose an option (1. Live Photo Capture, 2. Image Upload): ")
    
    if option == '1':
        original_image = capture_live_photo()
    elif option == '2':
        image_path = input("Enter the image path: ")
        original_image = upload_image(image_path)
    else:
        print("Invalid option. Please choose either 1 or 2.")
        return
    
    if original_image is None:
        print("Error: Could not open or read the image.")
        return
    
    # Create a copy of the original image
    image_with_shape = original_image.copy()
    
    # Detect face shapes and overlay facial landmarks on the copied image
    image_with_landmarks = detect_face_shape(image_with_shape)
    
    # Display the image with facial landmarks
    cv2.imshow("Image with Facial Landmarks", image_with_landmarks)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
