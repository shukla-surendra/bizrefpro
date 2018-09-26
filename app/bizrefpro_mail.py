import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_enquiry_email(name, e_email, phone, location):
   SENDER = 'info@bizrefpro.com'  
   SENDERNAME = 'BizRefPro Enquiry'
   RECIPIENT  = 'info@bizrefpro.com'
   USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
   PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
   HOST = "email-smtp.us-east-1.amazonaws.com"
   PORT = 587
   SUBJECT = 'BizRefPro Promotional Enquiry Form'
   BODY_TEXT = ""
   BODY_HTML = "<html><head></head><body><p>Name:"+name+"</p><p>Email:"+e_email+"</p><p>Phone:"+phone+"</p><p>Location:"+location+"</p></body></html>"
   msg = MIMEMultipart('alternative')
   msg['Subject'] = SUBJECT
   msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
   msg['To'] = RECIPIENT
   part1 = MIMEText(BODY_TEXT, 'plain')
   part2 = MIMEText(BODY_HTML, 'html')
   msg.attach(part1)
   msg.attach(part2)
   try:  
       server = smtplib.SMTP(HOST, PORT)
       server.ehlo()
       server.starttls()
       server.ehlo()
       server.login(USERNAME_SMTP, PASSWORD_SMTP)
       server.sendmail(SENDER, RECIPIENT, msg.as_string())
       server.close()
   except Exception as e:
       print("Error: ", e)
   else:
       print("Email sent!")


def send_userforget_password_link_mail(user):
   SENDER = 'info@bizrefpro.com'  
   SENDERNAME = 'BizRefPro Support'
   RECIPIENT  = user.email
   USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
   PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
   HOST = "email-smtp.us-east-1.amazonaws.com"
   PORT = 587
   SUBJECT = 'BizRefPro Password Reset Link'
   BODY_TEXT = "Please copy and paste this link to url http://bizrefpro.com/reset-user-password/"+user.verification_key
   BODY_HTML = "<html><head></head><body><a target='_blank' href='http://bizrefpro.com/reset-user-password/"+user.verification_key+"'>Reset Password</a><br/>if above link does not work. please copy and paste below link to your browser<br/>http://bizrefpro.com/reset-user-password/"+user.verification_key+"<br/></body></html>"
   msg = MIMEMultipart('alternative')
   msg['Subject'] = SUBJECT
   msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
   msg['To'] = RECIPIENT
   part1 = MIMEText(BODY_TEXT, 'plain')
   part2 = MIMEText(BODY_HTML, 'html')
   msg.attach(part1)
   msg.attach(part2)
   try:  
       server = smtplib.SMTP(HOST, PORT)
       server.ehlo()
       server.starttls()
       server.ehlo()
       server.login(USERNAME_SMTP, PASSWORD_SMTP)
       server.sendmail(SENDER, RECIPIENT, msg.as_string())
       server.close()
   except Exception as e:
       print("Error: ", e)
   else:
       print("Email sent!")


def send_otp(email_to_send, otp):
    SENDER = 'info@bizrefpro.com'  
    SENDERNAME = 'BizRefPro Support'
    RECIPIENT  = email_to_send
    USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
    PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
    HOST = "email-smtp.us-east-1.amazonaws.com"
    PORT = 587
    SUBJECT = 'OTP fro BizRefPro Thumsup'
    BODY_TEXT = "Your Bizrefpro otp is"+str(otp)
    BODY_HTML = "<html><head></head><body>Your Bizrefpro otp is "+str(otp)+"<br/></body></html>"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent!")


def send_invitation(name, email_to_send, inviter_name, key):
    SENDER = 'info@bizrefpro.com'  
    SENDERNAME = inviter_name
    RECIPIENT  = email_to_send
    USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
    PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
    HOST = "email-smtp.us-east-1.amazonaws.com"
    PORT = 587
    SUBJECT = inviter_name+' invited you to join Bizrefpro'
    BODY_TEXT = "copy and paste the link to browser user and signup  https://bizrefpro.com/login-register?referer="+key
    BODY_HTML = "<html><head></head><body> <p>Click on below link to signup <br/><a href='https://bizrefpro.com/login-register?referer="+key+"'>Click Here</a></p></body></html>"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME_SMTP, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent!")
