# DJ Chemboi — Backend (Django REST Framework + PostgreSQL)

REST API powering the DJ Chemboi website: shop, cart, orders, bookings, events,
gallery, and music — plus a fully customized Django admin as the "Admin Dashboard".

## Stack
- Django 5 + Django REST Framework
- PostgreSQL (via `django-environ`, falls back to SQLite automatically if `DATABASE_URL` isn't set)
- JWT auth via `djangorestframework-simplejwt`
- `django-cors-headers` for the React frontend
- `django-filter` for product search/filtering

## Setup

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # then edit DATABASE_URL, SECRET_KEY, etc.
```

### PostgreSQL
Create the database referenced in your `.env`:
```sql
CREATE DATABASE djchemboi;
CREATE USER djchemboi_user WITH PASSWORD 'djchemboi_pass';
GRANT ALL PRIVILEGES ON DATABASE djchemboi TO djchemboi_user;
```
No Postgres handy? Leave `DATABASE_URL` unset in `.env` and it'll use local SQLite instead — fine for development.

### Migrate, seed, and run
```bash
python manage.py migrate
python manage.py seed_demo_data       # optional: matches the frontend's mock data
python manage.py createsuperuser
python manage.py runserver
```

Admin dashboard: http://127.0.0.1:8000/admin/
API root: http://127.0.0.1:8000/api/

## API Overview

| Resource | Endpoint | Notes |
|---|---|---|
| Auth | `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/login/refresh/`, `GET/PATCH /api/auth/me/` | JWT, `login` expects `{email, password}` |
| Categories | `/api/categories/` | Read: public. Write: staff only |
| Products | `/api/products/?category__slug=hoodies&search=neon&ordering=price` | Filter, search, order |
| Cart | `/api/cart/`, `/api/cart/items/`, `/api/cart/items/<id>/` | Requires auth |
| Orders | `/api/orders/` (`POST` creates from current cart) | Requires auth; staff can update `status` |
| Bookings | `/api/bookings/` | `POST` is public (booking form); `GET` staff only |
| Events | `/api/events/` | Read: public. Write: staff only |
| Gallery | `/api/gallery/` | Read: public. Write: staff only |
| Tracks | `/api/tracks/` | Read: public. Write: staff only |

Order `status` values: `PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`, `CANCELLED`.

## Razorpay
Payment fields (`razorpay_order_id`, `razorpay_payment_id`, `is_paid`) and a commented-out
integration block already exist on `Order` / `OrderViewSet.create()` in `orders/views.py`.
Add your keys to `.env` (`RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`), `pip install razorpay`,
and uncomment that block to go live.

## Admin Dashboard capabilities
- Products: add/edit/delete, inline gallery images, stock-status badges, bulk price/stock edit
- Categories: manage, with product counts
- Orders: color-coded status badges, inline order items, staff-only status updates
- Bookings: manage enquiries with status pipeline (New → Contacted → Confirmed → Closed)
- Events, Gallery, Tracks: full CRUD with image previews

## Connecting the React frontend
Set `CORS_ALLOWED_ORIGINS` in `.env` to your frontend's dev/prod URL (defaults to
`http://localhost:5173`). The frontend's `AuthContext`/`CartContext` mock functions
map 1:1 to the endpoints above — swapping them for real `fetch`/`axios` calls is a
drop-in replacement, no restructuring needed.
