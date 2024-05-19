import smtplib
import ssl,qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'utsavpokemon9000chatterjee@gmail.com'
SMTP_PASSWORD = 'nzlettvkyviafplp'

class SendMail:

    @staticmethod
    def send_raw(sub:str,body:str,to:str):
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to
        message["Subject"] = sub
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        try:

            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD) 

            server.sendmail(SMTP_USERNAME, to, message.as_string())
            print("Email sent successfully")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            server.quit()
    
    @staticmethod
    def send_qr(sub:str,username:str,body:str,to:str,otp):
        message = MIMEMultipart()
        message["From"] = SMTP_USERNAME
        message["To"] = to
        message["Subject"] = sub
        message.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        try:
            qr=qrcode.make(otp.create(username=username))

            with BytesIO() as bio:
                qr.save(bio)
                qr_bytes = bio.getvalue()

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(qr_bytes)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={username}_qr.png')
            message.attach(part)

            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD) 

            server.sendmail(SMTP_USERNAME, to, message.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")

        finally:
            server.quit()


