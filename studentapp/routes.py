from studentapp import app, mysql

from flask import (Flask, redirect, render_template, request, url_for, flash)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


user = (User(username='ADMIN', password='password'))


@app.route('/', methods=['GET', 'POST'])
def login_Page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user.username == username and user.password == password:
            return redirect(url_for('system'))
        return redirect(url_for('login_Page'))

    return render_template('login.html')


@app.route('/system')
def system():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM student')
    data = cur.fetchall()
    cur.close()
    return render_template('system.html', student=data)


@app.route('/addstud', methods=['GET', 'POST'])
def addStudent():
    cur = mysql.connection.cursor()
    try:
        if request.method == 'POST':
            idNumber = request.form['idNumber']
            name = request.form['name']
            gender = request.form['gender']
            yearLevel = request.form['yearLevel']
            college = request.form['college']
            department = request.form['department']
            course = request.form['course']
            cur.execute("INSERT INTO student (idNumber, name, gender, yearLevel, college, department, course) VALUES (%s,%s, %s, %s,%s,%s,%s)",
                        (idNumber, name, gender, yearLevel, college, department, course))
            cur.execute("INSERT INTO student_college (idNumber, college, department, course) VALUES (%s,%s,%s,%s)",
                        (idNumber, college, department, course))
            mysql.connection.commit()
            flash('Student Added Successfully')
        return render_template('add.html')
    except:
        return render_template('exceptions.html')


@app.route('/edit/<idNumber>', methods=['GET'])
def getStudent(idNumber):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM student WHERE idNumber = %s', [idNumber])
    data = cur.fetchall()
    cur.close()
    return render_template('edit.html', student=data, )


@app.route('/update/<id>', methods=['POST'])
def updateStudent(id):
    try:
        if request.method == 'POST':
            idNumber = request.form['idNumber']
            name = request.form['name']
            yearLevel = request.form['yearLevel']
            college = request.form['college']
            department = request.form['department']
            course = request.form['course']
            cur = mysql.connection.cursor()
            cur.execute("""
                    UPDATE student 
                    SET idNumber = %s,
                        name = %s,
                        yearLevel = %s,
                        college = %s,
                        department = %s,
                        course = %s
                    WHERE idNumber = %s
                """, (idNumber, name, yearLevel, college, department, course, id))
            cur.execute("""
                    UPDATE student_college
                    SET college = %s,
                        department = %s,
                        course = %s
                    WHERE id = %s
                """, (college, department, course, id))
            flash('Student Updated Successfully')
            mysql.connection.commit()
            return redirect(url_for('system'))
    except:
        return render_template('exceptions.html')


@app.route('/delete/<string:idNumber>', methods=['GET', 'POST'])
def deleteStudents(idNumber):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE idNumber=%s", (idNumber,))
    cur.execute("DELETE FROM student_college WHERE idNumber=%s", (idNumber,))
    mysql.connection.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('system'))
