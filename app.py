import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


app.config.update(
    MAIL_SERVER=os.getenv('EMAIL_HOST'),
    MAIL_PORT=int(os.getenv('EMAIL_PORT')),
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('EMAIL_USER'),
    MAIL_PASSWORD=os.getenv('EMAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('EMAIL_SENDER')
)


mail = Mail(app)



@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404



@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500



def send_email(recipient_email, message_body):
    msg = Message(
        subject="Message from Flask App",
        recipients=[recipient_email],
        body=message_body
    )
    mail.send(msg)



@app.route('/send-email', methods=['POST'])
def send_email_route():
    try:

        data = request.get_json()


        message_body = data.get('message')
        recipient_email = data.get('email')


        if not message_body or not recipient_email:
            return jsonify({'error': 'Missing message or email'}), 400


        send_email(recipient_email, message_body)

        return jsonify({'success': True, 'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
