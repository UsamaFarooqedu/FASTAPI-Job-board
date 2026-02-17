from typing import List
from ..models.user import User

def send_email_notification(email: str, subject: str, body: str):
    # Mock email sending
    print(f"DEBUG: Sending email to {email}")
    print(f"DEBUG: Subject: {subject}")
    print(f"DEBUG: Body: {body}")

def notify_application_status_change(user_email: str, job_title: str, new_status: str):
    subject = f"Update on your application for {job_title}"
    body = f"Your application status has been updated to: {new_status}"
    send_email_notification(user_email, subject, body)

def notify_new_application(company_email: str, job_title: str, applicant_name: str):
    subject = f"New application for {job_title}"
    body = f"{applicant_name} has applied for your job posting: {job_title}"
    send_email_notification(company_email, subject, body)
