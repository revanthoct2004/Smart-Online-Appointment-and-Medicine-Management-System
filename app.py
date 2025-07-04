import telepot
from twilio.rest import Client
from flask import Flask, render_template, url_for, request, redirect, jsonify, session
import sqlite3
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

# Database setup
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create necessary tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    password TEXT, 
    mobile TEXT, 
    email TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctor(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT, 
    specialist TEXT,
    mobile TEXT, 
    email TEXT,
    hospital TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT, 
    PatientID TEXT,
    DoctorID TEXT,
    hospital TEXT,
    specialist TEXT,
    AppointmentDate TEXT,
    schedule TEXT)
""")

# Appointment timings

timings = {
    '1': {'starttime': '10:00AM', 'endtime': '10:30AM'},
    '2': {'starttime': '10:30AM', 'endtime': '11:00AM'},
    '3': {'starttime': '11:00AM', 'endtime': '11:30AM'},
    '4': {'starttime': '11:30AM', 'endtime': '12:00PM'},
    '5': {'starttime': '12:00PM', 'endtime': '12:30PM'},
    '6': {'starttime': '12:30PM', 'endtime': '01:00PM'},
    '7': {'starttime': '01:00PM', 'endtime': '01:30PM'},
    '8': {'starttime': '01:30PM', 'endtime': '02:00PM'},
    '9': {'starttime': '02:00PM', 'endtime': '02:30PM'},
    '10': {'starttime': '02:30PM', 'endtime': '03:00PM'},
    '11': {'starttime': '03:00PM', 'endtime': '03:30PM'},
    '12': {'starttime': '03:30PM', 'endtime': '04:00PM'},
    '13': {'starttime': '04:00PM', 'endtime': '04:30PM'},
    '14': {'starttime': '04:30PM', 'endtime': '05:00PM'},
    '15': {'starttime': '05:00PM', 'endtime': '05:30PM'},
    '16': {'starttime': '05:30PM', 'endtime': '06:00PM'}
    }

# Email-sending function
def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "manubhat458@gmail.com"  # Replace with your email from which you want to send  
    sender_password = "xrpoipuetnbfhpqo"     # Replace with your email  app password. Go to email security and turn on two step verification and then search for app password and then create one and paste here

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirmbook/<Id>')
def confirmbook(Id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    doctorid = session['doctorid']
    query = "SELECT name, specialist, email FROM doctor WHERE id = ?"
    cursor.execute(query, (doctorid,))
    dname1 = cursor.fetchone()
    dname, spe, doctor_email = dname1

    userid = session['userid']
    query = "SELECT name, email FROM user WHERE id = ?"
    cursor.execute(query, (userid,))
    uname1 = cursor.fetchone()
    uname, user_email = uname1

    Date = session['date']
    hospital = session['hospital']

    cursor.execute(
        "INSERT INTO appointments (PatientID, DoctorID, hospital, specialist, AppointmentDate, schedule) VALUES (?, ?, ?, ?, ?, ?)",
        (userid, doctorid, hospital, spe, Date, Id)
    )
    connection.commit()

    starttime = timings[str(Id)]['starttime']
    endtime = timings[str(Id)]['endtime']
    msg = f'Dear {uname}, Your appointment booked successfully on {Date} at {starttime}-{endtime} with Dr.{dname}({spe} Specialist) of {hospital}'

    # Send email notifications
    user_subject = "Appointment Confirmation"
    user_body = f"Dear {uname},\n\nYour appointment is confirmed for {Date} from {starttime} to {endtime} with Dr.{dname} ({spe} Specialist) at {hospital}.\n\nThank you!"
    send_email(user_email, user_subject, user_body)

    doctor_subject = "New Appointment Scheduled"
    doctor_body = f"Dear Dr.{dname},\n\nYou have a new appointment scheduled on {Date} from {starttime} to {endtime} with patient {uname}.\n\nThank you!"
    send_email(doctor_email, doctor_subject, doctor_body)

    return render_template('userlog.html', msg=msg)
def sendSMS(msg):
    try:
        bot = telepot.Bot('5505770046:AAHZ00lFDyhh9AL_r7XFrzKaqDT2LWp52V4')
        bot.sendMessage('1388858613', str(msg))
    except:
        pass

    try:
        account_sid = "AC1638ea405fee43359306124310db1ffe"
        auth_token = "e01c8d2ceeefb21c6d7b51212589cf9e"
        client = Client(account_sid, auth_token)
        client.api.account.messages.create(
            to="+919000688404",
            from_="+19036368995" ,
            body=msg)
    except:
        pass


timings = {
    '1': {'starttime': '10:00AM', 'endtime': '10:30AM'},
    '2': {'starttime': '10:30AM', 'endtime': '11:00AM'},
    '3': {'starttime': '11:00AM', 'endtime': '11:30AM'},
    '4': {'starttime': '11:30AM', 'endtime': '12:00PM'},
    '5': {'starttime': '12:00PM', 'endtime': '12:30PM'},
    '6': {'starttime': '12:30PM', 'endtime': '01:00PM'},
    '7': {'starttime': '01:00PM', 'endtime': '01:30PM'},
    '8': {'starttime': '01:30PM', 'endtime': '02:00PM'},
    '9': {'starttime': '02:00PM', 'endtime': '02:30PM'},
    '10': {'starttime': '02:30PM', 'endtime': '03:00PM'},
    '11': {'starttime': '03:00PM', 'endtime': '03:30PM'},
    '12': {'starttime': '03:30PM', 'endtime': '04:00PM'},
    '13': {'starttime': '04:00PM', 'endtime': '04:30PM'},
    '14': {'starttime': '04:30PM', 'endtime': '05:00PM'},
    '15': {'starttime': '05:00PM', 'endtime': '05:30PM'},
    '16': {'starttime': '05:30PM', 'endtime': '06:00PM'}
    }

@app.route('/Uhome')
def Uhome():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT hospital FROM doctor"
    cursor.execute(query)
    result = cursor.fetchall()
    result1 = []
    for row in result:
        result1.append(row[0])
    result = set(result1)
    return render_template('userlog.html', result=list(result))

@app.route('/viewuser')
def viewuser():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT id, name, mobile, email FROM user"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return render_template('userlist.html', result=result)
    else:
        return render_template('userlist.html', msg="user not found")

@app.route('/appointments')
def appointments():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM appointments"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        details = []
        for row in result:
            Id = row[0]
            query = "SELECT name, specialist FROM doctor where id = '"+row[2]+"'"
            cursor.execute(query)
            dname = cursor.fetchone()
            dname = dname[0]

            query = "SELECT name FROM user where id = '"+row[1]+"'"
            cursor.execute(query)
            uname = cursor.fetchone()
            uname = uname[0]

            hospital = row[3]
            spe = row[4]
            AppointmentDate = row[5]

            starttime = timings[str(row[6])]['starttime']
            endtime = timings[str(row[6])]['endtime']
            schedule = starttime+'-'+endtime

            details.append([Id, uname, dname, hospital, spe, AppointmentDate, schedule])
        return render_template('appointments.html', details=details)
    else:
        return render_template('userlist.html', msg="appointments not found")

@app.route('/Ahome')
def Ahome():
    return render_template('adminlog.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session['userid'] = result[0]
            query = "SELECT hospital FROM doctor"
            cursor.execute(query)
            result = cursor.fetchall()
            result1 = []
            for row in result:
                result1.append(row[0])
            result = set(result1)
            return render_template('userlog.html', result=list(result))
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        query = "SELECT * FROM user WHERE mobile = '"+mobile+"'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return render_template('index.html', msg='Phone number already exists, try with deferent number')
        else:
            cursor.execute("INSERT INTO user (name, password, mobile, email) VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
            connection.commit()

            return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']

        if name == 'admin' and password == 'admin':
            return render_template('adminlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')

@app.route('/add_doctors', methods=['GET', 'POST'])
def add_doctors():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        spe = request.form['spe']
        hospital = request.form['hospital']
        mobile = request.form['phone']
        email = request.form['email']
        
        cursor.execute("INSERT INTO doctor (name, specialist, mobile, email, hospital) VALUES ('"+name+"', '"+spe+"', '"+mobile+"', '"+email+"','"+hospital+"')")
        connection.commit()

        return render_template('adminlog.html', msg='Successfully added')
    
    return render_template('adminlog.html')

@app.route('/doctor_list')
def doctor_list():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM doctor"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return render_template('doctorslist.html', result=result)
    else:
        return render_template('doctorslist.html', msg="doctors not found")

@app.route('/get_doctor/<Id>')
def get_doctor(Id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM doctor WHERE id = '"+Id+"'"
    cursor.execute(query)
    result = cursor.fetchone()
    return render_template('updatedoctor.html', result=result)

@app.route('/update_doctors', methods=['GET', 'POST'])
def update_doctors():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        Id = request.form['Id']
        name = request.form['name']
        spe = request.form['spe']
        hospital = request.form['hospital']
        mobile = request.form['phone']
        email = request.form['email']

        cursor.execute("UPDATE doctor SET name = '"+name+"', specialist = '"+spe+"', mobile = '"+mobile+"', email = '"+email+"', hospital = '"+hospital+"' WHERE id = '"+Id+"'")
        connection.commit()

        return render_template('updatedoctor.html', msg='Successfully Updated')
    
    return render_template('updatedoctor.html')

@app.route('/delete_doctor/<Id>')
def delete_doctor(Id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("delete from doctor where id = '"+Id+"'")
    connection.commit()
    return redirect(url_for('doctor_list'))


@app.route('/add_Medicine', methods=['GET', 'POST'])
def add_Medicine():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        name = request.form['name']
        price = request.form['price']
        Date = request.form['Date']

        cursor.execute("INSERT INTO medicine (name, price, date) VALUES ('"+name+"', '"+price+"', '"+Date+"')")
        connection.commit()

        return render_template('medicine.html', msg='Successfully added')
    
    return render_template('medicine.html')

@app.route('/Medicine_list')
def Medicine_list():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM medicine"
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return render_template('medicinelist.html', result=result)
    else:
        return render_template('medicinelist.html', msg="medicine not found")

@app.route('/get_medicine/<Id>')
def get_medicine(Id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM medicine WHERE id = '"+Id+"'"
    cursor.execute(query)
    result = cursor.fetchone()
    return render_template('updatemedicine.html', result=result)

@app.route('/update_medicine', methods=['GET', 'POST'])
def update_medicine():
    if request.method == 'POST':

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        Id = request.form['Id']
        name = request.form['name']
        price = request.form['price']
        Date = request.form['Date']

        cursor.execute("UPDATE medicine SET name = '"+name+"', price = '"+price+"', date = '"+Date+"' WHERE id = '"+Id+"'")
        connection.commit()

        return render_template('updatemedicine.html', msg='Successfully Updated')
    
    return render_template('updatemedicine.html')

@app.route('/delete_medicine/<Id>')
def delete_medicine(Id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("delete from medicine where id = '"+Id+"'")
    connection.commit()
    return redirect(url_for('doctor_list'))

@app.route("/doctor_names",methods=["POST","GET"])
def doctor_names():
    if request.method == 'POST':
        hospital = request.form['hospital']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT name, specialist FROM doctor where hospital = '"+hospital+"'"
        cursor.execute(query)
        result = cursor.fetchall()

        names = []
        for row in result:
            names.append(row[0])

        spe = []
        for row in result:
            spe.append(row[1])

        return jsonify(names, spe)
    return jsonify("error")

@app.route("/doctor_availability",methods=["POST","GET"])
def docor_availability():
    if request.method == 'POST':
        hospital = request.form['hospital']
        doctor = request.form['doctor']
        Date = request.form['date']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM doctor where name = '"+doctor+"'"
        cursor.execute(query)
        result = cursor.fetchone()

        doctorid = str(result[0])
        session['doctorid'] = doctorid
        session['date'] = Date
        session['hospital'] = hospital

        query = "SELECT schedule FROM appointments where DoctorID = '"+doctorid+"' and hospital = '"+hospital+"' and AppointmentDate = '"+Date+"'"
        cursor.execute(query)
        result = cursor.fetchall()
        
        schedules = []
        if result:
            for row in result:
                schedules.append(row[0])
            return render_template('userlog.html', schedules=schedules, timings=timings)
        else:
            return render_template('userlog.html', schedules=schedules, timings=timings)
    return redirect(url_for('Uhome'))

@app.route("/medicine_availability", methods=['GET', 'POST'])
def medicine_availability():
    if request.method == 'POST':
        name = request.form['name']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        query = "SELECT * FROM medicine where name = '"+name+"'"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return render_template('medicinesearch.html', result=result)
        else:
            return render_template('medicinesearch.html', msg="medicine not found")
    return render_template('medicinesearch.html')

@app.route("/searchmedicine",methods=["POST","GET"])
def searchmedicine():
    check = request.args.get("text")
    
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    query = "SELECT name FROM medicine"
    cursor.execute(query)
    result = cursor.fetchall()
    result1 = []
    for row in result:
        result1.append(row[0])
    result = set(result1)
    result = list(result1)
    if result:
        return jsonify(result)
    else:
        return jsonify("error")

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
