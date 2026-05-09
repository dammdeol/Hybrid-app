# Hybrid App
## Stack Project

<img src="https://raw.githubusercontent.com/dammdeol/Hybrid-app/main/memoji.png" width='300'/>

<!--
<a href="https://dammdeol.github.io/MO-PCDE_M9_final_assignment/M9_Final_Assignment.ipynb"> Hybrid App </a>
-->
<a href="https://github.com/dammdeol/Hybrid-app"> Hybrid App </a>

---

## Overview

**Hybrid App** is a full-stack web application that combines **FastAPI** and **Flask** in a single process. FastAPI handles the REST API layer while Flask + Jinja2 powers the server-rendered frontend. Both frameworks coexist thanks to `a2wsgi`, which mounts the Flask WSGI app onto the FastAPI instance.

## Architecture

```
FastAPI (root app)
├── /api/items   → REST API (FastAPI + SQLAlchemy)
└── /            → Web UI (Flask + Jinja2 via WSGI middleware)
```

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| API        | FastAPI, Pydantic, fastapi-pagination |
| Web UI     | Flask, Jinja2                       |
| Database   | SQLAlchemy (SQLite by default)      |
| Bridge     | a2wsgi (WSGI ↔ ASGI)               |
| Server     | Uvicorn                             |

## Features

- **REST API** (`/api/items`) with full CRUD, pagination, and filtering by name and price range
- **Server-rendered pages** served by Flask at `/` and `/about`
- **Auto-seeded database** with sample items on first startup
- **Input validation** via Pydantic models

## Getting Started

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the app

```bash
python run.py
```

The app will be available at `http://localhost:8000`.

| Endpoint            | Description              |
|---------------------|--------------------------|
| `GET /`             | Flask home page          |
| `GET /about`        | Flask about page         |
| `GET /api/items`    | List items (paginated)   |
| `POST /api/items`   | Create a new item        |
| `GET /api/items/{id}` | Get item by ID         |
| `PUT /api/items/{id}` | Update an item         |
| `DELETE /api/items/{id}` | Delete an item    |
| `GET /docs`         | Interactive API docs (Swagger UI) |

## Project Structure

```
app/
├── main.py          # FastAPI app + Flask mount
├── config.py        # App configuration
├── db.py            # SQLAlchemy engine and session
├── models.py        # ORM models
├── api/
│   └── items.py     # Items REST API router
└── web/
    ├── routes.py    # Flask blueprints and routes
    ├── static/      # CSS assets
    └── templates/   # Jinja2 HTML templates
```
