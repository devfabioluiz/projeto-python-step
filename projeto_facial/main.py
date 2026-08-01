
import cv2
import os
import numpy as np

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

ARQUIVO_TREINO = "treino.yml"
PASTA_FACES = "faces"

def coletar():
    nome = input("Digite o nome da pessoa: ")
    destino = os.path.join(PASTA_FACES, nome)
    os.makedirs(destino, exist_ok=True)

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
            face = cv2.resize(cinza[y:y+h, x:x+w], (200, 200))
            cv2.imwrite(f"{destino}/{contador}.jpg", face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{contador}/30", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Coletando - Q para cancelar", frame)
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()
    print(f"Coleta de '{nome}' finalizada com {contador} amostras.")

def treinar():
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    faces, labels, label_map = [], [], {}

    if not os.path.isdir(PASTA_FACES):
        print("Nenhuma face encontrada para treino.")
        return {}

    for idx, pasta in enumerate(os.listdir(PASTA_FACES)):
        caminho = os.path.join(PASTA_FACES, pasta)
        if not os.path.isdir(caminho):
            continue
        label_map[idx] = pasta
        for arquivo in os.listdir(caminho):
            img = cv2.imread(os.path.join(caminho, arquivo), 0)
            if img is None:
                continue
            faces.append(cv2.resize(img, (200, 200)))
            labels.append(idx)

    if not faces:
        print("Nenhuma face encontrada para treino.")
        return {}

    recognizer.train(faces, np.array(labels))
    recognizer.save(ARQUIVO_TREINO)
    print(f"Treino concluido com {len(faces)} amostras.")
    return label_map

def reconhecer(label_map):
    if not os.path.exists(ARQUIVO_TREINO):
        print("Arquivo de treino nao encontrado. Treine primeiro.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer.create()
    recognizer.read(ARQUIVO_TREINO)

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
            cv2.rectangle(frame, (x, y), (x+w, y+h), cor, 2)
            cv2.putText(frame, f"{nome} ({confianca:.0f}%)",
                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)
        cv2.imshow("Reconhecimento - Q para sair", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("=== RECONHECIMENTO FACIAL ===")
    print("1 - Coletar amostras")
    print("2 - Treinar modelo")
    print("3 - Reconhecer ao vivo")
    opcao = input("Escolha uma opcao: ")

    if opcao == "1":
        coletar()
    elif opcao == "2":
        treinar()
    elif opcao == "3":
        if not os.path.exists(ARQUIVO_TREINO):
            treinar()
        mapa = {}
        if os.path.isdir(PASTA_FACES):
            for idx, pasta in enumerate(os.listdir(PASTA_FACES)):
                if os.path.isdir(os.path.join(PASTA_FACES, pasta)):
                    mapa[idx] = pasta
        reconhecer(mapa)
    else:
        print("Opcao invalida.")
