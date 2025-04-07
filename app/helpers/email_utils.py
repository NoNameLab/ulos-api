import smtplib
from email.message import EmailMessage
from ..core.settings import env


def send_registration_email(recipient: str, password: str, course_name: str):
    """
    Envía un correo electrónico al estudiante con la contraseña generada y datos del curso.
    """

    subject = f"Registro en el curso: {course_name}"
    content = (
        f"Hola,\n\n"
        f"Has sido registrado en el curso '{course_name}'.\n"
        f"Tu contraseña de acceso es: {password}\n\n"
        f"Por favor, cambia tu contraseña después de iniciar sesión.\n\n"
        f"Saludos."
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = env.SMTP_USER
    msg["To"] = recipient
    msg.set_content(content)

    try:
        with smtplib.SMTP_SSL(env.SMTP_HOST, env.SMTP_PORT) as smtp:
            smtp.login(env.SMTP_USER, env.SMTP_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error al enviar correo a {recipient}: {e}")
