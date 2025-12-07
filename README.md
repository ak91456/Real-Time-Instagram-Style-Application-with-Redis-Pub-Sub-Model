Instagram REST + Pub/Sub (Channels + Redis)
=========================================

What's included:
- REST API with JWT (accounts + posts)
- Likes, Comments, Feed
- Notifications app sending real-time messages via Channels/Redis
- WebSocket consumer at ws://127.0.0.1:8000/ws/notifications/

IMPORTANT: You need a running Redis server for Channels to function. Two options:

Option A — Run Redis locally (recommended for dev):
- Install Redis for your OS and start it (must listen on 127.0.0.1:6379)

Option B — Use Docker (if you have Docker)
- docker-compose up -d

Steps to run the project (exact order):
1) Extract zip & open terminal in project folder
2) python -m venv venv
   venv\Scripts\activate  (Windows) or source venv/bin/activate (Mac/Linux)
3) pip install -r requirements.txt
4) python manage.py makemigrations accounts
   python manage.py makemigrations posts
   python manage.py makemigrations notifications
5) python manage.py migrate
6) python manage.py createsuperuser
7) mkdir media media/avatars media/posts
8) Start Redis (see above)
9) Run ASGI server:
   daphne -b 0.0.0.0 -p 8000 instagram_clone.asgi:application
   (or) python manage.py runserver  # runserver can work for dev but use daphne for stable websockets
10) Connect WebSocket (must be authenticated via session or token if using a custom token middleware)
    ws://127.0.0.1:8000/ws/notifications/

WebSocket notes:
- This project uses Django's AuthMiddlewareStack for WebSocket authentication (session-based).
- For token-based WS auth we can add a small middleware that accepts ?token=<access_token> and authenticates the user for the scope.

API endpoints (same as REST-only):
- Register: POST /api/accounts/register/
- Login: POST /api/accounts/login/
- Token refresh: POST /api/accounts/token/refresh/
- Users list: GET /api/accounts/
- Follow toggle: POST /api/accounts/<id>/follow-toggle/ (JWT)
- Posts: GET/POST /api/posts/
- Like: POST /api/posts/<id>/like/
- Comment: POST /api/posts/<id>/comment/
- Feed: GET /api/posts/feed/

Notes:
- For development, you can log into /admin/ and then use browser + session to connect websockets.
- If you want token based WebSocket auth (recommended for APIs), say 'add token-ws-middleware' and I'll add it.
