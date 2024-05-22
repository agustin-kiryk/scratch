import smtplib
import ssl

smtp_server = 'smtp.gmail.com'
port = 587  # For starttls
sender_email = 'agustin.k.dsi@gmail.com'
password = 'umpipenwtftfpxjl'

# Create a secure SSL context
context = ssl.create_default_context()

try:
    server = smtplib.SMTP(smtp_server, port)
    server.set_debuglevel(1)  # Enable debug output
    server.ehlo()  # Can be omitted
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    print("Conexión SMTP exitosa")
except Exception as e:
    print(f"Error al conectar al servidor SMTP: {e}")
finally:
    server.quit()