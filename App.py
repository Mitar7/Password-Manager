"""Mitar Milovanovic
    Password-Manager"""

from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
import sqlite3
import time


def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


key = load_key()
fer = Fernet(key)


class LoginApp:
    def __init__(self):
        # Log in function
        def login():
            if self.username.get() == 'admin' and self.password.get() == 'admin':
                self.root.destroy()
                mg = ManagerApp()
            else:
                self.tries -= 1
                if self.tries > 0:
                    messagebox.showerror('Invalid login!', f'Wrong username/password! Tries left: {self.tries}')
                else:
                    self.root.destroy()

        # DEFINING Properties
        self.FONT_LOGIN = ("Roboto", 20)
        self.BG = "#333"
        self.FG = "white"
        self.tries = 3

        # Window options
        self.root = Tk()
        self.root.geometry('500x300')
        self.root.title('Log In')
        self.root.iconbitmap('img/key.ico')
        self.root.resizable(width=False, height=False)
        self.root.configure(bg=self.BG)

        # Window Elements
        self.LabelLogin = Label(self.root, text="WELCOME TO PASSWORD MANAGER", bg=self.BG,
                                fg=self.FG, font=('Roboto', 18, 'bold'))
        self.LabelLogin.place(relx=0.05, rely=0)

        # Username
        self.username = StringVar()
        self.LabelUser = Label(self.root, text="Username: ", bg=self.BG, fg=self.FG,
                               font=self.FONT_LOGIN)
        self.LabelUser.place(relx=0.1, rely=0.2)
        self.EntryUserName = Entry(self.root, width=30, textvariable=self.username)
        self.EntryUserName.place(relx=0.4, rely=0.23)

        # Password
        self.password = StringVar()
        self.LabelPassword = Label(self.root, text="Password: ", bg=self.BG, fg=self.FG,
                                   font=self.FONT_LOGIN)
        self.LabelPassword.place(relx=0.1, rely=0.35)
        self.EntryPassword = Entry(self.root, width=30, textvariable=self.password, show='*')
        self.EntryPassword.place(relx=0.4, rely=0.38)

        # Login Button
        self.btnLogin = Button(self.root, text="Login", fg=self.BG, bg='lime',
                               width=30, activebackground='darkgreen', activeforeground=self.FG,
                               command=login)
        self.btnLogin.place(relx=0.25, rely=0.6)
        self.root.mainloop()


class ManagerApp:
    def __init__(self):
        # DEFINING Properties
        self.FONT_MNG = ("Roboto", 18)
        self.BG = "#333"
        self.FG = "white"

        def save():
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            site_s = self.site.get()
            email_s = self.email.get()
            password_s = self.password.get()
            password_s = fer.encrypt(password_s.encode()).decode()
            curr_date = time.strftime("%m/%d/%Y, %H:%M:%S")

            # decrypt = fer.decrypt(password_s.encode()).decode()
            # print(f"{site_s} | {email_s} | {password_s} | {decrypt} | {curr_date}")

            if site_s:
                if email_s:
                    if self.EntryPassword.get():
                        cur.execute("""
                         INSERT INTO password
                         VALUES(?,?,?,?)
                        """, (site_s, email_s, password_s, curr_date))
                        con.commit()
                        con.close()
                        messagebox.showinfo('Successfully inserted!', 'Data inserted into database!')
                    else:
                        messagebox.showerror('Input Error', 'You need to enter password!')
                else:
                    messagebox.showerror('Input Error', 'You need to enter email!')
            else:
                messagebox.showerror('Input Error', 'You need to enter site!')

        def load_all():
            self.txtDisplay.delete('1.0', END)
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("""
            SELECT rowid,*
            FROM password
            """)
            text = cur.fetchall()
            result = ""
            for rowid, site, gmail, password, date in text:
                decrypt = fer.decrypt(password.encode()).decode()
                result += f"{rowid}. {site} | {gmail} | {decrypt} | {date}\n"
            self.txtDisplay.insert(INSERT, result)

        def load_by_email():
            self.txtDisplay.delete('1.0', END)
            mail = self.loadbymail.get()
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("""
            SELECT rowid,*
            FROM password
            WHERE email = ? """, (mail,))
            text = cur.fetchall()
            result = ""
            for rowid, site, gmail, password, date in text:
                decrypt = fer.decrypt(password.encode()).decode()
                result += f"{rowid}. {site} | {gmail} | {decrypt} | {date}\n"
            self.txtDisplay.insert(INSERT, result)

        def delete_all():
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("""DELETE FROM PASSWORD""")
            con.commit()
            con.close()
            messagebox.showinfo('Successfully deleted!', 'Data deleted from database!')

        def delete_by_id():
            id = self.deletebyid.get()
            con = sqlite3.connect('data.db')
            cur = con.cursor()
            cur.execute("""DELETE FROM PASSWORD WHERE rowid = ?""", (id,))
            con.commit()
            con.close()
            messagebox.showinfo('Successfully deleted!', 'Data with ID deleted from database!')

# Window options
        self.root = Tk()
        self.root.geometry('900x500')
        self.root.title('Password Manager')
        self.root.iconbitmap('img/key.ico')
        self.root.resizable(width=False, height=False)
        self.root.configure(bg=self.BG)

# Window Elements
# site elements
        self.site = StringVar()
        self.email = StringVar()
        self.password = StringVar()

# site
        self.LabelSite = Label(self.root, text="Site: ", bg=self.BG, fg=self.FG,
                               font=self.FONT_MNG)
        self.LabelSite.place(relx=0.1, rely=0.1)
        self.EntrySite = Entry(self.root, width=30, textvariable=self.site)
        self.EntrySite.place(relx=0.1, rely=0.16)

# email
        self.LabelEmail = Label(self.root, text="Email: ", bg=self.BG,
                                fg=self.FG, font=self.FONT_MNG)
        self.LabelEmail.place(relx=0.1, rely=0.2)
        self.EntryEmail = Entry(self.root, width=30, textvariable=self.email)
        self.EntryEmail.place(relx=0.1, rely=0.26)

# password
        self.LabelPassword = Label(self.root, text="Password: ", bg=self.BG,
                                   fg=self.FG, font=self.FONT_MNG)
        self.LabelPassword.place(relx=0.1, rely=0.3)
        self.EntryPassword = Entry(self.root, width=30, textvariable=self.password, show='*')
        self.EntryPassword.place(relx=0.1, rely=0.36)

# Save info
        self.btnSave = Button(self.root, text="Save", bg='lime', fg=self.BG
                              , command=save, width=25)
        self.btnSave.place(relx=0.1, rely=0.45)

# Load info
        self.btnLoad = Button(self.root, text="Load All information", bg='darkblue',
                              fg=self.FG, command=load_all, width=25)
        self.btnLoad.place(relx=0.1, rely=0.52)

# Load by mail
        self.loadbymail = StringVar()
        self.LabelLoadMail = Label(self.root, text="Load by mail: ", bg=self.BG,
                                   fg=self.FG, font=self.FONT_MNG)
        self.LabelLoadMail.place(relx=0.1, rely=0.6)
        self.EntryLoadMail = Entry(self.root, width=30, textvariable=self.loadbymail)
        self.EntryLoadMail.place(relx=0.1, rely=0.66)
        self.btnLoadMail = Button(self.root, text="Show info for mail",
                                  bg='darkblue', fg=self.FG, command=load_by_email, width=25)
        self.btnLoadMail.place(relx=0.1, rely=0.72)

# Display
        self.LabelShow = Label(self.root, text="Information: ", bg=self.BG,
                               fg=self.FG, font=self.FONT_MNG)
        self.LabelShow.place(relx=0.35, rely=0.03)
        self.txtDisplay = Text(self.root, height=20, width=80, font=('Roboto', 10))
        self.txtDisplay.place(relx=0.35, rely=0.1)

# Delete all information
        self.btnDeleteAll = Button(self.root, text="Delete all information",
                                   bg='red', fg=self.FG, command=delete_all, width=25)
        self.btnDeleteAll.place(relx=0.77, rely=0.78)

# Delete by id
        self.deletebyid = StringVar()
        self.LabelDeleteById = Label(self.root, text="DELETE BY ID: ", bg=self.BG,
                                     fg=self.FG, font=("Roboto", 15))
        self.LabelDeleteById.place(relx=0.57, rely=0.72)
        self.EntryDeleteById = Entry(self.root, width=5, textvariable=self.deletebyid)
        self.EntryDeleteById.place(relx=0.72, rely=0.7255)
        self.btnDeleteByID = Button(self.root, text="Delete by record ID",
                                    bg='red', fg=self.FG, command=delete_by_id, width=25)
        self.btnDeleteByID.place(relx=0.77, rely=0.72)

        self.root.mainloop()


if __name__ == '__main__':
    # Program starts with Login window
    lg = LoginApp()
