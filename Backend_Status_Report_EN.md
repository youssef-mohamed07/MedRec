# Backend Status Report - MedRec

## 🟢 System Overview (Completed)

The **MedRec** backend serves as the core intelligent engine. It manages intricate medicine databases, intelligent search capabilities, user safety, and seamless AI integration.

### 1. **Authentication Engine**
Fully secured endpoints utilizing **JWT (JSON Web Tokens)** allowing for stateless, swift authentication, perfectly fitted for mobile & front-end consumption without relying on sessions.

### 2. **Refined Medicine Database**
Extensively rich schema tracking everything from active chemical ingredients and generic alternatives to commercial packaging and detailed side effects.

### 3. **AI Pipeline**
Integrated intermediate skeleton (`ai_service.py`) designed to hook directly to a Machine Learning script, handling the heavy lifting of extracting predictions and cross-referencing them with actual database records securely.

---

## 🔌 Completely Detailed API Endpoints List

Below is an expanded dive into the current APIs, illustrating payload expectations and responses.

### 💊 **1. Medicines & Deep Search APIs**

#### `GET /api/medicines/`
* **Purpose:** List all active medicines.
* **Capabilities:** Supports pagination, categorical filtering (`?category=xyz`), and ordering parameters.

#### `GET /api/medicines/{code}/`
* **Purpose:** Fetch thorough, isolated details about a single medicine using its unique catalog code.
* **Returns:** Active ingredients, manufacturer, exact concentrations, textual warnings, pricing, and packaging details inside a beautifully formatted JSON.

#### `GET /api/medicines/search/?q={query}`
* **Purpose:** **The Advanced Deep-Search Engine.**
* **Algorithm:** An aggressive query resolver that doesn't just search the title, but simultaneously checks:
  - English & Arabic strings.
  - Active Ingredients.
  - Textual Alternatives list.
* **Use Case:** Typing "Paracetamol" returns Panadol, Fevadol, Congestal, etc. 

#### `GET /api/medicines/{code}/alternatives/` *(NEW)*
* **Purpose:** Intelligent Alternative generator.
* **Algorithm:** Given a medicine code, the backend automatically cross-engineers other medicines globally matching its exact *active ingredient*, presenting a list of reliable pharmaceutical substitutions instantly.

---

### 📷 **2. Camera & Image Analytics APIs**

#### `POST /api/uploads/new/`
* **Purpose:** The core Computer Vision API trigger. 
* **Payload:** Requires a form-data request containing `image=[file_binary]`.
* **Internal Routing:**
   1. Validates the JWT token.
   2. Writes the image safely to encrypted media storage.
   3. Sends the file path natively via `ai_service.py` to prompt the Object Detection model.
   4. Links the AI inference result with the valid database medicine.
* **Returns:** A comprehensive JSON block with `confidence_score`, `uploaded_image_url`, and the deeply nested JSON details of the predicted medicine so the mobile app doesn't have to launch a second request.

#### `GET /api/uploads/`
* **Purpose:** Chronological User Scan History.
* **Returns:** Lists the current authenticated user's previous uploads, useful to recreate a historical tracking interface of all medicines they've interacted with.

#### `GET /api/uploads/{id}/` *(NEW)*
* **Purpose:** Retrieves a definitive past scan along with the resulting AI analysis.

#### `DELETE /api/uploads/{id}/` *(NEW)*
* **Purpose:** Grants users privacy control, permitting deletion of past scanned images and result traces permanently.

---

### 🔐 **3. Auth Endpoints**
* `POST /auth/register/` ➔ Profile generation endpoint.
* `POST /api/token/` ➔ Grants Initial Login Tokens.
* `POST /api/token/refresh/` ➔ Refreshing continuous session lifetimes.

---

## 🔴 Immediate Actionable Backlog

1. **AI Model Docking:**
   - Plug the fully trained PyTorch/TensorFlow `.pt`/`.h5` detection script directly into the pre-fabricated `ai_service` proxy now that our extensive new dataset allows correct mappings.
2. **Cloud Server Bootstrapping:**
   - Push to production (AWS / DigitalOcean) utilizing PostgreSQL.
