import os
import base64
import io
import tempfile
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from audiorecorder import audiorecorder

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Audio Recorder App",
    page_icon="🎙️",
    layout="centered"
)

# Create a function to generate a download link


def get_binary_file_downloader_html(bin_data, file_label='File', file_name='recorded_audio.wav'):
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
st.markdown("<h1 class='main-header'>Browser Audio Recorder</h1>",
            unsafe_allow_html=True)
st.markdown("<p class='info-text'>Record audio directly in your browser and download it as a WAV file.</p>",
            unsafe_allow_html=True)

# Audio recorder component
st.markdown("<h2 class='sub-header'>Record Audio</h2>", unsafe_allow_html=True)

# Configure audio recorder with custom parameters
# Create an instance of the audio recorder and capture the recording directly
audio_bytes = audiorecorder("Click to record", "Recording... Click to stop")

# Instructions
with st.expander("How to use this app"):
    st.markdown("""
    1. Click the microphone button to start recording audio
    2. Speak into your device's microphone
    3. Click the microphone button again to stop recording
    4. Use the download button to save your recording as a WAV file
    """)

# Display and allow download if audio is recorded
if audio_bytes:
    # Display success message and audio player
    st.markdown("<p class='info-text'>Recording captured successfully!</p>",
                unsafe_allow_html=True)

    # Convert AudioSegment to wav bytes
    wav_bytes = io.BytesIO()
    audio_bytes.export(wav_bytes, format="wav")
    wav_bytes = wav_bytes.getvalue()

    # Display audio playback
    st.audio(wav_bytes, format="audio/wav")

    # Provide download button for the recorded audio
    st.markdown("<h3>Download Recording</h3>", unsafe_allow_html=True)
    st.markdown(get_binary_file_downloader_html(
        # Save to file option
        wav_bytes, "Download WAV File", "recorded_audio.wav"), unsafe_allow_html=True)
    if st.button("Save to file on server"):
        timestamp = st.session_state.get("recording_count", 0) + 1
        st.session_state["recording_count"] = timestamp

        filename = f"recording_{timestamp}.wav"
        save_path = os.path.join(os.path.dirname(__file__), filename)

        # Export the AudioSegment directly to a file
        audio_bytes.export(save_path, format="wav")

        st.success(f"Audio saved to {save_path}")

else:
    st.info("Click the microphone button above to start recording audio")

# Add a file uploader for transcription
st.markdown("<h2 class='sub-header'>Upload Audio for Transcription</h2>",
            unsafe_allow_html=True)

# Define voice options
voice_options = {
    "en-US": ["en-US-JennyNeural", "en-US-GuyNeural", "en-US-AriaNeural"],
    "en-GB": ["en-GB-SoniaNeural", "en-GB-RyanNeural"],
    "es-ES": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural"],
    "fr-FR": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural"],
    "de-DE": ["de-DE-KatjaNeural", "de-DE-ConradNeural"]
}

# Language selection for transcription
selected_language = st.selectbox(
    "Select language for transcription:",
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

uploaded_file = st.file_uploader("Choose a WAV file", type="wav")


def transcribe_audio(audio_file, language):
    """Transcribe audio file using Azure Speech Services"""
    try:
        # Get Azure credentials from environment variables
        speech_key = os.environ.get('AZURE_SPEECH_KEY')
        speech_region = os.environ.get('AZURE_REGION', 'eastus')

        # Validate Azure credentials
        if not speech_key or speech_key.startswith("your_") or speech_key == "":
            return "Error: Valid Azure Speech Key not found in environment variables. Please check your .env file."

        if not speech_region:
            return "Error: Azure Region not specified. Please check your .env file."

        # Debug information
        st.sidebar.markdown("### Debug Info")
        key_preview = speech_key[:3] + "..." + \
            speech_key[-3:] if speech_key else "Not found"
        st.sidebar.info(f"Region: {speech_region}, Key: {key_preview}")

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_file.write(audio_file.getvalue())
            temp_file_path = temp_file.name
            # Configure speech recognition
        try:
            speech_config = speechsdk.SpeechConfig(
                subscription=speech_key, region=speech_region)
            speech_config.speech_recognition_language = language

            # Create audio configuration using the temporary file
            audio_config = speechsdk.audio.AudioConfig(filename=temp_file_path)

            # Create speech recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, audio_config=audio_config)

            # Start recognition with explicit timeout handling
            result_future = speech_recognizer.recognize_once_async()
            st.sidebar.info("Connecting to Azure Speech Service...")
            result = result_future.get()

            # Clean up temporary file
            os.unlink(temp_file_path)
        except Exception as config_error:
            if "401" in str(config_error) or "WebSocket upgrade failed: Authentication error" in str(config_error):
                return "Error: Authentication failed with Azure Speech Service. Please check your subscription key and region."
            else:
                return f"Error during speech configuration: {str(config_error)}"

        # Process result
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized"
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation = result.cancellation_details
            if cancellation.reason == speechsdk.CancellationReason.Error:
                return f"Error: {cancellation.error_details}"
            else:
                return f"Canceled: {cancellation.reason}"
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"


# Process uploaded file
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(uploaded_file, selected_language)

        st.markdown("<h3>Transcription Result</h3>", unsafe_allow_html=True)
        st.write(transcription)

        # Save transcription to file
        if st.button("Save Transcription to File"):
            timestamp = st.session_state.get("transcription_count", 0) + 1
            st.session_state["transcription_count"] = timestamp

            filename = f"transcription_{timestamp}.txt"
            save_path = os.path.join(os.path.dirname(__file__), filename)

            with open(save_path, "w") as f:
                f.write(transcription)

            st.success(f"Transcription saved to {save_path}")

# Display app information in sidebar
with st.sidebar:
    st.markdown("## About")
    st.markdown(
        "This app allows you to record audio directly in your browser or upload audio files for transcription.")
    st.markdown("### Features")
    st.markdown("- Browser-based recording")
    st.markdown("- WAV file download")
    st.markdown("- Audio transcription with multiple language options")
    st.markdown("- Voice selection for future text-to-speech")

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
