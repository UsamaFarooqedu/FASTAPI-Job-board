# Job Board Platform

A comprehensive FastAPI-based job board platform with dual interfaces for Employers and Job Seekers.

## Features
- **Dual User Roles**: Employee (Job Seeker) and Company (Employer).
- **Authentication**: JWT-based secure login and registration.
- **Job Management**: Companies can post and manage job listings.
- **Job Applications**: Employees can upload resumes and apply to jobs.
- **Social Feed**: Professional content sharing with image support.
- **Responsive Design**: Modern, premium UI built with Vanilla CSS.

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
1. Navigate to the project directory:
   ```bash
   cd "d:/Job board/job_board"
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup environment variables:
   - Create a `.env` file (one has been provided for you).

### Technical Setup (Fast Track)
Since this is a development version with SQLite, you can initialize the database models directly:
```bash
# In an interactive python shell or via a script
from app.database import engine, Base
from app.models import user, job, application, post
Base.metadata.create_all(bind=engine)
```

### Running the Application
```bash
uvicorn app.main:app --reload
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure
- `app/api`: API route definitions.
- `app/models`: SQLAlchemy database models.
- `app/schemas`: Pydantic data validation schemas.
- `app/services`: Business logic (Auth, File handling).
- `templates`: Jinja2 HTML templates.
- `static`: CSS and user uploads.
