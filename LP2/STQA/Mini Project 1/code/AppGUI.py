from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from tkintertable import *
from PIL import Image,ImageTk
from AppBackendMySQL import *


loggedIn=0
dbList=[]
tbList=[]
systemDataBase=['information_schema', 'chartdata', 'mysql', 'performance_schema', 'sys', 'fakesysdb']
userJaid=['contact', 'contactbookphp', 'cse', 'grampanchayat', 'lang2', 'language','student', 'tkinterapp']

def hello():
    showinfo("Title",message="Hello")


def enableWorkbenchMenu(flag):
    if flag:
        if (mainMenu.entrycget(1, "state") == DISABLED):
            mainMenu.entryconfigure(1, state=NORMAL)
        if (mainMenu.entrycget(2, "state") == DISABLED):
            mainMenu.entryconfigure(2, state=NORMAL)
    else:
        if (mainMenu.entrycget(1, "state") == NORMAL):
            mainMenu.entryconfigure(1, state=DISABLED)
        if (mainMenu.entrycget(2, "state") == NORMAL):
            mainMenu.entryconfigure(2, state=DISABLED)


def clearAllFrameWidgets(frame):
    for widget in frame.winfo_children():
        #widget.destroy()
        widget.pack_forget()


def loginApp(username, password):
    global loggedIn
    loggedIn = sql.connectToMySQLdb('localhost', username, password)
    if (loggedIn > 0):
        print("Login Success")
        showinfo("Login Status", "Success")
        enableWorkbenchMenu(1)
        homeTab()
    else:
        loggedIn=0
        print("Login Failed")
        showerror("Login Status", "Failed")
    return loggedIn


def loginWorkbench():
    clearAllFrameWidgets(WorkFrame)

    LoginFrame = LabelFrame(WorkFrame, text="Login")
    LoginFrame.pack()
    usernameLabel = Label(LoginFrame, text="Username")
    usernameLabel.grid(row=0,column=0,sticky="ew",padx=5,pady=10)
    usernameInput = Entry(LoginFrame, width=30)
    usernameInput.grid(row=0,column=1,sticky="ew",padx=5,pady=10)
    passwordLabel = Label(LoginFrame, text="Password")
    passwordLabel.grid(row=1,column=0,sticky="ew",padx=5,pady=10)
    passwordInput = Entry(LoginFrame, width=30, show="\u2022")
    passwordInput.grid(row=1,column=1,sticky="ew",padx=5,pady=10)
    loginButton = Button(LoginFrame, text="Login", command=lambda: loginApp(usernameInput.get(), passwordInput.get()))
    loginButton.grid(row=2,column=1,sticky="ew",padx=5,pady=10)


def homeTab():
    clearAllFrameWidgets(WorkFrame)
    HomeFrame = LabelFrame(WorkFrame, text="Home\n"+serverMsg + " Connection Id:{} \n WELCOME TO WORKBENCH".format(loggedIn))
    HomeFrame.pack(fill=BOTH, expand=1,padx=20,pady=20)
    Information = "MySQL Workbench\n It comes with SQL Database Exploration Features,\n To Work this Application on your Machine" \
                  " you need to have SQL Server running on PORT NO:3306 before\n Enjoy GUI features of MySQL Workbench Project"
    messageSTR.set("LP2 mini project"+"\n"+Information)
    detailsLabel = Label(HomeFrame, textvariable=messageSTR)
    detailsLabel.pack(fill=BOTH, expand=1)
    #AppImage=ImageTk.PhotoImage(Image.open("mysqlworkbenchPNG.png"))
    #AppImage = PhotoImage(file="mysqlworkbenchPNG.png")
    #AppImage = ImageTk.PhotoImage(getPNGimage("mysqlworkbenchPNG.png"))
    #JPGImage=Image.open("mysqlworkbenchJPG.jpg")
    #AppImage=ImageTk.PhotoImage(JPGImage)
    '''
    imageLabel=Label(HomeFrame,image=PhotoImage(file="mysqlworkbenchPNG.png"))
    imageLabel.pack(fill=BOTH,expand=1)
    
    canvas = Canvas(HomeFrame, width=300, height=300)
    canvas.pack(fill=BOTH, expand=1)
    img = PhotoImage(file="mysqlworkbenchPNG.png")
    canvas.create_image(20, 20, anchor=NW, image=img)'''


def databasesTab():
    clearAllFrameWidgets(WorkFrame)
    workframeTitleVar.set(serverMsg + " Connection Id:{} \n Databases".format(loggedIn))
    databaseLabel= Label(WorkFrame, textvariable=workframeTitleVar)
    databaseLabel.pack()

    tableLayout = Notebook(WorkFrame)
    generalTab = Frame(tableLayout)
    generalTab.pack(fill=BOTH)
    tableLayout.add(generalTab, text="GENERAL")
    tableLayout.pack(fill=BOTH)

    showgeneralTab(generalTab)
    #Create new DB,TB,InsertData


def showgeneralTab(generalTab):
    dbList = sql.showdatabases()
    tbList=[]

    selectDB=StringVar()
    dbListOptions=["Choose Database"]+dbList
    dbDropdownList=OptionMenu(generalTab,selectDB,*dbListOptions)
    dbDropdownList.grid(row=0,column=0,sticky="ew")
    dbDropdownList.config(width=20)

    tree = Treeview(generalTab, show='headings', selectmode='browse')


    getDbButton=Button(generalTab,text="Select Database",width=20,command=( lambda : getDb(generalTab,selectDB,tbList,tree)))
    getDbButton.grid(row=1,column=0,sticky="ew")
    #
    delDbButton = Button(generalTab, text="Delete Database", width=20,command=( lambda : deleteDB(generalTab,selectDB)) )
    delDbButton.grid(row=2, column=0, sticky="ew")


def deleteDB(generalTab,selectDB):
    if selectDB.get() in sql.showdatabases():
        if (selectDB.get() not in systemDataBase) and (selectDB.get() not in userJaid):
            if(askyesno("Delete Database?","Are you Sure?\nIt will permenently DELETE DATABASE : "+selectDB.get()+" !!!")):
                sql.dropdatabase(selectDB.get())
                print("DELETED db :"+selectDB.get()+" Now new DBLIST :",sql.showdatabases())
                showgeneralTab(generalTab)
        else:
            showerror("SYSTEM DATABASES","You tried to delete SYS Databases from your server.\nCannot Delete : "+selectDB.get())


def getDb(generalTab,selectDB,tbList,tree):
    print(selectDB.get())
    if(sql.usedb(selectDB.get())):
        tbList=sql.showtables(selectDB.get())
    else:
        tbList=[]

    selectTB = StringVar()
    tbListOptions = ["Choose Table"] + tbList
    tbDropdownList = OptionMenu(generalTab, selectTB, *tbListOptions)
    tbDropdownList.grid(row=0, column=1, sticky="ew")
    tbDropdownList.config(width=20)
    getTbButton = Button(generalTab, text="Select Table", width=20, command=(lambda: getTb(generalTab,selectDB,selectTB,tree)))
    getTbButton.grid(row=1, column=1, sticky="ew")

    delTbButton = Button(generalTab, text="Delete Table", width=20,command=(lambda: deleteTb(generalTab,selectDB,selectTB)))
    delTbButton.grid(row=2, column=1, sticky="ew")

def deleteTb(generalTab,selectDB,selectTB):
    if selectDB.get() in sql.showdatabases():
        if (selectDB.get() not in systemDataBase) and (selectDB.get() not in userJaid):
            if (askyesno("Delete Table?","Are you Sure?\nIt will permenently DELETE TABLE : " + selectDB.get() + ">"+selectTB.get()+" !!!")):
                if(sql.droptable(selectDB.get(),selectTB.get())):
                    print("DEL : "+"Database :"+selectDB.get()+", Table :"+selectTB.get())
                    showgeneralTab(generalTab)
        else:
            showerror("SYSTEM TABLES","You tried to delete TABLE from SYS Databases from your server.\nCannot Delete : " + selectDB.get())
            print("ERROR:"+"Database :" + selectDB.get() + ", Table :" + selectTB.get())

def getTb(generalTab,selectDB,selectTB,tree):
    for i in tree.get_children():
        tree.delete(i)
    tree.grid_forget()

    print(selectTB.get())
    rows = sql.showAllTableDataFetchall(selectDB.get(), selectTB.get())
    columnTuple=None
    colname=[]
    describeTB=sql.describetable(selectDB.get(),selectTB.get())
    for i in range(1,len(describeTB)):
        field=describeTB[i].split("\t")
        colname.append(field[0])
    totalColumn=len(colname)
    templist=[]

    for i in range(0,totalColumn):
        templist.append("c"+str(i+1))
    columnTuple=tuple(templist)


    tree['column']=columnTuple
    for i in range(0,totalColumn):
        tree.column("#"+str(i+1), anchor=CENTER,width=100,minwidth=5, stretch=NO)
        tree.heading("#"+str(i+1), text=colname[i])

    tree.grid(row=3,column=3)

    vsb = Scrollbar(generalTab, orient="vertical", command=tree.yview)
    vsb.grid(row=3,column=2,sticky="ns")
    hsb = Scrollbar(generalTab, orient="horizontal", command=tree.xview)
    hsb.grid(row=4, column=3, sticky="ew")
    tree.configure(yscrollcommand=vsb.set)
    tree.configure(xscrollcommand=hsb.set)
    for row in rows:
        print(row)
        tree.insert("", END, values=row)

    tempDes=""
    for des in describeTB:
        tempDes=tempDes+des+"\n"

    treeDes="TABLE DATA:\n"+tempDes
    lb=Label(generalTab,text=".")
    lb.grid(row=3,column=4)


def SQLshellTab():
    clearAllFrameWidgets(WorkFrame)
    workframeTitleVar.set(serverMsg + " Connection Id:{} \n SQL Shell".format(loggedIn))
    SQLshellLabel = Label(WorkFrame, textvariable=workframeTitleVar)
    SQLshellLabel.pack(fill=X)
    WorkFrame.pack(fill=BOTH, expand=True)
    shellFrame=Frame(WorkFrame)
    shellFrame.pack(fill=BOTH,expand=1)

    QueryArea=Text(shellFrame, font="lucida 13", wrap=NONE)
    QueryArea.pack(anchor="nw",side=TOP,fill=BOTH,expand=1)
    ytextScroll = Scrollbar(QueryArea)
    ytextScroll.pack(anchor="e",side=RIGHT,fill=Y)
    ytextScroll.config(command=QueryArea.yview)
    xtextScroll = Scrollbar(QueryArea, orient='horizontal')
    xtextScroll.pack(anchor="s",side=BOTTOM,fill=X)
    xtextScroll.config(command=QueryArea.xview)
    QueryArea.config(yscrollcommand=ytextScroll.set, xscrollcommand=xtextScroll.set)

    SelectQuery = Button(shellFrame, text="Select",command=(lambda : selectQuery(QueryArea)))
    SelectQuery.pack(side=LEFT,padx=20,pady=15)

    InsertQuery = Button(shellFrame, text="Insert",command=(lambda : insertQuery(QueryArea)))
    InsertQuery.pack(side=LEFT,padx=20,pady=15)

    UpdateQuery = Button(shellFrame, text="Update",command=(lambda : updateQuery(QueryArea)))
    UpdateQuery.pack(side=LEFT,padx=20,pady=15)

    DeleteQuery = Button(shellFrame, text="Delete",command=(lambda : deleteQuery(QueryArea)))
    DeleteQuery.pack(side=LEFT,padx=20,pady=15)

    ClearTextQuery = Button(shellFrame, text="Clear",command=(lambda : clearQuery(QueryArea)))
    ClearTextQuery.pack(side=LEFT,padx=20,pady=15)

    RunQuery = Button(shellFrame, text="Run",command=(lambda : runQuery(QueryArea)))
    RunQuery.pack(side=LEFT,padx=20,pady=15)


def runQuery(QueryArea):
    userQuery=""
    userQuery=str(QueryArea.get(1.0,END))
    uq=userQuery.split("\n")
    if uq[0]!="":
        userQuery = uq[0]
        if(askyesno(title="Sure to Execute Query",message="Execute\n"+userQuery+" ?")):
            print(userQuery)
            #PASS TO BACKEND
            sql.UserQuery(userQuery)
            QueryArea.delete(1.0, END)
    else:
        showwarning(title="Empty Query",message="\t SORRY \n We cannot execute Empty Query\n OR Nothing found to execute / 1st Line left blank\n\nYour Query:\n"+userQuery)


def selectQuery(QueryArea):
    showinfo("SELECT Query info","To select from a table in MySQL, use the \"SELECT\" statement")
    selectQ=StringVar()
    selectQ.set("SELECT * FROM `tableName` WHERE 1")
    QueryArea.delete(1.0, END)
    QueryArea.insert(END, selectQ.get())


def insertQuery(QueryArea):
    showinfo("INSERT Query info", "To fill a table in MySQL, use the \"INSERT INTO\" statement.")
    insertQ=StringVar()
    insertQ.set("INSERT INTO `tableName`(`col1`, `col2`) VALUES ([value-1],[value-2])")
    QueryArea.delete(1.0, END)
    QueryArea.insert(END, insertQ.get())


def updateQuery(QueryArea):
    showinfo("UPDATE Query info", "You can update existing records in a table by using the \"UPDATE\" statement")
    updateQ=StringVar()
    updateQ.set("UPDATE `tableName` SET `col1`=[value-1],`col2`=[value-2] WHERE 1")
    QueryArea.delete(1.0, END)
    QueryArea.insert(END, updateQ.get())


def deleteQuery(QueryArea):
    showinfo("DELETE Query info", "You can delete records from an existing table by using the \"DELETE FROM\" statement")
    deleteQ=StringVar()
    deleteQ.set("DELETE FROM `tableName` WHERE 0")
    QueryArea.delete(1.0, END)
    QueryArea.insert(END, deleteQ.get())


def clearQuery(QueryArea):
    userQuery = ""
    userQuery = str(QueryArea.get(1.0, END))
    uq = userQuery.split("\n")
    if uq[0] != "":
        if(askokcancel("CLEAR Query","Sure! you want to <CLEAR> the Query.\nYou Typed in Shell")):
            QueryArea.delete(1.0, END)
    else:
        showwarning("CLEAR ?","Nothing found to clear / 1st Line left blank\n\nYour Query:\n"+userQuery)


def getPNGimage(image):
    PIL_image = Image.open(image)
    width = 100
    height = 100
    use_resize = True
    if use_resize:
        # Image.resize returns a new PIL.Image of the specified size
        PIL_image_small = PIL_image.resize((width, height), Image.ANTIALIAS)
    else:
        # Image.thumbnail converts the image to a thumbnail, in place
        PIL_image_small = PIL_image
        PIL_image_small.thumbnail((width, height), Image.ANTIALIAS)
    return  PIL_image_small


def aboutGUI():
    Information="MySQL Workbench\n It comes with SQL Database Exploration Features,\n To Work this Application on your Machine" \
                " you need to have SQL Server running on PORT NO:3306 before\n Enjoy GUI features of MySQL Workbench Project"
    showinfo("About MySQL Workbench",Information)


def exitGUI():
    if(askyesno("Are you Sure?","You really want to Close / Exit from MySQL Workbench")):
        if(loggedIn!=0):
            sql.closeConnection()
        app.destroy()


if __name__ == '__main__':
    sql = MYSQL()
    app = Tk()
    app.geometry("1350x420")
    app.wm_minsize(width=985,height=420)
    app.title("MySQL Workbench")
    app.wm_iconbitmap("mysqlworkbench.ico")
    app.protocol("WM_DELETE_WINDOW", exitGUI)

    # VARIBLES NEEDED
    workframeTitleVar = StringVar()
    messageSTR=StringVar()
    serverMsg = "Server : MySQL:3306"

    #FRAMES NEEDED
    WorkFrame = Frame(app)
    WorkFrame.pack(fill=BOTH)


    #MENU BAR SETTINGS
    mainMenu = Menu(app)

    databaseMenu = Menu(mainMenu, tearoff=0)
    databaseMenu.add_command(label="SQL Database", command=databasesTab)

    sqlMenu = Menu(mainMenu, tearoff=0)
    sqlMenu.add_command(label="SQL Shell", command=SQLshellTab)

    helpMenu = Menu(mainMenu, tearoff=0)
    helpMenu.add_command(label="About App", command=aboutGUI)
    helpMenu.add_command(label="Exit", command=exitGUI)

    mainMenu.add_cascade(label="Databases", menu=databaseMenu)
    mainMenu.add_cascade(label="SQL", menu=sqlMenu)
    mainMenu.add_cascade(label="Help", menu=helpMenu)
    app.config(menu=mainMenu)

    #EXECUTION FLOW
    enableWorkbenchMenu(0)
    loginWorkbench()

    app.mainloop()