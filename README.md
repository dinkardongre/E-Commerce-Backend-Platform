# E-Commerce Backend Platform

A robust, scalable, and modular e-commerce backend platform built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. This project supports advanced authentication, admin & seller roles, category and product management, shopping cart, and order processing for modern online shopping applications.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.116-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v14-blue)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## Features

- User roles: Admin, Seller, and Normal Users with role-based access control  
- Product and category management by admins and sellers  
- Shopping cart functionality per user  
- Order placement with stock validation and address management  
- JWT based authentication  
- Clean architecture with modular code organization  
- PostgreSQL database integration  

---

## Tech Stack

- Python 3.x  
- FastAPI  
- SQLAlchemy ORM  
- PostgreSQL

---

## Getting Started

### Prerequisites

- Python 3.8 or higher  
- PostgreSQL installed and running  
- Git command line tools  

### Installation

1. Clone the repository:

git clone https://github.com/dinkardongre/E-Commerce-Backend-Platform.git
cd E-Commerce-Backend-Platform

2. Create and activate a virtual environment:

python -m venv env
source env/bin/activate # Windows: env\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Configure environment variables:

Create a `.env` file in the root directory and add:

DATABASE_URL=postgresql://user:password@localhost:5432/your_db
SECRET_KEY=your_secret_key

5. Run the application:

fastapi dev main.py

7. Open [http://localhost:8000/docs](http://localhost:8000/docs) to access the interactive API documentation.

---

## API Endpoints

- User registration, login, and role management  
- Product and category CRUD operations (restricted to admin and seller)  
- Shopping cart management  
- Order placement with stock validation and order history  

---

## Contribution

Contributions and suggestions are welcome!  
Please open issues or submit pull requests for bug fixes, features, or improvements.

---

## Contact

For any questions or feedback, please reach out at **dongredinkar34@gmail.com**

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Last updated: September 2025*
