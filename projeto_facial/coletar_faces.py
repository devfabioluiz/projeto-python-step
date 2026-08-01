
import cv2
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

nome = input("Digite seu nome: ")
os.makedirs(f"faces/{nome}", exist_ok=True)

webcam = cv2.VideoCapture(0)
contador = 0

while contador < 30:
    ret, frame = webcam.read()
    if not ret:
        break

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(cinza, 1.3, 5)

    for (x, y, w, h) in rostos:
        contador += 1
        face = cinza[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))
        cv2.imwrite(f"faces/{nome}/{contador}.jpg", face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Amostra {contador}/30",
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Coletando Faces", frame)
    cv2.waitKey(100)

webcam.release()
cv2.destroyAllWindows()
print("Coleta finalizada!")
          