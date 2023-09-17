from PyQt5 import QtWidgets, uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QPushButton, QDialog, QLineEdit, QComboBox, QFileDialog, QTextEdit, QSpinBox
from PyQt5.QtCore import QTimer, pyqtSlot, QFile, QTextStream, QDateTime, QDate, QUrl, QStandardPaths, QRegExp
from PyQt5.QtGui import QIntValidator, QDesktopServices, QPixmap, QRegExpValidator
import sys
import pymysql
from datetime import date


admin_buttons = ["btnHome1", "btnRoom1", "btnReport1", "btnEmployee1", "btnSettings1", "btnHome2", "btnRoom2", "btnReport2", "btnEmployee2", "btnSettings2"]
cashier_buttons = ["btnHome1", "btnGuest1", "btnCheck1", "btnOut1", "btnSale1", "btnHistory1", "btnHome2", "btnGuest2", "btnCheck2", "btnOut2", "btnSale2", "btnHistory2"]
data_list=[]; user_profile_info=[]

class Hotel(QtWidgets.QMainWindow):
    def __init__(self):
        super(Hotel, self).__init__()
        uic.loadUi('hmsUI.ui', self)
        self.show()
        self.setWindowTitle('Hotel Accommodation Management System')
        self.lblLogin.hide()
        self.source_path=''
        self.attempts = 0; self.loginform = True
        self.locked = False
        self.timer = QTimer(); self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.unlock_system)
        self.btnLogin.clicked.connect(self.go_to_dashboard); self.btnEye.clicked.connect(self.visible_pass)
        self.get_users()
        self.minimum_stay=12
        #method to get minimum stay from ADMin ########################################################################################

    def user_profile(self):
        global user_profile_info
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = """SELECT pic, firstname, position, lastname FROM employees WHERE username=%s"""
        data_value=(self.txtUsername.text())
        cursor.execute(command, data_value)
        records = cursor.fetchall()
        user_profile_info = [list(record) for record in records]

    def get_users(self):
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = """SELECT username, password from employees"""
        cursor.execute(command)
        records = cursor.fetchall()
        self.users = {}
        for row in records:
            username, password = row
            self.users[username] = password
        command = """SELECT username, position from employees"""
        cursor.execute(command)
        records = cursor.fetchall()
        self.position = {}
        for row in records:
            username, position = row
            self.position[username] = position

    #Method for setting the password in of login form visible
    def visible_pass(self):
        if self.btnEye.isChecked():
            self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)

    #Method for displaying date and time
    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_date = current_datetime.toString("MMMM dd, yyyy")
        self.lblDate.setText(formatted_date)
        formatted_time = current_datetime.toString("hh:mm:ss AP")
        self.lblTime.setText(formatted_time)

        am_pm = self.lblTime.text(); last_two_chars = am_pm[-2:]
        if last_two_chars == 'PM':
            time_string = self.lblTime.text().replace('Time: ', '').replace(' PM', '');
            first_digit = time_string[1]
            if int(first_digit) <= 5:
                self.lblgreetings.setText('Good afternoon, ' + self.lblFname.text() + '!')
            else:
                self.lblgreetings.setText('Good evening, ' + self.lblFname.text() + '!')
        elif last_two_chars == 'AM':
            self.lblgreetings.setText('Good morning, ' + self.lblFname.text() + '!')

    def showDialog(self, text):
        dialog = QMessageBox()
        dialog.setText(text)
        dialog.setWindowTitle('Hotel Accommodation Management System')
        dialog.exec_()

    #This is the method to set the border of the line edit and combo boxes to RED if it was left empty
    def red_mark(self, list):
        for widget_name in list:
            widget = getattr(self, widget_name)
            is_line_edit = isinstance(widget, QtWidgets.QLineEdit)
            is_combo_box = isinstance(widget, QtWidgets.QComboBox)
            is_spin_box = isinstance(widget, QtWidgets.QSpinBox)
            is_text_edit = isinstance(widget, QtWidgets.QTextEdit)
            is_empty = (is_line_edit and widget.text().replace(" ", "") == '') or (is_combo_box and widget.currentText() == '') or (is_spin_box and widget.value() == 0) or (is_text_edit and widget.toPlainText() == '')
            if self.loginform == False:
                if is_empty:
                    widget.setStyleSheet("background-color: rgb(255, 255, 255); border: 1px solid red;")
                else:
                    widget.setStyleSheet("background-color: rgb(255, 255, 255); border: none;")
            elif self.loginform == True:
                if is_empty:
                    widget.setStyleSheet(
                        "background-color:transparent; border: 2px solid red; color: rgb(255, 255, 255);")
                else:
                    widget.setStyleSheet(
                        "background-color:transparent; border: 2px solid white; color: rgb(255, 255, 255);")

    #Method for removing the red borders for empty line edits and combo boxes
    def back_to_normal(self, list):
        for widget_name in list:
            widget = getattr(self, widget_name)
            widget.setStyleSheet("background-color: white; border: none;")

    #Method for proceeding to either the Admin Dashboard or the Cashier Dashboard
    def go_to_dashboard(self):
        style="background-color:transparent; border: 2px solid white; color: rgb(255, 255, 255);"
        if self.locked:
            self.showDialog("System is locked. Please try again after 1 minute.")
            return
        inputs = ["txtUsername", "txtPassword"]
        user_details = [self.txtUsername.text().replace(" ", ""), self.txtPassword.text().replace(" ", "")]
        if '' in user_details or self.txtUsername.text() not in self.users:
            if '' in user_details:
                self.lblLogin.show()
                self.red_mark(inputs)
            elif self.txtUsername.text() not in self.users:
                self.showDialog('Username is not registered!')
                self.txtUsername.setStyleSheet(style); self.txtPassword.setStyleSheet(style)
            self.attempts += 1
        elif self.txtUsername.text() in self.users:
            if self.users[self.txtUsername.text()] == self.txtPassword.text():
                self.attempts = 0
                self.user_profile()
                if self.position[self.txtUsername.text()] == 'Admin':
                    self.admin = Admin()
                    self.admin.show()
                    self.close()
                else:
                    self.cashier = Cashier()
                    self.cashier.show()
                    self.close()
            else:
                self.attempts+=1; self.showDialog('Wrong Password!')
        if self.attempts >= 3:
            self.lock_system()

    #Method for locking the system if maximum attempts is reached
    def lock_system(self):
        self.locked = True
        self.showDialog("Maximum login attempts exceeded. System locked for 1 minute.")
        self.timer.start(60000)  # 1 minute in milliseconds

    #Method for unlocking the system automatically after a minute
    def unlock_system(self):
        self.locked = False
        self.showDialog("System unlocked. You can now log in.")
        self.attempts = 0

    #Method for the action of buttons in the side panel
    def selected_menu(self, btn):
        button = getattr(self, btn)
        if button.isChecked():
            button_name = btn[3:-1]
            find_btn = getattr(self, button_name)
            self.stackedWidget.setCurrentWidget(find_btn)

    # METHOD TO CLEAR THE FIELDS
    def clear_fields(self, fields_list):
        for field in fields_list:
            if hasattr(self, field):
                attribute = getattr(self, field)
                if isinstance(attribute, QLineEdit) or isinstance(attribute, QTextEdit):
                    attribute.clear()
                elif isinstance(attribute, QComboBox):
                    attribute.setCurrentIndex(0)
                elif isinstance(attribute, QSpinBox):
                    attribute.setValue(0)

    def set_input_validators(self, line_edit_names, integer_line_edit_names):
        alpha_validator = QRegExpValidator(QRegExp("[a-zA-Z]+")); int_validator = QRegExpValidator(QRegExp("[0-9]+"))
        for line_edit_name in line_edit_names:
            widget = getattr(self, line_edit_name)
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setValidator(alpha_validator)
        for integer_line_edit_name in integer_line_edit_names:
            widget = getattr(self, integer_line_edit_name)
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setValidator(int_validator)

class Admin(Hotel):
    def __init__(self):
        super(Admin, self).__init__()
        uic.loadUi('adminUI.ui', self)
        self.show()
        self.loginform = False
        self.setWindowTitle('Hotel Accommodation Management System')
        self.system_info()
        self.sysname='Hotel Accommodation Management System'; self.syspic='C:/Users/user/Desktop/HMS_PROJECT/hotelB.png'
        self.setupTable_Rooms(); self.show_room_table()
        self.setup_employeetable(); self.show_employees_table(); self.view_add_employee(); self.SWemployee.setCurrentIndex(0)
        self.setup_archivetable(); self.show_archivetbl(); self.show_promos()
        #set user picture
        global user_profile_info
        self.list=user_profile_info[0]
        self.lblpic1.setPixmap(QPixmap(self.list[0])); self.lbluserpic2.setPixmap(QPixmap(self.list[0])); self.lblFname.setText(self.list[1]); self.lblposition.setText(self.list[2])
        self.update_combobox()
        self.wrongpass=False; self.widget = None
        self.field_data=[]; self.text=''; self.deletefromtbl=''
        text_only=['txtUDamenities', 'txtARroomtype', 'txtARamenities', 'txtEMfirstname', 'txtEMlastname', 'txtEMEfirstname', 'txtEMElastname']; int_only=['txtUDroomrate', 'txtARroomrate']
        self.set_input_validators(text_only, int_only)
        self.stackedWidget.setCurrentIndex(0)
        self.full_menu_widget.hide()
        # self.dt1.setDate(QDate.currentDate())
        self.month_name = QDate.currentDate().toString("MMMM")
        self.cboSDate.setCurrentText(self.month_name)
        self.SWrooms.setCurrentIndex(0); self.employeeTab.setCurrentIndex(0)
        button_connections = {'btnAddRoom': 'view_add_rooms', 'btnRoomBack': 'back_room', 'btnARback': 'back_room', 'btnSearchRoom': 'search_room', 'btnBacktoTableRoom': 'room_back_to_table', 'btnRoomSettings': 'room_settings', 'btnUDroomOK': 'update_room_type', 'btnRoomSave': 'room_save_data', 'btnARsave': 'add_new_roomdata', 'btnRTdelete': 'roomtype_delete', 'btnRMClear': 'reset_room_fields', 'btnARpic' : 'add_room_uploadpic', 'btnUDchangepic':'room_change_photo',
                              'btnRMClear2': 'reset_room_fields', 'btnRoomsView': 'view_room_info', 'btnRMdelete': 'show_question', 'btnExit1': 'redirect_to_hotel', 'btnExit2': 'redirect_to_hotel', 'btnSdelete':'show_SDquestion', 'btnSclear':'clear_empfields', 'btnEMupload':'employee_uploadpic', 'btnEMsave': 'add_employee_button', 'btnEMEcancel': 'update_empployee_cancelbtn', 'btnSupdateuser':'update_employee_info', 'btnEMEsave':'update_employee_save', 'btnRoomArchive': 'room_archive',
                              'btnArchBack': 'back_to_roomsettings', 'btnRMrestore': 'question_restore', 'btnEMEupload':'updateEmp_uploadpic', 'btnSchangephoto':'settings_uploadpic', 'btnSaveSettings':'save_settings', 'btnRestore_Default':'restore_default_Qdialog', 'btnAddPromo':'new_promo', 'btnRemovePromo':'remove_promo'}
        for button_name, method_name in button_connections.items():
            button = getattr(self, button_name); method = getattr(self, method_name)
            button.clicked.connect(method)
        self.btnHome1.setChecked(True); self.btnHome2.setChecked(True)
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000); self.update_datetime()  # Update immediately
        #Used to give actions for options in side panel
        for name in admin_buttons:
            button = getattr(self, name)
            button.clicked.connect(lambda checked, button_name=name: self.selected_menu(button_name))

    def remove_promo(self):
        try:
            deleter = self.tblPromo.item(self.tblPromo.currentRow(), 0).text().replace('PROMO-0', '')
            query = """UPDATE promo SET status = 'Expired' WHERE promo_id = %s;"""
            self.exec_query(query, deleter)
            QTimer.singleShot(100, lambda: self.showDialog('Promo Deleted!'))
            self.show_promos()
        except:
            self.showDialog('Select Promo from table first!')

    def new_promo(self):
        self.widget = uic.loadUi('NewPromo.ui')
        self.widget.dtStartDate.setDate(QDate.currentDate()); self.widget.dtExpireDate.setDate(QDate.currentDate())
        self.widget.btnPRsave.clicked.connect(self.save_new_promo)
        try:
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = "SELECT MAX(CAST(promo_id AS SIGNED)) FROM promo"
            cursor.execute(command)
            records = cursor.fetchall()
            val = records[0][0]
            self.count=val+1
            self.widget.txtPromoNo.setText('PROMO-0' + str(int(self.count)))
        except:
            self.widget.txtPromoNo.setText('PROMO-0' + str(1))
        self.widget.show()

    def save_new_promo(self):
        if self.widget.txtPromoName.text() == '' or self.widget.txtPromoVal.text() == '':
            text = 'Please fill out all the fields!'
        else:
            data = (self.widget.txtPromoNo.text().replace('PROMO-0', ''), self.widget.txtPromoName.text(), self.widget.txtPromoVal.text(), self.widget.dtStartDate.text(), self.widget.dtExpireDate.text(), 'Active')
            query = """INSERT INTO promo(promo_id,promo_name,value,start_date,expiry_date,status) VALUES (%s,%s,%s,%s,%s,%s);"""
            self.exec_query(query, data)
            text= "Promo successfully added!"
        self.widget.close(); self.showDialog(text)
        self.new_promo(); self.show_promos()

    def show_promos(self):
        self.tblPromo.clear(); self.tblPromo.setRowCount(2); self.tblPromo.setColumnCount(2)
        self.tblPromo.setItem(0, 0, QtWidgets.QTableWidgetItem('Promo No.'))
        self.tblPromo.setItem(0, 1, QtWidgets.QTableWidgetItem('Promo Name'))
        promo_names = []
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT promo_id, promo_name FROM promo WHERE status = 'Active' ORDER BY CAST(promo_id AS SIGNED) ASC"
        cursor.execute(command)
        records = cursor.fetchall()
        if len(records) == 0:
            self.tblPromo.setItem(1, 0, QtWidgets.QTableWidgetItem("No Available Promo"))
        else:
            for row in records:
                currentRowCount = self.tblPromo.rowCount()
                self.tblPromo.insertRow(currentRowCount)
                self.tblPromo.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('PROMO-0' + str(row[0])))
                self.tblPromo.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                promo_names.append(row[1])
        try:
            if len(promo_names) == 0:
                self.cboCpromos.addItem('No Available Promo')
            else:
                self.cboCpromos.clear(); self.cboCpromos.addItems(promo_names)
        except:
            pass

    def restore_default_Qdialog(self):
        self.widget = uic.loadUi('RestoreDefault.ui'); self.widget.setWindowTitle('Hotel Management System')
        self.widget.btnProceed.clicked.connect(self.system_restoredefault); self.widget.show()

    def system_restoredefault(self):
        self.widget.close()
        self.sysname='Hotel Accommodation Management System'; self.syspic='C:/Users/user/Desktop/HMS_PROJECT/hotelB.png'
        query = """UPDATE hotel_info SET hotel_name = %s, hotel_pic = %s WHERE hotel_id = '1';"""
        data_value=(self.sysname, self.syspic); self.exec_query(query, data_value)
        self.showDialog("Default settings restored successfully."); QTimer.singleShot(300, lambda: self.system_info())

    def save_settings(self):
        if self.txtsysname.text() == '':
            self.showDialog('Please Enter Hotel Name!')
        else:
            if self.source_path == '':
                data_value = (self.txtsysname.text(), self.syspic)
            else:
                data_value = (self.txtsysname.text(), self.source_path)
            query = """UPDATE hotel_info SET hotel_name = %s, hotel_pic = %s WHERE hotel_id = '1';"""
            self.exec_query(query, data_value)
            self.showDialog('System Settings Saved Successfully!')
            QTimer.singleShot(300, lambda: self.system_info())

    def system_info(self):
        data_list = []
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = """SELECT hotel_name, hotel_pic FROM hotel_info"""
        cursor.execute(command)
        records = cursor.fetchall()
        for data in records:
            data_list.extend(data)
        self.sysname=data_list[0].upper(); self.syspic=data_list[1]
        self.system_name.setText(self.sysname); self.sys_pic.setPixmap(QPixmap(self.syspic)); self.txtsysname.setText(data_list[0]); self.sys_picsettings.setPixmap(QPixmap(data_list[1]))

    def settings_uploadpic(self):
        self.browsefiles(); scaled_pixmap = self.pixmap.scaled(280, 280); self.sys_picsettings.setPixmap(scaled_pixmap)

    def clear_empfields(self):
        inputs = ['txtEMfirstname', 'txtEMlastname', 'txtEMusername', 'txtEMpass', 'txtEMrepass', 'cboEMposition', 'cboEMsched', 'txtEMEfirstname', 'txtEMElastname', 'txtEMEusername', 'txtEMEpassword', 'txtEMEnewpass', 'txtEMErenewpass', 'cboEMEposition', 'cboEMEsched']
        self.clear_fields(inputs); self.source_path=''; self.lblEMpic.setPixmap(QPixmap('user_icon.png')); self.lblEMEpic.setPixmap(QPixmap('user_icon.png')); self.back_to_normal(inputs)

    def updateEmp_uploadpic(self):
        self.browsefiles(); scaled_pixmap = self.pixmap.scaled(230, 230); self.lblEMEpic.setPixmap(scaled_pixmap)

    def update_employee_save(self):
        inputs = ['txtEMEfirstname', 'txtEMElastname', 'txtEMEusername', 'txtEMEpassword', 'txtEMEnewpass','txtEMErenewpass', 'cboEMEposition', 'cboEMEsched']
        self.user_new = [self.txtEMEemployee_id.text(), self.txtEMEfirstname.text().replace(" ", ""), self.txtEMElastname.text().replace(" ", ""), self.txtEMEusername.text().replace(" ", ""), self.txtEMEpassword.text().replace(" ", ""), self.cboEMEposition.currentText(), self.cboEMEsched.currentText()]
        if '' in self.user_new:
            self.showDialog('Please fill out all the fields!'); self.red_mark(inputs)
        else:
            self.back_to_normal(inputs); list=['txtEMEnewpass', 'txtEMErenewpass']
            if self.txtEMEnewpass.text() != self.txtEMErenewpass.text():
                self.red_mark(list)
                if str(self.txtEMEnewpass.styleSheet()) == "background-color: rgb(255, 255, 255); border: none;" and str(self.txtEMErenewpass.styleSheet()) == "background-color: rgb(255, 255, 255); border: none;":
                    self.showDialog("Password don't match!")
            else:
                data_value = self.txtEMusername.text()
                connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
                cursor = connection.cursor()
                command = """SELECT username from employees"""
                cursor.execute(command)
                records = cursor.fetchall()
                existing_usernames = [record[0] for record in records]
                if data_value in existing_usernames:
                    self.showDialog('Username already exists!')
                    self.txtEMEusername.setStyleSheet("background-color: white; border: 1px solid red;")
                else:
                    self.txtEMEusername.setStyleSheet("background-color: white; border: none;"); self.adminpass_show(); self.add_emp=False

    def update_empployee_cancelbtn(self):
        self.SWemployee.setCurrentIndex(0); self.clear_empfields(); self.show_employees_table()

    def update_employee_info(self):
        try:
            data_value = self.tblInfoEmployees.item(self.tblInfoEmployees.currentRow(), 0).text().replace('EM-23-0', '')
            self.SWemployee.setCurrentIndex(1); self.txtEMEpassword.hide(); self.lblcurrentpass.hide()
            data_list = []
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT employee_id, firstname, lastname, pic, username, password, position, schedule FROM employees WHERE employee_id = %s"""
            cursor.execute(command, data_value)
            records = cursor.fetchall()
            for data in records:
                data_list.extend(data)
            self.txtEMEemployee_id.setText('EM-23-0'+str(data_list[0])); self.txtEMEfirstname.setText(data_list[1]); self.txtEMElastname.setText(data_list[2]); self.txtEMEusername.setText(data_list[4]); self.txtEMEpassword.setText(data_list[5]); self.cboEMEposition.setCurrentText(data_list[6]); self.cboEMEsched.setCurrentText(data_list[7])
            self.source_path=data_list[3]
            if data_list[3] == '':
                self.lblEMEpic.setPixmap(QPixmap('user_icon.png'))
            else:
                self.lblEMEpic.setPixmap(QPixmap(str(data_list[3])))
        except:
            self.showDialog('Please select from the table first!')

    # METHOD TO SHOW DELETE QUESTION DIALOG
    def show_SDquestion(self):
        self.widget = uic.loadUi('DialogQuestion.ui')
        self.widget.setWindowTitle('Hotel Management System')
        self.deletefromtbl = self.tblInfoEmployees.item(self.tblInfoEmployees.currentRow(), 1).text()
        self.widget.txtQuestion.setText('Are you sure you want to remove ' + self.tblInfoEmployees.item(self.tblInfoEmployees.currentRow(), 1).text() + '?')
        self.widget.btnDelete.clicked.connect(self.emp_delete_proceed)
        self.widget.show()
    #DELETE FROM EMPLOYEES TBL
    def emp_delete_proceed(self):
        self.deletefromtbl = self.tblInfoEmployees.item(self.tblInfoEmployees.currentRow(), 0).text()
        deleter = self.deletefromtbl.replace('EM-23-0', '')
        if deleter != '':
            query = """UPDATE employees SET status = 'Terminated' WHERE employee_id = %s;"""
            self.exec_query(query, deleter)
            self.show_employees_table()
            text = 'Employee removed!'
            self.widget.close()
            QTimer.singleShot(300, lambda: self.showDialog(text))
            print(deleter)
            self.show_employees_table()
        else:
            self.showDialog('Select data from table first!')

    def view_add_employee(self):
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        command = "SELECT MAX(CAST(employee_id AS SIGNED)) FROM employees"
        cursor = connection.cursor()
        cursor.execute(command)
        records = cursor.fetchall()
        val = records[0][0]
        self.txtEMid.setText('EM-23-0' + str(int(val) + 1))

    def employee_uploadpic(self):
        self.browsefiles(); scaled_pixmap = self.pixmap.scaled(230, 230); self.lblEMpic.setPixmap(scaled_pixmap)

    def browsefiles(self):
        file_dialog = QFileDialog()
        desktop_location = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        file_dialog.setDirectory(desktop_location)
        file = file_dialog.getOpenFileName(self, "Upload File", "", "Image Files (*.jpg *.png)")
        self.source_path = file[0]
        print(self.source_path)
        self.pixmap = QPixmap(self.source_path)
        if self.source_path:
            import shutil
            import os
            current_directory = os.getcwd()
            destination_path = os.path.join(current_directory, os.path.basename(self.source_path))
            if current_directory != os.path.dirname(destination_path):
                shutil.copy(self.source_path, destination_path)
                self.source_path = destination_path
        else:
            self.pixmap = QPixmap('user_icon.png')

    # ADD NEW EMPLOYEE TO DATA BASE
    def add_employee_button(self):
        inputs = ['txtEMfirstname', 'txtEMlastname', 'txtEMusername', 'txtEMpass', 'txtEMrepass', 'cboEMposition', 'cboEMsched']
        self.user_new = [self.txtEMid.text(), self.txtEMfirstname.text().replace(" ", ""), self.txtEMlastname.text().replace(" ", ""), self.txtEMusername.text().replace(" ", ""), self.txtEMpass.text().replace(" ", ""), self.txtEMrepass.text().replace(" ", ""), self.cboEMposition.currentText(), self.cboEMsched.currentText()]
        if '' in self.user_new:
            self.showDialog('Please fill out all the fields!'); self.red_mark(inputs)
        else:
            if self.source_path != '':
                self.back_to_normal(inputs)
                if self.txtEMpass.text() == self.txtEMrepass.text():
                    data_value=self.txtEMusername.text()
                    connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
                    cursor = connection.cursor()
                    command = """SELECT username from employees"""
                    cursor.execute(command)
                    records = cursor.fetchall()
                    existing_usernames = [record[0] for record in records]
                    if data_value in existing_usernames:
                        self.showDialog('Username already exists!'); self.txtEMusername.setStyleSheet("background-color: white; border: 1px solid red;")
                    else:
                        self.txtEMusername.setStyleSheet("background-color: white; border: none;"); self.adminpass_show(); self.add_emp=True
                else:
                    self.showDialog('Passwords do not match!')
            else:
                self.showDialog('Please upload your photo!!')

    def adminpass_show(self):
        self.widget = uic.loadUi('admin_pass.ui'); self.widget.setWindowTitle('Hotel Management System')
        self.widget.admin_proceed.clicked.connect(self.adminpass_proceed); self.widget.show()

    def adminpass_proceed(self):
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = """SELECT password FROM employees WHERE position = 'Admin'"""
        cursor.execute(command)
        records = cursor.fetchall()
        data_list = [item[0] for item in records]
        if self.widget.txtadminpass.text() in data_list:
            if self.add_emp==True:
                text='Employee Successfully Added!'
                data_value = [self.txtEMid.text().replace('EM-23-0', ''), self.txtEMfirstname.text(), self.txtEMlastname.text(), self.source_path, self.txtEMusername.text(), self.txtEMpass.text(), self.cboEMposition.currentText(), self.cboEMsched.currentText(), 'Employed']
                query = """INSERT INTO employees (employee_id,firstname,lastname,pic,username,password,position,schedule,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s); """
                self.exec_query(query, data_value)
            elif self.add_emp == False:
                if self.txtEMErenewpass.text() == '':
                    data_value = [self.txtEMEemployee_id.text().replace('EM-23-0', ''), self.txtEMEfirstname.text(), self.txtEMElastname.text(), self.source_path, self.txtEMEusername.text(), self.txtEMEpassword.text(), self.cboEMEposition.currentText(), self.cboEMEsched.currentText()]
                else:
                    data_value = [self.txtEMEemployee_id.text().replace('EM-23-0', ''), self.txtEMEfirstname.text(), self.txtEMElastname.text(), self.source_path, self.txtEMEusername.text(), self.txtEMEnewpass.text(), self.cboEMEposition.currentText(), self.cboEMEsched.currentText()]

                query = """UPDATE employees SET firstname = %s, lastname = %s, pic = %s, username = %s, password = %s, position = %s, schedule = %s WHERE employee_id = %s;"""
                self.data_value = (data_value[1], data_value[2], data_value[3], data_value[4], data_value[5], data_value[6], data_value[7],data_value[0])
                self.exec_query(query, self.data_value)
                text = 'Changes Saved!'

            inputs = ['txtEMEfirstname', 'txtEMElastname', 'txtEMEusername', 'txtEMEpassword', 'txtEMEnewpass', 'txtEMErenewpass', 'cboEMEposition', 'cboEMEsched']
            self.show_employees_table()
            self.widget.close(); self.showDialog(text)
            self.clear_fields(inputs); self.source_path=''
            self.lblEMpic.setPixmap(QPixmap('user_icon.png')); self.lblEMEpic.setPixmap(QPixmap('user_icon.png'))
            self.view_add_employee(); QTimer.singleShot(300, lambda: self.update_empployee_cancelbtn())
        else:
            self.showDialog('Invalid Password!')

    def show_employees_table(self):
        self.setup_employeetable()
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT employee_id, username, position, schedule FROM employees WHERE status = 'Employed' ORDER BY CAST(employee_id AS SIGNED) ASC"
        cursor.execute(command)
        records = cursor.fetchall()
        if len(records) == 0:
            self.tblInfoEmployees.setItem(1, 0, QtWidgets.QTableWidgetItem("No data to display")); self.tblInfoEmployees.setItem(1, 1, QtWidgets.QTableWidgetItem("No data to display"))
            self.tblInfoEmployees.setItem(1, 2, QtWidgets.QTableWidgetItem("No data to display")); self.tblInfoEmployees.setItem(1, 3, QtWidgets.QTableWidgetItem("No data to display"))
        else:
            for row in records:
                currentRowCount = self.tblInfoEmployees.rowCount()  # 2 (0,1)
                self.tblInfoEmployees.insertRow(currentRowCount)
                self.tblInfoEmployees.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('EM-23-0' + str(row[0])))
                self.tblInfoEmployees.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                self.tblInfoEmployees.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                self.tblInfoEmployees.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            command = "SELECT COUNT(employee_id) FROM employees WHERE status = 'Employed';"
            cursor.execute(command)
            records = cursor.fetchall()
            val = records[0][0]
            self.lblEmployeesTotal.setText(str(int(val)))

    def setup_employeetable(self):
        self.table = self.tblInfoEmployees
        self.table.clear()
        self.table.setRowCount(2)  # headers # 1st row for 1st data
        self.table.setColumnCount(4)  # columns count
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem('Employee ID'))
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem('Username'))
        self.table.setItem(0, 2, QtWidgets.QTableWidgetItem('Position'))
        self.table.setItem(0, 3, QtWidgets.QTableWidgetItem('Schedule'))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

    #GO BACK TO LOG IN PAGE
    def redirect_to_hotel(self):
        self.hotel = Hotel(); self.hotel.show(); self.close()

    def question_restore(self):
        self.widget = uic.loadUi('RestoreQuestion.ui'); self.widget.setWindowTitle('Hotel Management System')
        self.deletefromtbl = self.tblRoomArchive.item(self.tblRoomArchive.currentRow(), 0).text()
        self.widget.txtQuestion.setText('Make room '+self.deletefromtbl+' Available?')
        self.widget.btnProceed.clicked.connect(self.restore_proceed); self.widget.show()

    def restore_proceed(self):
        deleter=self.deletefromtbl.replace('RM-0','')
        query = """UPDATE rooms SET Status = 'Available' WHERE room_number = %s;"""
        self.exec_query(query, deleter); self.show_archivetbl()
        text=self.deletefromtbl+' is now removed from archive!'
        self.widget.close(); QTimer.singleShot(300, lambda: self.showDialog(text)); self.show_archivetbl(); self.show_room_table()

    def show_archivetbl(self):
        self.setup_archivetable()
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT room_number, room_type, Status FROM rooms WHERE Status = 'Unavailable' ORDER BY CAST(room_number AS SIGNED) ASC"
        cursor.execute(command); records = cursor.fetchall()
        if len(records) == 0:
            self.tblRoomArchive.setItem(1, 0, QtWidgets.QTableWidgetItem("No data to display"))
        else:
            for row in records:
                currentRowCount = self.tblRoomArchive.rowCount()
                self.tblRoomArchive.insertRow(currentRowCount)
                self.tblRoomArchive.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('RM-0' + str(row[0])))
                self.tblRoomArchive.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1]))); self.tblRoomArchive.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2])))

    def setup_archivetable(self):
        self.table = self.tblRoomArchive; self.table.clear()
        self.table.setRowCount(2); self.table.setColumnCount(3)
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem('Room Number')); self.table.setItem(0, 1, QtWidgets.QTableWidgetItem('Room Type')); self.table.setItem(0, 2, QtWidgets.QTableWidgetItem('Status'))
        self.table.verticalHeader().setVisible(False); self.table.horizontalHeader().setVisible(False)

    #BACK TO ROOMS TABLE
    def back_room(self):
        self.SWrooms.setCurrentIndex(0); self.reset_room_fields(); self.show_room_table()

    #METHOD TO PUT ALL ROOM TYPE IN COMBO BOXES
    def update_combobox(self):
        global data_list
        data_list=[]
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT type FROM room_info"
        cursor.execute(command)
        records = cursor.fetchall()
        data_list = [item[0] for item in records]; data_list.insert(0, '')
        try:
            self.cboCroomtype.clear(); self.cboCroomtype.addItems(data_list)
        except:
            self.cboSearchRoom.clear(); self.cboUDroomtype.clear(); self.cboarchive.clear()
            self.cboSearchRoom.addItems(data_list); self.cboUDroomtype.addItems(data_list); self.cboarchive.addItems(data_list)

    #VIEW OTHER DETAILS OF THE ROOM METHOD
    def view_room_info(self):
        try:
            self.widget = uic.loadUi('ViewRoomInfo.ui')
            self.widget.setWindowTitle('Hotel Management System')
            data = []
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT room_number, room_type, room_rate, max_guest, bed, amenities FROM rooms WHERE room_number = %s"""
            data_value = self.tblInfo.item(self.tblInfo.currentRow(), 0).text().replace('RM-0',"")
            cursor.execute(command, data_value)
            records = cursor.fetchall()
            for d in records:
                data.extend(d)
            self.widget.txtVRRoomNum.setText('RM-0'+data[0])
            count = 1
            fields = ["txtVRroomtype", "txtVRroomrate", "txtVRmaxguests", "txtVRbed", "txtVRamenities"]
            for f in fields:
                getattr(self.widget, f).setText(str(data[count]))
                count += 1
            self.widget.show()
        except:
            self.showDialog('Select data from table first!')

    #METHOD TO SHOW REMOVE QUESTION DIALOG
    def show_question(self):
        try:
            self.widget = uic.loadUi('DialogQuestion.ui')
            self.widget.setWindowTitle('Hotel Management System')
            self.deletefromtbl = self.tblInfo.item(self.tblInfo.currentRow(), 0).text()
            self.widget.txtQuestion.setText('Are you sure you want to remove '+self.deletefromtbl+'?')
            self.widget.btnDelete.clicked.connect(self.delete_proceed)
            self.widget.show()
        except:
            self.showDialog('Select data from table first!')

    #METHOD TO DELETE SELECTED ROOM FROM TABLE
    def delete_proceed(self):
        deleter=self.deletefromtbl.replace('RM-0','')
        query = """UPDATE rooms SET Status = 'Unavailable' WHERE room_number = %s;"""
        self.exec_query(query, deleter)
        self.show_room_table()
        text=self.deletefromtbl+' was removed from rooms!'
        self.widget.close()
        QTimer.singleShot(300, lambda: self.showDialog(text))
        self.show_room_table(); self.show_archivetbl()

    #SEARCH ROOM METHOD
    def search_room(self):
        if self.cboSearchRoom.currentText() == '':
            pass
        else:
            self.setupTable_Rooms()
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT room_number, room_type, room_rate, Status FROM rooms WHERE room_type  = %s AND Status in ('Available', 'Occupied');"""
            data_value = self.cboSearchRoom.currentText()
            cursor.execute(command,data_value)
            records = cursor.fetchall()
            if len(records) == 0:
                self.tblInfo.setItem(1, 0, QtWidgets.QTableWidgetItem("No data to display"))
            else:
                for row in records:
                    currentRowCount = self.tblInfo.rowCount()  # 2 (0,1)
                    self.tblInfo.insertRow(currentRowCount)
                    self.tblInfo.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('RM-0' + str(row[0])))
                    self.tblInfo.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tblInfo.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tblInfo.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem(str(row[3])))

    #BACK TO TABLE BUTTON IN ROOMS
    def room_back_to_table(self):
        self.show_room_table(); self.cboSearchRoom.setCurrentIndex(0)

    def room_archive(self):
        self.SWrooms.setCurrentIndex(2); self.roomtab.setCurrentIndex(0)
    def back_to_roomsettings(self):
        self.SWrooms.setCurrentIndex(1)

    def room_settings(self):
        self.SWrooms.setCurrentIndex(1); self.source_path=''; self.roomtab.setCurrentIndex(0)

    #METHOD TO DELETE ROOM TYPE FROM TYPE OF ROOMS
    def roomtype_delete(self):
        if self.cboUDroomtype.currentText() != '':
            list=['cboUDroomtype']; self.back_to_normal(list)
            self.deleter = self.cboUDroomtype.currentText()
            query = """DELETE FROM room_info where type =%s"""
            data_value = (self.deleter)
            self.exec_query(query, data_value)
            #QUERY TO REMOVE ROOMS IN DATABASE
            query = """DELETE FROM rooms where room_type =%s"""
            data_value = (self.deleter)
            self.exec_query(query, data_value)
            self.show_room_table()
            self.showDialog(f'All {self.deleter} room were deleted successfully!')
            self.update_combobox(); self.reset_room_fields()
            # QUERY TO REMOVE RE-ARRANGE ORDER OF ID IN DATABASE
            # query = """UPDATE rooms SET room_number = new_id FROM (SELECT room_number, ROW_NUMBER() OVER (ORDER BY room_number) AS new_id FROM your_table) AS subquery WHERE rooms.room_number = subquery.room_number;"""
            # self.exec_query(query)
        else:
            self.showDialog('Select Room Type first!'); list=['cboUDroomtype']; self.red_mark(list)

    def room_change_photo(self):
        self.browsefiles(); scaled_pixmap = self.pixmap.scaled(230, 230); self.lblUDpic.setPixmap(scaled_pixmap)

    #OK BUTTON IN ROOM SETTINGS UPDATE
    def update_room_type(self):
        if self.cboUDroomtype.currentText() != '':
            data_list=[]
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT pax, rate, bed, room_amenities, room_pic FROM room_info WHERE type = %s"""
            data_value = self.cboUDroomtype.currentText()
            cursor.execute(command, data_value)
            records = cursor.fetchall()
            for data in records:
                data_list.extend(data)
            self.txtUDmaxguest.setValue(int(data_list[0])); self.txtUDroomrate.setText(str(data_list[1])); self.txtUDamenities.setText(str(data_list[3]))
            items = data_list[2].split(',')
            bt_dict = {item.split()[1]: item.split()[0] for item in items}
            if 'Single' in bt_dict:
                self.s1Single.setValue(int(bt_dict['Single']))
            if 'Double' in bt_dict:
                self.s1Double.setValue(int(bt_dict['Double']))
            if 'Queen' in bt_dict:
                self.s1Queen.setValue(int(bt_dict['Queen']))
            if 'King' in bt_dict:
                self.s1King.setValue(int(bt_dict['King']))
            if data_list[4] == '':
                self.lblUDpic.setPixmap(QPixmap('image.jpg'))
            else:
                self.lblUDpic.setPixmap(QPixmap(data_list[4]))
        else:
            pass

    #METHOD TO SHOW THE ADD ROOM FORM
    def view_add_rooms(self):
        global data_list
        self.widget = uic.loadUi('AddRoom.ui')
        self.widget.setWindowTitle('Hotel Management System')
        self.widget.btnAddRoomSaveButton.clicked.connect(self.add_new_rooms)
        self.widget.cboARroomtype.addItems(data_list)
        try:
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = "SELECT MAX(CAST(room_number AS SIGNED)) FROM rooms"
            cursor.execute(command)
            records = cursor.fetchall()
            val = records[0][0]
            self.count=val+1
            self.widget.txtRoomNum.setText('RM-0' + str(int(self.count)))
        except:
            self.widget.txtRoomNum.setText('RM-0' + str(1))
        self.widget.show()

    def cancel_add_rooms(self):
        self.SWrooms.setCurrentIndex(0); self.cboAddroomtype.setCurrentIndex(0); self.ARquantity.setValue(0)

    #METHOD TO ADD NEW ROOM TO DATABASE
    def add_new_rooms(self):
        if self.widget.cboARroomtype.currentText() != '':
            if self.widget.sbQuantity.value() ==0:
                text='Please input room quantity!'
            else:
                data = [self.widget.txtRoomNum.text().replace('RM-0', '')]
                connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
                cursor = connection.cursor()
                command = """SELECT type, pax, rate, bed, room_amenities FROM room_info WHERE type = %s"""
                data_value = self.widget.cboARroomtype.currentText()
                cursor.execute(command, data_value)
                records = cursor.fetchall()
                for a in records:
                    data.extend(a)
                quantity = self.widget.sbQuantity.value()
                query = """INSERT INTO rooms(room_number,room_type,max_guest,room_rate,bed,amenities,Status) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
                room_number = int(self.widget.txtRoomNum.text().replace('RM-0', ''))
                for i in range(quantity):
                    self.data_value = (room_number, data[1], data[2], data[3], data[4], data[5],'Available')
                    self.exec_query(query, self.data_value)
                    room_number+=1
                text= str(quantity) + " new " + data_value + " room successfully added!"
            self.widget.close(); self.showDialog(text); self.view_add_rooms(); self.show_room_table()
        else:
            self.showDialog('Select a Room Type!')

    def add_room_uploadpic(self):
        self.browsefiles(); scaled_pixmap = self.pixmap.scaled(230, 230); self.lblARpic.setPixmap(scaled_pixmap)

    #ADD ROOM CATEGORY FORM
    def add_new_roomdata(self):
        ARfields=['txtARroomtype', 'txtARroomrate', 'txtARmaxguest', 'txtARamenities']
        bed_type_dict = {'s2Single': 'Single Bed', 's2Double': 'Double Bed', 's2Queen': 'Queen Bed', 's2King': 'King Bed'}
        bed_type_list = [str(getattr(self, spinbox_name).value()) + ' ' + bed_type for spinbox_name, bed_type in bed_type_dict.items() if getattr(self, spinbox_name).value() > 0]
        self.field_data = [self.txtARroomtype.text(), str(self.txtARmaxguest.value()), str(self.txtARroomrate.text()), self.txtARamenities.toPlainText()]
        if '' in self.field_data:
            self.red_mark(ARfields)
            self.showDialog('Please fill all required fields!')
        else:
            self.back_to_normal(ARfields)
            self.field_data.insert(3, ', '.join(bed_type_list))
            if self.field_data[3] == '':
                self.showDialog('Please put at least 1 Bed Type!')
            else:
                self.back_to_normal(ARfields); self.field_data.append(self.source_path)
                self.text='New Room Category Added Successfully!'
                self.show_update_room('UpdateRoom.ui')

    #SAVING THE DATA FROM UPDATE ROOM FORM TO ROOMS DATABASE
    def room_save_data(self):
        UDfields = ['cboUDroomtype', 'txtUDroomrate', 'txtUDmaxguest', 'txtUDamenities']
        bed_type_dict = {'s1Single': 'Single Bed', 's1Double': 'Double Bed', 's1Queen': 'Queen Bed', 's1King':'King Bed'}
        bed_type_list = [str(getattr(self, spinbox_name).value()) + ' ' + bed_type for spinbox_name, bed_type in
                         bed_type_dict.items() if getattr(self, spinbox_name).value() > 0]
        self.field_data = [self.cboUDroomtype.currentText(), str(self.txtUDroomrate.text()), str(self.txtUDmaxguest.value()), self.txtUDamenities.toPlainText()]
        if '' in self.field_data:
            self.red_mark(UDfields)
            self.showDialog('Please fill all required fields!')
        else:
            self.back_to_normal(UDfields)
            self.field_data.insert(3, ', '.join(bed_type_list))
            if self.field_data[3] == '':
                self.showDialog('Please put at least 1 Bed Type!')
            else:
                self.back_to_normal(UDfields); self.field_data.append(self.source_path)
                self.text = 'Room Updated Successfully!'
                self.show_update_room('UpdateRoom.ui')

    #METHOD USED TO SHOW THE SUMMARY OF INPUTS IN ADD/UPDATE A ROOM
    def show_update_room(self, ui_file_path):
        self.widget = uic.loadUi(ui_file_path)
        self.widget.setWindowTitle('Hotel Management System')
        self.widget.btnUDroomsave.clicked.connect(self.UDroom_proceedbtn)
        fields = ["txtARroomtype", "txtARroomrate", "txtARmaxguests", "txtARbed", "txtARamenities"]
        for f in range(len(fields)):
            getattr(self.widget, fields[f]).setText(str(self.field_data[f]))
        self.widget.show()

    #UPDATE ROOM SAVE TO DATABASE METHOD
    def UDroom_proceedbtn(self):
        if self.text == 'Room Updated Successfully!':
            query = """UPDATE room_info SET rate = %s, pax = %s, bed = %s, room_amenities = %s, room_pic = %s WHERE type = %s;"""
            self.data_value=(self.field_data[1], self.field_data[2], self.field_data[3], self.field_data[4], self.field_data[5], self.field_data[0])
            self.exec_query(query,self.data_value)
            #SAVE UPDATED ROOM TYPE TO DATABASE ~~~
            query = """UPDATE rooms SET room_rate = %s, max_guest = %s, bed = %s, amenities = %s WHERE room_type = %s;"""
            self.data_value = (self.field_data[1], self.field_data[2], self.field_data[3], self.field_data[4], self.field_data[0])
            self.exec_query(query, self.data_value)
            self.showDialog(self.text)
        elif self.text == 'New Room Category Added Successfully!':
            query = """INSERT INTO room_info(type,pax,rate,bed,room_amenities,room_pic) VALUES (%s,%s,%s,%s,%s,%s); """
            self.data_value=(self.field_data[0], self.field_data[1], self.field_data[2], self.field_data[3], self.field_data[4], self.field_data[5])
            self.exec_query(query, self.data_value)
            self.showDialog(self.text)
            self.update_combobox()
        self.reset_room_fields()
        self.text=''; self.field_data=[]; self.source_path=''
        self.widget.close()

    #METHOD TO CLEAR ALL THE FIELDS
    def reset_room_fields(self):
        self.cboUDroomtype.setCurrentIndex(0);
        inputs = ['cboUDroomtype', 'txtUDroomrate', 'txtUDamenities', 'txtARroomtype', 'txtARroomrate', 'txtARamenities', 'txtUDmaxguest', 'txtARmaxguest', 's1Single', 's2Single', 's1Double', 's2Double', 's1Queen', 's2Queen', 's1King', 's2King']
        self.back_to_normal(inputs); self.clear_fields(inputs); self.source_path = ''; self.lblUDpic.setPixmap(QPixmap('image.jpg')); self.lblARpic.setPixmap(QPixmap('image.jpg'))

    # METHOD TO SHOW THE TABLE ON ROOMS OPTION
    def show_room_table(self):
        self.setupTable_Rooms()
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT room_number, room_type, room_rate, Status FROM rooms WHERE Status IN ('Available', 'Occupied') ORDER BY CAST(room_number AS SIGNED) ASC"
        cursor.execute(command)
        records = cursor.fetchall()
        if len(records) == 0:
            self.tblInfo.setItem(1, 0, QtWidgets.QTableWidgetItem("No data to display"))
        else:
            for row in records:
                currentRowCount = self.tblInfo.rowCount()
                self.tblInfo.insertRow(currentRowCount)
                self.tblInfo.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('RM-0' + str(row[0])))
                self.tblInfo.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1]))); self.tblInfo.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2]))); self.tblInfo.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            command = "SELECT COUNT(room_number) FROM rooms WHERE Status = 'Available';"
            cursor.execute(command)
            records = cursor.fetchall()
            val=records[0][0]
            self.lblAvailRooms.setText(str(int(val)))
            command = "SELECT COUNT(room_number) FROM rooms WHERE Status = 'Occupied';"
            cursor.execute(command)
            records = cursor.fetchall()
            val = records[0][0]
            self.lblOccRooms.setText(str(int(val)))

    def setupTable_Rooms(self):
        self.tblInfo.clear()
        self.tblInfo.setRowCount(2)
        self.tblInfo.setColumnCount(4)
        self.tblInfo.setItem(0, 0, QtWidgets.QTableWidgetItem('Room Number')); self.tblInfo.setItem(0, 1, QtWidgets.QTableWidgetItem('Room Type')); self.tblInfo.setItem(0, 2, QtWidgets.QTableWidgetItem('Room Rate')); self.tblInfo.setItem(0, 3, QtWidgets.QTableWidgetItem('Status'))
        self.tblInfo.verticalHeader().setVisible(False)
        self.tblInfo.horizontalHeader().setVisible(False)

    def exec_query(self,query_string,data_string):
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        cursor.execute(query_string,data_string)
        connection.commit()
        cursor.close()

class Cashier(Admin):
    def __init__(self):
        super(Cashier, self).__init__()
        uic.loadUi('cashierUI.ui', self)
        self.show()
        self.loginform = False
        self.system_info()
        self.stackedWidget.setCurrentIndex(0); self.full_menu_widget.hide()
        self.btnHome1.setChecked(True); self.btnHome2.setChecked(True)
        global user_profile_info
        self.list = user_profile_info[0]; self.lblhotelname.setText(self.system_name.text())
        self.lblpic1.setPixmap(QPixmap(self.list[0])); self.lbluserpic2.setPixmap(QPixmap(self.list[0])); self.lblFname.setText(self.list[1]); self.lblposition.setText(self.list[2])
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000); self.update_datetime(); self.update_combobox()
        self.cboCroomtype.currentIndexChanged.connect(self.update_cboCroomno_items)

        button_connections = {'btnExit1':'redirect_to_hotel', 'btnExit2':'redirect_to_hotel','btnAddClient':'add_new_client', 'btnACback':'add_client_back', 'btnACnext':'add_client_next', 'btnACRback':'addclient_roomback','btnACproceed':'add_client_proceed', 'btnEditClient':'edit_client_info', 'btndelclient':'del_client', 'btnRFIDenter':'rfid_checkin', 'btnCheck1':'checkin_page', 'btnCheck2':'checkin_page', 'btnOut1':'checkout_page', 'btnOut2':'checkout_page', 'btnRFIDout':'rfid_checkout', 'btnProceedPaymanet':'proceed_to_payment',
                              'btnCoutCancel':'cancel_checkout', 'btnpaycash':'pay_proceed', 'btnpayexit':'exit_payment'}
        for button_name, method_name in button_connections.items():
            button = getattr(self, button_name); method = getattr(self, method_name)
            button.clicked.connect(method)
        for name in cashier_buttons:
            button = getattr(self, name)
            button.clicked.connect(lambda checked, button_name=name: self.selected_menu(button_name))
        self.btnRFIDenter.hide(); self.btnRFIDout.hide(); self.show_promos(); self.txtOrate.hide()
        self.setup_clientinfo_tbl(); self.show_clientinfo_table(); self.SWClient.setCurrentIndex(0)
        self.setup_checkin_tbl(); self.show_checkin_tbl(); self.btnProceedPaymanet.setEnabled(False); self.btnCoutCancel.setEnabled(False)
        self.inputs_personal = ['txtCfirstname', 'txtClastname', 'cboCidtype', 'txtCidnum', 'txtCcontactno']; self.inputs_room = ['cboCroomtype', 'cboCroomno', 'cboCroomno', 'txtroomrate', 'txtCrfidNo']

    def cancel_checkout(self):
        self.btnProceedPaymanet.setEnabled(False); self.btnCoutCancel.setEnabled(False)
        self.clear_fields(self.check_out_fields)

    def exit_payment(self):
        self.showDialog('Thank you for staying here!')
        self.stackedWidget.setCurrentIndex(3)
        self.btnExit1.setEnabled(True); self.btnExit2.setEnabled(True)
        global cashier_buttons
        for button_name in cashier_buttons:
            button = getattr(self, button_name)
            button.setEnabled(True)
        #METHOD TO SAVE TO DATABASE AND CHANGE STATUS T CHECK OUT CALL TABLE SHECK IN
        checkout_client=self.client_deleter
        query = """UPDATE clients SET status = 'Check out' WHERE client_id = %s;"""
        self.exec_query(query, checkout_client)
        self.client_deleter = None
        self.show_clientinfo_table(); self.show_checkin_tbl()

    def proceed_to_payment(self):
        global cashier_buttons
        for button_name in cashier_buttons:
            button = getattr(self, button_name)
            button.setEnabled(False)
        self.stackedWidget.setCurrentIndex(4); self.lbldatetoday.setText(self.lblDate.text()); self.btnpaycash.setEnabled(True)
        query = """UPDATE clients SET checkout_date = %s, checkout_time = %s, days_stayed = %s WHERE rfid_no = %s;"""
        self.exec_query(query, self.data_value)
        self.client_deleter = self.txtOid.text().replace('HMS-23-0', '')
        self.lblcid.setText('Client ID: '+ self.txtOid.text()); self.lblcname.setText('Client Name: '+self.txtOfname.text()+' '+self.txtOlname.text()); self.lblroomno.setText('Room no.: '+self.txtOroomno.text()); self.lblcindate.setText('Check-in Date: '+self.txtOcindate.text()); self.lblcoutdate.setText('Check-out Date: '+self.txtOcoutdate.text())
        self.txtOpromo.show(); self.lblpromo.setText('Promo: '+self.txtOpromo.text()); self.txtOpromo.hide(); self.lblrecep.setText('Receptionist: '+self.lblFname.text()+' '+self.list[3])
        self.txtOrate.show(); self.lblpayroomrate.setText('Rate: ' + self.txtOrate.text()); self.txtOrate.hide()
        hours_stayed = int(self.txtOstay.text()[:-1]); min_rate= int(self.txtOrate.text().replace('PHP ',''))
        if self.txtOstay.text()[-1] == 'h':
            if hours_stayed <= self.minimum_stay:
                self.subtotal=min_rate
            else:
                additional_hours = hours_stayed - self.minimum_stay
                additional_payment = (additional_hours // self.minimum_stay) * min_rate

                total_payment = min_rate + additional_payment
                self.subtotal= total_payment
        else:
            self.subtotal=min_rate

        self.lblstay.setText('Length of stay: ' + self.txtOstay.text())
        # self.subtotal= int(self.lblpayroomrate.text().replace('Rate: ', ''))
        self.lblsubtotal.setText('Sub Total: PHP ' +str(self.subtotal))
        promoname = self.lblpromo.text().replace('Promo: ', '')


        # PALITAN NG PROMO ID INSTED #################################################################
        try:
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT value FROM promo WHERE promo_name = %s"""
            cursor.execute(command, promoname)
            records = cursor.fetchall()
            val=records[0][0]
            self.lblpromo_val.setText(str(val) + '% OFF')
            self.promoval = int(val)
        except:
            self.promoval=0; self.lblpromo_val.setText('')


        discounted_amount=self.subtotal * (self.promoval / 100)
        self.grandtotal=self.subtotal - discounted_amount
        self.lbltotal.setText('Total: PHP '+str(self.grandtotal)); self.txtgrandtotal.setText('PHP '+str(self.grandtotal))



        self.clear_fields(self.check_out_fields)
        self.btnProceedPaymanet.setEnabled(False); self.btnCoutCancel.setEnabled(False)
        self.btnpaycash.setEnabled(True); self.btnpayexit.setEnabled(False); self.btnpayprint.setEnabled(False)
        self.btnExit1.setEnabled(False); self.btnExit2.setEnabled(False)

    def pay_proceed(self):
        if self.txtcash.text().replace(' ','') == '':
            self.showDialog('Enter the amount of cash to proceed!')
        else:
            number=int(self.txtcash.text().replace(' ',''))
            if isinstance(number, int):
                cash = float(number)
            if cash < self.grandtotal:
                self.showDialog('Not enough cash!')
            else:
                change=cash-self.grandtotal
                self.txtcash.setText('PHP '+str(cash))

                self.txtchange.setText('PHP '+str(change))
                self.btnpaycash.setEnabled(False)
                self.btnpayexit.setEnabled(True); self.btnpayprint.setEnabled(True)



    def checkout_page(self):
        self.txtRFIDscanout.setFocus()
        self.txtOpromo.hide()
        lbls=['txtOid', 'txtOfname', 'txtOlname', 'txtOroomno', 'txtOstay', 'txtOcindate', 'txtOcintime', 'txtOcoutdate', 'txtOcouttime', 'txtOpromo', 'txtOrate']
        for label_name in lbls:
            label = getattr(self, label_name); label.setText('')

    def checkin_page(self):
        self.txtrfidcheckin.setFocus()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            current_index = self.stackedWidget.currentIndex()
            if current_index == 2 and self.btnRFIDenter.isHidden():
                self.rfid_checkin()
            elif current_index == 3 and self.btnRFIDout.isHidden():
                self.rfid_checkout()
            else:
                pass

    def rfid_checkout(self):
        try:
            data_list=[]; fields_list=['txtOid', 'txtOfname', 'txtOlname', 'txtOroomno', 'txtOcindate', 'txtOcintime']
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT client_id, first_name, last_name, room_no, checkin_date, checkin_time, promo, room_rate FROM clients WHERE rfid_no = %s"""
            cursor.execute(command, self.txtRFIDscanout.text())
            records = cursor.fetchall()
            for data in records:
                data_list.extend(data)
            for f in range(5):
                if f == 0:
                    getattr(self, fields_list[f]).setText(str('HMS-23-0'+data_list[f]))
                elif f == 3:
                    getattr(self, fields_list[f]).setText(str('RM-0' + data_list[f]))
                else:
                    getattr(self, fields_list[f]).setText(str(data_list[f]))
            self.txtOpromo.show(); self.txtOpromo.setText(data_list[6]); self.txtOpromo.hide()
            self.txtOrate.show(); self.txtOrate.setText('PHP '+str(data_list[7])); self.txtOrate.hide()
            self.length_of_stay=0; self.totalcharge=0
            self.checkin_datetime=data_list[4] + ' ' + data_list[5]; self.txtOcintime.setText(data_list[5])
            import datetime
            today = datetime.date.today()
            self.checkout_datetime = today.strftime("%m/%d/%Y") + ' ' + self.lblTime.text()
            self.compute_length_of_stay()
            self.txtOstay.setText(self.total_length_stay); self.txtOcoutdate.setText(today.strftime("%m/%d/%Y")); self.txtOcouttime.setText(self.lblTime.text())
            self.data_value = (today.strftime("%m/%d/%Y"), self.lblTime.text(), self.total_length_stay, self.txtRFIDscanout.text())
            self.to_check_out=self.txtRFIDscanout.text()
            self.btnProceedPaymanet.setEnabled(True); self.btnCoutCancel.setEnabled(True)
            self.check_out_fields=fields_list; self.check_out_fields.extend(['txtOstay','txtOcoutdate', 'txtOcouttime'])
            self.txtRFIDscanout.setText('')
        except:
            self.showDialog('RFID Card is not registered!'); self.txtRFIDscanout.setText('')

    def compute_length_of_stay(self):
        from datetime import datetime
        datetime_format = "%m/%d/%Y %I:%M:%S %p"
        checkin_datetime = datetime.strptime(self.checkin_datetime, datetime_format)
        checkout_datetime = datetime.strptime(self.checkout_datetime, datetime_format)
        time_diff = checkout_datetime - checkin_datetime

        total_seconds_passed = time_diff.total_seconds()
        total_hours_passed = int(total_seconds_passed // 3600)
        total_minutes_passed = int((total_seconds_passed % 3600) // 60)

        if total_hours_passed == 0:
            self.total_length_stay = f"{total_minutes_passed}m"
        else:
            self.total_length_stay = f"{total_hours_passed}h"

    def rfid_checkin(self):
        if self.txtrfidcheckin.text() == '':
            pass
        else:
            try:
                connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
                cursor = connection.cursor()
                command = """SELECT status FROM clients WHERE rfid_no = %s"""
                cursor.execute(command, self.txtrfidcheckin.text())
                records = cursor.fetchall()
                val = records[0][0]
                print(val)
                if val == 'Check in':
                    self.showDialog('Already Checked in!')
                elif val == 'New':
                    today = date.today()
                    timenow=self.lblTime.text(); datenow = today.strftime("%m/%d/%Y")
                    query = """UPDATE clients SET checkin_date = %s, checkin_time = %s, status = %s WHERE rfid_no = %s;"""
                    data_value = (datenow, timenow, 'Check in', self.txtrfidcheckin.text())
                    self.exec_query(query, data_value)
                    self.showDialog('Checked in succesfully!')
                    QTimer.singleShot(100, lambda: self.show_checkin_tbl())
                else:
                    self.showDialog('Client RFID not registered!')
                self.txtrfidcheckin.setText('')
            except:
                self.showDialog('Client RFID not registered!'); self.txtrfidcheckin.setText('')

    def show_checkin_tbl(self):
        self.setup_checkin_tbl()
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT client_id, first_name, last_name, room_no, checkin_date, checkin_time FROM clients WHERE status = 'Check in' ORDER BY CAST(client_id AS SIGNED) ASC"
        cursor.execute(command)
        records = cursor.fetchall()
        if len(records) == 0:
            self.tblCheckin.setItem(1, 0, QtWidgets.QTableWidgetItem("No clients yet"))
        else:
            for row in records:
                currentRowCount = self.tblCheckin.rowCount()
                self.tblCheckin.insertRow(currentRowCount)
                self.tblCheckin.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('HMS-23-0' + str(row[0])))
                self.tblCheckin.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1]))); self.tblCheckin.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2]))); self.tblCheckin.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem('RM-0' + str(row[3])))
                self.tblCheckin.setItem(currentRowCount - 1, 4, QtWidgets.QTableWidgetItem(str(row[4]))); self.tblCheckin.setItem(currentRowCount - 1, 5, QtWidgets.QTableWidgetItem(str(row[5])))

    def setup_checkin_tbl(self):
        self.tblCheckin.clear()
        self.tblCheckin.setRowCount(2); self.tblCheckin.setColumnCount(6)
        self.tblCheckin.setItem(0, 0, QtWidgets.QTableWidgetItem('Client ID')); self.tblCheckin.setItem(0, 1, QtWidgets.QTableWidgetItem('First Name')); self.tblCheckin.setItem(0, 2, QtWidgets.QTableWidgetItem('Last Name'))
        self.tblCheckin.setItem(0, 3, QtWidgets.QTableWidgetItem('Room No.')); self.tblCheckin.setItem(0, 4, QtWidgets.QTableWidgetItem('Check in Date')); self.tblCheckin.setItem(0, 5, QtWidgets.QTableWidgetItem('Check in Time'))

    def edit_client_info(self):
        try:
            data_value = self.tblClientInfo.item(self.tblClientInfo.currentRow(), 0).text().replace('HMS-23-0', '')
            self.SWClient.setCurrentIndex(1); self.lblClientPage.setText('Edit Client Details')
            self.edit_data_list = []
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT client_id, first_name, last_name, id_type, id_number, contact_no, room_type, room_no, room_rate, promo, rfid_no FROM clients WHERE client_id = %s"""
            cursor.execute(command, data_value)
            records = cursor.fetchall()
            for data in records:
                self.edit_data_list.extend(data)
            self.txtCid.setText('HMS-23-0'+self.edit_data_list[0]); self.txtCfirstname.setText(self.edit_data_list[1]); self.txtClastname.setText(self.edit_data_list[2]); self.cboCidtype.setCurrentText(self.edit_data_list[3]); self.txtCidnum.setText(self.edit_data_list[4]), self.txtCcontactno.setText(self.edit_data_list[5])
            self.cboCroomtype.setCurrentText(self.edit_data_list[6]); self.cboCroomno.addItem('RM-0'+str(self.edit_data_list[7])); self.txtroomrate.setText(self.edit_data_list[8]); self.cboCpromos.setCurrentText(self.edit_data_list[9]); self.txtCrfidNo.setText(self.edit_data_list[10])
        except:
            self.showDialog('Please select from table first!')

    def update_cboCroomno_items(self):
        if self.SWClient.currentIndex() == 2:
            if self.lblClientPage.text() == 'Add New Client':
                if self.cboCroomtype.currentText() == '':
                    self.cboCroomno.clear()
            elif self.lblClientPage.text() == 'Edit Client Details':
                self.cboCroomno.addItem('RM-0'+str(self.edit_data_list[7]))
            data_list=[]
            selected_item = self.cboCroomtype.currentText()
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = """SELECT room_number FROM rooms WHERE room_type = %s AND Status = 'Available' ORDER BY CAST(room_number AS SIGNED) ASC"""
            cursor.execute(command, selected_item)
            records = cursor.fetchall()
            data_list.extend('RM-0' + str(data[0]) for data in records)
            if len(data_list) == 0:
                self.cboCroomno.clear(); self.cboCroomno.addItem('No available room right now')
            else:
                self.cboCroomno.clear(); self.cboCroomno.addItems(data_list)
            try:
                command = """SELECT rate FROM room_info WHERE type = %s"""
                cursor.execute(command, selected_item)
                records = cursor.fetchall()
                val = records[0][0]
                self.txtroomrate.setText(str(val))
            except:
                pass

    def add_new_client(self):
        try:
            connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
            cursor = connection.cursor()
            command = "SELECT MAX(CAST(client_id AS SIGNED)) FROM clients"
            cursor.execute(command)
            records = cursor.fetchall()
            val = records[0][0]
            client_id_no=val+1
            self.txtCid.setText('HMS-23-0' + str(int(client_id_no)))
        except:
            self.txtCid.setText('HMS-23-0' + str(1))
        self.SWClient.setCurrentIndex(1); self.lblClientPage.setText('Add New Client')

    def add_client_back(self):
        self.clear_fields(self.inputs_personal); self.clear_fields(self.inputs_room); self.back_to_normal(self.inputs_personal); self.back_to_normal(self.inputs_room)
        self.SWClient.setCurrentIndex(0); self.show_clientinfo_table(); self.cboCroomtype.setCurrentIndex(0); self.cboCroomno.clear()

    def add_client_next(self):
        self.c_personal_input = [self.txtCid.text(), self.txtCfirstname.text().replace(" ", ""), self.txtClastname.text().replace(" ", ""), self.cboCidtype.currentText().replace(' ',''), self.txtCidnum.text().replace(" ", ""), self.txtCcontactno.text().replace(' ','')]
        if '' in self.c_personal_input:
            self.showDialog('Please fill out all the fields!'); self.red_mark(self.inputs_personal)
        else:
            self.lblC2.setText(self.lblClientPage.text()); self.back_to_normal(self.inputs_personal); self.SWClient.setCurrentIndex(2)
        #VALIDATION SA FIELDS ======================================================

    def addclient_roomback(self):
        self.SWClient.setCurrentIndex(1)

    def add_client_proceed(self):
        self.c_room_input = [self.cboCroomtype.currentText(), self.cboCroomno.currentText(), self.txtroomrate.text().replace(" ", ""), self.txtCrfidNo.text().replace(" ", "")]
        if '' in self.c_room_input:
            self.showDialog('Please fill out all the fields!'); self.red_mark(self.inputs_room)
        else:
            if self.cboCroomno.currentText() == 'No available room right now':
                self.showDialog('Choose an available room to proceed')
            else:
                promo_holder=''
                if self.cboCpromos.currentText() != 'No Available Promo':
                    promo_holder=self.cboCpromos.currentText()
                self.back_to_normal(self.inputs_room); self.back_to_normal(self.inputs_personal)
                self.c_personal_input = [self.txtCid.text(), self.txtCfirstname.text(), self.txtClastname.text(), self.cboCidtype.currentText(), self.txtCidnum.text(), self.txtCcontactno.text()]
                self.c_room_input = [self.cboCroomtype.currentText(), self.cboCroomno.currentText(), self.txtroomrate.text(), promo_holder, self.txtCrfidNo.text()]
                self.widget = uic.loadUi('AddClient.ui')
                self.all_info=self.c_personal_input+self.c_room_input
                fields = ['txtWcid', 'txtWfirstname', 'txtWlastname', 'txtWidtype', 'txtWidno', 'txtWcontactno', 'txtWroomtype','txtWroomno', 'txtWrromrate', 'txtWpromo', 'txtWrfidno']
                for f in range(len(fields)):
                    field_name = fields[f]
                    field_object = getattr(self.widget, field_name)
                    field_object.setText(self.all_info[f])
                self.widget.btnACsubmit.clicked.connect(self.client_added)
                self.widget.show()


    def client_added(self):
        self.widget.close()
        #ADD MO SI FUCKING ADDITIONAL D2
        if self.lblClientPage.text() == 'Add New Client':
            query = """INSERT INTO clients(client_id,first_name,last_name,id_type,id_number,contact_no,room_type,room_no,room_rate,promo,rfid_no,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); """
            self.data_value = (self.all_info[0].replace('HMS-23-0', ''), self.all_info[1], self.all_info[2], self.all_info[3], self.all_info[4], self.all_info[5], self.all_info[6], self.all_info[7].replace('RM-0', ''), self.all_info[8], self.all_info[9], self.all_info[10], 'New')
            text='New Client Added!'
        else:
            query = """UPDATE clients SET first_name = %s, last_name = %s, id_type = %s, id_number = %s, contact_no = %s, room_type = %s, room_no = %s, room_rate = %s, promo = %s, rfid_no = %s, status = %s WHERE client_id = %s;"""
            self.data_value = (self.all_info[1], self.all_info[2], self.all_info[3], self.all_info[4], self.all_info[5], self.all_info[6], self.all_info[7].replace('RM-0', ''), self.all_info[8], self.all_info[9], self.all_info[10], 'New', self.all_info[0].replace('HMS-23-0', ''))
            text='Changes Saved!'
        self.exec_query(query, self.data_value)
        self.add_client_back()
        QTimer.singleShot(300, lambda: self.showDialog(text))
        self.show_clientinfo_table()

    def del_client(self):
        try:
            self.client_deleter = None
            self.widget = uic.loadUi('DialogQuestion.ui')
            self.client_deleter = self.tblClientInfo.item(self.tblClientInfo.currentRow(), 0).text()
            self.widget.txtQuestion.setText('Are you sure you want to remove ' + self.client_deleter + '?')
            self.widget.btnDelete.clicked.connect(self.del_client_proceed)
            self.widget.show()
        except:
            self.showDialog('Select client from table first!')

    def del_client_proceed(self):
        self.widget.close()
        deleter = self.client_deleter.replace('HMS-23-0', '')
        query = """UPDATE clients SET status = 'removed' WHERE client_id = %s;"""
        self.exec_query(query, deleter)
        self.show_clientinfo_table()
        text = self.client_deleter + ' removed!'
        QTimer.singleShot(300, lambda: self.showDialog(text)); self.client_deleter = None

    def show_clientinfo_table(self):
        self.setup_clientinfo_tbl()
        connection = pymysql.connect(host="localhost", port=3308, user="miki", password="miki", database="hotel")
        cursor = connection.cursor()
        command = "SELECT client_id, first_name, last_name, rfid_no FROM clients WHERE status = 'New' ORDER BY CAST(client_id AS SIGNED) ASC"
        cursor.execute(command)
        records = cursor.fetchall()
        if len(records) == 0:
            self.tblClientInfo.setItem(1, 0, QtWidgets.QTableWidgetItem("No clients yet"))
        else:
            for row in records:
                currentRowCount = self.tblClientInfo.rowCount()
                self.tblClientInfo.insertRow(currentRowCount)
                self.tblClientInfo.setItem(currentRowCount - 1, 0, QtWidgets.QTableWidgetItem('HMS-23-0' + str(row[0])))
                self.tblClientInfo.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(row[1]))); self.tblClientInfo.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(row[2]))); self.tblClientInfo.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem(str(row[3])))

    def setup_clientinfo_tbl(self):
        self.tblClientInfo.clear()
        self.tblClientInfo.setRowCount(2); self.tblClientInfo.setColumnCount(4)
        self.tblClientInfo.setItem(0, 0, QtWidgets.QTableWidgetItem('Client ID')); self.tblClientInfo.setItem(0, 1, QtWidgets.QTableWidgetItem('First Name')); self.tblClientInfo.setItem(0, 2, QtWidgets.QTableWidgetItem('Last Name')); self.tblClientInfo.setItem(0, 3, QtWidgets.QTableWidgetItem('RFID Card Number'))






app = QtWidgets.QApplication(sys.argv)
#Loading style file
with open("style.qss", "r") as style_file:
    style_str = style_file.read()
app.setStyleSheet(style_str)
Window = Hotel()
app.exec_()