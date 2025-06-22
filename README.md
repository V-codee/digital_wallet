
# 💳 Digital Wallet System

A secure and efficient digital wallet system built using **FastAPI**, **MySQL**, and **SQLAlchemy**, providing functionalities such as wallet creation, deposit, withdrawal, money transfer, transaction history, add product, purchase any product and currency conversion using an external API.

---

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT + Bcrypt
- **External API**: [CurrencyAPI](https://currencyapi.com)

---

## 📦 Features

- 🔐 User registration and login (with JWT authentication)
- 👛 Wallet creation per user
- ➕ Deposit to wallet
- ➖ Withdraw from wallet
- 🔄 Transfer funds to other users
- 📜 Transaction history for every wallet
- 💱 Real-time currency conversion (INR <-> USD, etc.)
- 📂 Clean code structure and modular design

---

## 🔧 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/digital-wallet-system.git
cd digital-wallet-system
```

### 2. Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env` file

Create a `.env` file in the root directory and add:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=digital_wallet
SECRET_KEY=your_secret_key

```

### 5. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for Swagger UI.

---

## 🧪 API Endpoints

| Method | Endpoint                    | Description                  |
|--------|-----------------------------|------------------------------|
| POST   | /auth/register              | Register a new user         |
| POST   | /auth/login                 | Login user and get token    |
| POST   | /wallet/create              | Create wallet (auth)        |
| POST   | /wallet/deposit             | Deposit funds               |
| POST   | /wallet/withdraw            | Withdraw funds              |
| POST   | /wallet/transfer            | Transfer to another wallet  |
| GET    | /wallet/transactions        | Transaction history         |
| GET    | /wallet/convert-currency    | Convert currency            |

---

## ✅ TODO (Future Scope)

- Admin dashboard
- Email notifications
- Account deletion
- Wallet-to-bank withdrawal

---

## 🧑‍💻 Author

**Omm Prakash Sahoo**  
B.Tech CSE, ITER, SOA University  
[GitHub](https://github.com/V-codee)

---
