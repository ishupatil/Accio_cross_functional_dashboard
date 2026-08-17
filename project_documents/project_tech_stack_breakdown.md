# Technology Stack & System Components Breakdown

This document compiles the details of the technologies used throughout the project, categorized by their structural layers, explaining their exact roles in the architecture.

---

## 🎨 1. Frontend Layer (User Interface & Interactivity)

| Technology | Role / Purpose | Description |
| :--- | :--- | :--- |
| **Tailwind CSS** | Styling & Theme | Used to construct the corporate design system in Midnight Navy (`#0A192F`) and Champagne Gold (`#C5A880`). Ensures mobile-responsive grid cards and sidebar menus. |
| **ApexCharts.js** | Visualizations | Renders interactive, vector-based SVG charts (monthly combo trends, regional donuts, bank financing columns, simulator metrics) on the fly. |
| **Vanilla JavaScript** | Interactive Simulator | Captures slider actions in the Scenario Simulator, recalculating operating margins and updating chart data arrays dynamically in the browser DOM. |
| **HTML5** | Layout & Structure | Establishes the master page wrapper and page templates (`base.html`, sub-templates). |

---

## ⚙️ 2. Backend Layer (Server & Routing)

| Technology | Role / Purpose | Description |
| :--- | :--- | :--- |
| **Python** | Core Language | The primary development language of the dashboard application. |
| **Django Framework** | Web Server Engine | Manages URL routing, checks user session authentication (`login_required`), serves security headers, and compiles HTML templates. |
| **WhiteNoise** | Static Files Handler | Serves compiled static assets (CSS, JS) directly from Django, optimized for production web service speeds. |

---

## 🗄️ 3. Data Processing & Database Layer

| Technology | Role / Purpose | Description |
| :--- | :--- | :--- |
| **PostgreSQL** | Data Storage | Relational database containing sales, finance, showroom, and customer tables divided into custom schemas (`sales_transaction`, `finance_accounting`, etc.). |
| **Pandas** | Data Wrangling | Reads raw SQL tables dynamically on page load, performing data-type conversions, merges, and group-by calculations in-memory. |
| **SQLAlchemy** | Connection Pooling | Manages database pools, maintaining 5 warm connections in memory to prevent overhead from database handshakes. |
| **Psycopg2-binary** | DB Driver | The low-level database adapter letting Python query the PostgreSQL engine. |
| **python-dotenv** | Environments | Loads secret database credentials from `.env` locally. |
| **dj-database-url** | Cloud DB Parser | Parses Render's `DATABASE_URL` to configure the Django PostgreSQL backend. |

---

## ☁️ 4. DevOps & Cloud Infrastructure Layer

| Technology | Role / Purpose | Description |
| :--- | :--- | :--- |
| **Render.com** | Web & DB Hosting | Hosts the live Django web service and the managed PostgreSQL database service. |
| **Gunicorn** | WSGI Web Server | High-performance production HTTP server used to run the Django app. |
| **Git & GitHub** | CI/CD Pipeline | Manages version control. Pushing code to GitHub triggers Render's automated build and redeployment. |
| **`seed_db.py`** | Build Automation | Custom script that runs database migrations and seeds superusers during the Render build phase. |
