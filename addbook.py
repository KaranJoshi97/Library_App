from tkinter import *
from tkinter import messagebox
import sqlite3
con = sqlite3.connect('library.db')
cur = con.cursor()

class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False, False)

        ######## Frames ##########

        # this will be the top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # this will be the bottom frame
        self.bottomFrame = Frame(self, height=600, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # The heading, image,
        self.top_image = PhotoImage(file=r'icons/addbook.png')
        top_image_label = Label(self.topFrame, image = self.top_image, bg='white')
        top_image_label.place(x=120, y=10)
        heading = Label(self.topFrame, text='  Add Book ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ############################
        # Entries and Labels will be used here

        # name
        self.label_name = Label(self.bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_name.place(x=40, y=40)
        self.entry_name = Entry(self.bottomFrame, width=30, bd=4)
        self.entry_name.insert(0, 'Please enter a book name')
        self.entry_name.place(x=150, y=45)

        # author
        self.label_author = Label(self.bottomFrame, text='Author :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_author.place(x=40, y=80)
        self.entry_author = Entry(self.bottomFrame, width=30, bd=4)
        self.entry_author.insert(0, 'Please enter a author name')
        self.entry_author.place(x=150, y=85)

        # page
        self.label_page = Label(self.bottomFrame, text='Page :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_page.place(x=40, y=120)
        self.entry_page = Entry(self.bottomFrame, width=30, bd=4)
        self.entry_page.insert(0, 'Please enter page size')
        self.entry_page.place(x=150, y=125)

        # language
        self.label_language = Label(self.bottomFrame, text='Language :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_language.place(x=40, y=160)
        self.entry_language = Entry(self.bottomFrame, width=30, bd=4)
        self.entry_language.insert(0, 'Please enter a language')
        self.entry_language.place(x=150, y=165)

        # Button
        button = Button(self.bottomFrame, text='Add Book', command=self.addBook)
        button.place(x=270, y=200)

    def addBook(self):
        name = self.entry_name.get()
        author = self.entry_author.get()
        page = self.entry_page.get()
        language = self.entry_language.get()

        if (name and author and page and language != ""):
            try:
                query = "INSERT INTO 'books' (book_name, book_author, book_page, book_language) VALUES(?,?,?,?)"
                cur.execute(query,(name, author, page, language))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database", icon='info')

            except:
                messagebox.showerror("Error", "Can't add to database", icon='warning')

        else:
            messagebox.showerror("Error", "Fields can't be empty", icon='warning')








