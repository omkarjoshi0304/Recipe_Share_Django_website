# 🍽️ RecipeShare Django App

Welcome to **RecipeShare** — a collaborative platform where users can share and explore recipes, submit food ideas, and buy/sell kitchen items through an integrated marketplace. This project is built using **Django** and runs seamlessly inside a **Docker** container.

---

## 📦 Features

- User Registration, Login & Authentication
- Submit, Browse, and Edit Recipes
- Filter Recipes by Category
- Contact Form with AJAX
- Kitchen Marketplace for utensils & appliances
- Image uploads & reviews for items
- Responsive UI with Bootstrap
- Dockerized deployment

---

## 🚀 Run with Docker

### 🛠 Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- A running MySQL server locally

### 🔧 MySQL Setup

Open a MySQL terminal or client and run:

```sql
CREATE DATABASE IF NOT EXISTS myappdb;
CREATE USER 'myappdbuser'@'%' IDENTIFIED BY 'myappdbpass';
GRANT ALL PRIVILEGES ON myappdb.* TO 'myappdbuser'@'%';
FLUSH PRIVILEGES;
```

---

### 🐳 Build the Docker Image

```bash
docker build -t myapp .
```

### 💾 Create a Docker Volume

```bash
docker volume create myapp-storage
```

### ▶️ Run the Container

```bash
docker run -ti -e DATABASE_URL="mysql://myappdbuser:myappdbpass@host.docker.internal:3306/myappdb" -v myapp-storage:/app/storage -p 8000:8000 myapp
```

Visit 👉 `http://localhost:8000`

---

## ⚙️ Tech Stack

- Django 5.2
- Bootstrap 5
- MySQL
- JavaScript & AJAX
- Docker

---

## 📂 Project Structure

```
recipeshare/
├── main/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   └── forms.py
├── recipeshare/
├── requirements.txt
├── Dockerfile
└── entrypoint.sh
```

---

## 🐛 Troubleshooting

- Make sure MySQL is listening on all interfaces (`bind-address = 0.0.0.0`)
- Ensure user has privileges:
```sql
SHOW GRANTS FOR 'myappdbuser'@'%';
```
- If needed, try:
```bash
DATABASE_URL="mysql://myappdbuser:myappdbpass@host.docker.internal:3306/myappdb?allowPublicKeyRetrieval=true"
```

---

## 👨‍💻 Author

**Omkar Joshi**  
[GitHub](https://github.com/omkarjoshi0304)

---

## 📜 License

This project is part of an academic assignment. For educational use only.
