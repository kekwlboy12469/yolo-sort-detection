# Real-Time Object Detection and Tracking - Internship Evaluation

## Project Overview
This project performs real-time detection and tracking of objects from a video using:
- YOLOv5 (for object detection)
- SORT (Simple Online and Realtime Tracking)

It detects when an object is missing or when a new object appears in the frame.

## Technologies Used
- Python 3.9
- PyTorch
- OpenCV
- YOLOv5
- SORT tracking algorithm
- Docker

## Folder Structure
├── ai.py # Main application script ├── sort.py # SORT tracker ├── kalman_filter.py # Kalman filter used in SORT ├── yolov5/ # YOLOv5 model directory ├── input.mp4 # Input video ├── output.mp4 # Output video generated ├── Dockerfile # Docker container build file ├── README.md # report_Akshat_ML_intern.docx


## How to Run

### Build Docker Image
docker build -t yolo-sort-app .
Run Docker Container
docker run --rm -it -v C:/python:/app yolo-sort-app
The output video output.mp4 will be saved in the same folder (C:/python).

Results
FPS achieved: 5.17 (on CPU)

Tracked objects with unique IDs

Detection of missing and new appearing objects.

Author
[Akshat Singh]

