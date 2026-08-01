
import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer.create()
recognizer.read("treino.yml")

label_map = {0: "Joao", 1: "Maria"}  # Ajuste conforme sua coleta

webcam = cv2.VideoCapture(0)

while True:
    ret, frame = webcam.read()
    if not ret:
        break

    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_cascade.detectMultiScale(cinza, 1.3, 5)

    for (x, y, w, h) in rostos:
        face = cv2.resize(cinza[y:y+h, x:x+w], (200, 200))
        label, confianca = recognizer.predict(face)

        nome = label_map.get(label, "Desconhecido")
        cor = (0, 255, 0) if confianca < 70 else (0, 0, 255)
        texto = f"{nome} ({confianca:.0f}%)"

        cv2.rectangle(frame, (x, y), (x+w, y+h), cor, 2)
        cv2.putText(frame, texto, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

    cv2.imshow("Reconhecimento Facial - Pressione Q para sair", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
          