
import cv2

# Carrega o classificador
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Carrega a imagem
img = cv2.imread("grupo.jpg")
cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detecta rostos
rostos = face_cascade.detectMultiScale(
    cinza,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
)

# Desenha retângulos ao redor dos rostos
for (x, y, w, h) in rostos:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

print(f"Rostos detectados: {len(rostos)}")

cv2.imshow("Deteccao Facial", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
          