import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser  # para abrir páginas

def hablar(texto):
    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)
    engine.setProperty('rate', 170)

    print("Asistente:", texto)
    engine.say(texto)
    engine.runAndWait()
    engine.stop()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language="es-MX")
        print("Tú dijiste:", comando)
        return comando.lower()
    except sr.UnknownValueError:
        hablar("No entendí lo que dijiste.")
        return ""
    except sr.RequestError:
        hablar("Error al conectar con el servicio de reconocimiento.")
        return ""

def procesar(comando):
    # normalizamos
    comando = comando.lower()

    # ACTIVACIÓN OPCIONAL: si dices "hey asistente", la quitamos del texto
    if "hey asistente" in comando:
        comando = comando.replace("hey asistente", "").strip()
        if comando == "":
            hablar("Te escucho, ¿qué necesitas?")
            return True

    # --- COMANDOS BÁSICOS ---
    if "hola" in comando:
        hablar("Hola Erwin, ¿qué necesitas?")
    
    elif "hora" in comando:
        hora = datetime.datetime.now().strftime("%H:%M")
        hablar(f"Son las {hora}")
    
    elif "cómo estás" in comando or "como estas" in comando:
        hablar("De lujo, al cien por ciento. ¿Y tú?")

    # --- IDENTIDAD ---
    elif "quién eres" in comando or "quien eres" in comando:
        hablar("Soy un asistente de voz programado por Erwin para la materia de introducción a la inteligencia artificial.")

    elif "qué eres" in comando or "que eres" in comando:
        hablar("Soy un programa de inteligencia artificial simple, un asistente de voz que responde a tus comandos y te ayuda con tu tarea.")

    # --- ABRIR PÁGINAS ---
    elif "abre youtube" in comando or "abrir youtube" in comando:
        hablar("Abriendo YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "abre google" in comando or "abrir google" in comando:
        hablar("Abriendo Google.")
        webbrowser.open("https://www.google.com")

    # --- CHISTE ---
    elif "chiste" in comando:
        hablar("¿Sabes cuál es el colmo de un programador? Tener problemas con su ex, porque siempre vuelve a lo mismo.")

    # --- OPINIÓN DEL TRABAJO ---
    elif (("que opinas" in comando or "qué opinas" in comando) and "trabajo" in comando):
        hablar("Muy bien, espero que la maestra nos pase.")

    # --- OPINIÓN DE LA TAREA ---
    elif (("que opinas" in comando or "qué opinas" in comando) and "tarea" in comando):
        hablar("De lujo, espero que la maestra nos pase.")

    # --- SALUDO A LA MAESTRA ---
    elif (("saluda" in comando or "manda saludo" in comando or "manda saludos" in comando) 
          and "maestra" in comando):
        hablar("Un saludo muy especial para la maestra Reynalda, de parte de Erwin y de su asistente de voz.")

            # --- PONER CANCIÓN FAVORITA ---
    elif ("pon mi canción favorita" in comando 
          or "pon mi cancion favorita" in comando 
          or "mi canción favorita" in comando):
        hablar("Reproduciendo tu canción favorita, Erwin.")
        webbrowser.open("https://www.youtube.com/watch?v=UG5yfZKSsUc&list=RDGMEMHDXYb1_DDSgDsobPsOFxpAVMUG5yfZKSsUc&start_radio=1")

    # --- SALIR ---
    elif "salir" in comando:
        hablar("Hasta luego, cuídate.")
        return False

    else:
        hablar("Aún no tengo ese comando programado.")
    return True

def iniciar():
    hablar("Asistente iniciado. Puedes decir 'hey asistente' si quieres, y luego tu pregunta.")
    activo = True
    while activo:
        comando = escuchar()
        if comando:
            activo = procesar(comando)

iniciar()