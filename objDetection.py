import cv2
import numpy as np

net = cv2.dnn.readNet('./yolov3.weights', './yolov3.cfg')

classes = []
with open("yolov3.txt", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture(input("Enter the video: "))
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

# Get input video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Create output video writer
output_filename = "output.avi"
codec = cv2.VideoWriter_fourcc(*"XVID")
output_video = cv2.VideoWriter(output_filename, codec, fps, (width, height))

while True:
    ret, img = cap.read()
    if not ret:
        break

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255, 255, 255), 2)

    cv2.imshow('Image', img)
    output_video.write(img)  # Write frame to the output video

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
output_video.release()  # Release the output video writer
cv2.destroyAllWindows()
