Here’s a **professional, complete, production-grade `README.md`** for your repository **chat-microservices** based on your architecture (Django Auth Service + FastAPI Chat Service + Redis + Postgres + Celery + React Frontend + Docker Compose).

You can copy-paste directly into your repo.

---

# **Chat Microservices – Real-Time Chat System (Django + FastAPI + Redis + React + Docker)**

A fully containerized **microservices-based real-time chat application** built with:

* **Django REST Framework** → Authentication & User Service
* **FastAPI** → Real-time chat service
* **WebSockets** → Live messaging
* **Redis** → Message broker + real-time pub/sub
* **PostgreSQL** → Persistent database
* **Celery** → Notifications & background jobs
* **React + Vite** → Frontend UI
* **Docker Compose** → Full system orchestration

This project demonstrates a modern distributed architecture suitable for scalable production chat systems.

---

# ⚙️ **Architecture Overview**

```
                    +-------------------+
                    |    React Frontend |
                    |    Vite + Axios   |
                    +---------+---------+
                              |
                              v
                    +---------+---------+
                    |  Auth Service     |
                    |  Django + DRF     |
                    |  Token Auth (JWT) |
                    +---------+---------+
                              |
                              v
                    +---------+---------+
                    |   Chat Service    |
                    |   FastAPI         |
                    |   WebSockets      |
                    +---------+---------+
                              |
             Pub/Sub <--------+--------> Redis
                              |
                     Background Tasks
                              |
                    +---------+---------+
                    | Notification Svc  |
                    | Celery Workers    |
                    +-------------------+
```

---

# 🚀 **Features**

### ✅ Authentication (Django)

* JWT-based login
* User registration
* Secure token handling

### ✅ Real-Time Chat (FastAPI)

* Join rooms
* Send/receive messages using WebSockets
* Broadcast messages to all users in the room

### ✅ Notification Microservice

* Celery worker
* Uses Redis as broker
* Can send background notifications (emails, alerts)

### ✅ Frontend (React + Vite)

* Join chat rooms
* Real-time chat UI
* Connects to FastAPI WebSocket backend
* Integrates with Auth service

### ✅ Fully Dockerized

* All services run independently:

  * `auth-service`
  * `chat-service`
  * `notifications-service`
  * `frontend`
  * `redis`
  * `postgres`

---

# 🐳 **Run The Whole System with Docker**

Make sure Docker & Docker Compose are installed.

### **Start the entire system**

```bash
docker compose up --build
```

### **Visit the apps**

| Service                | URL                                            |
| ---------------------- | ---------------------------------------------- |
| Frontend               | [http://localhost:5173](http://localhost:5173) |
| Auth Service (DRF)     | [http://localhost:8000](http://localhost:8000) |
| Chat Service (FastAPI) | ws://localhost:8001/chat                       |
| Postgres               | localhost:5432                                 |
| Redis                  | localhost:6379                                 |

---

# 📁 Folder Structure

```
chat-microservices/
│
├── auth-service/               # Django Authentication Service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── user, JWT, API logic
│
├── chat-service/               # FastAPI Chat Service
│   ├── main.py
│   ├── WebSocket handlers
│   └── Dockerfile
│
├── notifications-service/      # Celery Worker
│   ├── tasks.py
│   ├── Dockerfile
│
├── frontend/                   # React Frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

# 🔐 **Authentication Service (Django + DRF)**

### Start locally

```bash
cd auth-service
pip install -r requirements.txt
python manage.py runserver
```

### Endpoints

| Method | Route            | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/api/register/` | Create user             |
| POST   | `/api/login/`    | Return JWT tokens       |
| GET    | `/api/user/`     | Get logged-in user info |

---

# 💬 **Chat Service (FastAPI + WebSockets)**

### Start locally

```bash
cd chat-service
uvicorn main:app --reload
```

### WebSocket endpoint

```
ws://localhost:8001/ws/{room_id}
```

---

# 🔔 **Notifications Service (Celery)**

Runs async tasks (send notifications, email, logs, etc.)

### Start worker

```bash
celery -A tasks worker --loglevel=info
```

---

# 🎨 **Frontend (React + Vite)**

### Start in development mode

```bash
cd frontend
npm install
npm run dev -- --host
```

The frontend communicates with:

* Auth API → REST
* Chat API → WebSockets

---

# 🧪 **Environment Variables**

### Example `.env` for Django

```
SECRET_KEY=your_secret_key
DB_NAME=chatdb
DB_USER=chatuser
DB_PASS=chatpass
DB_HOST=db
DB_PORT=5432
```

### Example `.env` for FastAPI

```
REDIS_HOST=redis
REDIS_PORT=6379
```

---

# 📦 **Docker Compose Services**

| Service                 | Tech         | Description             |
| ----------------------- | ------------ | ----------------------- |
| `auth-service`          | Django       | Handles authentication  |
| `chat-service`          | FastAPI      | WebSocket chat          |
| `notifications-service` | Celery       | Background tasks        |
| `redis`                 | Redis        | Pub/Sub + Celery broker |
| `db`                    | PostgreSQL   | Main user database      |
| `frontend`              | Vite + React | User interface          |

---

# 🧑‍💻 **Contribution Guide**

1. Fork the repository
2. Create a new branch
3. Commit changes
4. Create a Pull Request

---

# ⭐ **Future Improvements**

* Add JWT refresh token rotation
* Add typing indicators
* Add file/image messages
* Add message history using Postgres
* Add user presence (online/offline tracking)
* Add chat groups & channels

---

# 📜 **License**

This project is open-source and licensed under the MIT License.

---