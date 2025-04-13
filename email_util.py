from email.message import EmailMessage
import smtplib
import ssl

def send_excel_email(to_email, subject, body, attachment_bytes, filename,
                     from_email, app_password,
                     smtp_server="smtp.gmail.com", smtp_port=465):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email
        msg.set_content(body)

        # Attach the Excel file
        msg.add_attachment(
            attachment_bytes,
            maintype="application",
            subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)

        return True
    except Exception as e:
        return str(e)
