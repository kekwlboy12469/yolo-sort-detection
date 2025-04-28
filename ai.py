import cv2
import torch
import numpy as np
from sort import Sort  
import time


print("[INFO] Loading YOLOv5 model...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.4 
model.iou = 0.5   


video_path = "input.mp4"  
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("[ERROR] Failed to open video.")
    exit()

tracker = Sort()


previds = set()


frame_count = 0
start_time = time.time()


save_output = True
out = None

print("[INFO] Starting detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of video reached.")
        break 

    
    frame = cv2.resize(frame, (400, 270))

    
    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()

    
    detsforsort = []
    for det in detections:
        x1, y1, x2, y2, conf, cls = det[:6]
        detsforsort.append([x1, y1, x2, y2, conf])
    detsforsort = np.array(detsforsort)

    
    tracks = tracker.update(detsforsort)

    
    currentids = set()
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        currentids.add(int(track_id))

        
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f'ID {int(track_id)}', (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    
    newids = currentids - previds
    missingids = previds - currentids

    
    for track in tracks:
        x1, y1, x2, y2, trackid = track
        if int(trackid) in newids:
            cv2.putText(frame, 'NEW', (int(x1), int(y2) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    
    #cv2.imshow("YOLOv5 + SORT Tracker", frame)
    #if cv2.getWindowProperty('YOLOv5 + SORT Tracker', cv2.WND_PROP_VISIBLE) < 1:
     #   break
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break


    
    if save_output:
        if out is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output.mp4', fourcc, 30, (frame.shape[1], frame.shape[0]))
        out.write(frame)


    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break

    previds = currentids.copy()  


cap.release()
if out:
    out.release()
cv2.destroyAllWindows()

print(f"[INFO] Done. Average FPS: {fps:.2f}")
