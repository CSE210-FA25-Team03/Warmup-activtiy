# Demojifier Project 🚀


<p align="center">
  <img src="https://github.com/user-attachments/assets/5a568e5f-443a-4d93-bc11-084a28b4f561"
       alt="Demo Screenshot"
       width="700">
</p>


## 🔎 Overview
Demojifier is a web application that converts text containing emojis into their English meanings using both rules-based heuristics and an LLM (Large Language Model) backend. The project consists of a Python FastAPI backend and a simple HTML/JavaScript frontend.

## 📌 Table of Contents
- [Overview](#-Overview)
- [Features](#-features)
- [Project Structure](#️-project-structure)
- [Getting Started](#️-getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#-usage)
- [Example](#-example)
- [API Endpoints](#-api-endpoints)
- [Customization](#️-customization)
- [Testing](#-testing)
- [Documentation](#-documentation)
- [License](#️-license)
- [Credits](#-credits)
- [Contributors](#-contributors)




## ✅ Features
- Convert emojis to English text
- Two conversion modes: rules-only and LLM
- Simple web interface
- REST API support

## 🗂️ Project Structure
```
Warmup-Project/
├── backend/
│   ├── demojify_lib.py          # Core emoji conversion logic
│   ├── main.py                  # FastAPI backend server
│   ├── requirements.txt         # Python dependencies
│   ├── test/
│   │   └── test_demojify_api.py # Pytest-based API + logic unit tests
│   └── __pycache__/             # Python bytecode cache files (auto-generated)
├── frontend/
│   ├── index.html               # Web frontend
│   ├── script.js                # Frontend logic
│   └── style.css                # Stylesheet
├── docs/                        # Documents
│   ├── Full Project Recap.docx
│   ├── Technical Workflow.pdf
│   ├── Meeting Note.pdf
│   └── Presentation.pptx
├── pytest.ini                   # Pytest configuration (test discovery + options)
└── README.md                    # Project documentation (this file)
```

## 🛠️ Getting Started

### Backend Setup 
- Install Python 3.9+
- Install dependencies:
  ```
  pip install -r backend/requirements.txt
  ```
- Start the server:
  ```
  cd backend
  python main.py
  uvicorn main:app --reload --port 8000
  ```
- The API will run at `http://127.0.0.1:8000`
### Frontend Setup 
- Open `frontend/index.html` in your browser
- Or, after starting the backend, visit `http://127.0.0.1:8000/` (served by FastAPI)

## 🚀 Usage

- Paste text with emojis into the web app and click "Enter"
- The output will show the converted text and the source (llm or standard)
- Click "Clear" to reset the input box

## ✨ Example

**Input**

    That exam was 😭 but I finally passed 🎉

**Output (LLM Mode)**

    That exam was really tough, but I finally passed and I'm so relieved and happy.

**Output (Standard Mode)**

    That exam was (crying) but I finally passed (congrats)


## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/convert` | Convert emojis in text |
| GET    | `/health` | API health check |
| GET    | `/docs` | Interactive API docs (Swagger UI)|
| GET    | `/` or `/index` | Serves frontend |


## ⚙️ Customization

- Emoji mappings and rules are in `demojify_lib.py`
- LLM integration requires an API key (see environment variable `OPENAI_API_KEY`)


## 🧪 Testing

All tests are located in `backend/test/test_demojify_api.py` and executed with **pytest**.

**Test coverage includes:**
- Empty input validation  
- LLM acceptance, rejection, and error fallback  
- Standard mode bypass
- Emoji sanitization and output cleanup  
- Health endpoint contract check  
- Missing LLM client fallback  

Run all tests from the project root:

```bash
pytest -v
```


## 📚 Documentation
Read the **[Meeting Notes](docs/Meeting%20Note.pdf)** to follow our project discussion history  
Read the **[Presentation Slides](docs/Presentation.pptx)** for project summary and results  
Read the **[Technical Workflow](docs/Technical%20Workflow.pdf)** to learn how the Demojifier pipeline works  

Read the **[Full Project Recap](docs/Full%20Project%20Recap.docx)** for a full summary of the project

## ⚖️ License
This project is licensed under the **MIT License**.

## 💼 Credits

- **Backend** built with **FastAPI**, **Pydantic**, and the **emoji** Python package  
- **Frontend** developed using **HTML/CSS/JavaScript**

## 🤝 Contributors
**Team03 &lt;div&gt;ine coders**

- Abhishek Dhaka
- Aditya Melkote
- Andrew Pan
- Audria Montalvo
- Boqi Zhu
- Duc Khang Tran
- Gabrielle Kim
- Hongyi Pan
- Rui Sun
- Sriraksha Rajesh Rao
- Tongfei Yang
- Yuki Wu
- Yuting Wu
