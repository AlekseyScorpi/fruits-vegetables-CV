# 🍏 Python FRUITS-VEGETABLES SMART SCALES PET PROJECT

🚀 **PET project**, featuring:
- 📸 **YOLO (nano/small) models** for detecting fruits and vegetables (YOLOv8)
- 🖥️ **Qt application** (simulation of smart scales for automatic product detection)
- 🗄️ **Database** (PostgreSQL in a Docker container)  
  👉 Repository with the container: [fruits-vegetables-cv-docker](https://github.com/AlekseyScorpi/fruits-vegetables-cv-docker)

![Python](https://img.shields.io/badge/python-3.11-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-nano%2Fsmall-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Docker-blue)

---

## 🛠 Installation Guide

### 1️⃣ Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure the `.env` file:
Create a `.env` file and add the following parameters:

| Variable           | Example Value           | Description |
|---------------------|-------------------------|----------|
| `DEBUG`            | `TRUE` or `FALSE`       | Debug mode |
| `MODEL`            | `NANO` or `SMALL`       | YOLO version |
| `DATABASE_DBNAME`  | `smart_scales_db`       | Database name |
| `DATABASE_USERNAME`| `smart_scales_user`     | Database user |
| `DATABASE_PASSWORD`| `your_password`        | Database password |
| `DATABASE_HOST`    | `localhost` or IP       | Database host |
| `DATABASE_PORT`    | `5432` (or `5433`)      | Database port |

🔹 **Note**:  
The parameters `DBNAME`, `USERNAME`, and `PASSWORD` are set in the PostgreSQL container. Details can be found in the repository [fruits-vegetables-cv-docker](https://github.com/AlekseyScorpi/fruits-vegetables-cv-docker).

---

## 🚀 Running the Application

Simply execute the following command:
```bash
python main.py
```

---

## 🏆 About the Models

📖 More details about our models and the problem-solving approach can be found in our article:  
📝 **[elibrary.ru/item.asp?id=80257050](https://elibrary.ru/item.asp?id=80257050)** (in Russian)

📂 **Training logs and model weights 1-YOLOv8 (small), 2-YOLOv8 (nano), 3-YOLOv11 (nano), 4-YOLOv11 (small)**:  
📎 **[Google Drive](https://drive.google.com/file/d/1d2SuxCLBYriJ4DaPlrhQIz8JvasaTVLF/view?usp=drive_link)**

---

## ✉ Contact
📧 **Email**: timoshin_aleksey02@mail.ru  
🐙 **GitHub**: [AlekseyScorpi](https://github.com/AlekseyScorpi)
