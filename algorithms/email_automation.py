import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

class EmailAutomation:
    def __init__(self, user_email, user_password):
        self.user_email = user_email
        self.user_password = user_password

    def send_email(self, recipient_list, subject, body):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587) 
            server.starttls()
            server.login(self.user_email, self.user_password)
            for recipient in recipient_list:
                msg = MIMEMultipart()
                msg['From'] = self.user_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                server.send_message(msg)
                print(f"Email sent to {recipient} successfully!")
            server.quit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def schedule_email(self, recipient_list, subject, body, schedule_time):
        def job():
            print(f"Scheduled email sending triggered at {schedule_time}")
            self.send_email(recipient_list, subject, body)
        schedule.every().day.at(schedule_time).do(job)
        print(f"Email scheduled at {schedule_time}")
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    def fetch_emails_from_recipients(self, recipient_list):
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.user_email, self.user_password)
            mail.select('inbox')
            for recipient in recipient_list:
                print(f"Checking emails from: {recipient}")
                status, messages = mail.search(None, f'FROM "{recipient}"')
                email_ids = messages[0].split()
                for email_id in email_ids:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject = msg['subject']
                            sender = msg['from']
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print(f"From: {sender}\nSubject: {subject}\nBody: {body}\n")
                            else:
                                body = msg.get_payload(decode=True).decode()
                                print(f"From: {sender}\nSubject: {subject}\nBody: {body}\n")
            mail.logout()
        except Exception as e:
            print(f"An error occurred while fetching emails: {e}")


if __name__ == "__main__":
    # Collect user email information 
    user_email = input("Enter your email id: ")
    user_password = input("Enter your email password: ")

    recipients = ['abcd@123gmail.com', 'xyz@567yahoo.in']

    subject = "Test Email"
    body = "This is an automated email sent using Python."

    email_automation = EmailAutomation(user_email, user_password)
    
    option = input("Schedule your email (y for yes): ").lower()
    if (option != 'y' or option != 'yes'):
       print("Sending emails immediately...")
       email_automation.send_email(recipients, subject, body)
    else:
        schedule_time = input("Enter time as (HH:MM) : ")
        print(f"Scheduling email at {schedule_time}...")
        email_automation.schedule_email(recipients, subject, body, schedule_time)
     
     fetch_option = input("Do you want to check emails from recipients? (y for yes): ").lower()
     if fetch_option in ('y', 'yes'):
        print("Fetching emails from recipients...")
        email_automation.fetch_emails_from_recipients(recipients)
        
