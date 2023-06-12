# YOLO-object-detection-video-
## Download the following dependencies:
  * opencv
  * numpy
  
  by using
`pip install numpy opencv-python`


 Download the pre-trained YOLO v3 weights file from this [link](https://pjreddie.com/media/files/yolov3.weights) and place it in the current directory or you can directly download to the current directory in terminal using
 
 `$ wget https://pjreddie.com/media/files/yolov3.weights`
  
 `$ python yolo_opencv.py --image dog.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt`
 
*now properly add the paths of files in the input.

The resultant video will be downloaded in avi format change it to mp4 for further application.
