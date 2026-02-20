# 🚀 AI Content Rewriter Backend

A powerful Django REST API that rewrites text using multiple AI providers (Groq, OpenRouter) with automatic fallback, along with authentication, history tracking, and voice features.

---

## ✨ Features

* 🔐 JWT Authentication (Register/Login)
* 🤖 AI Content Rewriting
  * Groq 
  * OpenRouter 
* 📜 Rewrite History Management
* 📄 Export Rewritten Content as PDF
* 🎙️ Speech-to-Text (AI transcription)
* 🌍 Multi-language support
* 🔁 API Key Rotation support

---

## 🛠️ Tech Stack

* **Backend:** Django, Django REST Framework
* **Database:** MySQL
* **Authentication:** JWT (SimpleJWT)
* **AI APIs: Groq, OpenRouter
* **Others:** drf-yasg (Swagger), gTTS, ReportLab

---

## 📂 Project Structure

```
content_rewriter_backend/
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│
├── core/
│   ├── views.py
│   ├── models.py
│   ├── serializers.py
│   ├── utils.py
│   ├── voice.py
│   ├── exports.py
│
├── .env
├── requirements.txt
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/content-rewriter-backend.git
cd content-rewriter-backend
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup `.env` file

Create `.env` in root:

```env
SECRET_KEY=your_secret_key

# Groq (comma separated)
GROQ_API_KEYS=key1,key2,key3,key4

# OpenRouter (comma separated)
OPENROUTER_API_KEYS=key1,key2,key3,key4
```

---

### 5️⃣ Run migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Run server

```bash
python manage.py runserver
```

---

## 🔑 Authentication Flow

### Register

```
POST /api/register/
```

### Login

```
POST /api/login/
```

➡️ Returns:

* access token
* refresh token

---

## 📌 API Endpoints

| Endpoint                    | Method | Description    |
| --------------------------- | ------ | -------------- |
| `/api/register/`            | POST   | Register user  |
| `/api/login/`               | POST   | Login          |
| `/api/rewrite/`             | POST   | Rewrite text   |
| `/api/history/`             | GET    | Get history    |
| `/api/history/save/`        | POST   | Save history   |
| `/api/delete-history/<id>/` | DELETE | Delete history |
| `/api/export/pdf/<id>/`     | GET    | Download PDF   |
| `/api/speech-to-text/`      | POST   | Audio → Text   |

---

## 🧪 Testing (Postman)

👉 Add Header:

```
Authorization: Bearer <your_access_token>
```

---

## 📘 API Documentation

* Swagger UI → `/swagger/`
* Redoc → `/redoc/`

---

## ⚠️ Notes

* Do NOT push `.env` file
* API keys are rate-limited → rotation implemented
* Gemini free tier may hit quota limits

---

## 🚀 Future Improvements

* Rate limiting per user
* AI model selection from frontend
* Deployment (Railway / AWS)
* Caching responses

---

## 👨‍💻 Author

**Abhishek**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
