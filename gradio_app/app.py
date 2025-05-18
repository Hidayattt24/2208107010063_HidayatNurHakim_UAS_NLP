import os
import tempfile
import requests
import gradio as gr
import scipy.io.wavfile

def voice_chat(audio):
    if audio is None:
        return None
    
    sr, audio_data = audio

    # simpan sebagai .wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        scipy.io.wavfile.write(tmpfile.name, sr, audio_data)
        audio_path = tmpfile.name

    # kirim ke endpoint FastAPI
    try:
        with open(audio_path, "rb") as f:
            files = {"file": ("voice.wav", f, "audio/wav")}
            response = requests.post("http://localhost:8000/voice-chat", files=files)

        if response.status_code == 200:
            # simpan file respons audio dari chatbot
            output_audio_path = os.path.join(tempfile.gettempdir(), "tts_output.wav")
            with open(output_audio_path, "wb") as f:
                f.write(response.content)
            return output_audio_path
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

# Custom CSS untuk tampilan yang lebih menarik dan full screen
custom_css = """
    .gradio-container {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        min-height: 100vh !important;
        max-width: none !important;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    .main-content {
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 2rem !important;
        min-height: 100vh !important;
        box-sizing: border-box !important;
    }
    
    .main-title {
        text-align: center !important;
        color: #2d3436 !important;
        font-size: 3.5em !important;
        margin-bottom: 0.5em !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
        padding: 20px !important;
    }
    
    .main-subtitle {
        text-align: center !important;
        color: #636e72 !important;
        font-size: 1.5em !important;
        margin-bottom: 2em !important;
        padding: 0 20px !important;
    }
    
    .contain {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        margin: 15px !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2) !important;
        backdrop-filter: blur(4px) !important;
        min-height: 400px !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    .custom-button {
        background: linear-gradient(45deg, #6c5ce7, #a363d9) !important;
        border: none !important;
        color: white !important;
        padding: 15px 30px !important;
        border-radius: 15px !important;
        font-size: 1.2em !important;
        font-weight: bold !important;
        margin-top: 20px !important;
        width: 100% !important;
        max-width: 300px !important;
        margin: 20px auto !important;
        cursor: pointer !important;
    }
    
    .tips-section {
        text-align: center !important;
        margin-top: 30px !important;
        padding: 25px !important;
        border-radius: 15px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .tips-section h3 {
        color: #2d3436 !important;
        font-size: 1.8em !important;
        margin-bottom: 15px !important;
    }
    
    .audio-component {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    .column-title {
        font-size: 1.8em !important;
        color: #2d3436 !important;
        margin-bottom: 20px !important;
        text-align: center !important;
    }

    /* Responsiveness for smaller screens */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5em !important;
        }
        .main-subtitle {
            font-size: 1.2em !important;
        }
        .contain {
            padding: 15px !important;
            margin: 10px !important;
        }
    }
"""

# UI Gradio dengan desain yang ditingkatkan untuk full screen
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_classes="main-content"):
        gr.Markdown("# 🎙️ Voice Chatbot AI Assistant", elem_classes="main-title")
        gr.Markdown(
            "Selamat datang di Voice Chatbot AI! Berbicara langsung melalui mikrofon Anda dan dapatkan respons suara yang natural.",
            elem_classes="main-subtitle"
        )

        with gr.Row(elem_classes="content-row"):
            with gr.Column(elem_classes="contain"):
                gr.Markdown("### 📝 Input Suara", elem_classes="column-title")
                with gr.Column(elem_classes="audio-component"):
                    audio_input = gr.Audio(
                        sources=["microphone"],
                        type="numpy",
                        label="Rekam Suara Anda"
                    )
                    submit_btn = gr.Button(
                        "🎯 Kirim Pesan",
                        elem_classes="custom-button"
                    )

            with gr.Column(elem_classes="contain"):
                gr.Markdown("### 🤖 Respons AI", elem_classes="column-title")
                with gr.Column(elem_classes="audio-component"):
                    audio_output = gr.Audio(
                        type="filepath",
                        label="Dengarkan Balasan"
                    )

        gr.Markdown(
            """
            ### 💡 Tips Penggunaan
            1. Klik tombol mikrofon untuk mulai merekam
            2. Bicara dengan jelas dan natural
            3. Klik stop ketika selesai
            4. Tekan 'Kirim Pesan' dan tunggu respons
            """,
            elem_classes="tips-section"
        )

    submit_btn.click(
        fn=voice_chat,
        inputs=audio_input,
        outputs=audio_output
    )

# Konfigurasi untuk tampilan full screen
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",  # Allows external access
        server_port=7860,       # Specific port
        share=False,            # Disable sharing since it's causing issues
        debug=True             # Enable debug mode for better error messages
    )