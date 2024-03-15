<div style="display:flex; justify-content: center; align-items: center ; height" 100vh" align=center>
  <img src='https://github.com/BaraSedih11/Bookstore/assets/98843912/51d3309c-21ae-4e6c-b237-b2d32869a3dd' /> 

  <br />
  <br />
  
   ![GitHub repo size](https://img.shields.io/github/repo-size/BaraSedih11/Bookstore_Flask) ![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/BaraSedih11/Bookstore_Flask) [![Python Version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Pip Version](https://img.shields.io/badge/pip-21.0-orange)](https://pypi.org/project/pip/21.0/)
 ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/BaraSedih11/Bookstore_Flask/main)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue)](https://github.com/BaraSedih/Bookstore_Flask/releases/tag/v1.0.0)
[![Contributors](https://img.shields.io/github/contributors/BaraSedih11/Bookstore_Flask)](https://github.com/BaraSedih11/Bookstore_Flask/graphs/contributors)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/BaraSedih11/Bookstore_Flask)
<!-- ![GitHub issues](https://img.shields.io/github/issues-raw/BaraSedih11/Bookstore)  -->
</div>
<br />

This is a Flask-based web application for managing a bookstore. Users can sign up, log in, browse books, add books to their shopping cart, and place orders. Managers can add, update, and delete books from the inventory.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/BaraSedih11/Bookstore_Flask.git
```

2. Navigate to the project directory:
```bash
cd Bookstore_Flask
```

3. Install the dependencies:
```python
from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
import os
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import sessionmaker
```

4. Run the application:
```bash
python app.py
```

The application will be accessible at 'http://127.0.0.1:5000/' in your web browser.

## Features
* User Authentication: Users can sign up, log in, and log out. Passwords are hashed for security.
* Book Management: Managers can add, update, and delete books from the inventory.
* Shopping Cart: Users can add books to their shopping cart and view their cart contents.
* Order Placement: Users can place orders for books in their shopping cart.
* Order History: Users can view their order history and total sales.

## Technologies Used
* Flask: Web framework for building the application.
* SQLAlchemy: Object-Relational Mapping (ORM) library for database interactions.
* Marshmallow: Library for object serialization and deserialization.
* SQLite: Lightweight relational database management system.

## Documentation
For detailed documentation and user guides, please refer to the [Documentation](https://documenter.getpostman.com/view/33323023/2sA2xnw9fR).

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

