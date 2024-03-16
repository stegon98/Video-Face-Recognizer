# Usa un'immagine di Ubuntu come base
FROM ubuntu:22.04

# Aggiorna i repository e installa Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip


# Imposta il working directory all'interno del container
WORKDIR /app

# Copia i file necessari nell'immagine del container
COPY requirements.txt .
COPY mainV2.py .


# Installa le dipendenze del progetto
RUN mkdir output
RUN mkdir img
RUN mkdir video
RUN apt update
#RUN apt install build-essential checkinstall zlib1g-dev libssl-dev -y
RUN apt install cmake -y
RUN pip install --no-cache-dir -r requirements.txt

ENV VIDEO_DIR "/app/video"
ENV IMG_DIR "/app/img"


# Comando di esecuzione predefinito quando il container viene avviato
CMD [ "python", "./mainV2.py" ]
