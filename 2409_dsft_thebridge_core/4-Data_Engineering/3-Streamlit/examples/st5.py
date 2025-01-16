import streamlit as st

# Título de la aplicación
st.title("Reproductor de Video y Audio en Streamlit")

# Cargar un video de YouTube
st.header("Reproductor de Video de YouTube")
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # URL del video de YouTube
st.video(video_url)

# Reproductor de Audio
st.header("Reproductor de Audio")
audio_file = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"  # URL del archivo de audio
st.audio(audio_file, format="audio/mp3")

# Instrucciones
st.write("""
    Puedes interactuar con el reproductor de YouTube y escuchar el archivo de audio mientras exploras la aplicación.
""")