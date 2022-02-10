import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pandas as pd


app = Flask(__name__)

path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['txt']
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/output', methods=["POST","GET"])
def output():

    if request.method == 'POST':

        if 'chosen_file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('chosen_file')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            else:
                msg = 'Please Select .txt file.'
                return render_template('output2.html', file_name=file.filename, MSG=msg)


        Timings = []

        with open(f'/home/ricool/mysite/uploads/{filename}','r') as file:
            case = "Time Log:"
            f_case = case.lower()
            if f_case not in file.readline().lower():
                msg = '"Time Log:" is missing in the file.'
                return render_template('output2.html', file_name=filename, MSG=msg)

            Line_Number = 1
            for line in file.readlines():
                x = line.strip().split(" ")

                try:
                    index = x.index("-")
                    #print(index)

                    if index != 0:
                        Timings.append(x[index-1:index+2])
                        #print(Timings)
                    else:
                        pass
                        #print(f"Line Number {Line_Number} Has no Information")
                except:
                    for i in x:
                        if '-' in i:
                            index = i.index('-')
                            ls = i.split('-')
                            ls.insert(1,'-')
                            Timings.append(ls)

                Line_Number += 1
            minutes = 0
            hour = 0

            count = 1
            for i in Timings:
                try:
                    total_time_spends_seconds = str(pd.to_datetime(i[2]) - pd.to_datetime(i[0]))
                    b = total_time_spends_seconds.split()[2].lstrip("+")
                    c = b.split(":")
                    minutes += int(c[1])
                    hour += int(c[0])

                    hr = minutes//60 + hour
                    min = minutes%60

                except:
                    error = (f"error in line {count}")

                count += 1

    return render_template('output.html', file_name=filename ,Hours=hr, Minutes=min)


@app.route('/about')
def about_page():
    return render_template('about.html')