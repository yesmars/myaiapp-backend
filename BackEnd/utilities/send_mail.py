# utilities/email.py
from flask_mail import Message
from flask import current_app
from BackEnd.extensions import mail

def send_welcome_email(to_email, first_name):
    msg = Message(
        subject='Welcome to Van-AI!', 
        sender='vanailearnmore@gmail.com',  # Ensure this matches MAIL_USERNAME
        recipients=[to_email],  # Replace with actual recipient's email
        html=f'<strong>Hello {first_name},</strong><br> <br>Welcome to VanAI! <br> <br> We are excited to have you on board. Thank you for trying our website!<br> <br> We are always here to help you. If you have any questions, feel free to ask us. <br> <br> We hope you enjoy your time with us! <br> <br><br> <br> Best Regards, <br> VanAI Team<br>vanailearnmore@gmail.com<br>https://www.van-ai.com'
    )
    
    
    mail.send(msg)
    print("Message sent!")
    return "Message sent!"
