import os
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)

UPLOAD_FOLDER = 'static/fotos_instructores'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'instructores'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)




mysql = MySQL()

@app.route('/')
def index():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM instructores')
    data = cursor.fetchall()
      # flash('Contact')
    return render_template('home.html',instructores = data)

@app.route('/agregar', methods=['POST','GET'])
def agregar():
    if request.method == 'POST':
        apellido = request.form['apellido']
        nombre = request.form['nombre']
                
        documento = request.form['documento']

        telefono = request.form['telefono']
        correo = request.form['correo']
        foto = request.files['foto']
        especialidad = request.form['especialidad']


        if foto.filename != '':
            filename = secure_filename(foto.filename)
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(foto_path)
            # foto_relative_path = 'fotos_instructores/' + filename


        

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO instructores (documento,nombre,apellido,correo,telefono,foto,especialidad) VALUES(%s,%s,%s,%s,%s,%s,%s)',(documento,nombre,apellido,correo,telefono,foto_path,especialidad))
        # flash('Contact')
        mysql.connection.commit()
        
        return redirect(url_for('index'))
    else:
        return render_template('agregarIns.html')
        
    


@app.route('/editar/<int:id>',methods=['POST','GET'])
def editar(id):

    if request.method == "POST":

        apellido = request.form['apellido']
        nombre = request.form['nombre']
        documento = request.form['documento']
        telefono = request.form['telefono']
        correo = request.form['correo']
        foto = request.files['foto']
        especialidad = request.form['especialidad']


        if foto.filename != '':
            filename = secure_filename(foto.filename)
            foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto.save(foto_path)

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE instructores SET documento = %s,nombre = %s,apellido = %s,correo = %s,telefono = %s,foto = %s,especialidad = %s WHERE id = %s',
                       (documento,nombre,apellido,correo,telefono,foto_path,especialidad,id))
        # flash('Contact')
        mysql.connection.commit()




        return redirect(url_for('index'))
    else:

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM instructores where id = {0}'.format(id))
        data = cursor.fetchall()
      

        return render_template('editarIns.html', instructor = data[0])

@app.route('/eliminar/<int:id>')
def eliminar(id):

    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM instructores WHERE id = {0}'.format(id))
    # flash('Contact')
    mysql.connection.commit()





    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)



