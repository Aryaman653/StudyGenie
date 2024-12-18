# StudyGenie: Your Ultimate Study Assistant

StudyGenie is an AI-powered personal study assistant that helps students with summarizing notes, explaining complex topics, generating practice questions, and more. Built using Streamlit and Langchain, StudyGenie provides a range of study-related tools to improve learning efficiency and productivity.

## Features

- **Summarizing Notes**: Automatically summarizes uploaded PDFs for easy revision.
- **Explaining Concepts**: Get detailed, easy-to-understand explanations of complex topics.
- **Generating Practice Questions**: Create multiple-choice questions (MCQs), statement-based questions, and assertion-reasoning questions for self-assessment.
- **Flashcards**: Generate flashcards for better retention and quick review.
- **Study Plans**: Get personalized study schedules based on study time and topics.
- **YouTube Notes**: Generate detailed notes from YouTube videos to improve comprehension.
- **Essay Generation**: Create essays on any topic with a word limit and proper formatting.

## Tech Stack

- **Streamlit**: Framework for building the web application.
- **Langchain**: A library for building applications with large language models (LLMs).
- **Groq API**: Used for running models like Gemma2-9b-It.
- **PyPDFLoader**: Extracts text from uploaded PDF files.
- **Validators**: Ensures valid URLs for YouTube video links.
- **Dotenv**: Manages environment variables (like the Groq API key).

## Installation

To run StudyGenie locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/StudyGenie.git
How to Use
Enter your Groq API key in the sidebar to proceed.
Upload a PDF file (for summarizing) or provide a YouTube URL (for generating notes from a video).
Choose one of the following options:
Summarize Notes
Write Essay
Explain Concept
Generate Practice Questions (MCQ, Statement-based, or Assertion-Reasoning)
Generate Flashcards
Generate Study Planner
Generate Notes from YouTube Video
Example Usage
Summarize Notes: Upload a PDF document, and StudyGenie will summarize the key points for easy revision.
Explain Concept: Enter a topic (e.g., "Newton's Laws of Motion"), and get a concise explanation.
Generate Questions: Enter a topic, and StudyGenie will generate MCQs or other types of practice questions.
Contributing
Feel free to fork the repository, create a new branch, and submit a pull request with your contributions. Whether it's bug fixes, new features, or improvements, your help is appreciated!

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Langchain and Groq for powering the language models.
Streamlit for providing an easy way to create web apps.
PyPDFLoader for PDF extraction.
sql
Copy code
