import yaml
import cv2
from ultralytics import YOLO


with open("config.yaml") as f:
    cfg = yaml.safe_load(f)


model = YOLO(cfg["model"])
cap = cv2.VideoCapture(cfg.get("camera", 0))
conf = float(cfg.get("conf", 0.5))

def to_pixels(points, W, H):
    return [(int(x*W), int(y*H)) for x, y in points]

def points_in_poly(px, py, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > py) != (y2 > py)):
            xintens = (x2 - x1)*(py-y1)/(y2-y1+1e-9)+x1
            if px < xintens:
                inside = not inside
    return inside

while True:
    ok, frame = cap.read()
    if not ok:
        print("Tidak dapat menemukan Webcam")
        break

    H, W = frame.shape[:2]
    active = to_pixels(cfg["roi_active"], W, H)
    guard = to_pixels(cfg["roi_guard"], W, H)

##MEMBUAT SHAPE DI TENGAN
    cv2.polylines(frame, [__import__("numpy").array(guard)], True, (0, 255, 255), 2)
    cv2.polylines(frame, [__import__("numpy").array(active)], True,(255, 0, 0), 2)
    cv2.putText(frame, "GUARD :tidak bisa", (guard[0][0], guard[0][1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(frame, "ACTIVE : Berhasil", (active[0][0], active[0][1]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    res = model.predict(frame, conf=conf, verbose=False)[0]

    for b in res.boxes:
        x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cls_id= int(b.cls[0])
        label=f"{res.names[cls_id]} {float(b.conf[0]):.2f}"

        in_active= points_in_poly(cx, cy, active)
        in_guard= points_in_poly(cx, cy, guard)

        if in_active:
            cv2.rectangle(frame, (x1,y1), (x2, y2), (0,255,255), 2)
            cv2.circle(frame, (cx, cy), 4, (0,255,0), -1)
            cv2.putText(frame, label, (x1,y1-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            
        elif in_guard:
            cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 255, 255), 2)
            cv2.putText(frame, "Geser Ke tengah", (x1, y1-8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        else:
            pass

    cv2.imshow("demoroi- q: quit s:save", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord("q"):
        break
