# EcoLogger – Real‑Time Micro‑Climate Logger

> **IoT · Environmental Sensing · 2025**
>
> EcoLogger turns low‑cost sensors into a **live micro‑weather dashboard**.  Readings streamed from tiny IoT devices are stored in MongoDB Atlas and delivered to users instantly via WebSockets / Server‑Sent Events.

---

## 📑 Contents

1. [Why EcoLogger?](#why-ecologger)
2. [System Architecture](#system-architecture)
3. [Repository Layout](#repository-layout)
4. [Getting Started (Local Dev)](#getting-started-local-dev)
5. [Deploy to the Cloud](#deploy-to-the-cloud)
6. [API Reference](#api-reference)
7. [Extending](#extending)
8. [Contributing](#contributing)
9. [License](#license)

---

## Why EcoLogger?

Home weather stations and indoor environmental sensors often silo data on‑device or in proprietary clouds.  EcoLogger provides:

* **Vendor‑agnostic ingestion** – HTTP & MQTT endpoints for any ESP32 / Raspberry Pi sensor payload.
* **Instant updates** – Backend broadcasts new docs to connected browsers — no polling.
* **Pluggable storage** – Defaults to MongoDB Atlas but swap in PostgreSQL, InfluxDB or DynamoDB.
* **Open‑source dashboards** – React + Socket.IO frontend or a one‑file Streamlit app for quick visualisation.

---

## System Architecture

```
┌────────────┐      🔌 HTTP / MQTT         ┌────────────────┐       WebSocket / SSE      ┌──────────────┐
│  IoT Node  │ ─────────────────────────▶ │  Django API    │ ─────────────────────────▶ │   Frontend   │
│  (ESP32)   │  JSON payload              │  + Channels     │  JSON doc broadcast       │  React / St  │
└────────────┘                             │  (Backend)     │                            │   reamlit    │
        ▲                                   │    |           │                            └──────────────┘
        │                                   │    ▼           │                                  ▲
        │                                   │ MongoDB Atlas  │          REST export           │
        └───────────────  OTA / Wi‑Fi  ─────┴───────────────┘  CSV / Parquet / InfluxDB  ───┘
```

**Key Components**

* **IoT Client** (folder `nodejs/`) – sample NodeMCU firmware sending JSON `{temp, humidity, pressure, timestamps}` every 30 s.
* **Backend Server** (folder `BackendServer/`) – Django 4 + Django REST Framework; real‑time via **Django Channels** & Redis.
* **Database** (folder `DataBase/`) – MongoDB Atlas cluster; schema described in `DataBase/schemas/sensor_reading.bson`.
* **Web UI** (folder `Web/`) – React 18 + Socket.IO; pulls the latest 100 readings and listens for `reading:new` events.
* **hello\_django/** – quick‑start tutorial for a minimal Django project (kept for educational context).

> The MVP logic mirrors the short README stub in the original repo: IoT device ➜ Mongo ➜ WebSocket ➜ UI ([raw.githubusercontent.com](https://raw.githubusercontent.com/xlumzee/EcoLogger/main/README.md))

---

## Repository Layout

```
EcoLogger/
├── BackendServer/           # Django project & apps
│   ├── core/                # settings, urls, ASGI, Consumers
│   ├── sensors/             # models, serializers, views
│   └── requirements.txt
├── DataBase/                # Mongo schema dumps + migration helpers
├── Web/                     # React UI (Vite + TailwindCSS)
│   ├── src/
│   └── package.json
├── nodejs/                  # ESP32 / NodeMCU firmware (JavaScript SDK example)
├── hello_django/            # step‑by‑step beginner walkthrough (can be removed in production)
├── docker-compose.yml       # one‑command dev stack (Django + Mongo + Redis)
└── README_EcoLogger.md      # you’re here
```

---

## Getting Started (Local Dev)

### 1. Clone & bootstrap

```bash
git clone https://github.com/xlumzee/EcoLogger.git
cd EcoLogger
```

### 2. Spin up the dev stack

```bash
# requires Docker & Docker Compose v2
cp BackendServer/.env.example BackendServer/.env  # add your Mongo URI
cp Web/.env.example Web/.env                      # add API base URL

docker compose up --build   # builds Django, React, pulls Mongo & Redis images
```

* Django API ➜ [http://localhost:8000/api/readings/](http://localhost:8000/api/readings/)
* React UI  ➜ [http://localhost:5173/](http://localhost:5173/)

### 3. Push fake data (optional)

```bash
python BackendServer/scripts/seed_fake_data.py --n 500
```

The dashboard will update in real time.

---

## Deploy to the Cloud

| Target                | Guide                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------- |
| **Render.com**        | 1‑click blueprint `render.yaml` – provisions a free web‑service + docDB‑compatible Mongo. |
| **Heroku**            | `Procfile`, `heroku.yml`, and a **MongoDB Atlas Add‑On** sample script included.          |
| **AWS ECS (Fargate)** | `infrastructure/ecs/` holds Terraform modules (optional).                                 |

For ESP32 firmware OTA builds, see `nodejs/README.md`.

---

## API Reference

| **Endpoint**     | **Method** | **Description**                                                        |
| ---------------- | ---------- | ---------------------------------------------------------------------- |
| `/api/readings/` | `GET`      | List latest 100 readings (paginated)                                   |
| `/api/readings/` | `POST`     | Push single sensor payload `{device_id, temp, humidity, pressure, ts}` |
| `/ws/readings/`  | WebSocket  | Subscribe; backend emits `{reading: {...}}` every insert               |

Authentication is handled via simple API keys (optional) using the `X‑API‑KEY` header.

---

## Extending

* 🗺️ **Add GPS & mapping** – store `lat, lon` to visualise IoT network coverage.
* 📈 **Historical analytics** – dump to InfluxDB & display Grafana dashboards.
* 🤖 **Alerting** – add `celery` worker to trigger email/SMS if readings exceed thresholds.
* 🕵️‍♀️ **Security** – enable JWT auth & rate‑limiting on POST endpoint.

Road‑map items tracked in GitHub Issues.

---

## Contributing

PRs and issues welcome!  Please run `pre‑commit run --all-files` before submitting.

---

## License

Released under the **MIT License**.  See `LICENSE` for details.
