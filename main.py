import cv2
import pytesseract

def ocr_en_frame(video_path, frame_num, roi):
    """
    Realiza OCR en una región específica de un frame de un video.
    
    Args:
        video_path (str): Ruta al archivo de video.
        frame_num (int): Número del frame deseado.
        roi (tuple): Región de interés (x, y, ancho, alto).
    """
    # Configuración de Tesseract (asegúrate de que esté instalado y configurado)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # Abrir el video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return
    
    # Establecer el frame deseado
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    
    # Leer el frame
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el frame especificado.")
        cap.release()
        return
    
    # Extraer la ROI del frame
    x, y, w, h = roi
    roi_frame = frame[y:y+h, x:x+w]
    
    if False :
        # Mostrar la región de interés
        cv2.imshow("ROI", roi_frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # Convertir la ROI a escala de grises (opcional, mejora OCR)
    roi_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar OCR
    texto = pytesseract.image_to_string(roi_gray, config="--psm 6 digits")
    
    #print("Texto detectado:", texto)
    
    # Liberar recursos
    cap.release()

    return texto

# Ruta al video y número del frame deseado
ruta_video = "ruta_al_video.mp4"
frame_0 = 30*50  # Cambia estos valores
frame_n = frame_0 + 30*60*7
periodo = 30
roi_velocidad = (220, 600, 80, 28)  # Cambia a (x, y, ancho, alto) km/h
roi_altitud = (230, 630, 70, 28)


valores=[]
max = (frame_n - frame_0) / periodo
for i,frame in enumerate(range(frame_0,frame_n,periodo)):
    velocidad=ocr_en_frame(ruta_video, frame, roi_velocidad)
    altitud=ocr_en_frame(ruta_video, frame, roi_altitud)
    print(f"{i} / {int(max)}")
    valores.append([i,(velocidad[:-1]),altitud[:-1]])
# Abrir el archivo en modo escritura ('w') y escribir los valores
with open("valores.txt", "w") as archivo:
    archivo.write(f"i;velocidad;altitud\n")  # Escribir cada valor en una nueva línea
    for valor in valores:
        archivo.write(f"{valor[0]};{valor[1]};{valor[2]}\n")  # Escribir cada valor en una nueva línea

print("Valores escritos en valores.txt")