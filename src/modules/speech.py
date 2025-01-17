import io
import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder

def transcribe_audio(audio_bio, max_retries=3):
    for _ in range(max_retries):
        try:
            transcript = st.session_state.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_bio,
            )
            return transcript.text
        except Exception as e:
            print(str(e))  
    return None

def stt(key="speech-to-text"):
    if '_last_speech_to_text_transcript_id' not in st.session_state:
        st.session_state._last_speech_to_text_transcript_id = 0
    
    if '_last_speech_to_text_transcript' not in st.session_state:
        st.session_state._last_speech_to_text_transcript = None
    
    if key and key + '_output' not in st.session_state:
        st.session_state[key + '_output'] = None

    col1, col2, col3 = st.columns([4, 3, 4])
    if st.session_state.openai_api_token:
        with col2:
            audio = mic_recorder(
                start_prompt="🎙️ Ask Your Question",
                stop_prompt="🚫 Stop recording",
                just_once=False,
                use_container_width=True,
                format="webm", 
                key=key
            )

        if audio is None:
            output = None
        else:
            id = audio['id']
            if id > st.session_state._last_speech_to_text_transcript_id:
                st.session_state._last_speech_to_text_transcript_id = id
                audio_bio = io.BytesIO(audio['bytes'])
                audio_bio.name = 'audio.webm'
                output = transcribe_audio(audio_bio)
                st.session_state._last_speech_to_text_transcript = output
            else:
                output = None

        if key:
            st.session_state[key + '_output'] = output
        
        return output


def generate_audio(text, id):
    response = st.session_state.openai_client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    output_path = f"audio/{id}.wav"
    response.stream_to_file(output_path)
    return output_path

def tts(text, title="blog"):
    if not os.path.exists("audio"):
        os.makedirs("audio")
    text = text[:4000]
    audio_file = generate_audio(text, title)
    return audio_file