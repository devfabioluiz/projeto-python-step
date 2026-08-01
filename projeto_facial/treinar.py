
import cv2
import os
import sys
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer.create()

if not os.path.isdir("faces"):
    print("Erro: pasta 'faces' nao encontrada. Rode coletar_faces.py primeiro.")
    sys.exit(1)

faces = []
labels = []
label_map = {}
label_id = 0

for pasta in os.listdir("faces"):
    caminho = os.path.join("faces", pasta)
    if not os.path.isdir(caminho):
        continue
    label_map[label_id] = pasta
    for arquivo in os.listdir(caminho):
        img = cv2.imread(os.path.join(caminho, arquivo), 0)
        if img is None:
            continue
        img = cv2.resize(img, (200, 200))
        faces.append(img)
        labels.append(label_id)
    label_id += 1

recognizer.train(faces, np.array(labels))
recognizer.save("treino.yml")

print("Treino concluido!")
print("Mapa de labels:", label_map)
