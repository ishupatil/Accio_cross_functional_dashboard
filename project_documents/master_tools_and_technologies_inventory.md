# Master Tools & Technologies Inventory

This document compiles the absolute master inventory of every language, library, framework, tool, and cloud service used throughout the entire lifecycle of the project (data profiling, data cleaning, exploratory analysis, backend development, frontend design, testing, and cloud deployment).

---

## 💻 1. Core Languages
* **Python (3.10 / 3.12):** The primary language used for data analysis, backend web serving, and database automation scripts.
* **SQL (PostgreSQL Dialect):** Used for schema partitioning, table management, index creation, and raw transaction queries.
* **JavaScript (ES6):** Powers browser-side interactive simulator calculations and initializes charting vectors.
* **HTML5 & CSS3:** Provides semantic page layout wrappers and customized style properties.

---

## 📊 2. Data Science & Analysis Stack (Jupyter Environment)
* **Jupyter Notebook & IPyKernel:** The environment used for writing and executing the data profiling, cleaning, and business insights code files.
* **Pandas (2.x):** Used for data cleaning, handling null values, type-casting columns, merging relational datasets, and grouping dataframes.
* **NumPy:** Used for array calculations, numeric operations, and handling NaN values.
* **Matplotlib & Seaborn:** Visualization libraries used inside the Jupyter notebooks to generate static analysis graphs (e.g. histograms, correlation matrices).

---

## 🗄️ 3. Database Connectivity & Storage Stack
* **PostgreSQL Server:** The enterprise-grade relational database engine (run locally via pgAdmin 4 and hosted as a managed database service on Render).
* **SQLAlchemy (2.x):** Object-relational mapping tool used to initialize the connection manager class with built-in connection pooling (`pool_size=5`).
* **Psycopg2-binary:** Low-level PostgreSQL adapter enabling Python applications to write to and read from the database.
* **python-dotenv:** Reads configurations and DB passwords from local `.env` files.
* **dj-database-url:** Parses cloud-scope connection strings (`DATABASE_URL`) on Render.

---

## ⚙️ 4. Backend Application Server Stack
* **Django (5.x):** The core MTV framework used to structure views, configure URL mappings, handle forms, and manage secure user sessions.
* **Django Contrib Auth & Session Middleware:** Restricts dashboard access to registered users, manages login cookies, and handles session caching.
* **WhiteNoise:** Integrated static file compiler that serves JS and CSS assets directly in production.

---

## 🎨 5. Frontend & Visualization Stack
* **Tailwind CSS:** Utility-first CSS library loaded via CDN, used to style grid layouts, card widgets, navigation panels, and active highlights.
* **ApexCharts.js:** Vector-based charting library used to render interactive combo charts, donuts, and columns on the frontend.
* **Google Fonts (Outfit & Inter):** External web fonts integrated into the master layout header for typography.

---

## ☁️ 6. DevOps, Version Control, & Deployment Stack
* **Render.com:** Cloud platform hosting the live Django web application container and the production PostgreSQL database.
* **Gunicorn:** Production-grade WSGI HTTP server used to run the Django app in the cloud.
* **Git:** The local version control system used to track changes and record project commits.
* **GitHub:** Hosts the repository code files and acts as the trigger for Render's CI/CD deployments.
* **`seed_db.py`**: Custom script created to run migrations and seed admin accounts automatically during the Render build command phase.

---

## 🛠️ 7. Local Workstation Tools
* **VS Code (Visual Studio Code):** The primary code editor.
* **pgAdmin 4:** The desktop database client used to connect to local and remote PostgreSQL databases to run queries and manage tables.
* **PowerShell / Windows Command Prompt:** Local execution shells.
* **Microsoft Word & Excel:** Used in the early stages of data gathering (`Finance Dashboard Data Dictionary.docx`, `Schemas and Tables.xls`).
