import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender():
    def __init__(self,path):
        self.subject = "An email with Bug attachment"
        self.body = "An email with Bug attachment"
        self.sender_email = "attdev27@gmail.com"
        self.receiver_email = "attdev27@gmail.com"
        self.password = "tomAriel"
        self.path = path

    def send(self, exception):
        exception = self.checkHeaderValidation(exception)
        try:
            self.body = exception
            self.subject = exception
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.receiver_email
            message["Subject"] = self.subject
            message["Bcc"] = self.receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(self.body, "plain"))

            filename = self.path  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()

            # Log in to server using secure context and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, self.receiver_email, text)

        except Exception as e:
            print(e)

    def checkHeaderValidation(self, exception):
        lastChar = ''
        for i in range(len(exception)):
            if (lastChar == '\n' and exception[i] != ' '):
                exception = exception[:i] + ' ' + exception[i:]
            lastChar = exception[i]
        return exception
