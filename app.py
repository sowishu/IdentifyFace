import glob
import urllib
import base64

import face_recognition
from flask import Flask, request, render_template

from dbop import Profile, ProfileManager
from binascii import a2b_base64
import base64
import datetime
import time
import calendar
import cv2
from cv2 import imread
import os

app = Flask(__name__)


# def student():!pip install cmake dlib face_recognition numpy opencv-python


@app.route('/dataentry', methods=['POST'])
def result():
    if request.method == 'POST':
        result = request.form
        name = result.get('name')
        lastname = result.get('lastname')
        gender = result.get('gender')
        age = result.get('age')
        address = result.get('address')
        phone = result.get('phone')
        aadhar = result.get('aadhar')
        mail = result.get('mail')
        imgUrl = result.get('img')

        up = urllib.parse.urlparse(imgUrl)
        head, data = up.path.split(',', 1)

        bits = head.split(';')
        mime_type = bits[0] if bits[0] else 'text/plain'
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True

        # plaindata = data.decode("base64")
        plaindata = base64.b64decode(data)
        epoch = time.time()
        e2 = calendar.timegm(time.gmtime())
        e1 = str(e2) + ".jpg"

        with open(e1, 'wb') as f:
            f.write(plaindata)

        p = Profile(e2, name, lastname, gender, age, address, phone, aadhar, mail, data);
        pm = ProfileManager();
        pm.createProfile(p);
    return render_template('index.html')


@app.route('/listAll', methods=['GET', 'POST'])
def listall():
    pm = ProfileManager();
    rows = pm.listall(50);

    str = "<table id='_userid'>"

    str = str + "<th>DELETE</th>"
    str = str + "<th>EDIT</th>"
    str = str + "<th>NAME</th>"
    str = str + "<th>GENDER</th>"
    str = str + "<th>AGE</th>"
    str = str + "<th>ADDRESS</th>"
    str = str + "<th>PHONE</th>"
    str = str + "<th>AADHAR</th>"
    str = str + "<th>MAIL</th>"
    str = str + "<th>PHOTO</th>"

    for row in rows:
        all_columns = list(row)
        str = str + "<tr>"
        str = str + "<td> <input type='button' value='Delete' id=D{} onclick='onDelete()' /></td>".format(row[0])
        str = str + "<td> <input type='button' value='Edit' id=E{} onclick='onEdit()' /></td>".format(row[0])
        name = row[1]
        lastname = row[2]
        gender = row[3]
        age = row[4]
        address = row[5]
        phone = row[6]
        aadhar = row[7]
        mail = row[8]
        picture = row[9]

        str = str + "<td>" + name + " " + lastname + "</td>"
        str = str + "<td>" + gender + "</td>"
        str = str + "<td>" + age + "</td>"
        str = str + "<td>" + address + "</td>"
        str = str + "<td>" + phone + "</td>"
        str = str + "<td>" + aadhar + "</td>"
        str = str + "<td>" + mail + "</td>"
        # str = str + "<td>" + picture + "</td>"

        str = str + "</tr>"

    str = str + "</table>"

    return render_template("ListAll.html", tablestr=str)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    result = request.form
    id = result.get('userid')
    pm = ProfileManager();
    pm.deleteProfile(id);
    return render_template("List.html")


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    result = request.form
    id = result.get('userid')

    p = Profile(id, '', '', '', '', '', '', '', '','');
    pm = ProfileManager();
    row = pm.select(p);

    return render_template('DataResult.html', Rname=row[0], Rlastname=row[1], Rgender=row[2], Rage=row[3],
                           Raddress=row[4], Rphone=row[5], Raadhar=row[6], Rmail=row[7])


@app.route('/fetch', methods=['POST', 'GET'])
def fetch():
    if request.method == 'POST':
        result = request.form

        imgUrl = result.get('img')
        up = urllib.parse.urlparse(imgUrl)
        head, data = up.path.split(',', 1)
        bits = head.split(';')
        mime_type = bits[0] if bits[0] else 'text/plain'
        charset, b64 = 'ASCII', False
        for bit in bits:
            if bit.startswith('charset='):
                charset = bit[8:]
            elif bit == 'base64':
                b64 = True

        plaindata = base64.b64decode(data)
        with open("tmp.jpg", 'wb') as f:
            f.write(plaindata)

        curr_img = face_recognition.face_encodings(face_recognition.load_image_file("tmp.jpg"))


        if (len(curr_img) <= 0):
            return render_template('Error.html')
        curr_img = curr_img[0]
        matchingFile = ""

        for file in glob.glob("*.jpg"):
            print("======================>" + file)
            if (file != "tmp.jpg" and matchingFile == ""):
                dir_img = face_recognition.face_encodings(face_recognition.load_image_file(file))[0]
                img_result = face_recognition.compare_faces([curr_img], dir_img)

                print(img_result)

                if (img_result == [True]):
                    matchingFile = file
                    id, txt = matchingFile.split('.', 1)
                    p = Profile(id, '', '', '', '', '', '', '', '', '');
                    print(id)
                    pm = ProfileManager();
                    row = pm.select(p);
                    print(row)
                    break;
        if (matchingFile == ""):
             return render_template('Error.html')

    return render_template('DataResult.html', Rname=row[0], Rlastname=row[1], Rgender=row[2], Rage=row[3],
                           Raddress=row[4], Rphone=row[5], Raadhar=row[6], Rmail=row[7])


if __name__ == '__main__':
    app.run(debug=True)
