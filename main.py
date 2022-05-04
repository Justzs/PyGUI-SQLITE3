import sqlite3
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from datetime import date
from tkcalendar import Calendar #pip install tkcalendar
from tkcalendar import DateEntry 

def mainwindow() :
    global emptyMenubar
    root = Tk()
    x = root.winfo_screenwidth()/2 - w/2
    y = root.winfo_screenheight()/2 - h/1.78
    root.geometry("%dx%d+%d+%d"%(w,h,x,y))
    # root.overrideredirect(True)
    # root.state('zoomed')
    # root.geometry("%dx%d+400+40"%(w,h))
    #root.config(bg='#4a3933')
    root.config(bg='#28527a')
    root.title("Student Service System by Narongsak Jeroenpanyasak")
    root.option_add('*font',"Mali 10")
    style = ttk.Style(root)
    style.configure("Treeview", font=('Mali', 10), rowheight=30)
    emptyMenubar = Menu(root)
    root.rowconfigure((0,1,2,3),weight=1)
    root.columnconfigure((0,1,2,3),weight=1)
    return root

def createconnection() :
    global conn,cursor
    conn = sqlite3.connect('database/emp_dbms.db')
    cursor = conn.cursor()

def loginlayout() :
    global userentry
    global pwdentry
    global loginframe
    
    loginframe = Frame(root,bg='#709fb0')
    loginframe.rowconfigure((0,1,2,3),weight=1)
    loginframe.columnconfigure((0,1),weight=1)
    root.title("Employee Management System")
    
    Label(loginframe,text="Account login",font="Calibri 26 bold",image=img1,compound=TOP,bg='#709fb0',fg='#e4fbff').grid(row=0,columnspan=2)
    Label(loginframe,text="Username : ",bg='#709fb0',fg='#e4fbff',padx=20).grid(row=1,column=0,sticky='e')
    userentry = Entry(loginframe,bg='#e4fbff',width=20,textvariable=userinfo)
    userentry.grid(row=1,column=1,sticky='w',padx=20)
    pwdentry = ttk.Entry(loginframe, width=20,show='*',textvariable=pwdinfo)
    pwdentry.grid(row=2,column=1,sticky='w',padx=20)
    Label(loginframe,text="Password  : ",bg='#709fb0',fg='#e4fbff',padx=20).grid(row=2,column=0,sticky='e')
    ttk.Button(loginframe,text="Login", width=10,command=loginclick).grid(row=3,column=1,sticky='e',padx=20, ipady=10, ipadx=10)
    
    Button(loginframe,text="Exit",width=10,command=quit).grid(row=3,column=0)
    loginframe.grid(row=1,column=1,columnspan=2,rowspan=2,sticky='news')
    
def loginclick() :
    if  userinfo.get() == '':
        messagebox.showwarning("Warning", "Please enter your username!")
        userentry.focus_force()
    elif pwdinfo.get() == '':
        messagebox.showwarning("Warning", "Please enter your password!")
        pwdentry.focus_force()
    else:
        sql_auth = "SELECT a_username FROM Admin WHERE a_username=? and a_password=?"

        params = [userinfo.get(), pwdinfo.get()]
        cursor.execute(sql_auth, params)
        result_login = cursor.fetchone()

        if result_login:
            employeesLayout(result_login[0])
            messagebox.showinfo("Admin :", "Login Successfully.")
        else :
            messagebox.showwarning("Admin", "Username or password is invalid.")
            userentry.select_range(0, END)

def employeesLayout(username):
    global myEmpTree, empFrame, de_list, leftFrame
    global emp_fname, emp_lname, emp_phone, emp_salary, emp_department, emp_address, emp_gender, emp_email, emp_datepick
    global btn_add, btn_update, btn_delete, label_id, findoption, search_option
    sql = '''
        SELECT Admin.a_fname, Admin.a_lname, Permissions.perm_description, Permissions.perm_name
        FROM Admin INNER JOIN Permissions ON Admin.a_permission = Permissions.perm_id
        WHERE Admin.a_username = ?
    '''
    cursor.execute(sql, [username])
    result = cursor.fetchone()
    root.title("Welcome : " + result[0] +" "+ result[1] + " (" +result[2]+ ")")
    empFrame = Frame(root, bg='#28527a')
    empFrame.columnconfigure((0,1),weight=1)
    empFrame.rowconfigure((0,1),weight=1)

    leftFrame = LabelFrame(empFrame, text="Employees")
    leftFrame.columnconfigure((0,1),weight=1)
    leftFrame.rowconfigure((0),weight=3)
    leftFrame.rowconfigure((0,1,2),weight=1)
    myEmpTree = ttk.Treeview(leftFrame, columns=('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7'))
    myEmpTree.grid(row=0, column=0, columnspan=2, sticky='news')

    myEmpTree.heading('col1', text='ID')
    myEmpTree.heading('col2', text='Firstname')
    myEmpTree.heading('col3', text='Lastname')
    myEmpTree.heading('col4', text='Phone No.')
    myEmpTree.heading('col5', text='Email')
    myEmpTree.heading('col6', text='Department')

    myEmpTree.column('col1', anchor=W, width=100)
    myEmpTree.column('col2', anchor=W, width=100)
    myEmpTree.column('col3', anchor=W, width=100)
    myEmpTree.column('col4', anchor=CENTER, width=130)
    myEmpTree.column('col5', anchor=W, width=220)
    myEmpTree.column('col6', anchor=CENTER, width=130)
    myEmpTree.column('#0', width=0, minwidth=0)

    my_display(0)
    # fetchEmployees()
    myEmpTree.bind('<Double-1>', treeviewClick)
    # #----------------------------------------------------------------#
    # |====================== Right Top Frame =========================|
    # #----------------------------------------------------------------#
    rightTop = LabelFrame(empFrame, text="Search")
    rightTop.columnconfigure((0,1,3),weight=1)
    rightTop.rowconfigure((0),weight=1)

    findoption = StringVar()
    findoption.set("ID")
    option = ttk.OptionMenu(rightTop,findoption,"","ID","Name","Department")
    option.grid(row=0,column=0,ipady=8, padx=10,sticky='we')

    search_option = ttk.Combobox(rightTop)
    search_option.grid(row=0, column=1, sticky='we')
    search_option.bind('<Enter>', onChange)
    search_option.bind('<Leave>', onChange)

    # searchbox = ttk.Entry(rightTop,width=25)
    # searchbox.grid(row=0,column=1,columnspan=2,pady=10, padx=10,sticky='news')

    search_button = ttk.Button(rightTop, text="Search",command=searchClick)
    search_button.grid(row=0,column=3,ipady=8, padx=10, sticky='we')

    # #----------------------------------------------------------------#
    # |======================== Right Frame ===========================|
    # #----------------------------------------------------------------#
    rightFrame = LabelFrame(empFrame, text="View")
    rightFrame.columnconfigure((0,1),weight=1)
    # rightFrame.rowconfigure((),weight=1)

    label_id = Label(rightFrame,text="ID :",padx=20)
    label_id.grid(row=0,column=0,sticky='w')

    Label(rightFrame,text="Firstname : *",padx=20).grid(row=1,column=0,sticky='w')
    emp_fname = ttk.Entry(rightFrame, width=35)
    emp_fname.grid(row=2,column=0,sticky='ew',padx=10)

    Label(rightFrame,text="Lastname : *",padx=20).grid(row=1,column=1,sticky='w')
    emp_lname = ttk.Entry(rightFrame, width=35)
    emp_lname.grid(row=2,column=1,sticky='ew',padx=10)

    Label(rightFrame,text="BirthDate : dd-mm-yyy",padx=20).grid(row=6,column=0,sticky='w')
    emp_datepick = DateEntry(rightFrame, selectmode='day',date_pattern='dd-mm-yyy')
    emp_datepick.grid(row=7, column=0, sticky='news', padx=10)
    emp_datepick.set_date('01-01-2022')
    
    Label(rightFrame,text="Email : ",padx=20).grid(row=6,column=1,sticky='w')
    emp_email = ttk.Entry(rightFrame, width=35)
    emp_email.grid(row=7,column=1,sticky='ew',padx=10)

    Label(rightFrame,text="Address : ",padx=20).grid(row=8,column=0,sticky='w')
    emp_address = Text(rightFrame, width=35, height=2)
    emp_address.grid(row=9,column=0, columnspan=2, sticky='ew',padx=10)

    Label(rightFrame,text="Phone : ",padx=20).grid(row=10,column=0,sticky='w')
    emp_phone = ttk.Entry(rightFrame, width=35)
    emp_phone.grid(row=11,column=0, sticky='ew',padx=10)

    Label(rightFrame,text="Salary : ",padx=20).grid(row=10,column=1,sticky='w')
    emp_salary = ttk.Entry(rightFrame, width=35)
    emp_salary.grid(row=11,column=1,sticky='ew',padx=10)

    Label(rightFrame,text="Department : ",padx=20).grid(row=14,column=0,sticky='w')
    emp_department = ttk.Combobox(rightFrame, width=35)
    emp_department.grid(row=15,column=0,sticky='ew',padx=10)

    Label(rightFrame,text="Gender : ",padx=20).grid(row=14,column=1,sticky='w')
    emp_gender = ttk.Combobox(rightFrame, width=35, values=["Male","Female"])
    emp_gender.grid(row=15,column=1,sticky='ew',padx=10)

    if result[3] == "admin":
        adminMenubar = Menu(root)
        adminMenubar.add_command(label="User Account", command=userLayout)
        adminMenubar.add_command(label="Logout",command=logoutClick)
        adminMenubar.add_command(label="Exit",command=root.quit)
        root.config(bg='lightblue',menu=adminMenubar)
        btn_add = ttk.Button(rightFrame, text="Add", command=addEmployee)
        btn_add.grid(row=20, column=0, sticky='news', ipadx=5, ipady=10, pady=5, padx=5)
        btn_update = ttk.Button(rightFrame, text="Update", command=updateEmployee)
        btn_update.grid(row=20, column=1, sticky='news', ipadx=5, ipady=10, pady=5, padx=5)
        btn_delete = ttk.Button(rightFrame, text="Delete", command=deleteEmployee)
        btn_delete.grid(row=21, column=0, sticky='news', ipadx=5, ipady=10, pady=5, padx=5)
        ttk.Button(rightFrame, text="Clear", command=clearData).grid(row=21, column=1, sticky='news', ipadx=5, ipady=10, pady=5, padx=5)
        btn_update.config(state="disabled")
        btn_delete.config(state="disabled")
    elif result[3] == "editor":
        pass
    elif result[3] == "viewer":
        menubar = Menu(root)
        menubar.add_command(label="Logout",command=logoutClick)
        menubar.add_command(label="Exit",command=root.quit)
        root.config(bg='lightblue',menu=menubar)

    sql_de = "SELECT de_name FROM Departments"
    cursor.execute(sql_de)
    departments = cursor.fetchall()
    de_list = []
    for i, data in enumerate(departments):
        de_list.append(data[0])
    emp_department['value'] = de_list


    leftFrame.grid(row=0, column=0, rowspan=2, sticky='news', padx=10, pady=10)
    rightTop.grid(row=0, column=1, sticky='news', padx=10, pady=10)
    rightFrame.grid(row=1, column=1, sticky='news', padx=10, pady=10)
    empFrame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky='news')

def fetchEmployees():
    myEmpTree.delete(*myEmpTree.get_children())
    sql = '''
        SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_phone, Employees.emp_email, Departments.de_name
        FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id WHERE Employees.emp_status != "disable"
        ORDER BY Employees.emp_id DESC LIMIT 10;
    '''
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        for i, data in enumerate(result):
            myEmpTree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5]))

def empRequiredField():

    if emp_fname.get() == '':
        messagebox.showwarning('Admin', "Please enter firstname.")
        emp_fname.focus_force()
        return False
    elif emp_lname.get() == '':
        messagebox.showwarning('Admin', "Please enter lastname.")
        emp_lname.focus_force()
        return False
    elif emp_email.get() == '':
        messagebox.showwarning('Admin', "Please enter email.")
        emp_email.focus_force()
        return False
    elif emp_phone.get() == '':
        messagebox.showwarning('Admin', "Please enter phone number.")
        emp_phone.focus_force()
        return False
    elif emp_salary.get() == '':
        messagebox.showwarning('Admin', "Please enter salary.")
        emp_salary.focus_force()
        return False
    elif emp_department.get() == '':
        messagebox.showwarning('Admin', "Please enter department.")
        emp_department.focus_force()
        return False
    elif emp_gender.get() == '':
        messagebox.showwarning('Admin', "Please enter gender.")
        emp_gender.focus_force()
        return False
    else:
        return True
    
def getEmpData():
    sql = "SELECT * FROM Departments"
    cursor.execute(sql)
    result = cursor.fetchall()

    for i, data in enumerate(result):
        if data[1] == emp_department.get():
            department = data[0]
        else:
            pass

    date = emp_datepick.get_date()
    data = date.strftime("%d-%m-%Y")
    empData = [
            emp_fname.get(),
            emp_lname.get(),
            data,
            emp_address.get(1.0, 'end'),
            emp_phone.get(),
            emp_salary.get(),
            department,
            emp_gender.get(),
            emp_email.get(),]
    return empData

def addEmployee():
    if empRequiredField():
        # print("True")

        sql_ins = '''
            INSERT INTO Employees (emp_fname, emp_lname, emp_born, emp_address, emp_phone, emp_salary, emp_department, emp_gender, emp_email, emp_status)
            VALUES (?,?,?,?,?,?,?,?,?,"enable")
        '''
        cursor.execute(sql_ins, getEmpData())
        conn.commit()
        messagebox.showinfo("Admin", "Employee added successfully.")
        fetchEmployees()
        clearData()
    else:
        # print("False")
        pass   
def updateEmployee():
    if empRequiredField():
        sql = '''
            UPDATE Employees SET emp_fname=?, emp_lname=?, emp_born=?, emp_address=?, emp_phone=?, emp_salary=?, emp_department=?, emp_gender=?, emp_email=?
            WHERE emp_id = ?
        '''
        params = getEmpData()
        params.append(emp_id)
        print(params)
        cursor.execute(sql, params)
        conn.commit()
        messagebox.showinfo("Admin", "Employee updated successfully.")
        fetchEmployees()
        clearData()
    else:
        pass
def deleteEmployee():
    msg = messagebox.askquestion('Delete!', 'Press yes to delete this employee.')
    if msg == 'yes':
        sql = '''
            DELETE FROM Employees WHERE emp_id=?
        '''
        cursor.execute(sql, [emp_id])
        conn.commit()
        messagebox.showinfo("Admin", "Employee " +str(emp_id)+ " hasbeen updated successfully.")
        fetchEmployees()
        clearData()

def userLayout():
    pass

def treeviewClick(e):
    global emp_id
    emp = myEmpTree.item(myEmpTree.focus(), 'values')
    sql = '''
        SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_born, Employees.emp_address,
        Employees.emp_phone, Employees.emp_salary, Employees.emp_gender, Employees.emp_email, Departments.de_name
        FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id
        WHERE Employees.emp_status != "disable" AND Employees.emp_id = ?
    '''
    id = emp[0]
    cursor.execute(sql, [id])
    data = cursor.fetchone()
    clearData()

    if data != "":
        emp_id = data[0]
        label_id.config(text="ID : " + str(data[0]))
        emp_fname.insert(0, data[1])
        emp_lname.insert(0, data[2])
        emp_datepick.set_date(data[3])
        emp_address.insert("end", data[4])
        emp_phone.insert(0, data[5])
        emp_salary.insert(0, data[6])
        emp_gender.insert(0, data[7])
        emp_email.insert(0, data[8])
        emp_department.insert(0, data[9])
        btn_add.config(state="disabled")
        btn_update.config(state="normal")
        btn_delete.config(state="normal")

def clearData():
    btn_add.config(state="normal")
    btn_update.config(state="disabled")
    btn_delete.config(state="disabled")

    emp_fname.delete(0, END)
    emp_lname.delete(0, END)
    emp_datepick.set_date('01-01-2022')
    emp_address.delete(1.0, 'end')
    emp_phone.delete(0, END)
    emp_salary.delete(0, END)
    emp_department.delete(0, END)
    emp_gender.delete(0, END)
    emp_email.delete(0, END)
    emp_fname.focus_force()
    label_id.config(text="ID :")

def clearLoginEntry():
    userentry.delete(0, END)
    userentry.focus_force()
    pwdentry.delete(0, END)
    
def logoutClick() :
    empFrame.destroy()
    root.config(bg='lightblue',menu=emptyMenubar)
    root.config(bg='#28527a')
    loginlayout() #Show login
    clearLoginEntry()

def searchClick():
    global search_result

    myEmpTree.delete(*myEmpTree.get_children())

    # ค้นหาจากแผนก
    optiondata = findoption.get()
    if search_option.get() == "":
        fetchEmployees()
        messagebox.showwarning("Admin","Not found.")
    else:
        if optiondata == 'ID':
            sql = '''
                SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_phone, Employees.emp_email, Departments.de_name
                FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id
                WHERE Employees.emp_status != "disable" AND Employees.emp_id = ?
                ORDER BY Employees.emp_id DESC;
            '''
            cursor.execute(sql, [search_option.get()])
            search_result = cursor.fetchall()
        elif optiondata == 'Name':
            sql = '''
                SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_phone, Employees.emp_email, Departments.de_name
                FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id 
                WHERE Employees.emp_status != "disable" AND Employees.emp_fname LIKE ? OR Employees.emp_lname LIKE ?
                ORDER BY Employees.emp_id DESC
            '''
            cursor.execute(sql, [search_option.get(),search_option.get()])
            search_result = cursor.fetchall()
        elif optiondata == 'Department':
            sql_departments = "SELECT * FROM Departments"
            cursor.execute(sql_departments)
            departments = cursor.fetchall()
            department = ""
            for i,data in enumerate(departments):
                if data[1] == search_option.get():
                    department = data[0]

            sql = '''
                SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_phone, Employees.emp_email, Departments.de_name
                FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id 
                WHERE Employees.emp_status != "disable" AND Employees.emp_department = ?
                ORDER BY Employees.emp_id DESC
            '''
            cursor.execute(sql, [department])
            search_result = cursor.fetchall()

        elif optiondata == 'Gender':
            pass

        if search_result:
            for i, data in enumerate(search_result):
                myEmpTree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5]))

def onChange(e):
    optiondata = findoption.get()
    if optiondata == "Department":
        sql_de = "SELECT de_name FROM Departments"
        cursor.execute(sql_de)
        departments = cursor.fetchall()
        departmentList = []
        for i, data in enumerate(departments):
            departmentList.append(data[0])
        search_option['value'] = departmentList
    else:
        search_option['value'] = []

def my_display(offset):    
    limit = 5
    cursor.execute("SELECT count(*) as no FROM Employees")
    row = cursor.fetchone()
    no_rec = row[0]
    my_str = StringVar()
    sql = '''
        SELECT Employees.emp_id, Employees.emp_fname, Employees.emp_lname, Employees.emp_born, Employees.emp_address,
        Employees.emp_phone, Employees.emp_salary, Employees.emp_gender, Employees.emp_email, Departments.de_name
        FROM Employees INNER JOIN Departments ON Employees.emp_department = Departments.de_id
        WHERE Employees.emp_status != "disable"
        ORDER BY Employees.emp_id DESC LIMIT
    ''' + str(offset) + ''',''' + str(limit)

    cursor.execute(sql)
    result = cursor.fetchall()

    # q="SELECT * from student LIMIT "+ str(offset) +","+str(limit)
    # r_set=my_conn.execute(q)
    myEmpTree.delete(*myEmpTree.get_children())
    for i, data in enumerate(result):
            myEmpTree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5]))

    # Show buttons 
    back = offset - limit # This value is used by Previous button
    next = offset + limit # This value is used by Next button       
    b1 = Button(leftFrame, text='< Prev', command=lambda: my_display(back))
    b1.grid(row=1,column=0,sticky='news')
    b2 = Button(leftFrame, text='Next >', command=lambda: my_display(next))
    b2.grid(row=1,column=1,sticky='news')

    if(no_rec <= next): 
        b2["state"]="disabled" # disable next button
    else:
        b2["state"]="active"  # enable next button
        
    if(back >= 0):
        b1["state"]="active"  # enable Prev button
    else:
        b1["state"]="disabled"# disable Prev button 
    # for your understanding of how the offset value changes
    # query is displayed here, it is not part of the script 
    my_str.set("sql" + '\n' + "next: " + str(next) + "\n back:"+str(back))
    l1 = Label(leftFrame, textvariable=my_str)
    l1.grid(row=2,column=0)

def dataPicker():
    datePickerWindow = Toplevel(root)
    datePickerWindow.geometry("150x150")
    datePickerWindow.title("DatePicker")

w = 1400 #width of application
h = 750 #height of application

createconnection()
root = mainwindow()

userinfo = StringVar()
pwdinfo = StringVar()
img1 = PhotoImage(file='images/login.png').subsample(4,4)
img_m = PhotoImage(file='images/profile.png').subsample(3,3)
img_f = PhotoImage(file='images/profile_f.png').subsample(3,3)

loginlayout()

root.mainloop()
cursor.close() #close cursor
conn.close() #close database connection