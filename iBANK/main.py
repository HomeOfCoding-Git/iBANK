"""
iBANK
Author @Home Of Coding

There are over 100 print statements to help better understand the code..
Please remove this block of text for the print lines to match up.

Replace all exceptions with pass, example:
except:
    pass

Please add a gmail address and password in the..
Email_DB directory / file is connect.py
"""
from tkinter import *
from tkinter import END
from tkinter import messagebox
import os
import random
import sqlite3 as sq
# -- Email --
import smtplib
from email.message import EmailMessage
from Email_DB import connect

# App Defaults _____________________
app_size = '600x440'
splash_file = 'img/bank-splash.png'
# Frames __________
app_bg = '#185185'
main_bg = '#296296'
header_bg = '#296296'
# Foregrounds _____
main_fg = '#fff'
header_fg = '#fff'
footer_fg = '#fff'
# Backgrounds _____
footer_bg = '#396396'
check_btn_bg = '#269269'
# Fonts ___________
header_font = 'arial, bold', 14
error_font = 'arial, bold', 14
# Amount and Pin Buttons and Some Labels
A12 = 'arial, 12'
# Footer Button and Check Button Fonts
fbf = 'arial, bold', 12
cbf = 'arial', 11
# END: App Defaults ________________

# app = Tk()
def main():
    print('def main: Line 37')

    app = Tk()
    gui = Main(app)
    gui.app.mainloop()


class Main:
    print('Class Main: Line 45')

    def __init__(self, win):
        print('def __init__: Line 48')

        # Window Defaults
        self.app = win
        self.app.title('iBANK')
        self.app.geometry(app_size)
        self.app.resizable(False, False)
        self.app.configure(bg=app_bg)

        # Database
        dir_name = 'DB/'
        if dir_name != os.path.basename(dir_name):
            try:
                os.mkdir(dir_name)
            except:
                None
        
        self.DATABASE = 'DB/contacts_data.db'
        self.conn = ''
        self.cur = ''
        # _______________________________________

        # Getters
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.user_name = StringVar()
        self.email_addr = StringVar()
        # Emailed Unique Pin Number
        self.email_pin_num = StringVar()

        # Globals
        self.pin = ''
        self.get_user = ''
        self.get_pin = ''
        self.number = ''
        self.amount_in = ''
        self.amount_out = ''
        self.get_amount_in = ''
        self.get_amount_out = ''
        self.email_input = ''
        self.unique_pin = ''
        self.balance = ''
        self.new_balance = ''
        
        self.left_frame1 = Frame()
        self.left_frame2 = Frame()
        self.right_frame1 = Frame()
        self.right_frame2 = Frame()
        self.header_frame = Frame()
        self.form_frame1 = Frame()
        self.form_frame2 = Frame()
        self.form_frame3 = Frame()
        self.form_frame4 = Frame()
        self.form_frame5 = Frame()
        # New Account Form (input errors)
        self.error_frame = Frame()
        self.check_btn = Button()

        # _________________________________
        # Top: Home Screen
        print('Home Screen: Line 109')

        self.main_frame = Frame(self.app, bg=main_bg)
        self.main_frame.pack(expand=True)

        # Splash Image (Home Screen)
        self.photo = PhotoImage(file=splash_file)
        self.photo_image = Label(self.main_frame, image=self.photo, border=0)
        self.photo_image.pack()
        self.photo_image.bind('<Button-1>', self.get_coordinates)

        # _________________________________
        # Footer: Buttons Frame
        
        self.buttons_frame = Frame(self.app)
        self.buttons_frame.pack(side='bottom', fill='x')
        
        # In Footer: Login Button
        self.footer_btn = Button(self.buttons_frame, text='Login', bg=footer_bg, fg=footer_fg, \
                           font=fbf, relief='flat', cursor='hand2', command=self.user_login)
        self.footer_btn.pack(fill='x', ipadx=5, ipady=8)

    # ======================================================================================
    # Go Back to Home Screen from Login Page
    # Go Back to Home Screen from Create Account Page
    
    def home(self):
        print('def home: Line 135')

        # Remove Frames
        self.refresh()

        # Show the Home Screen
        self.main_frame = Frame(self.app)
        self.main_frame.pack(expand=True)

        # Show Home Page Image
        self.photo = PhotoImage(file=splash_file)
        self.photo_image = Label(self.main_frame, image=self.photo, border=0)
        self.photo_image.pack()
        self.photo_image.bind('<Button-1>', self.get_coordinates)

        # In Footer: Change back to login button
        self.footer_btn['text'] = 'Login'
        self.footer_btn['command'] = self.user_login
    
    # ======================================================================================
    # Refresh Screen
    
    def refresh(self):
        print('def refresh: Line 158')

        self.photo_image.destroy()
        self.header_frame.destroy()
        self.error_frame.destroy()
        self.form_frame1.destroy()
        self.form_frame2.destroy()
        self.form_frame3.destroy()
        self.form_frame4.destroy()
        self.form_frame5.destroy()
        self.left_frame1.destroy()
        self.left_frame2.destroy()
        self.right_frame1.destroy()
        self.right_frame2.destroy()
        self.main_frame.destroy()
        self.balance = ''

    # ======================================================================================
    # Update Balance
    
    def update_balance(self):
        print('def deposit_balance: Line 179')

        try:
            self.conn = sq.connect(self.DATABASE)
            self.cur = self.conn.cursor()

            with self.conn:
                print('\nCheck if monies in account\nwhen pressing the check balance button\n--------')
                self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                 (self.get_user, self.get_pin))
                checking = self.cur.fetchone()
                for checking_balance in checking:
                    if checking_balance == '0' or checking_balance == '0':
                        self.amount_label.config(text='Current Balance\n\n£0', fg=main_fg)
                        print('1: £' + checking_balance)
                    else:
                        self.balance = checking_balance
                        self.amount_label.config(text='Current Balance\n\n£' + str(self.balance), fg=main_fg)
                        print('2: £' + self.balance)


            # Close Database
            self.conn.close()

        except Exception as e:
            print(str(e))
        except sq.OperationalError as soe:
            self.conn.close()
            print('Database Issues:\n' + str(soe))

        self.check_btn.config(text='', bg=main_bg, state='disabled')
        print('\nNew Balance', self.balance)

    # ======================================================================================
    # Get amount value from the lambda button function (def monies_screen)
    
    def btn_amount(self, amount):
        print('def btn_amount: Line 216')

        self.amount_btn1.config(state=DISABLED)
        self.amount_btn2.config(state=DISABLED)
        self.amount_btn3.config(state=DISABLED)
        self.amount_btn4.config(state=DISABLED)
        self.amount_btn5.config(state=DISABLED)
        self.amount_btn6.config(state=DISABLED)

        self.amount_btn7.config(state=DISABLED)
        self.amount_btn8.config(state=DISABLED)
        self.amount_btn9.config(state=DISABLED)
        self.amount_btn10.config(state=DISABLED)
        self.amount_btn11.config(state=DISABLED)
        self.amount_btn12.config(state=DISABLED)

        self.amount_btn13.config(state=DISABLED)
        self.amount_btn14.config(state=DISABLED)
        self.amount_btn15.config(state=DISABLED)
        self.amount_btn16.config(state=DISABLED)
        self.amount_btn17.config(state=DISABLED)
        self.amount_btn18.config(state=DISABLED)

        self.amount_btn19.config(state=DISABLED)
        self.amount_btn20.config(state=DISABLED)
        self.amount_btn21.config(state=DISABLED)
        self.amount_btn22.config(state=DISABLED)
        self.amount_btn23.config(state=DISABLED)
        self.amount_btn24.config(state=DISABLED)

        self.get_amount_in = self.get_amount_in + str(amount)
        self.get_amount_out = self.get_amount_out + str(amount)

        self.amount_label.config(text='', fg=main_fg)

        self.deposit_btn.config(text='DEPOSIT', bg=check_btn_bg, state='normal')
        self.withdraw_btn.config(text='WITHDRAW', bg='#e23e23', state='normal')
    
    # ======================================================================================
    # Deposit
    
    def deposit_amount(self):
        print('def deposit_amount: Line 258')

        self.deposit_btn.config(text='', bg=main_bg, state='disabled')
        self.withdraw_btn.config(text='', bg=main_bg, state='disabled')

        try:
            self.conn = sq.connect(self.DATABASE)
            self.cur = self.conn.cursor()

            with self.conn:
                print('\nFIRST DEPOSIT SELECTED\n--------')
                self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                 (self.get_user, self.get_pin))
                item = self.cur.fetchone()
                for get_item in item:
                    if get_item == '':
                        self.balance = self.get_amount_in
                        
                        with self.conn:
                            print('\n1: Inserting first deposit update into database!')
                            self.cur.execute("UPDATE ibank SET deposit=?, balance=? WHERE username=? AND pin=?", \
                                             (self.get_amount_in, self.balance, self.get_user, self.get_pin))
                            self.conn.commit()


                        self.amount_label.config(text='DEPOSITING\n\n£' + self.get_amount_in, fg=main_fg)
                        self.check_btn.config(\
                            text='Check Balance', bg=check_btn_bg, state='normal', command=self.update_balance)

                        print('\nAdded ' + str(self.get_amount_in))
                        print('\nNew Balance ' + str(self.balance))

                    else:
                        with self.conn:
                            self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                     (self.get_user, self.get_pin))
                            items = self.cur.fetchone()
                            
                            for update_item in items:
                                print('\nUPDATE DEPOSIT SELECTED\n--------')
                                print('1: Get deposit from database £' + str(update_item))
                                update_item = int(update_item)
                                update_item = int(update_item) + int(self.get_amount_in)
                                print('2: Get added items: £', update_item)
                                self.get_amount_in = str(self.get_amount_in)
                                display_amount = self.get_amount_in
                                print('\n1: Added ' + display_amount)
                                self.get_amount_in = str(update_item)
                                self.balance = int()
                                self.balance = int(self.balance) + int(self.get_amount_in)
                                print('\nself.balance = £' + str(self.balance))
                                self.balance = str(self.balance)
                                
                                with self.conn:
                                    print('\n2: Inserting deposit update into database!')
                                    self.cur.execute(\
                                        "UPDATE ibank SET deposit=?, balance=? WHERE username=? AND pin=?", \
                                        (self.get_amount_in, self.balance, self.get_user, self.get_pin))
                                    self.conn.commit()


                                self.amount_label.config(text='DEPOSITING\n\n£' + display_amount, fg=main_fg)
                                self.check_btn.config(\
                                    text='Check Balance', bg=check_btn_bg, state='normal', \
                                    command=self.update_balance)
                        
                        print('\n2: Added ' + display_amount)
                        print('\nNew Balance ' + str(self.balance))
            

            # Close Database
            self.conn.close()

        except Exception as e:
            print(str(e))
        except sq.OperationalError as soe:
            self.conn.close()
            print('Database Issues:\n' + str(soe))

        # Clear the amount, otherwise the next amount..
        # will be added to last input amount
        self.get_amount_in = ''
        self.get_amount_out = ''
        self.balance = ''

    # ======================================================================================
    # Withdrawal
    
    def withdraw_amount(self):
        print('def withdraw_amount: Line 347')
        
        self.deposit_btn.config(text='', bg=main_bg, state='disabled')
        self.withdraw_btn.config(text='', bg=main_bg, state='disabled')

        try:
            self.conn = sq.connect(self.DATABASE)
            self.cur = self.conn.cursor()
            
            amount_out = self.get_amount_out

            with self.conn:
                print('\nCHECKING IF £0 FUNDS SELECTED\n------')
                self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                 (self.get_user, self.get_pin))
                zero_funds = self.cur.fetchone()
                for zero_balance in zero_funds:
                    print('Amount Out: £' + zero_balance)
                    if zero_balance == '' in zero_funds or zero_balance == '0' in zero_funds:
                        self.monies_screen()
                        self.amount_label.config(text='Not enough funds.',
                                                 fg='#e23e23', font=error_font)
            
                    elif zero_balance != '' in zero_funds or zero_balance != '0' in zero_funds:
                        with self.conn:
                            print('\nCHECKING WITHDRAWAL SELECTED\n------')
                            self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                             (self.get_user, self.get_pin))
                            check_balance = self.cur.fetchone()
                            get_balance = int()
                            for get_balance in check_balance:
                                self.get_amount_out = int(self.get_amount_out)
                                print('amount out: ', self.get_amount_out)
                                if self.get_amount_out > int(get_balance):
                                    self.monies_screen()
                                    self.amount_label.config(text='Not enough funds.',
                                                             fg='#e23e23', font=error_font)

                    else:   
                        with self.conn:
                            print('\nUPDATING WITHDRAWAL SELECTED\n------')
                            self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                             (self.get_user, self.get_pin))
                            new_balance = self.cur.fetchone()
                            update_balance = int()
                            for update_balance in new_balance:
                                amount_out = int()
                                amount_out = int(self.get_amount_out)
                                if amount_out > int(update_balance):
                                    self.monies_screen()
                                    self.amount_label.config(text='Not enough funds.',
                                                             fg='#e23e23', font=error_font)

                                else:
                                    print('1: Balance: £', update_balance)
                                    print('Withdrawing: £', amount_out)
                                    update_balance = int(update_balance) - int(amount_out)
                                    print('2: New balance: £', update_balance)
                                    self.get_amount_out = str(self.get_amount_out)
                                    self.get_amount_out = str(amount_out)
                                    self.balance = str(update_balance)
                                    print('\nself.balance = £' + self.balance)
                                    
                                    with self.conn:
                                        print('\nInserting withdraw update into database!')
                                        self.cur.execute(\
                                            "UPDATE ibank SET withdraw=?, balance=? WHERE username=? AND pin=?", \
                                            (self.get_amount_out, self.balance, self.get_user, self.get_pin))
                                        self.conn.commit()


                                    self.amount_label.config(\
                                        text='WITHDRAWAL\n\n£' + self.get_amount_out, fg=main_fg)
                                    self.check_btn.config(\
                                    text='Check Balance', bg=check_btn_bg, state='normal', \
                                    command=self.update_balance)
                                    
                                    print('Balance £' + str(update_balance))
                                    print('\nMinus £' + str(self.get_amount_out))
                                    print('\nNew Balance £' + self.balance)


            # Close Database
            self.conn.close()

        except Exception as e:
            print(str(e))
        except sq.OperationalError as soe:
            self.conn.close()
            print('Database Issues:\n' + str(soe))

        # Clear the amount, otherwise the next amount..
        # will be added to last input amount
        self.get_amount_in = ''
        self.get_amount_out = ''
        self.balance = ''

    # ======================================================================================
    # Deposit Monies Screen
    
    def monies_screen(self):
        print('def deposit_monies: Line 448')
        self.app.configure(bg=main_bg)

        self.refresh()

        # Header Frame (Page Title) ___________________________________________
        self.header_frame = Frame(self.app, bg=header_bg)
        self.header_frame.pack(fill='x')

        # Header Title
        self.header_label = Label(self.header_frame, text='iBANK: Transaction', \
                                       bg=header_bg, fg=header_fg, font=header_font)
        self.header_label.pack(side='left', fill='x', padx=(20, 0), ipady=20)

        try:
            self.conn = sq.connect(self.DATABASE)
            self.cur = self.conn.cursor()

            with self.conn:
                print('\nCHECKING IF £0 FUNDS SELECTED\n------')
                self.cur.execute("SELECT balance FROM ibank WHERE username=? AND pin=?", \
                                 (self.get_user, self.get_pin))
                no_funds = self.cur.fetchone()
                for zero in no_funds:
                    print('Amount Out: £' + zero + '\nHiding Button')
                    if zero == '':
                        # Hide: Check Balance Button
                        print('Hiding "Check Balance" button')
                        self.check_btn = Button(self.header_frame, width=14, text='', relief='flat', \
                                                bg=main_bg, fg=main_fg, state='disabled')
                        self.check_btn.pack(side='right', padx=(0, 14))
                    else:
                        if zero != '':
                            # Show: Check Balance Button
                            print('Showing "Check Balance" button')
                            self.check_btn = Button(self.header_frame, width=14, text='Check Balance', \
                                                    bg='#369369', fg=main_fg, font=cbf, relief='flat', \
                                                    state='normal', command=self.update_balance)
                            self.check_btn.pack(side='right', padx=(0, 14))


            # Close Database
            self.conn.close()

        except Exception as e:
            print(str(e))
        except sq.OperationalError as soe:
            self.conn.close()
            print('Database Issues:\n' + str(soe))

        # ________________________________________________

        # Left Buttons Frame 1 (£ amount)
        self.left_frame1 = Frame(self.app, bg=main_bg)
        self.left_frame1.pack(side='left', fill='both')

        # Left Row Frame 1 (£ amount)
        self.left_row1 = Frame(self.left_frame1, bg=main_bg)
        self.left_row1.pack(fill='both')

        # Left Side Buttons (from 1 to 6)
        # Amount £5
        self.amount_btn1 = Button(self.left_row1, width=8, text='£5', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(5))
        self.amount_btn1.pack(ipady=10)

        # Amount £15
        self.amount_btn2 = Button(self.left_row1, width=8, text='£15', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(15))
        self.amount_btn2.pack(ipady=10)

        # Amount £25
        self.amount_btn3 = Button(self.left_row1, width=8, text='£25', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(25))
        self.amount_btn3.pack(ipady=10)

        # Amount £35
        self.amount_btn4 = Button(self.left_row1, width=8, text='£35', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(35))
        self.amount_btn4.pack(ipady=10)

        # Amount £45
        self.amount_btn5 = Button(self.left_row1, width=8, text='£45', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(45))
        self.amount_btn5.pack(ipady=10)

        # Amount £55
        self.amount_btn6 = Button(self.left_row1, width=8, text='£55', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(55))
        self.amount_btn6.pack(ipady=10)

        # ________________________________________________

        # Left Buttons Frame (£ amount)
        self.left_frame2 = Frame(self.app, bg=main_bg)
        self.left_frame2.pack(side='left', fill='both')

        # Left Row Frame 2 (£ amount)
        self.left_row2 = Frame(self.left_frame2, bg=main_bg)
        self.left_row2.pack(fill='both')

        # Left Side Buttons (from 7 to 12)
        # Amount £10
        self.amount_btn7 = Button(self.left_row2, width=8, text='£10', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(10))
        self.amount_btn7.pack(ipady=10)

        # Amount £20
        self.amount_btn8 = Button(self.left_row2, width=8, text='£20', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(20))
        self.amount_btn8.pack(ipady=10)

        # Amount £30
        self.amount_btn9 = Button(self.left_row2, width=8, text='£30', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(30))
        self.amount_btn9.pack(ipady=10)

        # Amount £40
        self.amount_btn10 = Button(self.left_row2, width=8, text='£40', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(40))
        self.amount_btn10.pack(ipady=10)

        # Amount £50
        self.amount_btn11 = Button(self.left_row2, width=8, text='£50', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(50))
        self.amount_btn11.pack(ipady=10)

        # Amount £60
        self.amount_btn12 = Button(self.left_row2, width=8, text='£60', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(60))
        self.amount_btn12.pack(ipady=10)

        # ________________________________________________

        # Right Buttons Frame 2 (£ amount)
        self.right_frame2 = Frame(self.app, bg=main_bg)
        self.right_frame2.pack(side='right', fill='both')

        # Right Row Frame 2 (£ amount)
        self.right_row2 = Frame(self.right_frame2, bg=main_bg)
        self.right_row2.pack(fill='both')

        # Right Side Buttons (from 19 to 24)
        # Amount £70
        self.amount_btn19 = Button(self.right_row2, width=8, text='£70', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(70))
        self.amount_btn19.pack(ipady=10)

        # Amount £80
        self.amount_btn20 = Button(self.right_row2, width=8, text='£80', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(80))
        self.amount_btn20.pack(ipady=10)

        # Amount £90
        self.amount_btn21 = Button(self.right_row2, width=8, text='£90', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(90))
        self.amount_btn21.pack(ipady=10)

        # Amount £100
        self.amount_btn22 = Button(self.right_row2, width=8, text='£100', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(100))
        self.amount_btn22.pack(ipady=10)

        # Amount £150
        self.amount_btn23 = Button(self.right_row2, width=8, text='£200', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(200))
        self.amount_btn23.pack(ipady=10)

        # Amount £200
        self.amount_btn24 = Button(self.right_row2, width=8, text='£300', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(300))
        self.amount_btn24.pack(ipady=10)

        # ________________________________________________

        # Right Buttons Frame 1 (£ amount)
        self.right_frame1 = Frame(self.app, bg=main_bg)
        self.right_frame1.pack(side='right', fill='both')

        # Right Row Frame 1 (£ amount)
        self.right_row1 = Frame(self.right_frame1, bg=main_bg)
        self.right_row1.pack(fill='both')

        # Right Side Buttons (from 13 to 18)
        # Amount £5
        self.amount_btn13 = Button(self.right_row1, width=8, text='£65', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(65))
        self.amount_btn13.pack(ipady=10)

        # Amount £15
        self.amount_btn14 = Button(self.right_row1, width=8, text='£75', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(75))
        self.amount_btn14.pack(ipady=10)

        # Amount £25
        self.amount_btn15 = Button(self.right_row1, width=8, text='£85', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(85))
        self.amount_btn15.pack(ipady=10)

        # Amount £35
        self.amount_btn16 = Button(self.right_row1, width=8, text='£95', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(95))
        self.amount_btn16.pack(ipady=10)

        # Amount £45
        self.amount_btn17 = Button(self.right_row1, width=8, text='£150', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(150))
        self.amount_btn17.pack(ipady=10)

        # Amount £55
        self.amount_btn18 = Button(self.right_row1, width=8, text='£250', bg=main_bg, fg=main_fg, font=A12, \
                               command=lambda:self.btn_amount(250))
        self.amount_btn18.pack(ipady=10)

        # ________________________________________________

        # Main Frame
        self.main_frame = Frame(self.app, bg=main_bg)
        self.main_frame.pack(fill='both')

        # Main Frame Label (show chosen amount)
        self.amount_label = Label(self.main_frame, text='Choose Amount to\n Deposit or Withdraw', \
                                  bg=main_bg, fg=main_fg, font=('arial, bold', 14))
        self.amount_label.pack(pady=(50, 30))

        # Deposit Button
        self.deposit_btn = Button(self.main_frame, width=14, bg=main_bg, fg=main_fg, font=cbf, \
                                  relief='flat', state='disabled', command=self.deposit_amount)
        self.deposit_btn.pack(pady=(0, 5))

        # Withdraw Button
        self.withdraw_btn = Button(self.main_frame, width=14, bg=main_bg, fg=main_fg, font=cbf, \
                                   relief='flat', state='disabled', command=self.withdraw_amount)
        self.withdraw_btn.pack()

    # ======================================================================================
    # Grab Pin Number..
    # From "existing user" login screen..
    # Check if: (user pin input) MATCHES (database pin for username)
    
    def get_entered_pin(self):
        print('def get_entered_pin: Line 689')

        # If empty username entry field..
        if self.user_name.get() == '':
            self.refresh()
            self.user_login()
        
        # No buttons on keypad pressed except "OK" button
        elif self.pin == '':
            self.refresh()
            self.user_login()

        # Continue to database if correct input data from user
        else:
            try:
                # Store Pin for later (updating balance)
                self.get_user = self.user_name.get()
                self.get_pin = self.pin
                # Connect to Database
                self.conn = sq.connect(self.DATABASE)
                self.cur = self.conn.cursor()
                
                with self.conn:
                    self.cur.execute("SELECT * FROM ibank WHERE username=? AND pin=?", \
                                     (self.user_name.get(), self.pin,))
                    rows = self.cur.fetchall()
                    
                    for row in rows:
                        if self.user_name.get() not in row and self.pin not in row:
                            print('No Match')
                            print('User: ', self.user_name.get())
                            print('Unique Pin: ', self.pin)
                            self.pin = ''
                            self.refresh()
                            self.user_login()

                        else:
                            if self.user_name.get() in row and self.pin in row:
                                print('MATCHED')
                                print('User: ', self.user_name.get())
                                print('Unique Pin: ', self.pin)
                                self.pin = ''
                                self.refresh()
                                self.monies_screen()

                self.conn.close()
                self.pin = ''
            
            except Exception as e:
                self.conn.close()
                print(str(e))
    
    # ======================================================================================
    # From Login Page (account already exists here)
    # Gather individual button values from user: pin number (4 digits)
    
    def get_btn_data(self, number):
        print('def get_btn_data: Line 746')
        
        self.pin = (self.pin + str(number))

    # ======================================================================================
    # Email Log In
    
    def email_login(self):
        print('def email_login: Line 754\n(getting email pin number)')

        # Refresh Page
        self.refresh()
        
        # Header Frame (Page Title) ___________________________________________
        self.header_frame = Frame(self.app, bg=header_bg)
        self.header_frame.pack(fill='x')

        # Header Title
        self.header_label = Label(self.header_frame, text='iBANK: Login', \
                                       bg=header_bg, fg=header_fg, font=('arial, bold', 14))
        self.header_label.pack(side='left', fill='x', padx=(20, 0), ipady=20)

        # Main Frame
        self.main_frame = Frame(self.app, bg=main_fg)
        self.main_frame.pack(pady=(68, 0))

        # Message Label (Enter your new pin number from emil)
        self.msg_label = Label(self.main_frame, text='iBANK:\nCheck your emails for pin number', \
                                       justify='center', bg=main_fg, fg=main_bg, font=('arial, bold', 11))
        self.msg_label.pack(pady=(0, 20))

        # Getter
        self.email_pin_num = StringVar()

        # Entry Field (pin number from email)
        self.email_pin_entry = Entry(self.main_frame, width=22, bg=main_fg, fg=main_bg, \
                            font=('arial', 14), textvariable=self.email_pin_num)
        self.email_pin_entry.focus()
        self.email_pin_entry.pack(side='left', ipady=4)

        # Submit Button
        self.pin_sub_btn = Button(self.main_frame, text='Submit', bg=main_bg, fg=main_fg, \
                            font=A12, relief='flat', command=self.pin_submit_data)
        self.app.bind('<Return>', self.pin_submit_data)
        self.pin_sub_btn.pack(anchor='e')

    # ======================================================================================
    # Stored Email Pin Number Data
    
    def pin_submit_data(self, *args):
        print('def pin_submit_data: Line 796')

        # No Input from user
        if self.email_pin_num.get() == '':
            self.email_pin_num.set('')
            self.email_login()
            print('No Pin data')
        elif self.email_pin_num.get() != '':
            self.email_pin_num.get()

            # ****  QUERY DATABASE HERE FOR EMAIL PIN MATCH ****
            try:
                # Connect to Database
                self.conn = sq.connect(self.DATABASE)
                self.cur = self.conn.cursor()
                
                with self.conn:
                    self.cur.execute("SELECT * FROM ibank WHERE pin=?", (self.unique_pin,))
                    rows = self.cur.fetchall()
                    
                    for row in rows:
                        if self.email_pin_num.get() not in row:
                            print('No Pin Match')
                            print('Input Pin: ', self.email_pin_num.get())
                            print('Unique Pin: ', self.unique_pin)
                            self.email_login()

                        else:
                            if self.email_pin_num.get() in row:
                                print('PIN MATCHED')
                                print('Input Pin: ', self.email_pin_num.get())
                                print('Unique Pin: ', self.unique_pin)
                                self.refresh()
                                self.email_pin_num.set('')
                                self.user_login()
                
            
            except Exception as e:
                self.conn.close()
                print(str(e))
        
        else:
            print('String not valid')
            self.email_pin_num.set('')
            self.email_login()

    # ======================================================================================
    # Stored New Account Form Data
    
    def submit_data(self, *args):
        print('def submit_data: Line 846\n')

        # If empty fields..
        if self.first_name.get() == '':
            self.error_msg.config(text='Please enter first name.')
            self.entry_first.focus()
        elif self.last_name.get() == '':
            self.error_msg.config(text='Please enter last name.')
            self.entry_last.focus()
        elif self.user_name.get() == '':
            self.error_msg.config(text='Please enter username.')
            self.entry_user.focus()
        elif self.email_addr.get() == '':
            self.error_frame.pack(padx=(24, 0))
            self.error_msg.config(text='Please enter email address.')
            self.entry_email.focus()
        
        # else Regex email verification here
        # Checking for Regular Expressions (regex)
        # Text and numbers @symble .com
        # [text-nums][.-][nums-text-nums][@][text-nums][.][com] or [.][co.uk] or [.][other]
        else:
            self.email_input = self.email_addr.get()
            pattern = re.compile(r"^[a-zA-Z0-9]+([a-zA-Z0-9]+[\.-]"\
                                 "[a-zA-Z0-9]+)?@([a-zA-Z0-9\d-])"\
                                 "+\.([a-zA-Z]{2,15})(\.[a-zA-Z]{2,8})?$")
            matches = pattern.search(self.email_input)

            # Email Address is Valid
            if matches:
                # Clear error message field
                self.error_msg.config(text='')
                print('\nBefore DB: ' + self.email_input)

                # Connect to Database
                self.conn = sq.connect(self.DATABASE)
                self.cur = self.conn.cursor()
                
                try:
                    with self.conn:
                        self.cur.execute(""" CREATE TABLE IF NOT EXISTS ibank (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        first TEXT,
                        last TEXT,
                        username TEXT,
                        email TEXT,
                        pin TEXT,
                        deposit TEXT,
                        withdraw TEXT,
                        balance TEXT)""")
                
                
                    # Generate a random pin here (for user to log in with).
                    # Generate 4 random digits, example: 2736
                    self.unique_pin = random.randrange(1000, 9999)
                    print(self.unique_pin)

                    # If database is empty, add first user (no checks required)
                    with self.conn:
                        self.cur.execute("SELECT pin FROM ibank")
                        pin_num = self.cur.fetchall()
                        if pin_num == self.unique_pin:
                            # Generate a new unique pin number if matched in database
                            self.unique_pin = random.randrange(1000, 9999)
                            print('Changed Pin', self.unique_pin)
                            

                    # If database is empty, add first user (no checks required)
                    with self.conn:
                        self.cur.execute("SELECT * FROM ibank")
                        rows = self.cur.fetchall()
                        if rows == []:
                            print('\n1: Inserting first row into database!')
                            self.cur.execute("INSERT INTO ibank VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", \
                                             (self.first_name.get(), self.last_name.get(), \
                                              self.user_name.get(), self.email_addr.get(), \
                                              self.unique_pin, self.get_amount_in, \
                                              self.get_amount_out, self.balance))
                            self.conn.commit()


                            EA = connect.EMAIL_USER
                            EP = connect.EMAIL_PASS

                            # Process Email
                            msg = EmailMessage()
                            msg['subject'] = 'iBank Account'
                            msg['From'] = EA
                            msg['To'] = self.email_addr.get()
                            msg.set_content(\
                                f'Hi {self.first_name.get()}!'
                                '\nThank you for choosing to bank with iBANK. \n'\
                                f'\nThis is your unique pin number: {self.unique_pin}\n'\
                                '\nRemember your pin number!\nYou will need this, '\
                                'to login to your account.')

                            # Send Email
                            try:
                                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                                    smtp.login(EA, EP)
                                    smtp.send_message(msg)

                            
                            except Exception as e:
                                print(e)
                                # Error message
                                messagebox.showerror(\
                                        'Email Server Error', 'Sorry!\n\nWe have experienced a server issue.'\
                                        '\nPlease check your internet connection\nand try again.')

                            self.email_login()
                                                
                            print(self.first_name.get())
                            print(self.last_name.get())
                            print(self.user_name.get())
                            print(self.email_addr.get())
                            print(self.unique_pin)

                            self.entry_user.delete(0, END)
                            self.entry_email.delete(0, END)
                            self.unique_pin = ''
                                
                        else:
                            with self.conn:
                                self.cur.execute("SELECT * FROM ibank")
                                rows = self.cur.fetchall()
                                # Check If User Already Exits (in database)
                                for row in rows:
                                    print('2: ', row)
                                    # Username
                                    if self.user_name.get() in row:
                                        self.error_frame.pack(padx=0)
                                        self.error_msg.pack(padx=0)
                                        self.error_msg.config(text='Username taken!.')
                                        self.entry_user.focus()
                                        print('\nFound Username Match: Username Taken!')
                                        return
                                    # Email
                                    elif self.email_input in row:
                                        self.error_frame.pack(padx=(50, 0))
                                        self.error_msg.config(text='Person already in database.')
                                        self.entry_email.focus()
                                        print('\nFound Email Match: Email Taken!')
                                        return
                                    # Pin
                                    elif self.unique_pin in row:
                                        self.unique_pin = ''
                                        self.error_msg.config(text='Person already in database.')
                                        print('\nFound Pin Match: Pin Exists!')
                                        return
                                    else:
                                        print('\nElse No Match: Continuing!')
                                        
                                        with self.conn:
                                            print('\n2: Inserting into database!')
                                            self.cur.execute("INSERT INTO ibank VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", \
                                                             (self.first_name.get(), self.last_name.get(), \
                                                              self.user_name.get(), self.email_addr.get(), \
                                                              self.unique_pin, self.get_amount_in, \
                                                              self.get_amount_out, self.balance))
                                            self.conn.commit()


                                        EA = connect.EMAIL_USER
                                        EP = connect.EMAIL_PASS

                                        # Process Email
                                        msg = EmailMessage()
                                        msg['subject'] = 'iBank Account'
                                        msg['From'] = EA
                                        msg['To'] = self.email_addr.get()
                                        msg.set_content(\
                                            f'Hi {self.first_name.get()}!'
                                            '\nThank you for choosing to bank with iBANK. \n'\
                                            f'\nThis is your unique pin number: {self.unique_pin}\n'\
                                            '\nRemember your pin number!\nYou will need this, '\
                                            'to login to your account.')

                                        # Send Email
                                        try:
                                            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                                                smtp.login(EA, EP)
                                                smtp.send_message(msg)

                                        
                                        except Exception as e:
                                            print(e)
                                            # Error message
                                            messagebox.showerror(\
                                                    'Email Server Error', 'Sorry!\n\nWe have experienced a server issue.'\
                                                    '\nPlease check your internet connection\nand try again.')
                                        
                                        self.email_login()
                                        
                                        print(self.first_name.get())
                                        print(self.last_name.get())
                                        print(self.user_name.get())
                                        print(self.email_addr.get())
                                        print(self.unique_pin)

                                        self.entry_user.delete(0, END)
                                        self.entry_email.delete(0, END)
                                        self.unique_pin = ''
                
                except Exception as e:
                    print(str(e))
                except sq.OperationalError as soe:
                    self.conn.close()
                    print('Database Issues:\n' + str(soe))

                self.conn.close()
                
            else:
                self.error_frame.pack(padx=0)
                self.error_msg.config(text='Email address not valid!')
                self.entry_email.focus()
    
    # ======================================================================================
    # User Log In
    
    def user_login(self):
        print('def user_login: Line 1067\nLogging In')

        self.app.configure(bg=main_bg)
        # Refresh Page
        self.refresh()
        
        # Header Frame (Page Title) ___________________________________________
        self.header_frame = Frame(self.app, bg=header_bg)
        self.header_frame.pack(fill='x')

        # Header Title
        self.header_label = Label(self.header_frame, text='iBANK: Login', \
                                       bg=header_bg, fg=header_fg, font=('arial, bold', 14))
        self.header_label.pack(side='left', fill='x', padx=(20, 0), ipady=20)

        # Main Frame
        self.main_frame = Frame(self.app, bg=app_bg)
        self.main_frame.pack(padx=20, ipady=10, expand=True)

        # ________________________________________________________________________________

        # User Name Frame
        self.form_frame3 = Frame(self.main_frame, bg=app_bg)
        self.form_frame3.pack(padx=10, pady=(0, 20))

        # User Name Label
        self.u_name_label = Label(self.form_frame3, text='Username:', \
                                       bg=app_bg, fg=main_fg, font=A12)
        self.u_name_label.pack(side='left', padx=(0, 11), pady=(10, 0))

        self.user_name = StringVar()

        # User Name Entry Field
        self.entry_user = Entry(self.form_frame3, width=22, bg=main_fg, fg=main_bg, \
                            font=A12, textvariable=self.user_name)
        self.entry_user.focus()
        self.entry_user.pack(side='left', pady=(10, 0))

        # Create Login Pin
        self.login_label = Label(self.main_frame, text='Enter Pin', bg=app_bg, fg=main_fg, \
                                 font=A12)
        self.login_label.pack(pady=(0, 6))

        # ========================================================================================
        # ### KEYPAD ###

        # Pin Number Frame (1-3) _______________________________________________
        self.pin_frame = Frame(self.main_frame, bg=app_bg)
        self.pin_frame.pack()
        
        # Pin Numbers (from 1 to 3)
        # Num 1
        self.pin_btn1 = Button(self.pin_frame, text='1', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(1))
        self.pin_btn1.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 2
        self.pin_btn2 = Button(self.pin_frame, text='2', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(2))
        self.pin_btn2.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 3
        self.pin_btn3 = Button(self.pin_frame, text='3', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(3))
        self.pin_btn3.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Pin Number Frame (4-6) _______________________________________________
        self.pin_frame = Frame(self.main_frame, bg='#185185')
        self.pin_frame.pack()

        # Pin Numbers (from 4 to 6)
        # Num 4
        self.pin_btn4 = Button(self.pin_frame, text='4', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(4))
        self.pin_btn4.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 5
        self.pin_btn5 = Button(self.pin_frame, text='5', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(5))
        self.pin_btn5.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 6
        self.pin_btn6 = Button(self.pin_frame, text='6', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(6))
        self.pin_btn6.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Pin Number Frame (7-9) _______________________________________________
        self.pin_frame = Frame(self.main_frame, bg=app_bg)
        self.pin_frame.pack()

        # Pin Numbers (from 7 to 8)
        # Num 7
        self.pin_btn7 = Button(self.pin_frame, text='7', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(7))
        self.pin_btn7.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 8
        self.pin_btn8 = Button(self.pin_frame, text='8', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(8))
        self.pin_btn8.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Num 9
        self.pin_btn9 = Button(self.pin_frame, text='9', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(9))
        self.pin_btn9.pack(side='left', padx=4, pady=4, ipadx=10, ipady=5)

        # Pin Number Frame (0) _______________________________________________
        self.pin_frame = Frame(self.main_frame, bg='#185185')
        self.pin_frame.pack()

        # Num 0
        self.pin_btn0 = Button(self.pin_frame, text='0', bg=main_bg, fg=main_fg, font=A12, \
                               relief='flat', command=lambda:self.get_btn_data(0))
        self.pin_btn0.pack(side='left', padx=(55, 4), pady=4, ipadx=10, ipady=5)

        # O.K Button (submit)
        self.sub_pin = Button(self.pin_frame, text='OK', bg='#369369', fg=main_fg, font=A12, \
                               relief='flat', command=self.get_entered_pin)
        self.sub_pin.pack(side='right', padx=4, pady=4, ipadx=3, ipady=5)

        # _____________________________________________________________________

        # Change login to back to home button
        self.footer_btn['text'] = 'Back'
        self.footer_btn['command'] = self.home

    # ======================================================================================
    # Create Account
    
    def new_account(self):
        print('def new_account: Line 1197')
        print('Create Account')

        # Remove Home Page Image
        self.app.configure(bg='#fff')
        # Refresh Page
        self.refresh()

        # Header Frame (Page Title) ___________________________________________
        self.header_frame = Frame(self.app, bg=header_bg)
        self.header_frame.pack(fill='x')

        # Header Title
        self.header_label = Label(self.header_frame, text='iBANK: New Account', \
                                       bg=header_bg, fg=header_fg, font=('arial, bold', 14))
        self.header_label.pack(side='left', fill='x', padx=(20, 0), ipady=20)

        # ________________________________________________________________________________

        # ### NEW ACCOUNT FORM ###

        # Getters
        self.first_name = StringVar()
        self.last_name = StringVar()
        self.user_name = StringVar()
        self.email_addr = StringVar()

        # First Name Frame
        self.error_frame = Frame(self.app, bg=main_fg)
        self.error_frame.pack(pady=(50, 0))

        # Error Message Label
        self.error_msg = Label(self.error_frame, bg=main_fg, fg='#e23e23', font=('arial', 10))
        self.error_msg.pack(padx=(30, 0), pady=(10,10))
        
        # First Name Frame
        self.form_frame1 = Frame(self.app, bg=main_fg)
        self.form_frame1.pack(pady=5)

        # First Name Label
        self.f_name_label = Label(self.form_frame1, text='First name:', \
                                       bg=main_fg, fg='#296296', font=A12)
        self.f_name_label.pack(side='left', padx=(0, 9))

        # First Name Entry Field
        self.entry_first = Entry(self.form_frame1, width=22, bg=main_fg, fg=main_bg, \
                            font=A12, textvariable=self.first_name)
        self.entry_first.focus()
        self.entry_first.pack(side='left')

        # ________________________________________________________________________________

        # Last Name Frame
        self.form_frame2 = Frame(self.app, bg=main_fg)
        self.form_frame2.pack(pady=5)

        # Last Name Label
        self.l_name_label = Label(self.form_frame2, text='Last name:', \
                                       bg=main_fg, fg=main_bg, font=A12)
        self.l_name_label.pack(side='left', padx=(0, 9))

        # Last Name Entry Field
        self.entry_last = Entry(self.form_frame2, width=22, bg=main_fg, fg=main_bg, \
                            font=A12, textvariable=self.last_name)
        self.entry_last.pack(side='left')

        # ________________________________________________________________________________

        # User Name Frame
        self.form_frame3 = Frame(self.app, bg='#fff')
        self.form_frame3.pack(pady=5)

        # User Name Label
        self.u_name_label = Label(self.form_frame3, text='Username:', \
                                       bg=main_fg, fg=main_bg, font=A12)
        self.u_name_label.pack(side='left', padx=(0, 11))

        # User Name Entry Field
        self.entry_user = Entry(self.form_frame3, width=22, bg=main_fg, fg=main_bg, \
                            font=A12, textvariable=self.user_name)
        self.entry_user.pack(side='left')        

        # ________________________________________________________________________________

        # Email Address Frame
        self.form_frame4 = Frame(self.app, bg=main_fg)
        self.form_frame4.pack(pady=5)

        # Email Address Label
        self.e_name_label = Label(self.form_frame4, text='Email Addr:', \
                                       bg=main_fg, fg=main_bg, font=A12)
        self.e_name_label.pack(side='left', padx=(0, 5))

        # Email Address Entry Field
        self.entry_email = Entry(self.form_frame4, width=22, bg=main_fg, fg=main_bg, \
                            font=A12, textvariable=self.email_addr)
        self.entry_email.pack(side='left')

        # ________________________________________________________________________________

        # Submit Button Frame
        self.form_frame5 = Frame(self.app, bg='#fff')
        self.form_frame5.pack(pady=5, ipadx=116)

        # Submit Button
        self.sub_btn = Button(self.form_frame5, text='Submit', bg=main_bg, fg=main_fg, \
                            font=A12, relief='flat', command=self.submit_data)
        self.app.bind('<Return>', self.submit_data)
        self.sub_btn.pack(anchor='e')

        # ________________________________________________________________________________
        
        # Change login to back to home button
        self.footer_btn['text'] = 'Back'
        self.footer_btn['command'] = self.home

    # ======================================================================================
    # If Mouse is in the "Create Account Area" of the Image
    
    def get_coordinates(self, event):
        x_pos = event.x
        y_pos = event.y
        if x_pos >= 158 and x_pos <= 448 and y_pos >= 268 and y_pos <=330:
            self.new_account()

# ======================================================================================
# Root Defaults

if __name__ == '__main__':
    main()
