from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()

class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False, False)

        # 0 = available for book status, 1 for not available for book status
        query = "SELECT * FROM books WHERE book_status = 0"
        books = cur.execute(query).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + "-" + book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + "-" + member[1])


        ######## Frames ##########
        # this will be the top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # this will be the bottom frame
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # The heading, image,
        self.top_image = PhotoImage(file=r'icons/addperson.png')
        top_image_label = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_label.place(x=120, y=10)
        heading = Label(self.topFrame, text='  Lend a Book ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ############################
        # Entries and Labels will be used here

        # # member_name
        self.book_name = StringVar()
        self.label_name = Label(self.bottomFrame, text='Book :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.place(x=150, y=45)


        # # phone
        self.member_name = StringVar()
        self.label_phone = Label(self.bottomFrame, text='Member :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list
        self.combo_member.place(x=150, y=85)

        # Button
        button = Button(self.bottomFrame, text='Lend Book', command=self.lendBook)
        button.place(x=220, y=120)

    def lendBook(self):
        book_name = self.book_name.get()
        self.book_id = book_name.split('-')[0]
        member_name = self.member_name.get()

        if (book_name and member_name != ""):
            try:
                query = "INSERT INTO 'borrows' (bbook_id, bmember_id) VALUES(?,?)"
                cur.execute(query, (book_name, member_name))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database!", icon='info')
                cur.execute("UPDATE books SET book_status =? WHERE book_id=?", (1, self.book_id))
                con.commit()
            except:
                 messagebox.showerror("Error", "Cant add to database", icon='warning')

        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')
