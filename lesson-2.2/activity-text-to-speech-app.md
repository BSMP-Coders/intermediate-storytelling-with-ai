# Activity - Text to Speech Synthesis: Convert written text to spoken audio using Azure AI Speech Services

## Summary

In this activity, you'll learn how to use a Streamlit web application to convert written text into natural-sounding speech using Azure AI Speech Services. This hands-on exercise demonstrates how AI can transform text into spoken language, a key technology used in audiobooks, virtual assistants, navigation systems, and accessibility tools. By the end, you'll understand how to work with text-to-speech synthesis, voice selection, and audio file handling.

![Text to Speech Process](https://aka.ms/azai/vision/text-to-speech-diagram)

## Prerequisites

Before beginning this activity, ensure you have:

1. **Azure Speech Services setup**: You need an Azure account with Speech Services enabled
2. **Environment variables**: Create a `.env` file based on the `.env.sample` with these variables:
   ```
   AZURE_SPEECH_KEY=your_speech_key_here    # Your Azure Speech Service API key
   AZURE_ENDPOINT=your_endpoint_here        # Your Azure Speech Service endpoint URL
   AZURE_REGION=your_region_here            # Your Azure region (e.g., eastus, westeurope)
   ```
3. **Audio output device**: Speakers or headphones for listening to synthesized speech
4. **Web browser**: Modern browser with JavaScript enabled
5. **Stable internet connection**: Required for API calls to Azure services

## Activity Steps

1. **Launch the Text-to-Speech Application**: Begin by launching the application using VS Code:

   ```bash
   # Open VS Code's Run and Debug panel (Ctrl+Shift+D)
   # Select "Streamlit: Text to Speech App" from the dropdown
   # Click the green play button or press F5
   ```

   The application will open in your default web browser at http://localhost:8501

2. **Select a Voice**: Choose a language and voice that interests you:

   - In the "Select Voice" section, choose a language from the dropdown menu
   - Select one of the available neural voices for that language
   - Note how each language provides different voice options

3. **Enter Your Text**: Input the text you want to convert to speech:

   - In the "Enter Text" text area, you'll see an example text in your selected language
   - Replace it with your own text (a paragraph about your experience with AI)
   - Try to include a variety of sentence structures and punctuation
   - Keep it between 100-200 words for best results

4. **Convert to Speech**: Use Azure AI to synthesize speech from your text:

   - Click the "Convert to Speech" button
   - Wait for the Azure Speech Service to process your text
   - Listen to the synthesized audio that appears on the page
   - Pay attention to the naturalness of speech, pronunciation, and intonation

5. **Download the Audio**: Save the synthesized speech to your local device:

   - Find the "Download Audio" section below the audio player
   - Click the "Download WAV File" link
   - Note where the file is saved on your computer

6. **Experiment and Compare**: Try different voices and text variations:

   - Change to a different language and voice
   - Try the same text with different voices
   - Try different text with the same voice
   - Notice how the synthesis quality varies between languages and voices

## Extended Learning

1. **Create a Dialogue**: Write a conversation between two characters and synthesize each part with a different voice.

2. **Language Learning**: If you're learning another language, try synthesizing phrases to hear proper pronunciation.

3. **Narrative Reading**: Create a short story and convert it to an audiobook format using appropriate voices.

4. **Complete the Loop**: Take the transcription from your previous speech-to-text activity, make edits if needed, and convert it back to speech.

## Reflection Questions

1. How natural did the synthesized speech sound? Could you tell it was AI-generated?
2. Which voices or languages sounded most natural to you? Why do you think that is?
3. How might text-to-speech technology be useful in your daily life or work?
4. What are the limitations you noticed with the current technology?
5. What ethical considerations arise from the ability to synthesize human-sounding speech?