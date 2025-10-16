# Demojifier Project 🚀


# 🔎 Overview
Demojifier is a web application that converts text containing emojis into their English meanings using both rules-based heuristics and an LLM (Large Language Model) backend. The project consists of a Python FastAPI backend and a simple HTML/JavaScript frontend.



## 📌 Table of Contents
- [Overview](#-Overview)
- [Features](#-features)
- [Project-Structure](#️-project-structure)
- [Getting-Started](#️-getting-started)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Customization](#️-customization)
- [Documentation](#-documentation)
- [Testing](#-testing)
- [License](#️-license)
- [Credits](#-credits)
- [Contributors](#-Contributors)


## ✅ Features
- Convert emojis to English text
- Two conversion modes: rules-only and LLM
- Simple web interface
- REST API support

## 🗂️ Project Structure
```
Warmup project/
├── backend/
│   ├── demojify_lib.py      # Core emoji conversion logic
│   ├── main.py              # FastAPI backend server
│   ├── llm_test_script.py   # Standalone test script
│   ├── requirements.txt     # Python dependencies
│   └── __pycache__/         # Python cache files
├── frontend/
│   └── index.html           # Web frontend
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

- Paste text with emojis into the web app and click "Convert"
- Choose "rules only" for offline conversion, or "auto" for LLM + rules fallback
- The output will show the converted text and the source (llm or standard)


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

## 📚 Documentation
Read the **[Meeting Notes](https://docs.google.com/document/d/1DLak7VWDhTTRcfv64Gbn3qyaIHMTnSWEAE6VK-vTGZk/edit?usp=sharing)** to follow our project discussion history  
View the **[Presentation Slides](https://docs.google.com/presentation/d/1Z6JvXAd2ZDwGjGqeZTaM_HdVlnZxKXbSda8f-Um7mF0/edit)** for project summary and results  
Read the **[Technical Overview](https://drive.google.com/file/d/1XLBwsODNhjaRPGjTNb2JogixVMo3hJyE/view?usp=sharing)** to learn how the Demojifier pipeline works

Read the **Full Project Workflow**


## 🧪 Testing

- Run `peter_colab.py` for standalone testing of the conversion logic

## ⚖️ License
This project is licensed under the **MIT License**.

## 💼 Credits

- **Backend** built with **FastAPI**, **Pydantic**, and the **emoji** Python package  
- **Frontend** developed using **HTML/CSS/JavaScript**

## 🧑‍💻 Contributors
<p align="left">
  <a href="https://github.com/adityamelkote"><img src="https://avatars.githubusercontent.com/adityamelkote" width="50" style="border-radius:50%" alt="@adityamelkote" /></a>
  <a href="https://github.com/abhishekdhakaab"><img src="https://avatars.githubusercontent.com/abhishekdhakaab" width="50" style="border-radius:50%" alt="@abhishekdhakaab" /></a>
  <a href="https://github.com/ansarav"><img src="https://avatars.githubusercontent.com/ansarav" width="50" style="border-radius:50%" alt="@ansarav" /></a>
  <a href="https://github.com/dttran0"><img src="https://avatars.githubusercontent.com/dttran0" width="50" style="border-radius:50%" alt="@dttran0" /></a>
  <a href="https://github.com/pandrew99"><img src="https://avatars.githubusercontent.com/pandrew99" width="50" style="border-radius:50%" alt="@pandrew99" /></a>
  <a href="https://github.com/Siirui"><img src="https://avatars.githubusercontent.com/Siirui" width="50" style="border-radius:50%" alt="@Siirui" /></a>
  <a href="https://github.com/Bobby-Zhu"><img src="https://avatars.githubusercontent.com/Bobby-Zhu" width="50" style="border-radius:50%" alt="@Bobby-Zhu" /></a>
  <a href="https://github.com/kkimmmi"><img src="https://avatars.githubusercontent.com/kkimmmi" width="50" style="border-radius:50%" alt="@kkimmmi" /></a>
  <a href="https://github.com/YukiWu7"><img src="https://avatars.githubusercontent.com/YukiWu7" width="50" style="border-radius:50%" alt="@YukiWu7" /></a>
  <a href="https://github.com/cyang406"><img src="https://avatars.githubusercontent.com/cyang406" width="50" style="border-radius:50%" alt="@cyang406" /></a>
</p>
