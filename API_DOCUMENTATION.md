# API Endpoints Documentation

## Authentication Endpoints
Base URL: `/auth/`

### User Registration
- **POST** `/auth/register/`
- **POST** `/auth/login/`
- **POST** `/auth/logout/`
- **POST** `/auth/token/refresh/`
- **GET** `/auth/profile/`
- **PUT/PATCH** `/auth/profile/update/`
- **POST** `/auth/password/change/`

---

## Medicine Endpoints
Base URL: `/api/`

### List All Medicines
**GET** `/api/medicines/`

Query Parameters:
- `search` - Search by code, name (AR/EN), scientific name, category
- `category` - Filter by category
- `ordering` - Sort by: name_ar, name_en, price, created_at

Example:
```
GET /api/medicines/?category=مسكنات&ordering=price
GET /api/medicines/?search=بانادول
```

Response:
```json
[
  {
    "id": 1,
    "code": "MED001",
    "name_ar": "بانادول",
    "name_en": "Panadol",
    "category": "مسكنات",
    "price": "15.50"
  }
]
```

---

### Get Medicine Details
**GET** `/api/medicines/{code}/`

Example: `GET /api/medicines/MED001/`

Response:
```json
{
  "id": 1,
  "code": "MED001",
  "name_ar": "بانادول",
  "name_en": "Panadol",
  "scientific_name": "Paracetamol 500mg",
  "manufacturer": "GlaxoSmithKline",
  "description_ar": "مسكن للألم وخافض للحرارة",
  "description_en": "Pain reliever and fever reducer",
  "dosage": "قرص واحد كل 4-6 ساعات",
  "side_effects": "نادراً: غثيان، طفح جلدي",
  "warnings": "لا تتجاوز الجرعة الموصى بها",
  "category": "مسكنات",
  "price": "15.50",
  "image": null,
  "image_url": null,
  "is_active": true,
  "created_at": "2025-12-09T10:00:00Z",
  "updated_at": "2025-12-09T10:00:00Z"
}
```

---

### Search Medicines
**GET** `/api/medicines/search/?q={query}`

Example: `GET /api/medicines/search/?q=بانادول`

Returns up to 20 matching medicines with full details.

---

## Image Upload Endpoints

### Upload & Detect Medicine
**POST** `/api/uploads/new/`

Headers:
```
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

Body (form-data):
```
image: [file]
```

Response:
```json
{
  "id": 1,
  "image": "/media/uploads/2025/12/09/medicine.jpg",
  "image_url": "http://localhost:8000/media/uploads/2025/12/09/medicine.jpg",
  "detected_medicine": 1,
  "medicine_details": {
    "id": 1,
    "code": "MED001",
    "name_ar": "بانادول",
    "name_en": "Panadol",
    "scientific_name": "Paracetamol 500mg",
    "category": "مسكنات",
    "price": "15.50"
  },
  "confidence": 0.85,
  "result": "{\"medicine_code\": \"MED001\", \"confidence\": 0.85, ...}",
  "created_at": "2025-12-09T12:30:00Z"
}
```

---

### List User Uploads
**GET** `/api/uploads/`

Returns all uploads for the authenticated user, ordered by newest first.

Response:
```json
[
  {
    "id": 1,
    "image": "/media/uploads/2025/12/09/medicine.jpg",
    "image_url": "http://localhost:8000/media/uploads/2025/12/09/medicine.jpg",
    "detected_medicine": 1,
    "medicine_details": { ... },
    "confidence": 0.85,
    "result": "...",
    "created_at": "2025-12-09T12:30:00Z"
  }
]
```

---

## Setup Instructions

### 1. Run Migrations
```bash
cd medrec
python manage.py makemigrations
python manage.py migrate
```

### 2. Load Sample Data
```bash
python manage.py load_sample_medicines
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Run Server
```bash
python manage.py runserver
```

---

## AI Model Integration

Edit `medrec/core/ai_service.py` and replace the `infer()` function with your actual model:

```python
def infer(image_path: str) -> dict:
    # 1. Load your trained model
    model = load_model('path/to/model')
    
    # 2. Preprocess image
    image = preprocess_image(image_path)
    
    # 3. Run prediction
    prediction = model.predict(image)
    
    # 4. Return result
    return {
        'medicine_code': prediction['code'],
        'confidence': prediction['confidence'],
        'description': 'Detected successfully',
        'alternatives': prediction['alternatives']
    }
```

---

## Testing with Postman

Import `MedRec_API.postman_collection.json` for ready-to-use API requests.
