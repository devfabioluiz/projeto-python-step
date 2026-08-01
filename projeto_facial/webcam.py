
import cv2
import sys

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Erro: nao foi possivel abrir a webcam.")
    sys.exit(1)

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(cinza, 1.1, 5)

    for (x, y, w, h) in rostos:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Webcam - Pressione Q para sair", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
