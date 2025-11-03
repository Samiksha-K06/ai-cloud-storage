# 🌩️ AI Cloud Storage  
---

## 🚀 Overview  
**AI Cloud Storage** is a personal cloud platform that lets users **upload, manage, and analyze files** using **Google Gemini AI**.  
Built with **FastAPI, MongoDB Atlas, and Vanilla JS**, it demonstrates full-stack development combined with generative AI integration.

---

## ✨ Key Features  
- 🔐 **User Authentication** (Signup/Login with MongoDB Atlas)  
- 📂 **File Uploads** — PDF, DOCX, TXT  
- 🤖 **AI File Summarization** using Gemini API  
- 🧭 **Interactive Dashboard UI** (HTML, CSS, JS)  
- ⚙️ **Modular FastAPI Backend** with clean routes  

---

## 🏗️ Tech Stack  
| Layer            | Technologies           
|----------------- |----------------------
| **Frontend**     | HTML, CSS, JavaScript 
| **Backend**      | FastAPI (Python) 
| **Database**     | MongoDB Atlas 
| **AI**           | Google Gemini (via `google-generativeai`) 

---

## ⚙️ Setup Instructions  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Samiksha-K06/ai-cloud-storage.git
cd ai-cloud-storage/backend
2️⃣ Create Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate   # Windows
# or source venv/bin/activate   # macOS/Linux
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Create .env File (inside /backend)
bash
Copy code
MONGODB_URI=your_mongo_uri
GEMINI_API_KEY=your_gemini_api_key

⚠️ .env is already included in .gitignore, so your credentials remain private.

5️⃣ Run the App
uvicorn app:app --reload

6️⃣ Open Frontend
Open frontend/index.html in your browser.

🧠 Example Use
Log in or Sign up

Upload a .pdf, .txt, or .docx file

Click Analyze with AI

Instantly get summarized insights powered by Gemini

💡 Future Enhancements
✅ JWT Authentication

💬 “Chat with Document” Feature

📊 Analytics Dashboard for File Insights

🧰 Folder Structure

ai-cloud-storage/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── auth.py
│   ├── routes/
│   ├── uploads/
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── script.js
│   └── style.css
│
└── .gitignore

👩‍💻 Author
Samiksha Kapse
🎓 3rd-Year Engineering Student | 💻 AI & Full-Stack Developer

🌐 GitHub
💼 “Building intelligent, user-centric applications with AI and clean design.”

⭐ Show Your Support
If you like this project, please give it a ⭐ on GitHub — it motivates me to build more and better AI-powered solutions!

---
