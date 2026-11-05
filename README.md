# 🚀 Smart Resume AI

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)
![Gemini AI](https://img.shields.io/badge/AI-Gemini%20Pro-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Smart Resume AI** is a powerful, AI-driven application designed to revolutionize the job application process. It combines advanced natural language processing with a modern, intuitive interface to help users create ATS-optimized resumes, analyze their existing resumes against job descriptions, and find relevant job opportunities across multiple platforms.

---

## ✨ Key Features

### 🤖 AI Resume Analysis
*   **Deep Analysis**: Utilizes Google Gemini AI (or OpenAI) to provide a comprehensive review of your resume.
*   **ATS Scoring**: Calculates a detailed ATS (Applicant Tracking System) score based on keywords, formatting, and content.
*   **Actionable Feedback**: Identifies missing skills, formatting issues, and provides specific recommendations for improvement.
*   **Job Matching**: Compares your resume against specific job descriptions to calculate a match percentage and identify gaps.

### 📝 Smart Resume Builder
*   **Multiple Templates**: Choose from **Modern**, **Professional**, **Minimal**, and **Creative** templates.
*   **Real-time Preview**: See changes instantly as you input your details.
*   **PDF Generation**: Export your polished resume as a high-quality PDF.
*   **AI Assistance**: Get AI-powered suggestions for your professional summary and experience bullet points.

### 🔍 Job Search Engine
*   **Aggregated Search**: Search for jobs across multiple platforms (LinkedIn, Indeed, etc.) from a single interface.
*   **LinkedIn Scraper**: Built-in tool to scrape real-time job listings directly from LinkedIn.
*   **Market Insights**: Visualize trending skills, top locations, and salary insights for your target role.
*   **Smart Filters**: Filter jobs by experience level, salary range, and job type.

### 📊 Analytics Dashboard
*   **User Metrics**: Track your resume scores, improvement trends, and application history.
*   **Skill Distribution**: Visualize your skill set and identify areas for growth.
*   **Admin Panel**: (For administrators) Monitor system usage, user statistics, and export data to Excel/CSV/JSON.

---

## 🛠️ Technology Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) (Python-based web framework) with custom CSS/HTML components.
*   **Backend**: Python 3.11+
*   **AI/ML**: 
    *   [Google Gemini](https://deepmind.google/technologies/gemini/) (Generative AI)
    *   [OpenAI](https://openai.com/) (Optional alternative)
    *   [NLTK](https://www.nltk.org/) & [Spacy](https://spacy.io/) (NLP)
*   **Database**: SQLite (Lightweight, serverless database)
*   **Tools & Libraries**:
    *   `selenium`: For web scraping (Job Search).
    *   `pdf2image` & `poppler`: For converting PDF resumes to images.
    *   `pytesseract` & `tesseract-ocr`: For extracting text from image-based resumes.
    *   `plotly`: For interactive charts and graphs.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
2.  **Google Chrome**: Required for the Selenium-based job scraper.
3.  **Poppler**: Required for PDF processing.
4.  **Tesseract OCR**: Required for image text extraction.

---

## 🚀 Installation Guide

### 1. Clone the Repository
```bash
git clone <repository-url>
cd resume-analyzer
```

### 2. Install System Dependencies

#### Windows
1.  **Poppler**:
    *   Download the latest binary from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/).
    *   Extract the zip file.
    *   Add the `bin` folder (e.g., `C:\Program Files\poppler-xx\bin`) to your System **PATH**.
2.  **Tesseract**:
    *   Download the installer from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
    *   Run the installer and complete the setup.
    *   Add the installation directory (e.g., `C:\Program Files\Tesseract-OCR`) to your System **PATH**.

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr libtesseract-dev
```

#### macOS
```bash
brew install poppler tesseract
```

### 3. Install Python Dependencies
We recommend using `uv` for faster and more reliable package management, but `pip` works as well.

**Using `uv` (Recommended):**
```bash
# Install uv if you haven't already
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

**Using `pip`:**
```bash
python -m venv venv
# Activate venv (same as above)
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:

```env
# Required for AI Analysis
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional: For OpenAI integration
OPENAI_API_KEY=your_openai_api_key

# Optional: For database configuration (defaults to local SQLite)
DB_PATH=resume_database.db
```

---

## ▶️ Running the Application

### Local Development
Once dependencies are installed and the environment is configured, run the app:

```bash
streamlit run app.py
```
The application will open in your default browser at `http://localhost:8501`.

### Docker Deployment
You can also run the application using Docker.

1.  **Build the image:**
    ```bash
    docker build -t resume-analyzer .
    ```
2.  **Run the container:**
    ```bash
    docker run -p 8501:8501 --env-file .env resume-analyzer
    ```

---

## 📂 Project Structure

```
resume-analyzer/
├── app.py                  # Main Streamlit application entry point
├── ui_components.py        # Reusable UI components (cards, headers, etc.)
├── requirements.txt        # Python dependencies
├── packages.txt            # System dependencies (for Streamlit Cloud)
├── Dockerfile              # Docker configuration
├── DEPLOYMENT.md           # Detailed deployment instructions
├── utils/                  # Core utility modules
│   ├── ai_resume_analyzer.py   # AI analysis logic (Gemini/OpenAI)
│   ├── resume_analyzer.py      # Standard rule-based analysis
│   ├── resume_builder.py       # Resume generation logic
│   ├── db_manager.py           # Database interactions
│   └── ...
├── jobs/                   # Job search functionality
│   ├── job_search.py           # Search engine logic
│   ├── linkedin_scraper.py     # LinkedIn scraping module
│   └── ...
├── dashboard/              # Analytics dashboard
│   └── dashboard.py            # Dashboard rendering and metrics
└── assets/                 # Static assets (images, styles)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📚 Additional Resources

*   **[HR Interview Questions Guide](hr-interview-questions.md)**: Comprehensive guide with common HR interview questions and sample answers to help you prepare for job interviews.
*   **[Dependencies Explanation](DEPENDENCIES.md)**: Detailed breakdown of all project dependencies, their purposes, and installation requirements.

## 🙏 Acknowledgments

*   Built with [Streamlit](https://streamlit.io/)
*   Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
*   PDF processing by [Poppler](https://poppler.freedesktop.org/)
