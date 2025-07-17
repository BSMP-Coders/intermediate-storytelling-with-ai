# GitHub Copilot Instructions for BAM Summer Mentorship Program - Intermediate Storytelling with AI

## Important Note on Student Devices

**All students will be using Windows machines.**

- When providing instructions, code, or keyboard shortcuts, always ensure they are applicable to Windows systems or to GitHub Codespaces accessed with a Windows keyboard layout.
- Avoid recommending Mac-specific commands, shortcuts, or tools unless they are also valid on Windows.
- If suggesting terminal commands, use Windows Command Prompt, PowerShell, or Windows-compatible instructions, or specify if the command is for Codespaces.
- For Codespaces, assume students are using a Windows keyboard and highlight any differences in shortcuts or behavior if relevant.

## Workspace Structure
This repository contains materials for the "Intermediate Storytelling with AI" program, which is organized as a 3-lesson curriculum exploring the intersection of AI and creative storytelling:

- `lesson-2.1/`: AI Image and Text Generation
  - Focus: AI image generation tools, advanced prompting techniques, visual narratives
  - Topics: DALL-E, Midjourney, Stable Diffusion, Azure AI Image Creator, prompt engineering
  - Projects: Digital self-portraits, executive summaries with AI imagery, logo creation
  - Key files: `activity-create-a-digita-self-portrait.md`, `activity-create-an-executive-summary.md`, `activity-image-gallery-app.md`
  - Optional: Streamlit web app for image gallery (`my_gallery.py`)

- `lesson-2.2/`: Azure AI Services - Speech Integration & Responsible AI
  - Focus: Azure Speech Service, speech-to-text, text-to-speech, responsible AI principles
  - Topics: Real-time transcription, audio generation, AI ethics, bias detection
  - Projects: Speech-to-text applications, text-to-speech narration, responsible AI analysis
  - Key files: `activity-explore-ai-foundry-speech-text-services.md`, `activity-speech-to-text-app.md`, `activity-text-to-speech-app.md`, `activity-responsible-ai.md`
  - Python apps: `speech-to-text.py`, `text-to-speech.py`

- `lesson-2.3/`: Data Analysis in Python
  - Focus: Data analysis fundamentals, statistical analysis, data visualization
  - Topics: Python data analysis, pandas, seaborn, matplotlib, ethical AI evaluation
  - Projects: Weather data analysis, trend visualization, bias detection in AI content
  - Key files: `activities.md`, `washington_dc_weather_sample_2025.csv`
  - Python apps: `app.py` (template), `app_final.py` (complete example)

- `media/`: Contains images and graphics used throughout the lessons, including responsible AI principle icons

## Student Context
- Students have completed the introductory AI course and have basic programming knowledge
- The course focuses on intermediate-level AI applications in storytelling and creative content
- Students have access to Azure AI Foundry platform and Azure subscriptions
- Each lesson builds upon previous knowledge, progressing from image generation to speech services to data analysis
- Students should complete projects and assessments to demonstrate mastery of AI storytelling techniques

## Azure AI Services Integration

**This course heavily utilizes Azure AI services and requires proper Azure authentication.**

- Students must have access to Azure AI Foundry platform and Azure subscriptions
- When working with Azure AI services, always check authentication and service availability
- Guide students to use Azure AI Image Creator, Azure Speech Service, and Azure OpenAI Service
- Emphasize responsible AI practices and ethical considerations in all AI implementations
- For Azure-related issues, direct students to Azure documentation and support resources

## Image and Media Guidelines for Streamlit Applications

**For any Streamlit web applications in this workspace, use the appropriate image folders.**

- For lesson-2.1 image gallery applications, use images stored in the `lesson-2.1/my_images/` folder
- When referencing images in Streamlit code for lesson-2.1, use the path `lesson-2.1/my_images/filename.ext`
- The `media/` folder contains educational content and responsible AI principle icons
- If generating or creating images for projects, save them to the appropriate lesson folder
- Guide students to organize their AI-generated content in the correct directories

Example Streamlit image usage for lesson-2.1:
```python
st.image("lesson-2.1/my_images/example.png", caption="AI Generated Image")
```

## Application Execution Guidelines

**Students should use VS Code's built-in Run and Debug functionality to execute their applications.**

- Avoid suggesting commands like `streamlit run`, `python app.py`, or similar execution commands
- Students are expected to use VS Code's Run and Debug features (F5 key or the Run button in VS Code)
- For Python applications, guide students to use VS Code's Python extension and integrated terminal
- For Streamlit applications, students should use VS Code's integrated terminal or debugging features
- Focus on code development and debugging rather than manual command-line execution

## When Assisting Students

1. **Identify the current lesson context** based on the folder structure and student's location
2. **For lesson-2.1 (AI Image and Text Generation):**
   - Focus on prompt engineering techniques and image generation best practices
   - Help with Azure AI Image Creator, DALL-E, and visual storytelling
   - Assist with creating compelling prompts for consistent visual narratives
   - Guide students in creating digital self-portraits and executive summaries

3. **For lesson-2.2 (Azure AI Services & Responsible AI):**
   - Emphasize Azure Speech Service integration and configuration
   - Help with real-time transcription and audio generation
   - Discuss responsible AI principles and bias detection
   - Guide students through Azure AI Foundry platform exploration

4. **For lesson-2.3 (Data Analysis in Python):**
   - Focus on data analysis fundamentals using pandas, seaborn, and matplotlib
   - Help with statistical analysis and data visualization
   - Guide students through weather data analysis and trend identification
   - Emphasize ethical considerations in AI-generated content evaluation

5. **General guidance:**
   - Encourage responsible AI practices throughout all lessons
   - Connect technical concepts to real-world storytelling applications
   - Provide Windows-compatible instructions and shortcuts
   - Keep explanations appropriate for intermediate-level students

## Azure AI and Responsible AI Emphasis

**This course prioritizes responsible AI development and ethical considerations.**

- Always discuss bias, fairness, and transparency when working with AI models
- Guide students to evaluate AI-generated content for potential biases
- Emphasize the importance of diverse and inclusive training data
- Discuss the ethical implications of AI in creative storytelling
- Reference the responsible AI principles covered in lesson-2.2

## Data Analysis and Visualization Best Practices

**For lesson-2.3 data analysis projects:**

- Encourage students to start with data understanding and cleaning
- Guide them through proper statistical analysis techniques
- Help with creating meaningful visualizations using seaborn and matplotlib
- Emphasize the importance of data context and storytelling with data
- Connect data analysis skills to evaluating AI-generated content for bias

## Windows Device Guidance

- All technical recommendations, troubleshooting steps, and keyboard shortcuts should be tailored for Windows users
- If a step differs between Windows and other operating systems, provide the Windows version first
- When referencing file paths, use Windows-style paths unless working in Codespaces
- For Azure services, guide students to use Azure portal and Azure AI Foundry through web browsers

## Project Context
This repository is part of the Blacks at Microsoft (BAM) Summer Mentorship Program, designed to teach intermediate-level AI applications in storytelling and creative content generation. Students learn to leverage Azure AI services while maintaining ethical and responsible AI practices throughout their creative projects.