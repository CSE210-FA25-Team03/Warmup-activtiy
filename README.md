# Demojifier Project 🚀


<p align="center">
  <img src="https://github.com/user-attachments/assets/5a568e5f-443a-4d93-bc11-084a28b4f561"
       alt="Demo Screenshot"
       width="700">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1ab3d6cf-22d3-4f7b-b196-8b7ee96393ba" alt="Demo Screenshot" width="700">
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
Warmup project/
├── backend/
│   ├── demojify_lib.py      # Core emoji conversion logic
│   ├── main.py              # FastAPI backend server
│   ├── requirements.txt     # Python dependencies
│   └── __pycache__/         # Python cache files
├── frontend/
│   └── index.html           # Web frontend
|   └── script.js            # Frontend logic
|   └── style.css            # Stylesheet
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



## 📚 Documentation
Read the **[Meeting Notes](https://docs.google.com/document/d/1DLak7VWDhTTRcfv64Gbn3qyaIHMTnSWEAE6VK-vTGZk/edit?usp=sharing)** to follow our project discussion history  
Read the **[Presentation Slides](https://docs.google.com/presentation/d/1Z6JvXAd2ZDwGjGqeZTaM_HdVlnZxKXbSda8f-Um7mF0/edit)** for project summary and results  
Read the **[Technical Workflow](https://drive.google.com/file/d/1XLBwsODNhjaRPGjTNb2JogixVMo3hJyE/view?usp=sharing)** to learn how the Demojifier pipeline works

Read the **[Full Project Recap](https://docs.google.com/document/d/1w93eijPeWnHzrmrYtTznc84b64LylgV1/edit?usp=sharing&ouid=108800923190919022098&rtpof=true&sd=true)** for more project details.

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
