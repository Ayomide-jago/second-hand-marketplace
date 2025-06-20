# Second‑Hand Marketplace

A web application built with **Django** that enables people to buy and sell pre‑owned items safely and conveniently.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Running Tests](#running-the-tests)
6. [Deployment](#deployment)
7. [Contributing](#contributing)
8. [License](#license)
9. [Author](#author)

---

## Features

* **Browse & Search** second‑hand items by category, condition, price, and location.
* **Seller Dashboard** to create, edit, and delete listings (images, description, price).
* **Messaging System** so buyers can contact sellers directly (email or in‑app inbox).
* **Ratings & Reviews** — buyers can leave feedback after a successful transaction.
* **Favorites/Watch‑list** to bookmark interesting items.
* **User Authentication** (sign‑up, login, password reset) with email verification.
* **Responsive UI** built entirely with **Bootstrap 5**.
* **Lightweight Codebase** — no `forms.py`; forms are rendered with plain HTML + Bootstrap classes.
* SEO‑friendly URLs and meta tags.

---

## Tech Stack

| Layer        | Tech                             |
| ------------ | -------------------------------- |
| **Backend**  | Python 3.12 · Django 5.x         |
| **Database** | SQLite (dev) · PostgreSQL (prod) |
| **Frontend** | HTML5 · Bootstrap 5 · Vanilla JS |
| **Images**   | Pillow                           |
| **Dev Ops**  | Docker · GitHub Actions (CI/CD)  |

---

## Quick Start

### 1 · Clone & Install

```bash
# Clone
git clone https://github.com/<Ayomide-jago>/second-hand-marketplace.git
cd secondhand-marketplace

# Create virtual env
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install deps
pip install -r requirements.txt
```

```

### 2 · Database & Static Assets

```bash
python manage.py migrate             # create tables
python manage.py loaddata seed       # optional: demo data
python manage.py collectstatic       # only for production
```

### 4 · Run the Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and start exploring!

---


## Running the Tests

```bash
python manage.py test
```

---

## Deployment

One‑click deploy recipes for **Heroku**, **Railway**, and **Fly.io** are provided in the `deploy/` folder (Dockerfile, Procfile, and GitHub Actions workflow).

---

## Contributing

Pull requests are welcome!  To contribute:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/awesome‑thing`.
3. Commit your changes: `git commit -m 'Add awesome thing'`.
4. Push to the branch: `git push origin feature/awesome‑thing`.
5. Open a Pull Request.

---

## License

Distributed under the **MIT License**.  See `LICENSE` for more information.

---

## Author

**Odugbesan Leke**  ·  <[https://github.com/Ayomide-jago/second-hand-marketplace]

Feel free to reach out if you have questions or suggestions!

---

> *Screenshots coming soon — add screenshots or a short demo GIF here to showcase the app in action.*
