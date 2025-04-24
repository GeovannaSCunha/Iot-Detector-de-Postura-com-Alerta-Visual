import cv2
import mediapipe as mp
import numpy as np
import serial


arduino = serial.Serial('COM6', 9600,)

# Inicializa o Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)


# Configurações
LIMIAR_INCLINACAO = 0.08  # (0.05 a 0.15)
POSTURA_RUIM_TEMPO = 0    # Contador de tempo em postura ruim

cap = cv2.VideoCapture(0)  # Webcam (0) ou caminho do video gravado "video.mp4"

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Obtém os pontos do nariz (1) e queixo (152)
            pontos = face_landmarks.landmark
            nariz = [pontos[1].x, pontos[1].y] 
            queixo = [pontos[152].x, pontos[152].y]  

            # Calcula a diferença vertical normalizada (0-1)
            diferenca = abs(nariz[1] - queixo[1])

            # Detecta inclinação
            if diferenca < LIMIAR_INCLINACAO:
                POSTURA_RUIM_TEMPO += 1
                status = "POSTURA RUIM! (Cabeca inclinada)"
                cor = (0, 0, 255)  # Vermelho
                arduino.write(b'1')  # LED vermelho
            else:
                status = "POSTURA CORRETA"
                cor = (0, 255, 0)  # Verde
                arduino.write(b'0')  # LED verde

            # Exibe informações
            cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor, 2)
            cv2.putText(frame, f"Diff: {diferenca:.3f}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Tempo ruim: {POSTURA_RUIM_TEMPO}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Desenha os pontos de referência
            h, w = frame.shape[:2]
            cv2.circle(frame, (int(nariz[0] * w), int(nariz[1] * h)), 5, (0, 255, 0), -1)
            cv2.circle(frame, (int(queixo[0] * w), int(queixo[1] * h)), 5, (0, 0, 255), -1)

    cv2.imshow("Detector de Postura ao mexer no celular", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
