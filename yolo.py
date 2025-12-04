import cv2
from detector import YOLODetector
from tracker import Tracker
from postprocess import MobileUsePostProcessor
from utils import draw_annotations

# URL del live de YouTube
url = "https://www.youtube.com/watch?v=rnXIjl_Rzy4"

# Captura el stream con OpenCV (requiere ffmpeg)
# Primero, obtenemos el stream directo con yt-dlp
import subprocess

def get_live_stream(url):
    # extrae URL directa de YouTube Live
    cmd = [
        "yt-dlp",
        "-g",  # solo URL
        url
    ]
    stream_url = subprocess.check_output(cmd).decode().strip()
    return stream_url

stream_url = get_live_stream(url)
cap = cv2.VideoCapture(stream_url)

# Inicializa detector, tracker y postprocess
detector = YOLODetector(model_path='models/best_phone_model.pt', classes=['person','phone','hand'])
tracker  = Tracker()
post = MobileUsePostProcessor(history_len=30, fps=25)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detectar
    detections = detector.predict(frame)
    # Trackear
    tracks = tracker.update(detections, frame)
    # Post-process
    results = post.update(tracks, detections, frame_time=cap.get(cv2.CAP_PROP_POS_FRAMES))
    # Dibujar y mostrar
    vis = draw_annotations(frame, tracks, results)
    cv2.imshow("MobileUse Live", vis)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
