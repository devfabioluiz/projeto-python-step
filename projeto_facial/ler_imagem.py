
import cv2
import sys

# Carrega a imagem
img = cv2.imread("foto.jpg")
if img is None:
    print("Erro: imagem 'foto.jpg' nao encontrada. Coloque-a ao lado dos scripts.")
    sys.exit(1)

# Converte para tons de cinza (necessário para detecção)
cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Exibe a imagem
cv2.imshow("Minha Imagem", cinza)

# Aguarda tecla e fecha
cv2.waitKey(0)
cv2.destroyAllWindows()
