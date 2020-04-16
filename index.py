from email.message import EmailMessage
import smtplib
import email
import email as qwe
import imaplib
from os import path
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from random import randint
import pymysql as MySQLdb
from PyQt5.QtCore import *
import sys
from PyQt5.uic import loadUiType
from playsound import playsound
import speech_recognition as sr
from datetime import datetime
####################################################3
####################################################3
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
#################################################################################
################################################################################
ans=[]
cc=""
name=""
email =""
password =""
doctor_email=""
doctor_pass=""
patient_email=""
patient_pass=""
ui1,_ = loadUiType('main0.ui')
class register(QMainWindow , ui1):
    global cc
    global ans
    global name
    global email
    global password
    global doctor_email
    global patient_email
    global patient_pass
    def __init__(self , parent=None):
        super(register , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_bytton()
    def handel_bytton(self):
         self.pushButton.clicked.connect(self.send_code)
         self.pushButton_2.clicked.connect(self.forget_pass)
         self.pushButton_3.clicked.connect(self.login)
         self.pushButton_4.clicked.connect(self.assistance)
         self.pushButton_5.clicked.connect(self.confirm)
    def store_answer(self,sound):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            playsound(sound)
            audio = r.listen(source)
        # Speech recognition using Google Speech Recognition
        try:
            c = r.recognize_google(audio)
            print(c)
            ans.append(c)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("check your connection to internet")
    def ck(self):
        if "yes" in ans:
            playsound("canser_question//check.wav")
            return True
    def assistance(self):
        QApplication.processEvents()
        playsound("canser_question//start.wav")
        QApplication.processEvents()
        self.store_answer("canser_question//q1.wav")
        if self.ck(): return
        QApplication.processEvents()
        self.store_answer("canser_question//q2.wav")
        if self.ck(): return
        QApplication.processEvents()
        self.store_answer("canser_question//q3.wav")
        if self.ck(): return
        QApplication.processEvents()
        self.store_answer("canser_question//q4.wav")
        if self.ck(): return
        QApplication.processEvents()
        self.store_answer("canser_question//q5.wav")
        if self.ck(): return
        QApplication.processEvents()
    def get_password(self, email):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select password from register where email='%s' " % (email)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            cc = []
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    cc.append(j)
        except:
            print("error")
        db.close()
        return cc[0]
    def forget_pass(self):
        try:
            email = self.email.text()
            c = self.get_password(email)
            msg = EmailMessage()
            msg['Subject'] = 'about forget your password'
            msg['From'] = 'allamco4@gmail.com'
            msg['To'] = email
            pas="your password is : "+c
            msg.set_content(pas)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('allamco4@gmail.com', '00000000001')
                smtp.send_message(msg)
            QMessageBox.information(self, "ok", "check your email")
        except:
            QMessageBox.information(self, "ok", "enter correct email")
    def get_condition(self, email, password):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select condotion from register where email='%s' and password='%s'" % (email, password)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            cc = []
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    cc.append(j)
        except:
            print("error")
        db.close()
        return cc
    def login(self):
        global doctor_email
        global doctor_pass
        global patient_email
        global patient_pass
        e = self.email.text()
        p = self.password.text()
        result=self.get_condition(e,p)
        if len(result)==0 :
            QMessageBox.information(self,"failed","email or password are wrong try again")
        else :
            if result[0]=="doctor":
                doctor_email=e
                doctor_pass=p
                self.close()
                self.open = doctor()
                self.open.show()
            if result[0]=="patient":
                patient_email=e
                patient_pass=p
                self.close()
                self.open = patient()
                self.open.show()
            if result[0]=="lab":
                self.close()
                self.open = lab()
                self.open.show()
    def remove_current(self):
        box_animation1 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation1.setDuration(2500)
        box_animation1.setStartValue(QRect(20, 20, 621, 331))
        box_animation1.setEndValue(QRect(0, 0, 0, 0))
        box_animation1.start()
        self.box_animation1 = box_animation1
        box_animation2 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(0, 0, 0, 0))
        box_animation2.setEndValue(QRect(10, 30, 611, 231))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def insert_new_patient(self,name,email,password):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        cursor = db.cursor()
        sql = "insert into register values ('%s','%s','%s','patient')" % (name,email,password)
        try:
            cursor.execute(sql)
            db.commit()
            QMessageBox.information(self, "my dear", "you register succesfuly")
        except:
            db.rollback()
            QMessageBox.information(self, "my dear", "you register fail try again")
        db.close()
    def confirm(self):
        code=str(self.lineEdit_5.text())
        if code ==cc :
            self.insert_new_patient(name,email,password)
        else:
            QMessageBox.information(self, "my dear", "you register fail try again")
    def send_code(self):
        global cc
        global name
        global email
        global password
        name=str(self.lineEdit_1.text())
        email=str(self.lineEdit_2.text())
        password=str(self.lineEdit_3.text())
        password_conf=str(self.lineEdit_4.text())
        if name=="":QMessageBox.information(self,"my dear","name is empty")
        if email=="":QMessageBox.information(self,"my dear","email is empty")
        if password=="":QMessageBox.information(self,"my dear","password is empty")
        if password_conf=="":QMessageBox.information(self,"my dear","confirm password is empty")
        if password != password_conf :
                 QMessageBox.information(self, "my dear", "2 password not identical")
        else:
                for _ in range(5):
                    value = randint(0, 9)
                    cc+=str(value)
                code="my dear "+name+" your confirmation code is : "+cc
                try:
                    msg = EmailMessage()
                    msg['Subject'] = 'confirmation code'
                    msg['From'] = 'allamco4@gmail.com'
                    msg['To'] = email
                    msg.set_content(code)
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login('allamco4@gmail.com', '00000000001')
                        smtp.send_message(msg)
                    self.remove_current()
                    print("sent")
                except:
                    print("error")
##############################################################################################3
##############################################################################################3
ui3,_ = loadUiType('main2.ui')
class lab(QMainWindow , ui3):
    patient_name=""
    def __init__(self , parent=None):
        super(lab , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_bytton()
    def handel_bytton(self):
         self.pushButton.clicked.connect(self.broese)
         self.pushButton_2.clicked.connect(self.upload_result)
         self.pushButton_3.clicked.connect(self.exit)
    def exit(self):
        self.close()
        self.open = register()
        self.open.show()

    def get_condition(self, email , name):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select condotion from register where email='%s' and name ='%s'" % (email,name)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            cc = []
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    cc.append(j)
        except:
            print("error")
        db.close()
        return cc
    def broese(self):
        url_dir = QFileDialog.getOpenFileName(self, 'Select image', '', 'Image Files (*)')
        Directory = url_dir[0]
        self.patient_name=Directory
        base = path.basename(Directory)
        name = path.splitext(base)[0]
        self.label_5.setText(name+" result upload")
    def send_res_doctor_patient(self, dr_name,patient_name,patient_email,patient_result):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        cursor = db.cursor()
        date=str(datetime.today().strftime('%Y-%m-%d'))
        if dr_name=="dr allam":
            sql = "insert into dr_allam  values ('%s','%s','%s','%s')" % (patient_name,patient_email,patient_result,date)
            yy="allamco4@gmail.com"
        elif dr_name=="dr ali":
            sql = "insert into dr_ali  values ('%s','%s','%s','%s')" % (patient_name,patient_email,patient_result,date)
            yy="dr_ali@gmail.com"
        elif dr_name=="dr sara":
            sql = "insert into dr_sara  values ('%s','%s','%s','%s')" % (patient_name,patient_email,patient_result,date)
            yy="dr_sara@gmail.com"
        else:
            sql = "insert into dr_allam  values ('%s','%s','%s','%s')" % (patient_name,patient_email,patient_result,date)
            yy = "allamco4@gmail.com"
        try:
            sqll = "insert into patient  values ('%s','%s','%s','%s','%s')" % (patient_name, patient_email, patient_result,date,yy)
            cursor.execute(sql)
            cursor.execute(sqll)
            db.commit()
            QMessageBox.information(self,"ok","send to doctor and patient")
        except:
            db.rollback()
            QMessageBox.information(self,"error","try again")
        db.close()
    def upload_result(self):
        et_name = self.lineEdit_1.text()
        et_email = self.lineEdit_2.text()
        et_result = self.patient_name
        et_doctor = str(self.comboBox.currentText())
        if et_name=="" or et_email=="" or et_result=="" :
            QMessageBox.information(self,"error","enter all fields")
        else:
            found=self.get_condition(et_email,et_name)
            print(found)
            if len(found) > 0 :
                   self.send_res_doctor_patient(et_doctor,et_name,et_email,et_result)
            else :
                QMessageBox.information(self, "error", "patient not register in data")
#################################################################################################
#################################################################################################

ui4,_ = loadUiType('main3.ui')
class patient(QMainWindow , ui4):
    global patient_email
    global patient_pass
    def __init__(self , parent=None):
        super(patient , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget_3.setCurrentIndex(0)
        yy = self.get_lastresult_patient()[-1]
        self.get_history_patient()
        self.label_12.setPixmap(QPixmap(yy))
        self.handel_bytton()
    def handel_bytton(self):
         self.pushButton_6.clicked.connect(self.signout)
         self.pushButton_7.clicked.connect(self.signout)
         self.pushButton_11.clicked.connect(self.patient_history)
         self.pushButton_8.clicked.connect(self.sent_to_doctor)
         self.pushButton_9.clicked.connect(self.receive_msg_from_dr)
    def signout(self):
        self.close()
        self.open = register()
        self.open.show()
    def get_lastresult_patient(self):
            global patient_email
            db = MySQLdb.connect("localhost", "root", "", "hospital")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            sql = "select patient_result from patient where email = '%s'"%(patient_email)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = list(cursor.fetchall())
                q=[]
                for i in results:
                    for j in i:
                        q.append(j)
            except:
                print("error")
            db.close()
            return q
    def get_history_patient(self):
            global patient_email
            db = MySQLdb.connect("localhost", "root", "", "hospital")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            sql = "select date from patient where email = '%s'"%(patient_email)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = list(cursor.fetchall())
                for i in results:
                    for j in i:
                        self.comboBox_3.addItem(j)
            except:
                print("error")
            db.close()
    def patient_history(self):
        global patient_email
        his=str(self.comboBox_3.currentText())
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select patient_result from patient where date = '%s' and email ='%s'" % (his,patient_email)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = list(cursor.fetchall())
            qq=[]
            for i in results:
                for j in i:
                    qq.append(j)
        except:
            print("error")
        print(qq[0])
        self.label_12.setPixmap(QPixmap(qq[0]))
        db.close()
    def get_dr_email(self):
        global patient_email
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        sql = "select dr_email from patient where email = '%s'" % (patient_email)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            k = []
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    k.append(j)
        except:
            print("error")
        return k[0]
    def sent_to_doctor(self):
        global patient_email
        global patient_pass
        dr=self.get_dr_email()
        c=str(self.plainTextEdit_6.toPlainText())
        try:
            msg = EmailMessage()
            msg['Subject'] = 'hospital'
            msg['From'] = patient_email
            msg['To'] = dr
            msg.set_content(c)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(patient_email, patient_pass)
                smtp.send_message(msg)
            QMessageBox.information(self,"my dear","it sent to doctor")
        except:
            QMessageBox.information(self,"my dear","there is an error")
    def receive_msg_from_dr(self):
        global patient_email
        global patient_pass
        dr = self.get_dr_email()
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(patient_email, patient_pass)
        mail.list()
        mail.select("inbox")  # connect to inbox.
        result, data = mail.search(None, '(FROM {} SUBJECT "hospital")'.format(dr))
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        try :
            latest_email_id = id_list[-1]  # get the latest
            result, data = mail.fetch(latest_email_id,"(RFC822)")
            raw_email = qwe.message_from_bytes(data[0][1])
            for part in raw_email.walk():
                if part.get_content_type() == 'text/plain':
                    rr=part.get_payload()
                    print(rr)
                    self.plainTextEdit_7.setPlainText(str(rr))
        except :
            QMessageBox.information(self,"my doctor","no messages received")
####################################################################################################
####################################################################################################
'''select distinct patient_name from dr_allam'''
ui5,_ = loadUiType('main4.ui')
class doctor(QMainWindow , ui5):
    global doctor_email
    name_of_my_patient=""
    def __init__(self , parent=None):
        super(doctor , self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_bytton()
        self.all_my_patient(doctor_email)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
    def all_my_patient(self,doctor_email):
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        if doctor_email=="dr_sara@gmail.com":sql = "select distinct patient_name from dr_sara"
        elif doctor_email=="dr_ali@gmail.com":sql = "select distinct patient_name from dr_ali"
        else:
            sql = "select distinct patient_name from dr_allam"
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = list(cursor.fetchall())
            for i in results:
                for j in i:
                    self.comboBox.addItem(j)
        except:
            print("error")
        db.close()
    def get_lastresult_patient(self,name):
            global doctor_email
            db = MySQLdb.connect("localhost", "root", "", "hospital")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            if doctor_email == "dr_sara@gmail.com":
                sql = "select patient_result from dr_sara where patient_name = '%s'"%(name)
            elif doctor_email == "dr_ali@gmail.com":
                sql = "select patient_result from dr_ali where patient_name = '%s'"%(name)
            else:
                sql = "select patient_result from dr_allam where patient_name = '%s'"%(name)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = list(cursor.fetchall())
                q=[]
                for i in results:
                    for j in i:
                        q.append(j)
            except:
                print("error")
            db.close()
            return q
    def get_history_patient(self,name):
            global doctor_email
            db = MySQLdb.connect("localhost", "root", "", "hospital")
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            if doctor_email == "dr_sara@gmail.com":
                sql = "select date from dr_sara where patient_name = '%s'"%(name)
            elif doctor_email == "dr_ali@gmail.com":
                sql = "select date from dr_ali where patient_name = '%s'"%(name)
            else:
                sql = "select date from dr_allam where patient_name = '%s'"%(name)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                # Fetch all the rows in a list of lists.
                results = list(cursor.fetchall())
                for i in results:
                    for j in i:
                        self.comboBox_2.addItem(j)
            except:
                print("error")
            db.close()
    def handel_bytton(self):
         self.pushButton.clicked.connect(self.patient_page)
         self.pushButton_4.clicked.connect(self.patient_history)
         self.pushButton_3.clicked.connect(self.send_msg)
         self.pushButton_2.clicked.connect(self.receive_msg)
         self.pushButton_6.clicked.connect(self.exit)
         self.pushButton_5.clicked.connect(self.back)
    def exit(self):
        self.close()
        self.open = register()
        self.open.show()
    def back(self):
        self.tabWidget.setCurrentIndex(0)
    def patient_page(self):
        self.name_of_my_patient=str(self.comboBox.currentText())
        self.tabWidget.setCurrentIndex(1)
        yy=self.get_lastresult_patient(self.name_of_my_patient)[-1]
        self.get_history_patient(self.name_of_my_patient)
        self.label_2.setPixmap(QPixmap(yy))
    def patient_history(self):
        global doctor_email
        his=str(self.comboBox_2.currentText())
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        if doctor_email == "dr_sara@gmail.com":
            sql = "select patient_result from dr_sara where date = '%s'" % (his)
        elif doctor_email == "dr_ali@gmail.com":
            sql = "select patient_result from dr_ali where date = '%s'" % (his)
        else:
            sql = "select patient_result from dr_allam where date = '%s'" % (his)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = list(cursor.fetchall())
            q=[]
            for i in results:
                for j in i:
                    q.append(j)
        except:
            print("error")
        self.label_2.setPixmap(QPixmap(q[0]))
        db.close()

    def sent_to_patient(self,patient_email, c):
        global doctor_email
        global doctor_pass
        try:
            msg = EmailMessage()
            msg['Subject'] = 'hospital'
            msg['From'] = doctor_email
            msg['To'] = patient_email
            msg.set_content(c)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(doctor_email, doctor_pass)
                smtp.send_message(msg)
            QMessageBox.information(self,"my doctor","it sent to patient")
        except:
            QMessageBox.information(self,"my doctor","there is an error")
    def patient_acc(self):
        global doctor_email
        namee=str(self.comboBox.currentText())
        db = MySQLdb.connect("localhost", "root", "", "hospital")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        if doctor_email == "dr_sara@gmail.com":
            sql = "select patient_email from dr_sara where patient_name = '%s'" % (namee)
        elif doctor_email == "dr_ali@gmail.com":
            sql = "select patient_email from dr_ali where patient_name = '%s'" % (namee)
        else:
            sql = "select patient_email from dr_allam where patient_name = '%s'" % (namee)
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = list(cursor.fetchall())
            q=[]
            for i in results:
                for j in i:
                    q.append(j)
        except:
            print("error")
        db.close()
        return q[0]
    def send_msg(self):
        my_msg=str(self.plainTextEdit_3.toPlainText())
        self.sent_to_patient(self.patient_acc(),my_msg)
    def receive_msg(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(doctor_email, doctor_pass)
        mail.list()
        mail.select("inbox")  # connect to inbox.
        result, data = mail.search(None, '(FROM {} SUBJECT "hospital")'.format(self.patient_acc()))
        ids = data[0]  # data is a list.
        id_list = ids.split()  # ids is a space separated string
        try :
            latest_email_id = id_list[-1]  # get the latest
            result, data = mail.fetch(latest_email_id,"(RFC822)")
            raw_email = qwe.message_from_bytes(data[0][1])
            for part in raw_email.walk():
                if part.get_content_type() == 'text/plain':
                    rr=part.get_payload()
                    print(rr)
                    self.plainTextEdit_2.setPlainText(str(rr))
        except :
            QMessageBox.information(self,"my doctor","no messages received")
####################################################################################################
####################################################################################################
def main():
    app = QApplication(sys.argv)
    window = register()
    window.show()
    app.exec_()
if __name__ == '__main__':
    sys.excepthook = except_hook
    main()
####################################################3
####################################################3