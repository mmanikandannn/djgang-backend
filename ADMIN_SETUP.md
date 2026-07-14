# Custom Admin Dashboard

The dashboard uses Django's existing `admin.site`, so all model registrations remain available.

Files:
- `config/admin_views.py` — statistics and staff-only pages
- `config/templates/admin/index.html` — dashboard homepage
- `config/templates/admin/analytics.html` — analytics
- `config/templates/admin/management.html` — management shortcuts
- `config/urls.py` — admin dashboard routes
- `config/settings.py` — template directory

Run `python manage.py migrate`, create a superuser, and open `/admin/`.
