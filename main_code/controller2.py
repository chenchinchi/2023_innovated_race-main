from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from login_page import Login_page
from main_page import MainPage
import datetime
import csv
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class main_page_controller(QtWidgets.QWidget):
    def __init__(self):
        self.user_account = "None" #default user account
        #讀取價目表（.csv格式）
        price =pd.read_csv('price.csv', header=None, index_col=0,).to_dict()
        self.price = price[1]
        super().__init__()
        self.timer = QtCore.QTimer()#啟動資料更新計時器
        self.timer.start(500)
        self.main = MainPage() #定義ui
        self.main.setupUi(self)
        self.setup_control_main() #定義控制元件
        
    ## 事件宣告
    def setup_control_main(self):
        self.timer.timeout.connect(self.update)
        self.main.login_button.clicked.connect(self.login)
        self.main.pay_button.clicked.connect(self.pay)
        self.main.cancel_button.clicked.connect(self.cancel)
        pass

    def pay(self):#sent email
        
        content = MIMEMultipart()  #建立MIMEMultipart物件
        content["subject"] =  str(datetime.datetime.today())[:10] #郵件標題
        content["from"] = "t109810022@gmail.com"  #寄件者
        content["to"] = str(self.account) #self.account #收件者 
        content.attach(MIMEText(str(self.invoice)))  #郵件內容
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("t109810022@gmail.com", "vcilwxiizhbwtgps")  # 登入寄件者gmail
                smtp.send_message(content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
        self.close()
        

    def login(self):
        self.login_page = login_page_controller()
        self.login_page.show()
        self.login_page.login.pushButton.clicked.connect(self.send_account)

    def cancel(self):
        self.close()
        print("please return the cart to the counter")
        pass

    def update(self):
        self.main.time.setText(str(datetime.datetime.today())[:-5]) #時間顯示
        ## 讀取動態，獲取放入或取出動作，以計算商品在購物車的數量
        with open("action.csv", "r") as csvfile:
            shopping_list = {}
            rows = csv.reader(csvfile)
            rows = list(rows)
            #將商品數量做統計-->字典方式儲存
            for row in rows[1:]:
                if row[-1] not in shopping_list:
                    shopping_list[row[-1]] = 1
                else:
                    shopping_list[row[-1]] = shopping_list[row[-1]]+int(row[1])
        #將統計好的字典分別輸出至table上
        shopping_list = {key: value for key, value in shopping_list.items() if value != 0}
        self.main.table.setRowCount(len(shopping_list))
        need_to_pay = 0
        for r,item in enumerate(shopping_list):
            if shopping_list[item] !=0:
                newItem = QTableWidgetItem(item)
                self.main.table.setItem(r, 0, newItem)
                newitem = QTableWidgetItem(str(shopping_list[item]))
                self.main.table.setItem(r, 1, newitem)
                price = QTableWidgetItem(str(self.price[item]))
                self.main.table.setItem(r, 2, price)
                total = QTableWidgetItem(str(self.price[item]*shopping_list[item]))
                self.main.table.setItem(r, 3, total)
                need_to_pay = need_to_pay+self.price[item]*shopping_list[item]
        self.main.price.setText("total price :  "+ str(need_to_pay))
        self.invoice = shopping_list


    ##子視窗功能
    def send_account(self):
        self.account = self.login_page.login.account_getter.toPlainText()
        self.login_page.close()
        self.main.welcome.setText("welcome!    "+self.account)

class login_page_controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login = Login_page()
        self.login.setup_login_Ui(self)
        self.setup_control_login()

    def setup_control_login(self):
        self.login.pushButton.clicked.connect(self.close)
