# 🍏 Apple Store (Dummy Payment Integration)

This project is a **Flask-based backend** for a dummy Apple Store that simulates order creation and payment handling.  
It uses **Razorpay-like APIs** but does not connect to real Razorpay — useful for testing and learning payment flows.

---

## 📂 Project Structure

```
apple-store/
│── app.py                 # Main Flask entry point
│── requirements.txt       # Dependencies
│── README.md              # Project documentation
│
├── models/                # Database models
│   ├── order_model.py
│   ├── payment_model.py
│
├── routes/                # API routes
│   ├── order_routes.py    # Order creation & management
│   ├── payment_routes.py  # Payment creation & updates
│
└── utils/                 # Helper functions
    ├── db.py              # Database connection
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/apple-store.git
cd apple-store
```

### 2. Create a virtual environment
```bash
python -m venv .venv
```

### 3. Activate the virtual environment
- **Windows (PowerShell):**
  ```bash
  .venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Project

Start the Flask app:
```bash
python app.py
```

The backend will be available at:
```
http://127.0.0.1:5000/
```

---

## 📌 API Endpoints

### 🔹 Create Order
```http
POST /order/create
Content-Type: application/json

{
  "product_id": 1,
  "amount": 1200
}
```
✅ Returns:
```json
{
  "order_id": "ORD123",
  "status": "created",
  "amount": 1200
}
```

---

### 🔹 Create Payment
```http
POST /payment/create
Content-Type: application/json

{
  "order_id": "ORD123",
  "razorpay_payment_id": "pay_987xyz"
}
```
✅ Returns:
```json
{
  "payment_id": "PAY123",
  "status": "success"
}
```

---

### 🔹 Update Payment Status
```http
POST /payment/update
Content-Type: application/json

{
  "razorpay_payment_id": "pay_987xyz",
  "status": "success"
}
```

---

## 🛠️ Tech Stack
- **Python 3.11+**
- **Flask**
- **SQLite / PostgreSQL (configurable)**

---

## ⚠️ Note
- This project **does not use real Razorpay**.
- Payment IDs and Orders are **dummy generated for testing**.
- Useful for **learning payment flow integration**.

---

## 👨‍💻 Author
Created by **Janardhan Reddy** 🚀  
For testing and learning purposes only.
