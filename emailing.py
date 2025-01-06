import smtplib
import imghdr
from email.message import EmailMessage


sender = "Email id"
password = "Your password"
receiver = "Email id"


def send_emai(image_path):
    email_message = EmailMessage()
    email_message["subject"] = "Alert"
    email_message.set_content("Someone showed up at your door")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()


if __name__== "__main__":
    send_emai(image_path="images/16.png")