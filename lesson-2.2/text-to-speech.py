# filepath: /workspaces/intermediate-storytelling-with-ai/lesson-2.2/text-to-speech.py
import os
import base64
import io
import tempfile
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Text to Speech App",
    page_icon="🔊",
    layout="centered"
)

# Create a function to generate a download link


def get_binary_file_downloader_html(bin_data, file_label='File', file_name='synthesized_audio.wav'):
    """
    Generate a link that allows the user to download binary data as a file
    """
    b64 = base64.b64encode(bin_data).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="{file_name}">{file_label}</a>'
    return href


# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1E88E5;
    margin-bottom: 1rem;
}
.sub-header {
    font-size: 1.5rem;
    color: #424242;
    margin-bottom: 1rem;
}
.info-text {
    font-size: 1.1rem;
    color: #424242;
    margin-bottom: 1.5rem;
}
.success-box {
    background-color: #E3F2FD;
    border-left: 5px solid #1E88E5;
    padding: 1rem;
    border-radius: 5px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>Text to Speech Converter</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='info-text'>Convert text to speech using Azure AI voices.</p>",
            unsafe_allow_html=True)

# Define voice options
voice_options = {
    "en-US": ["en-US-JennyNeural", "en-US-GuyNeural", "en-US-AriaNeural", "en-US-DavisNeural"],
    "en-GB": ["en-GB-SoniaNeural", "en-GB-RyanNeural", "en-GB-LibbyNeural"],
    "es-ES": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural", "es-ES-AbrilNeural"],
    "fr-FR": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural", "fr-FR-EloiseNeural"],
    "de-DE": ["de-DE-KatjaNeural", "de-DE-ConradNeural", "de-DE-AmalaNeural"]
}

# Language selection
st.markdown("<h2 class='sub-header'>Select Voice</h2>", unsafe_allow_html=True)

# Language selection for speech synthesis
selected_language = st.selectbox(
    "Select language:",
    options=list(voice_options.keys()),
    format_func=lambda x: {
        "en-US": "English (US)",
        "en-GB": "English (UK)",
        "es-ES": "Spanish",
        "fr-FR": "French",
        "de-DE": "German"
    }.get(x, x)
)

# Voice selection based on chosen language
selected_voice = st.selectbox(
    "Select voice:",
    options=voice_options[selected_language]
)

# Display example text based on language
example_texts = {
    "en-US": "Hello! This is an example of text-to-speech using Azure AI.",
    "en-GB": "Hello! This is an example of text-to-speech using Azure AI.",
    "es-ES": "¡Hola! Este es un ejemplo de texto a voz usando Azure AI.",
    "fr-FR": "Bonjour! Voici un exemple de synthèse vocale utilisant Azure AI.",
    "de-DE": "Hallo! Dies ist ein Beispiel für Text-zu-Sprache mit Azure AI."
}

# Text input
st.markdown("<h2 class='sub-header'>Enter Text</h2>", unsafe_allow_html=True)
user_text = st.text_area("Text to convert to speech:",
                         value=example_texts[selected_language], height=150)


def synthesize_speech(text, language, voice_name):
    """Synthesize speech from text using Azure Speech Services"""
    try:
        # Get Azure credentials from environment variables
        speech_key = os.environ.get('AZURE_SPEECH_KEY')
        speech_region = os.environ.get('AZURE_REGION', 'eastus2')

        # Validate Azure credentials
        if not speech_key or speech_key.startswith("your_") or speech_key == "":
            return None, "Error: Valid Azure Speech Key not found in environment variables. Please check your .env file."

        if not speech_region:
            return None, "Error: Azure Region not specified. Please check your .env file."

        # Debug information
        st.sidebar.markdown("### Debug Info")
        key_preview = speech_key[:3] + "..." + \
            speech_key[-3:] if speech_key else "Not found"
        st.sidebar.info(f"Region: {speech_region}, Key: {key_preview}")

        # Create a temporary file to store the audio output
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file_path = temp_file.name
        temp_file.close()

        try:
            # Configure speech synthesis
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key, region=speech_region)
            speech_config.speech_synthesis_voice_name = voice_name

            # Create audio configuration with the specified output file
            audio_config = speechsdk.audio.AudioOutputConfig(
                filename=temp_file_path)

            # Create speech synthesizer
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )

            # Start synthesis
            st.sidebar.info("Connecting to Azure Speech Service...")
            result = speech_synthesizer.speak_text_async(text).get()

            # Process result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                # Read the audio file
                with open(temp_file_path, 'rb') as audio_file:
                    audio_data = audio_file.read()

                # Clean up temporary file
                os.unlink(temp_file_path)

                return audio_data, None
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    return None, f"Error: {cancellation.error_details}"
                else:
                    return None, f"Canceled: {cancellation.reason}"
            else:
                return None, "Unknown error during speech synthesis"

        except Exception as config_error:
            if "401" in str(config_error) or "WebSocket upgrade failed: Authentication error" in str(config_error):
                return None, "Error: Authentication failed with Azure Speech Service. Please check your subscription key and region."
            else:
                return None, f"Error during speech synthesis: {str(config_error)}"

    except Exception as e:
        return None, f"Error synthesizing speech: {str(e)}"


# Synthesis button
if st.button("Convert to Speech"):
    if not user_text.strip():
        st.error("Please enter some text to convert to speech.")
    else:
        with st.spinner("Converting text to speech..."):
            audio_data, error = synthesize_speech(
                user_text, selected_language, selected_voice)

        if error:
            st.error(error)
        else:
            st.success("Text converted to speech successfully!")

            # Play audio
            st.audio(audio_data, format="audio/wav")

            # Download option
            st.markdown("<h3>Download Audio</h3>", unsafe_allow_html=True)
            st.markdown(get_binary_file_downloader_html(
                audio_data, "Download WAV File", f"{selected_voice}.wav"),
                unsafe_allow_html=True
            )

            # Save to file option
            if st.button("Save to file on server"):
                timestamp = st.session_state.get("synthesis_count", 0) + 1
                st.session_state["synthesis_count"] = timestamp

                filename = f"synthesis_{timestamp}.wav"
                save_path = os.path.join(os.path.dirname(__file__), filename)

                with open(save_path, "wb") as f:
                    f.write(audio_data)

                st.success(f"Audio saved to {save_path}")

# Instructions
with st.expander("How to use this app"):
    st.markdown("""
    1. Select your desired language and voice from the dropdown menus
    2. Enter or paste the text you want to convert to speech
    3. Click the "Convert to Speech" button
    4. Listen to the synthesized audio
    5. Download the audio file or save it to the server
    """)

# Display app information in sidebar
with st.sidebar:
    st.markdown("## About")
    st.markdown(
        "This app converts text to speech using Azure AI Speech Services.")
    st.markdown("### Features")
    st.markdown("- Multiple languages and voices")
    st.markdown("- Natural-sounding neural voices")
    st.markdown("- WAV file download option")
    st.markdown("- Server-side file saving")

    # Display Azure configuration status
    st.markdown("## Configuration")
    azure_key = os.environ.get('AZURE_SPEECH_KEY')
    azure_region = os.environ.get('AZURE_REGION', 'eastus')

    if azure_key:
        st.success("Azure Speech Key: Configured")
    else:
        st.error("Azure Speech Key: Missing")

    st.info(f"Azure Region: {azure_region}")

    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit and Azure AI")
