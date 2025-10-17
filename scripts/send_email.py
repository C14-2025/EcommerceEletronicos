import os
from email.message import EmailMessage
import smtplib
 
def main():
    
    RECIPIENT = os.getenv("RECIPIENT")
    PIPELINE_MSG = os.getenv("PIPELINE_MSG", "Pipeline executado!")
 
    if not RECIPIENT:
        print("Warning: RECIPIENT not set. Email will not be sent.")
        return
 
    msg = EmailMessage()
    msg["From"] = "no-reply@example.com"
    msg["To"] = RECIPIENT
    msg["Subject"] = "CI Pipeline Notification"
    msg.set_content(f"{PIPELINE_MSG}\n\nThis is an automated message from GitHub Actions.")
 
    try:
        
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
        print(f"Email sent to {RECIPIENT} (via localhost).")
    except Exception as e:
        print("Failed to send email:", e)
        print("No SMTP server configured. Email not sent, but pipeline continues.")
 
if __name__ == "__main__":
    main()