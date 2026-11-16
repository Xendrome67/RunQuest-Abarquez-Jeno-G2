# IM2 Project - Account Feature

A Django-based web application with a complete Account Feature including registration, login/logout, role-based dashboards, and user profiles.

## Features

- **Account Registration**: Users can create accounts with validation (required fields, valid email, unique username/email, password confirmation)
- **Login/Logout**: Secure authentication with email or username, session management
- **Role-Based Dashboards**: Two roles (Admin & Customer) with protected, role-specific dashboards
- **User Profile**: View and edit profile information (name, email, phone, profile photo)
- **Security**: Passwords hashed using Django's built-in authentication, CSRF protection, secure sessions

## Tech Stack

- **Backend**: Django 6.1.3
- **Database**: PostgreSQL (Supabase compatible)
- **Frontend**: Django Templates with Bootstrap 5.3
- **Environment**: Python 3.12+

## Project Structure

```
IM2-Project/
├── accounts/                 # Accounts app
│   ├── migrations/          # Database migrations
│   ├── templates/accounts/  # Account templates
│   ├── admin.py            # Admin configuration
│   ├── forms.py            # Forms (registration, login, profile)
│   ├── models.py           # Custom User model with roles
│   ├── signals.py          # Django signals
│   ├── urls.py             # URL routing
│   └── views.py            # Views for all account features
├── im2_project/            # Project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL configuration
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Media uploads (profile photos)
├── templates/              # Base templates
├── .env                    # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### 1. Prerequisites

- Python 3.12+
- PostgreSQL 14+ (or Supabase account)
- Git

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd IM2-Project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Local PostgreSQL

1. Install PostgreSQL and create a database:
```sql
CREATE DATABASE im2_db;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE im2_db TO postgres;
```

#### Option B: Supabase (PostgreSQL)

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Settings > Database to get connection details
3. Use the connection string or individual parameters

### 4. Environment Configuration

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
SECRET_KEY=your-secure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=im2_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## Usage

### Registration
1. Navigate to `/accounts/register/`
2. Fill in username, email, role (Admin/Customer), phone (optional), password
3. Submit to create account

### Login
1. Navigate to `/accounts/login/`
2. Enter email/username and password
3. Redirected to role-based dashboard

### Dashboards
- **Admin Dashboard** (`/accounts/dashboard/admin/`): User statistics, recent users, quick actions
- **Customer Dashboard** (`/accounts/dashboard/customer/`): Personalized overview, available services

### Profile
- View profile: `/accounts/profile/`
- Edit profile: `/accounts/profile/edit/`

### Admin Panel
Access Django admin at `/admin/` (requires superuser)

## Role-Based Access Control

- **Admin**: Full access to admin dashboard, can view all users
- **Customer**: Access to customer dashboard, can only view/edit own profile
- **URL Protection**: Users cannot access other roles' dashboards via direct URL

## Security Features

- Password hashing via Django's PBKDF2
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS protection via template auto-escaping
- Secure session management
- Environment-based configuration

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
```bash
# Install development dependencies
pip install black flake8 isort

# Format code
black .
isort .

# Lint
flake8
```

## Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` for your domain
4. Use PostgreSQL with SSL
5. Set up static file serving (nginx, WhiteNoise, or CDN)
6. Configure HTTPS
7. Set up database backups
8. Configure logging

### Docker (Optional)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "im2_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## License

This project is for educational purposes.

## Author

IM2 Project - Lastname-Firstname-Section