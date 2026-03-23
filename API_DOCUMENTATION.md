# Comprehensive MedRec System & API Documentation

**Welcome to the MedRec System Guide!**
This document is designed to be fully understandable for both **Non-Technical Project Managers/Stakeholders** and **Technical Developers (Front-end/Mobile engineers)**. It explains what each part of our system does, how it works in real life, and the exact technical codes to trigger those functions.

---

## 🔐 1. User Accounts & Security (Authentication)
* **What it does for the user:** It ensures that every patient/user has a private, secure profile. Nobody can access their medical scanning history without their permission.
* **Technical details:** We use `JWT` (JSON Web Tokens), which is a stateless security mechanism perfect for smooth mobile app experiences without logging users out randomly.

**Developer Endpoints (Base URL: `/auth/`):**
- **POST** `/auth/register/` : Use this to create a brand new account (needs email, password, etc.).
- **POST** `/auth/login/` : Send username and password here to receive the security `Token`.
- **POST** `/auth/logout/` : Kills the active session token gracefully.
- **POST** `/auth/token/refresh/` : Re-activates an expiring token automatically in the background so the user isn't annoyed.

---

## 💊 2. The Core Medicine Library (Catalogs)
* **What it does for the user:** This is our giant digital pharmacy. It stores everything about a medicine (price, exactly what chemicals are inside it, and who manufactured it). It allows users to browse medicines easily.

**Developer Endpoints (Base URL: `/api/`):**
### List All Medicines
- **GET** `/api/medicines/`
  - **In plain English:** Show me the menu of all medicines.
  - **For Devs:** Returns a fast, lightweight list. You can add `?ordering=price` to sort cheapest first, or `?category=Vitamins` to filter them out.

### Get Top/Latest Medicines
- **GET** `/api/medicines/top/`
  - **In plain English:** What are the most recent 10 medicines added to our database?
  - **For Devs:** Perfect for building the "Newly Added Medicines" slider on the app's home screen.

### Get the Whole Story of a Single Medicine
- **GET** `/api/medicines/{code}/` (Example: `/api/medicines/MED001/`)
  - **In plain English:** I clicked on "Panadol". Open its page and show me everything!
  - **For Devs:** Returns a massive JSON payload containing the Active Ingredients, strict medical Warnings, Side Effects, price, and descriptive paragraphs.

---

## 🔍 3. The Smart Search Engines (Advanced Locators)
* **What it does for the user:** Sometimes users don't remember the exact brand name of a drug. Our smart engines act like a real pharmacist, searching by the medical ingredients, side effects, or suggesting cheaper alternatives!

**Developer Endpoints:**
### The "Google-like" Universal Search
- **GET** `/api/medicines/search/?q={query}`
  - **In plain English:** Just type what you remember. It will check English names, Arabic names, and even the chemical ingredients inside the drugs all at once to find what you mean.
  - **For Devs:** The fastest way to build an omni-search bar.

### Search by Exact Active Ingredient (Chemists' Tool)
- **GET** `/api/medicines/ingredient/{ingredient}/` (Example: `/ingredient/Paracetamol/`)
  - **In plain English:** Show me every single drug in your database that operates using "Paracetamol".

### The "Find a Substitute" Engine
- **GET** `/api/medicines/{code}/alternatives/`
  - **In plain English:** "My pharmacy ran out of Panadol (MED001). Can you give me an exact identical alternative?" — Yes, this tool checks the active ingredient and lists all other brands with that exact same formula.

### The "Side Effects Warning" Checker
- **GET** `/api/medicines/effect/{effect_keyword}/` (Example: `/effect/Dizziness/`)
  - **In plain English:** "I need to drive today, show me which medicines in the database cause Dizziness so I can avoid them."
  - **For Devs:** Filters specifically by checking the inner strings of the `warnings` and `side_effects` columns.

### Filter by Categories and Companies
- **GET** `/api/medicines/category/{category_name}/` ➔ E.g., Give me only the "Antibiotics".
- **GET** `/api/medicines/company/{company_name}/` ➔ E.g., List all drugs manufactured by "Pfizer".

---

## 📷 4. AI Camera & Medical Scan History
* **What it does for the user:** The star feature! The user opens their phone camera, snaps a picture of a random medicine box, and our Artificial Intelligence immediately recognizes it and saves a record. "Ah, this is Brufen!"

**Developer Endpoints:**
### Perform and Save the AI Scan
- **POST** `/api/uploads/new/`
  - **In plain English:** Here is a photo from my camera, tell me what drug is in it.
  - **For Devs:** Requires `multipart/form-data`. Attach the binary file as `image`. The backend saves the image to a secure vault, triggers the `core/ai_service.py` to identify it, links the image to the actual database medicine, and returns the result with an "AI Confidence Score" (e.g., 96% sure).

### View My Private History Log
- **GET** `/api/uploads/`
  - **In plain English:** I want to look at the list of all the images I analyzed in the past 3 months.
  - **For Devs:** Returns a neat, chronological list of their previous AI scans.

### Erase My Private History
- **DELETE** `/api/uploads/clear-history/`
  - **In plain English:** Delete everything I ever scanned from your servers. I want absolute privacy.
  - **For Devs:** Instantly drops the user's entire upload footprint from the database.

---
**Note for Setup & Developers:** 
To kickstart this system from zero on a new PC, run:
1. `python manage.py makemigrations api` 
2. `python manage.py migrate` 
3. `python manage.py import_comprehensive_medicines comprehensive_medicines_dataset.csv`
4. `python manage.py runserver`