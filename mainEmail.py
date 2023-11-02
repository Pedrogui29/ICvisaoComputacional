import cv2
import numpy as np
import ssl
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

# Desativa a verificação do certificado SSL
ssl._create_default_https_context = ssl._create_unverified_context

# Variável que recebe o que vai ser lido, podendo ser vídeos, fotos e webcam
video = cv2.VideoCapture(0)

# Nome da classe que você deseja detectar
object_to_detect = "Bottle"

classes = []
with open('coco.names', 'rt') as arquivo:  # objetos capazes de detectar
    classes = arquivo.read().rstrip('\n').split('\n')

modeloConf = 'yolov3.cfg'
modeloWeights = 'yolov3.weights'

# Precisão da detecção
confThresh = 0.5

# Funções da biblioteca YOLO para ajustar imagem
net = cv2.dnn.readNetFromDarknet(modeloConf, modeloWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Configuração do SendGrid
sg = SendGridAPIClient(api_key=('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'))
email_sender = "pedropgfo@gmail.com"
email_receiver = "pedrorokero29@gmail.com"

# Variável de controle para rastrear se o e-mail já foi enviado
email_enviado15 = False
email_enviado10 = False
email_enviado5 = False
email_acabou = False

# Variáveis para controlar o tempo
tempo_anterior = time.time()
intervalo_tempo = 60 # 30 minutos em segundos

while True:
    # Processamento da imagem
    check, img = video.read()
    img = cv2.resize(img, (1090, 720))
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    imH, imW, imC = img.shape
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThresh and classes[classId].lower() == object_to_detect.lower():
                w, h = int(det[2] * imW), int(det[3] * imH)
                x, y = int((det[0] * imW) - w / 2), int((det[1] * imH) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThresh, 0.3)

    num_bottles = 0  # Inicializa a contagem de garrafas

    # Box de reconhecimento da imagem
    for i in indices:
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, f'{classes[classIds[i]].upper()} {int(confs[i] * 100)}%', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        num_bottles += 1  # Incrementa a contagem de garrafas

    # Mostra a contagem de garrafas no terminal
    print(f"Garrafas detectadas: {num_bottles}")

    # Verifica se o número de garrafas é menor ou igual a 2 e envia um e-mail

    # Verifica se o número de garrafas está entre 11 e 15 e envia um e-mail
    if num_bottles <= 15 and num_bottles > 10 and not email_enviado15:
        subject = "Alerta: Número baixo de garrafas detectadas"
        message = f"Atenção, apenas {num_bottles} garrafas foram detectadas na imagem!"

        # Cria o e-mail usando a API do SendGrid
        message = Mail(
            from_email=email_sender,
            to_emails=email_receiver,
            subject=subject,
            plain_text_content=message)

        # Envia o e-mail usando o SendGrid
        try:
            response = sg.send(message)
            print("E-mail enviado com sucesso!")
            email_enviado15 = True  # Define a variável de controle como True após enviar o e-mail
        except Exception as e:
            print("Erro ao enviar o e-mail:", e)

    # Verifica se o número de garrafas está entre 6 e 10 e envia um e-mail
    if num_bottles <= 10 and num_bottles > 5 and not email_enviado10:
        subject = "Alerta: Número baixo de garrafas detectadas"
        message = f"Atenção, apenas {num_bottles} garrafas foram detectadas na imagem!"

        # Cria o e-mail usando a API do SendGrid
        message = Mail(
            from_email=email_sender,
            to_emails=email_receiver,
            subject=subject,
            plain_text_content=message)

        # Envia o e-mail usando o SendGrid
        try:
            response = sg.send(message)
            print("E-mail enviado com sucesso!")
            email_enviado10 = True  # Define a variável de controle como True após enviar o e-mail
        except Exception as e:
            print("Erro ao enviar o e-mail:", e)

    # Verifica se o número de garrafas é menor que 5 e maior que 1 e envia um e-mail
    if num_bottles <= 5 and num_bottles >= 1 and not email_enviado5:
        subject = "Alerta: Número baixo de garrafas detectadas"
        message = f"Atenção, apenas {num_bottles} garrafas foram detectadas na imagem!"

        # Cria o e-mail usando a API do SendGrid
        message = Mail(
            from_email=email_sender,
            to_emails=email_receiver,
            subject=subject,
            plain_text_content=message)

        # Envia o e-mail usando o SendGrid
        try:
            response = sg.send(message)
            print("E-mail enviado com sucesso!")
            email_enviado5 = True  # Define a variável de controle como True após enviar o e-mail
        except Exception as e:
            print("Erro ao enviar o e-mail:", e)

    # Verifica se o número de garrafas acabaram
    if num_bottles == 0 and not email_acabou:
        subject = "Alerta: As garrafas acabaram"
        message = f"Atenção, o estoque de garrafas acabou!"

        # Cria o e-mail usando a API do SendGrid
        message = Mail(
            from_email=email_sender,
            to_emails=email_receiver,
            subject=subject,
            plain_text_content=message)

        # Envia o e-mail usando o SendGrid
        try:
            response = sg.send(message)
            print("E-mail enviado com sucesso!")
            email_acabou = True  # Define a variável de controle como True após enviar o e-mail
        except Exception as e:
            print("Erro ao enviar o e-mail:", e)

    # Verifica se passou o tempo para enviar um e-mail com a quantidade atual de garrafas
    tempo_atual = time.time()
    if (tempo_atual - tempo_anterior) >= intervalo_tempo:
        subject = "Atualização: Quantidade atual de garrafas detectadas"
        message = f"Quantidade atual de garrafas detectadas: {num_bottles}"

        # Cria o e-mail usando a API do SendGrid
        message = Mail(
            from_email=email_sender,
            to_emails=email_receiver,
            subject=subject,
            plain_text_content=message)

        # Envia o e-mail usando o SendGrid
        try:
            response = sg.send(message)
            print("E-mail de atualização enviado com sucesso!")
            tempo_anterior = tempo_atual  # Atualiza o tempo anterior para o momento atual
        except Exception as e:
            print("Erro ao enviar o e-mail de atualização:", e)

    cv2.imshow('Video', img)
    cv2.waitKey(1)
