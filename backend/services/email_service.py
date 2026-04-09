import datetime

class EmailService:
    """
    A service for handling automated email communications.
    Currently simulates sending emails and returning the log data.
    Designed to easily integrate with Google OAuth / Gmail API in the future.
    """

    def __init__(self, google_auth_token=None):
        # Future implementation: Initialize Google API client with OAuth token
        # self.creds = Credentials(google_auth_token)
        # self.service = build('gmail', 'v1', credentials=self.creds)
        self.google_auth_token = google_auth_token

    def send_email(self, to_email, subject, body, email_type="general", candidate_name=None):
        """
        Sends an email (simulated for now) and returns a structured dictionary
        representing the communication, ready to be appended to Firestore.
        """
        # --- Future Gmail API Implementation --- #
        # message = MIMEText(body)
        # message['to'] = to_email
        # message['subject'] = subject
        # raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        # self.service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        
        print(f"\n[EMAIL SIMULATION] Sending '{subject}' to {to_email}")
        
        return {
            "type": email_type,
            "subject": subject,
            "body": body,
            "to": to_email,
            "sent_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

    def send_advancement_email(self, to_email, candidate_name, job_title, company, next_round_name):
        subject = f"Update on your application for {job_title} at {company}"
        body = f"""Hi {candidate_name},

Great news! The team has reviewed your application and we'd like to move you forward to the next round: {next_round_name}.

We will be in touch shortly with more details on the next steps.

Best regards,
The {company} Hiring Team"""
        return self.send_email(to_email, subject, body, "advancement", candidate_name)

    def send_hired_email(self, to_email, candidate_name, job_title, company):
        subject = f"Offer for {job_title} at {company}!"
        body = f"""Hi {candidate_name},

Congratulations! We were extremely impressed with you throughout the interview process and we are thrilled to offer you the {job_title} position at {company}.

We will be sending over the official offer details and paperwork shortly. We can't wait to have you on the team!

Best regards,
The {company} Hiring Team"""
        return self.send_email(to_email, subject, body, "offer", candidate_name)

    def send_rejection_email(self, to_email, candidate_name, job_title, company, current_round_name):
        subject = f"Update on your application for {job_title} at {company}"
        body = f"""Hi {candidate_name},

Thank you for taking the time to apply for the {job_title} role and for speaking with us. 

While we were impressed with your background, we have decided to move forward with other candidates whose experience more closely matches the specific needs of the role at this time.

We wish you the best of luck in your job search and future career endeavors.

Best regards,
The {company} Hiring Team"""
        return self.send_email(to_email, subject, body, "rejection", candidate_name)
