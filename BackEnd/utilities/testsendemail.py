from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'vanailearnmore@gmail.com'  # Use your actual Gmail address
app.config['MAIL_PASSWORD'] =  ''    # Use your generated App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/")
def index():
    msg = Message(
        subject='Welcome to Van-AI!', 
        sender='vanailearnmore@gmail.com',  # Ensure this matches MAIL_USERNAME
        recipients=['vnncly@gmail.com'],  # Replace with actual recipient's email
        html=f'<strong>Hello van,</strong><br> <br>Welcome to VanAI! <br> <br> We are excited to have you on board. Thank you for trying our website!<br> <br> We are always here to help you. If you have any questions, feel free to ask us. <br> <br> We hope you enjoy your time with us! <br> <br><br> <br> Best Regards, <br> VanAI Team<br>vanailearnmore@gmail.com<br>https://www.van-ai.com'
    )
    
    
    mail.send(msg)
    print("Message sent!")
    return "Message sent!"

if __name__ == '__main__':
    app.run(debug=True)
