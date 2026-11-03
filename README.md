# 🚀 מדריך הפעלה - בוט דין משמעתי לוואטספ

מדריך זה מסביר שלב אחר שלב כיצד להעלות את הקוד לשרת חינמי (Render) ולחבר אותו לוואטספ.

---

## 📋 שלב 1: פתיחת חשבון ב-Green API (חיבור לוואטספ)
1. הירשם בשירות Green API (ניתן להירשם במסלול Developer).
2. צור Instance חדש וסרוק את קוד ה-QR מהטלפון שלך (כמו התחברות לוואטספ ווב).
3. העתק מלוח הבקרה:
   - `idInstance` (לדוגמה: `7135123456`)
   - `apiTokenInstance` (מחרוזת התווים המאובטחת)

---

## 🔑 שלב 2: הוצאת מפתח Gemini API
1. היכנס ל-Google AI Studio.
2. לחץ על **Create API key** והעתק את מפתח ה-API (`GEMINI_API_KEY`).

---

## 🌐 שלב 3: העלאת השרת ל-Render
1. הירשם בפלטפורמת Render.
2. לחץ על **New +** ובחר **Web Service**.
3. העלה את קובצי הקוד (`main.py`, `requirements.txt`).
4. הגדר את הפרטים הבאים:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
5. תחת **Environment Variables** (משתני סביבה), הוסף:
   - `GEMINI_API_KEY`: המפתח מ-Google AI Studio
   - `GREEN_API_INSTANCE`: ה-idInstance מ-Green API
   - `GREEN_API_TOKEN`: ה-apiTokenInstance מ-Green API
6. לחץ על **Create Web Service** והעתק את הכתובת שהוקצתה לשרת.

---

## 🔗 שלב 4: הגדרת Webhook ב-Green API
1. חזור ללוח הבקרה ב-Green API.
2. תחת הגדרות ה-Instance, הזן את כתובת השרת בתוספת `/webhook` בסופה:
   `https://<your-render-app>.onrender.com/webhook`
3. ודא שהאפשרות `incomingMessageReceived` מופעלת.

---

🎉 **המערכת מוכנה לפעולה!**
