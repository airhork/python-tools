"""
handles the mail related
"""

MAIL_GROUP_SEAL = 'SH_HE_Agility_DEV_SEAL'
DEFAULT_TO_ADD = 'max.zhang@agfa.com'
DEFAULT_FROM_ADD = 'max.zhang@agfa.com'
SMTP_SERVER = 'smtp1.aspac.local'

def sendmail(content, to='max.zhang@agfa.com'):
	import smtplib
	server = smtplib.SMTP(SMTP_SERVER)
	fromadd = 'max.zhang@agfa.com'
	server.sendmail(fromadd,to, content)

def textMail(text,to=DEFAULT_TO_ADD,subject='Build notification'):
	from email.mime.text import MIMEText
	if 'html' in text:
		message = MIMEText(text,'html')	
	else:
		message = MIMEText(text, 'plain')
	message['subject'] = subject
	message['From'] = DEFAULT_FROM_ADD
	message['To'] = to
	sendMessage(message)


def sendMessage(message):
	import smtplib
	server = smtplib.SMTP(SMTP_SERVER)
	server.send_message(message)

 
  
  
