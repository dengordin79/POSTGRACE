from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import ssl, smtplib


def send_email(
        smtp_config:dict,
        receiver_to:str,
        message_subject:str,
        attachments:list,
        message_HTML_body:str="",
        message_text_body:str="",
        reply_to:str="",
        receiver_bcc:str="",
        receiver_cc:str=""
    ):
    if len(smtp_config)==0:
        print('Error: SMTP config empty') 
        return
    

    #creating message
    message=MIMEMultipart('alternative')
    message['Subject']=message_subject
    message['From']=smtp_config.get("smtp_user")
    message['To']=receiver_to
    message['Cc']=receiver_cc
    message['Bcc']=receiver_bcc
    message['Replay-To']=reply_to
    # with open(message_HTML_body_path) as f: html_body=f.read()
    # with open(message_text_body_path) as f: text_body=f.read()
    text_body = message_text_body
    html_body = message_HTML_body
    #Add plain text message part and html part
    message_body_text_part=MIMEText(text_body,'plain')
    message_body_html_part=MIMEText(html_body,'html')
    message.attach(message_body_text_part)
    message.attach(message_body_html_part)
    #add attachments part
    for next_attacment in attachments:
        #open file in binary mode
        with open(next_attacment,"rb") as f:
            attachment_part=MIMEBase("application","octet_stream")
            attachment_part.set_payload(f.read())
            encoders.encode_base64(attachment_part)
            #add header
            f_name=next_attacment.split('\\')[-1]
            attachment_part.add_header(
                "Content-Disposition",
                f"attacment; filename={f_name}"
            )
            message.attach(attachment_part)
            pass
        pass        
    
    # smtplib.SMTP.set_debuglevel(debuglevel=2)
    with smtplib.SMTP_SSL(
        smtp_config.get("smtp_host"),
        smtp_config.get("smtp_port"),
        context=ssl.create_default_context()) as server:
        server.login(smtp_config.get("smtp_user"),smtp_config.get("smtp_password"))
        send_errors=server.sendmail(smtp_config.get("smtp_user"),[receiver_to],message.as_string())
        pass
    pass