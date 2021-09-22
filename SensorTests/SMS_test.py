# Code taken from https://dev.to/mraza007/sending-sms-using-python-jkd

import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os #For environment variables.

# If your email uses 2-step verification, an app password should be used.
# https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637678745617100032-1453695746&rd=1

email = os.environ.get('SMS_Email')
pas = os.environ.get('SMS_Password')

sms_gateway = '2085158976@tmomail.net' #Change the number here to your own.
# The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
# and port is also provided by the email provider.
smtp = "smtp.gmail.com" 
port = 587
# This will start our email server
server = smtplib.SMTP(smtp,port)
# Starting the server
server.starttls()
# Now we need to login
server.login(email,pas)

# Now we use the MIME module to structure our message.
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = sms_gateway
# Make sure you add a new line in the subject
msg['Subject'] = "You can insert anything\n"
# Make sure you also add new lines to your body
body = "You can insert message here\n"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email,sms_gateway,sms)

# lastly quit the server
server.quit()
