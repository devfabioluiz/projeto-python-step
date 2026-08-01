
import cv2

# Carrega a imagem
img = cv2.imread("foto.jpg")

# Converte para tons de cinza (necessário para detecção)
cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Exibe a imagem
cv2.imshow("Minha Imagem", cinza)

# Aguarda tecla e fecha
cv2.waitKey(0)
cv2.destroyAllWindows()