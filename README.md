# Dynamic Wumpus Logic Agent (Web App)

A web-based **AI knowledge-based agent** that navigates a Wumpus World using **propositional logic and resolution inference**.
The agent makes decisions based on logical reasoning instead of knowing the environment in advance.

---

## 🚀 Live Demo

🔗 https://wumpus-agent-gcsc.onrender.com

---

## 📌 Features

* Dynamic grid size (user-defined)
* Random placement of Wumpus and pits
* Percepts:

  * Breeze → near pit
  * Stench → near Wumpus
* Knowledge Base (TELL / ASK)
* CNF-based logical representation
* Resolution refutation for inference
* Safe cell detection using logic
* Real-time grid visualization:

  * 🟩 Safe cells
  * 🟥 Inferred hazards
  * ⬜ Unknown cells
  * 🟦 Agent position
* Metrics dashboard:

  * Inference steps
  * Current percepts

---

## 🧠 How It Works

1. The agent starts with no knowledge of the environment
2. It receives percepts (breeze/stench)
3. Adds logical rules to the Knowledge Base (**TELL**)
4. Uses **resolution** to infer safe or dangerous cells (**ASK**)
5. Moves only to cells proven safe

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **AI Logic:** Propositional Logic + Resolution

---

## 📁 Project Structure

```
wumpus_app/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

---

---

## 🌐 Deployment

This project is deployed on **Render** using:

```
Build: pip install -r requirements.txt
Start: gunicorn app:app
```

---

## 🎯 Learning Outcomes

* Knowledge-Based Agents
* Propositional Logic
* CNF Conversion
* Resolution Algorithm
* Web-based AI visualization

---

## 👤 Author

**Taha Saleem Sheikh**
📧 [saleemt765@gmail.com](mailto:saleemt765@gmail.com)

---

## 📄 License

This project is for educational purposes.
