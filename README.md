
# EmmitrFit - AI-Powered Personal Health Coach

##  Table of Contents
1. [About The Project](#about-the-project)
2. [System Architecture](#system-architecture)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [Getting Started](#getting-started)
6. [API Documentation](#api-documentation)
7. [How It Works (Under the Hood)](#how-it-works)
8. [Project Structure](#project-structure)
9. [Contributing](#contributing)
10. [References](#references)

---

## About The Project

Standard workout apps often fail to account for individual constraints such as injuries, chronic diseases, or dietary restrictions. EmmitrFit bridges this gap by treating every user as unique.

The application collects granular data points (from "stress levels" to "specific injuries") and constructs a complex context window for the AI. This allows it to generate:
* **Safe Workout Plans:** Excluding exercises that might aggravate existing injuries.
* **Culturally Relevant Diets:** Specifically focused on Indian dietary preferences (Veg/Non-Veg/Vegan/Keto).
* **Audio Motivation:** An integrated AI voice coach that reads the summary of the plan.

---

## System Architecture

The application follows a decoupled **Client-Server Architecture**:

1.  **Frontend (Client):** A React.js Single Page Application (SPA) that handles user interaction, state management, and data visualization.
2.  **Backend (Server):** A Django REST Framework API that manages business logic, database interactions, and authentication.
3.  **AI Layer:** An external integration with Groq for generating intelligence and a ElevenLabs TTS engine for audio.
4.  **Database:** MySQL relational database for structured storage of user profiles and medical records.

---

## Key Features

### 1. Advanced Medical Profiling
Unlike simple fitness apps, EmmitrFit allows users to log **multiple** active diseases or conditions.
* **Logic:** Users can add, edit, and delete conditions dynamically.
* **Impact:** The AI prompts are dynamically adjusted. For example, if a user lists "Hypertension," the AI is instructed to avoid high-intensity interval training (HIIT) spikes.

### 2. Intelligent Plan Generation
* **Workout Engine:** Generates a 7-day schedule split by muscle groups or activity types, customized for location (Home/Gym).
* **Diet Engine:** Creates a meal-by-meal plan (Breakfast, Lunch, Dinner) respecting the user's caloric needs and taste preferences.

### 3. Audio Coaching Integration
* The backend processes the generated text plan and converts the summary into an audio file (MP3/WAV).
* This is served to the frontend via a base64 string or file URL, allowing users to "listen" to their coach on the go.

### 4. Secure Authentication
* Implements **JWT (JSON Web Token)** authentication.
* Access and Refresh tokens are handled automatically by the frontend interceptors to keep the user logged in securely.

---

## Technology Stack

### Frontend
* **Library:** React.js (Vite Build Tool)
* **Routing:** React Router DOM v6
* **HTTP Client:** Axios (with Interceptors for Auth)
* **Styling:** Modern CSS3 (Grid/Flexbox), CSS Variables, Responsive Design

### Backend
* **Framework:** Django 5.x
* **API:** Django REST Framework (DRF)
* **Database:** MySQL (via `mysqlclient`)
* **Documentation:** drf-spectacular (OpenAPI 3.0)
* **Auth:** SimpleJWT

### External APIs
* **LLM Provider:** Groq (Model: `llama-3.1-8b-instant`)
* **TTS Provider:** gTTS / ElevenLabs (Configurable)

---

## Getting Started

Follow these steps to set up the project locally.

### Prerequisites
* Python 3.10+
* Node.js v18+
* MySQL Server running locally

### 1. Clone the Repository
```bash
git clone https://github.com/codegeek004/emmitr_assignment.git
cd emmitr_assignment

```

### 2. Backend Setup

Navigate to the root directory where `manage.py` is located.

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add this to your .env
OPENAI_API_KEY = your_api_key
ELEVENLABS_API_KEY = your_api_key
VOICE_ID = 'JBFqnCBsd6RMkjVDRZzb'
MODEL_ID = 'eleven_multilingual_v2'
OUTPUT_FORMAT ='mp3_44100_128'
OPENAI_API_KEY = your_api_key
HOST = 'localhost'
DB_USER = your_mysql_username
PASSWORD = your_mysql_password
DB_NAME = 'emmitr'

# Run Migrations
python manage.py makemigrations
python manage.py migrate

# Start Server
python manage.py runserver

```

### 3. Frontend Setup

Open a new terminal and navigate to the `frontend` folder.

```bash
cd frontend

# Install packages
npm install

# Run development server
npm run dev

```

Access the App: `http://localhost:5173`
Access the API: `http://127.0.0.1:8000`

---

## 📡 API Documentation

The backend includes fully interactive Swagger documentation.
Once the server is running, visit:

👉 **[http://127.0.0.1:8000/api/docs/](https://www.google.com/search?q=http://127.0.0.1:8000/api/docs/)**

### Core Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/register/` | User Registration |
| `POST` | `/api/login/` | JWT Login |
| `GET/POST` | `/api/user_info/` | Lifestyle data (Stress, Smoking, etc.) |
| `GET/POST/PUT/PATCH` | `/api/fitness_info/` | Goals and fitness levels |
| `GET/POST/DELETE` | `/api/diseases/` | **CRUD** for medical conditions |
| `POST` | `/api/workout_plan/` | Trigger AI Workout Generation |
| `POST` | `/api/diet_plan/` | Trigger AI Diet Generation |

---

## 🧠 How It Works (Under the Hood)

### The Prompt Engineering Strategy

When a user clicks "Generate Plan", the backend gathers data from four different database tables (`CustomUser`, `FitnessInfo`, `AdditionalInfo`, `Diseases`).

It constructs a **System Prompt** that acts as a strict JSON enforcer:

> "You are a JSON API. Return ONLY valid JSON. Do not include markdown."

And a **User Prompt** rich with context:

> "Generate a 7-day plan for a 25-year-old Male, Vegetarian, suffering from 'Lower Back Pain' and 'Asthma'. His goal is Muscle Gain at Home. Ensure exercises are safe for his back."

### The Multi-Disease Logic

We solved the complex problem of users having multiple conditions by creating a One-to-Many relationship model (`User` -> `Diseases`).

* **Frontend:** Maintains a dynamic array of disease objects. When saving, it uses `Promise.all` to send parallel requests to the backend.
* **Backend:** The `DiseaseView` handles atomic creations and specific deletions using ID verification to ensure data integrity.

---

## 📂 Project Structure

```text
.
├── emmitr/                      # Project Configuration Directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Main settings (DB, Apps, Middleware, CORS)
│   ├── urls.py                  # Global URL routing (Admin + API path)
│   └── wsgi.py
│
├── fitness/                     # Main Django Application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/              # Database migration files
│   ├── models.py                # Database Schema (CustomUser, FitnessInfo, Diseases)
│   ├── serializers.py           # DRF Serializers for JSON validation & conversion
│   ├── tests.py
│   ├── tests_api/               # Integration Tests
│   │   ├── __init__.py
│   │   ├── test_auth.py         # Tests for Login/Register flows
│   │   ├── test_diet_plan.py    # Tests for AI Diet generation
│   │   ├── test_diseases.py     # Tests for Disease CRUD operations
│   │   ├── test_profile.py      # Tests for User Profile management
│   │   ├── test_workout_plan.py # Tests for AI Workout generation
│   │   └── utils.py             # Helper functions for testing
│   ├── text_to_speech.py        # Logic for converting AI text plans to Audio
│   ├── urls.py                  # App-specific URL routes
│   └── views.py                 # API Views (Controllers) for handling requests
│
└── frontend/                    # React Frontend Application
    └── src/
        ├── api.js               # Axios instance with JWT Interceptors
        ├── components/          # Reusable UI components (e.g., Navbar)
        ├── pages/               # Main Application Views
        │   ├── Dashboard.jsx    # User Dashboard (Plans & Audio Player)
        │   └── ProfileSetup.jsx # Profile creation & Disease management
        └── App.css              # Global styling system

```

---


## References
### Backend & Database
* [Django Project](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
* [Django REST Framework](https://www.django-rest-framework.org/) - A powerful and flexible toolkit for building Web APIs.
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - JSON Web Token authentication for Django REST Framework.
* [drf-spectacular](https://drf-spectacular.readthedocs.io/) - Flexible OpenAPI 3 schema generation for Django.
* [MySQL](https://www.mysql.com/) - Open source relational database.

### Frontend
* [React](https://react.dev/) - The library for web and native user interfaces.
* [Vite](https://vitejs.dev/) - Next Generation Frontend Tooling.
* [Axios](https://axios-http.com/) - Promise-based HTTP client for the browser and node.js.
* [React Router](https://reactrouter.com/) - Declarative routing for React web applications.

### AI & External Services
* [Groq API](https://console.groq.com/docs/models) - Fast AI inference (Llama 3.1).
* [ElevenLabs](https://elevenlabs.io/api) - Realistic AI Text-to-Speech generation.

## 🤝 Contributing

We welcome contributions!

1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

