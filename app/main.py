from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .api import auth, users, jobs, applications, posts
import os

app = FastAPI(title="Job Board Platform")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["Applications"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])

# HTML Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.get("/dashboard")
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/jobs")
async def jobs_page(request: Request):
    return templates.TemplateResponse("jobs/index.html", {"request": request})

@app.get("/feed")
async def feed_page(request: Request):
    return templates.TemplateResponse("posts/index.html", {"request": request})

@app.get("/company/post-job")
async def post_job_page(request: Request):
    return templates.TemplateResponse("company/post_job.html", {"request": request})

@app.get("/company/manage-jobs")
async def manage_jobs_page(request: Request):
    return templates.TemplateResponse("company/manage_jobs.html", {"request": request})

@app.get("/employee/profile")
async def employee_profile_page(request: Request):
    return templates.TemplateResponse("employee/profile.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
