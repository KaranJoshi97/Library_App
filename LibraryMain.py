from tkinter import *
from tkinter import ttk
import sqlite3
import addbook, addmember, givebook
from tkinter import messagebox

con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(object):
    def __init__(self, master):
        self.master = master

        def displayStatistics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            print(count_books)
            self.label_book_count.config(text="Total: " + str(
                count_books[0][0]) + ' books in library')  ### Python returns list and inside list is another tuple

            self.label_member_count.config(text="Total member: " + str(count_members[0][0]))
            self.label_taken_count.config(text="Taken books: " + str(taken_books[0][0]))
            displayBooks(self)

        def displayBooks(self):
            # This function will return all the books from the database
            books = cur.execute("SELECT * FROM books").fetchall()
            count = 0

            self.list_books.delete(0, END)
            for book in books:
                print(book)
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

            def bookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?", (id,))
                book_info = book.fetchall()
                print(book_info)
                self.list_details.delete(0, 'end')
                self.list_details.insert(0, "Book Name : " + book_info[0][1])
                self.list_details.insert(1, "Author : " + book_info[0][2])
                self.list_details.insert(2, "Page : " + book_info[0][3])
                self.list_details.insert(3, "Language : " + book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4, "Status : Avaiable")
                else:
                    self.list_details.insert(4, "Status : Not Avaiable")

            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('-')[0]
                give_book = GiveBook()

            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatistics)
            # self.tabs.bind('<ButtonRelease-1>', displayBooks())
            self.list_books.bind('<Double-Button-1>', doubleClick)


        # Frames
        mainFrame = Frame(self.master)
        mainFrame.pack()
        # top frames
        # topFrame will be child of my main frame
        topFrame = Frame(mainFrame, width=1350, height=70, bg='#fafafa', padx=2, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)

        # center frame
        centerFrame = Frame(mainFrame, width=1350, relief=RIDGE, bg='#e0f0f0', height=680)
        centerFrame.pack(side=TOP)

        # center left frame
        centerLeftFrame = Frame(centerFrame, width=900, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerLeftFrame.pack(side=LEFT)

        # center right frame
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerRightFrame.pack()

        # search bar
        search_bar = LabelFrame(centerRightFrame, width=440, height=175, text='Search Box', bg='#9bc9ff')
        search_bar.pack(fill=BOTH)

        self.label_search = Label(search_bar, text='Search :', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.label_search.grid(row=0, column=0, padx=20, pady=20)
        self.entries_search = Entry(search_bar, width=30, bd=10)
        self.entries_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(search_bar, text='search', font='arial 12', bg='#fcc324', fg='white',
                                 command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)

        # list bar
        list_bar = LabelFrame(centerRightFrame, width=440, height=175, text='List Box', bg='#fcc324')
        list_bar.pack(fill=BOTH)
        label_list = Label(list_bar, text='Sort By', font='times 16 bold', fg='#2488ff', bg='#fcc324')
        label_list.grid(row=0, column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(list_bar, text='All Books', var=self.listChoice, value=1, bg='#fcc324')
        rb2 = Radiobutton(list_bar, text='In Library', var=self.listChoice, value=2, bg='#fcc324')
        rb3 = Radiobutton(list_bar, text='Borrowed Books', var=self.listChoice, value=3, bg='#fcc324')
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(list_bar, text='List Books', bg='#2488ff', fg='white', font='arial 12',
                          command=self.listBooks)
        btn_list.grid(row=1, column=3, padx=40, pady=10)

        # title and image
        image_bar = Frame(centerRightFrame, width=440, height=350)
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar, text='Welcome to our Library',
                                 font='arial 16 bold', padx=10)
        self.title_right.grid(row=0)
        self.image_library = PhotoImage(file=r'icons/library.png')
        self.labelImage = Label(image_bar, image=self.image_library)
        self.labelImage.grid(row=1)

        ###############################3 Tool Bar ########################

        # add book
        self.iconbook = PhotoImage(file=r'icons/add_book.png')
        self.btnbook = Button(topFrame, text='Add Book', image=self.iconbook,
                              compound=LEFT, font='arial 12 bold', command=self.addBook)
        self.btnbook.pack(side=LEFT, padx=10)

        # add member button
        self.iconmember = PhotoImage(file=r'icons/users.png')
        self.btnmember = Button(topFrame, text='Add Member', font='arial 12 bold', padx=10, command=self.addMember)
        self.btnmember.configure(image=self.iconmember, compound=LEFT)
        self.btnmember.pack(side=LEFT)

        # give book
        self.icongive = PhotoImage(file=r'icons/givebook.png')
        self.btngive = Button(topFrame, text='Give Book', font='arial 12 bold',
                              padx=10, image=self.icongive, compound=LEFT, command=self.giveBook)
        self.btngive.pack(side=LEFT)

        ################ Tabs #####################

        #############tab1#############
        # All information for the first tab

        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.tab1_icon = PhotoImage(file=r'icons/books.png')
        self.tab2_icon = PhotoImage(file=r'icons/members.png')
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Library Management', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)

        # list books
        self.list_books = Listbox(self.tab1, width=40, height=30, bd=5, font='Times 12 bold')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0))
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N + S + E)

        # list details
        self.list_details = Listbox(self.tab1, width=80, height=30, bd=5, font='times 12 bold')
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        #############tab2#############
        # All information for the second tab
        # Information for the statistics

        self.label_book_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.label_book_count.grid(row=0)
        self.label_member_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.label_member_count.grid(row=1, sticky=W)
        self.label_taken_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.label_taken_count.grid(row=2, sticky=W)

        # Functions
        displayBooks(self)
        displayStatistics(self)

    # Creating the definitions
    # Create instance
    def addBook(self):
        add = addbook.AddBook()

    def addMember(self):
        member = addmember.AddMember()

    def searchBooks(self):
        value = self.entries_search.get()
        search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + value + '%',)).fetchall()
        print(search)
        self.list_books.delete(0, END)
        count = 0
        for book in search:
            self.list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in allbooks:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status = ?", (0,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status = ?", (1,)).fetchall()
            self.list_books.delete(0, END)

            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

    def giveBook(self):
        give_book = givebook.GiveBook()


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Lend Book")
        self.resizable(False, False)
        global given_id
        # # print(type(given_id))
        self.book_id = int(given_id)
        query = "SELECT * FROM books"
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
        heading = Label(self.topFrame, text='  Add Person ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        ############################
        # Entries and Labels will be used here

        # # member_name
        self.book_name = StringVar()
        self.label_name = Label(self.bottomFrame, text='Book :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.label_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.current(self.book_id-1)
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


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+350+200")
    root.iconbitmap('icons/icon.ico')
    root.mainloop()


if __name__ == '__main__':
    main()
