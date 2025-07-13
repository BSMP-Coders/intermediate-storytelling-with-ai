# Activity - Voice to Text Transcription: Record, download, and transcribe your voice using Azure AI Speech Services

## Summary

In this activity, you'll learn how to use a Streamlit web application to record your voice, download the audio file, and then use Azure AI Speech Services to transcribe the audio to text. This hands-on exercise demonstrates how AI can convert spoken language into written text, a fundamental technology behind virtual assistants, closed captioning, and other speech-enabled applications. By the end, you'll understand how to work with audio recording, file handling, and cloud-based speech recognition services.

![Speech to Text Process](https://aka.ms/azai/vision/speech-to-text-diagram)

## Prerequisites

Before beginning this activity, ensure you have:

1. **Working microphone**: Your device must have a functioning microphone for audio recording
2. **Azure Speech Services setup**: You need an Azure account with Speech Services enabled
3. **Environment variables**: Create a `.env` file based on the `.env.sample` with these variables:
   ```
   AZURE_SPEECH_KEY=your_speech_key_here    # Your Azure Speech Service API key
   AZURE_ENDPOINT=your_endpoint_here        # Your Azure Speech Service endpoint URL
   AZURE_REGION=your_region_here            # Your Azure region (e.g., eastus, westeurope)
   ```
4. **Web browser**: Modern browser with JavaScript enabled
5. **Stable internet connection**: Required for API calls to Azure services

## Activity Steps

1. **Launch the Speech-to-Text Application**: Begin by launching the application using VS Code:

   ```bash
   # Open VS Code's Run and Debug panel (Ctrl+Shift+D)
   # Select "Streamlit: Audio Recorder App" from the dropdown
   # Click the green play button or press F5
   ```

   The application will open in your default web browser at http://localhost:8501

2. **Record Your Voice**: Use the application to record a 30-second audio clip:

   - Click the "Click to record" button in the Audio Recorder section
   - Speak clearly into your microphone for up to 20 seconds
   - Talk about what you learned about AI in this course so far
   - Click the button again to stop recording
   - Verify your recording by listening to the playback

3. **Download the Audio File**: Save your recording to your local device:

   - Find the "Download Recording" section below the audio player
   - Click the "Download WAV File" link
   - Note where the file is saved on your computer

4. **Upload Your Recording**: Now upload the same file for transcription:

   - Scroll down to the "Upload Audio for Transcription" section
   - Select your preferred language from the dropdown menu (Skip the voice selection)
   - Click "Browse files" or drag and drop your downloaded WAV file
   - Verify that the file appears in the upload area

5. **Transcribe Your Audio**: Use Azure AI to convert your speech to text:

   - Click the "Transcribe Audio" button
   - Wait for the Azure Speech Service to process your audio
   - Review the transcription results that appear on the screen
   - Notice how accurately (or inaccurately) your speech was transcribed
   - Note any words or phrases that weren't recognized correctly
   - Consider factors that might affect accuracy (accent, background noise, speaking clarity)

## Extended Learning

1. **Try Different Languages**: If you speak multiple languages, try recording in different languages and see how well the transcription works.

2. **Experiment with Voice Styles**: Record the same text using different speaking styles (fast, slow, whispered, etc.) and compare the transcription accuracy.

3. **Improve Your Prompts**: Just like with image generation, clear and well-structured speech improves results. Try organizing your thoughts before recording for better transcription.

4. **Text-to-Speech Application**: After completing this activity, try the text-to-speech application to convert written text back into spoken audio, creating a full circle of voice transformation.

## Reflection Questions

1. How accurate was the transcription compared to what you actually said?
2. What factors might affect the accuracy of speech-to-text conversion?
3. What practical applications can you imagine for this technology?
4. How might this technology be improved in the future?
5. What ethical considerations should be taken into account when using speech recognition technology?

## Seeing an error?
1. If it looks like this [error message](../media/error-missing-config.png). Make sure your env file exists in the same folder as the text-to-speech.py file. You may have to restart the program once you make a change.