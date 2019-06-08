import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import timedelta


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
    SUBJECT = 'BiZRefPro OTP for Rating'
    BODY_TEXT = "Your Bizrefpro otp is "+str(otp)
    BODY_HTML = "<html><head></head><body>Your BizRefPro OTP for rating is "+str(otp)+"<br/></body></html>"
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

def send_otp_for_referral(email_to_send, otp):
    SENDER = 'info@bizrefpro.com'
    SENDERNAME = 'BizRefPro Support'
    RECIPIENT  = email_to_send
    USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
    PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
    HOST = "email-smtp.us-east-1.amazonaws.com"
    PORT = 587
    SUBJECT = 'BiZRefPro OTP for Rating'
    BODY_TEXT = "Your Bizrefpro otp is "+str(otp)
    BODY_HTML = "<html><head></head><body>Your BizRefPro OTP for referral is "+str(otp)+"<br/></body></html>"
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
    SUBJECT =inviter_name+' has invited you to join World 1 st Referral base Search Engine'
    BODY_TEXT = inviter_name+" has invited to Join you world’s 1st referral base search engine. Please visit below link or copy and paste the link to browser user and signup  https://bizrefpro.com/login-register?referer="+key
    BODY_HTML = "<html><head></head><body><p>Hii</p> <p>"+inviter_name+" has invited you to Join world’s 1st referral base search engine. Please <a href='https://bizrefpro.com/register-user?referer="+key+"'>Click Here</a> to signup and get business lead</p><br/><br/><br/><strong>BizRefPro Team</strong><br/>Email : info@bizrefpro.com<br/>Web   : https://www.bizrefpro.com<br/><b>ItInfo Technologies Pvt. Ltd</b></body></html>"
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


class BizEmailService:
    SENDER = 'info@bizrefpro.com'
    USERNAME_SMTP = "YOUR_SES_SMTP_USERNAME"
    PASSWORD_SMTP = "YOUR_SES_SMTP_PASSWORD"
    HOST = "email-smtp.us-east-1.amazonaws.com"
    PORT = 587

    def __init__(self):
        pass

    def send_signup_notification_to_admin(self, user):
        SUBJECT = 'New User Registation'
        BODY_TEXT = "A new user is waiting for your approval"
        BODY_HTML = "<html><head></head><body> <p>A new user is waiting for your approval</p><p>User Name:"+user.name+"</p><p>User Eamail:"+user.email+"</p></body></html>"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr(('BizRefPro New User', self.SENDER))
        msg['To'] = self.SENDER
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        msg.attach(part2)
        try:
            server = smtplib.SMTP(self.HOST, self.PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER, self.SENDER, msg.as_string())
            server.close()
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")



    def send_signup_notification_to_executive(self, user, executive):
        SUBJECT = 'New User Registation'
        BODY_TEXT = "A new user is waiting for your approval"
        BODY_HTML = "<html><head></head><body> <p>A new user is waiting for admin approval</p><p>User Name:"+user.name+"</p><p>User Eamail:"+user.email+"</p></body></html>"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr(('BizRefPro New User', self.SENDER))
        msg['To'] = executive.email
        part1 = MIMEText(BODY_TEXT, 'plain')
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part1)
        msg.attach(part2)
        try:
            server = smtplib.SMTP(self.HOST, self.PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER, executive.email, msg.as_string())
            server.close()
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")

    def send_approval_notification_to_user(self, user, password):
        start_date = user.created_at.strftime("%d/%m/%Y")
        end_time = user.created_at + timedelta(364)
        end_date = end_time.strftime("%d/%m/%Y")
        SUBJECT = 'BiZRefPro Registration Successfully Completed'
        BODY_TEXT = "Thanks for registration your application has been approved. Now you can able to login and update your profile and business information.  Below are your login Detail Username : " + user.email + ", Password  : Your entered password. Please feel free to ask if you have any query regarding this."
        BODY_HTML = "<html><head></head><body> <p>Hii</p><p>Thanks for registration your application has been approved. Now you can able to login and update your profile and business information. Below are your login Detail <br/>Username : " + user.email + " <br/>Password  : " + password + " <br/></p><p>Please feel free to ask if you have any query regarding this.</p><br/><br/><br/><strong>BizRefPro Team</strong><br/>Email : info@bizrefpro.com<br/>Web   : https://www.bizrefpro.com<br/><b>ItInfo Technologies Pvt. Ltd</b><br/><img src='https://www.bizrefpro.com/static/mail_logo/logo.png' /></body></html>"
        EMAIL_TEMPLATE = """
          <html><body>
          Dear <b>{name}</b>,
          <p>
          Thanks for registration your application has been pending for approval. But you can still able to login and update your profile and business information. Below are your login Detail
          </p>
          <p>Username : {email}<br/>
          Password : {password}
          </p>
          <p>
          Kindly find below detail for your service.
          </p>
          BizRefPro Listing - 1 Year/s ({start_date} - {end_date}) Rs. 1400<br/>
          ------------------------------------------------------<br/>
          Sub Total: Rs. 1400<br/>
          Credit: Rs. 0.00<br/>
          Total: Rs. 1400<br/>
          ------------------------------------------------------<br/>
          </p>
          <p>
          Payment Method<br/>
          Wire Transfer/NEFT : You can Wire Transfer funds to the following account:<br/>
          <br/>
          Bank Name - ICICI<br/>
          Name - Technologies Pvt. Ltd.<br/>
          Account Type - Current<br/>
          A/c No - XXXXXXXXXXXX<br/>
          IFSC - XXXX0000000
          </p>
          <p>
          Online Payment Link :  <a href="https://payments.example.com/pay/EXAMPLE">Click here</a> or copy below link and paste it in your browser<br/>
            https://payments.example.com/pay/EXAMPLE
          </p>
          Please let us know with transaction id so that we can notify your payment and list your business in BizRefPro. Please feel free to ask if you have any query regarding this.
          <p>
          BizRefPro Team<br/>
          Support No : 0000000000<br/>
          Email : info@bizrefpro.com<br/>
          Web : https://www.bizrefpro.com<br/>
          It Info Technologies Pvt. Ltd<br/><br/>
          <img src='https://www.bizrefpro.com/static/mail_logo/logo.png' />
          </p>
          </body></html>
          """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr(('BizRefPro New User', self.SENDER))
        msg['To'] = user.email
        part1 = MIMEText(BODY_TEXT, 'plain')
        replace_dict = {"name": user.name, "email": user.email, "password": password, "start_date": start_date,
                        "end_date": end_date}
        part2 = MIMEText(EMAIL_TEMPLATE.format(**replace_dict), 'html')
        msg.attach(part1)
        msg.attach(part2)
        try:
            server = smtplib.SMTP(self.HOST, self.PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER,user.email, msg.as_string())
            server.close()
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")

    def notify_referred_to_admin(self, referrar, user):
        SUBJECT = user.name+' added new referal'
        BODY_HTML = "<html><head></head><body> <p>Hii</p><p> Below is referral detail <br/><table><tr><th>Name</th><td>"+referrar.name+"</td></tr><tr><th>Email</th><td>"+referrar.email+"</td></tr><tr><th>Contact</th><td>"+referrar.phone+"</td></tr></table></p>Referred By:"+user.name+"<br/><br/><br/><strong>BizRefPro Team</strong><br/>Email : info@bizrefpro.com<br/>Web   : https://www.bizrefpro.com<br/><b>ItInfo Technologies Pvt. Ltd</b></body></html>"
        msg = MIMEMultipart('alternative')
        msg['Subject'] = SUBJECT
        msg['From'] = email.utils.formataddr(('BizRefPro Alert', self.SENDER))
        msg['To'] = self.SENDER
        part2 = MIMEText(BODY_HTML, 'html')
        msg.attach(part2)
        try:
            server = smtplib.SMTP(self.HOST, self.PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.USERNAME_SMTP, self.PASSWORD_SMTP)
            server.sendmail(self.SENDER, self.SENDER, msg.as_string())
            server.close()
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")

