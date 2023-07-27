from subprocess import call
from tkinter import *
import tkinter.messagebox
from time import sleep
import mysql.connector as sql
class CallPy():
    def __init__(self):
        pass
    def __python__(self,txt):
        call(['Python','{}'.format(txt)])
def Edit(a):
    global mycursor
    global db
    pathy=CallPy()
    global dep
    dep=Tk()
    dep.geometry('1000x450')
    dep.resizable(False,False)
    global userid
    global password
    def datadelete(username,password):
        statement=f'''DELETE FROM username WHERE (name = '{username}');'''
        mycursor.execute(statement)
        db.commit()
        mycursor.execute(f'DROP TABLE {username};')
        pathy.__python__('project.py')
    def editing(username,password):
        dep=Tk()
        global location
        global file_name
        def changes():
            global location
            global file_name
            locationaka=location.get('1.0','end-1c')
            file= open('nouse.txt','w')
            file.write(locationaka)
            file.close()
            file = open('nouse.txt','r')
            locationaka=file.readlines()
            file.close()
            file= open('nouse.txt','w')
            file.write(file_name.get('1.0','end-1c'))
            file.close()
            file = open('nouse.txt','r')
            file_name=file.readlines()
            file.close()
            tablecontent=list()

            for i in range(len(locationaka)):
                if locationaka[i]==None:
                    locationaka.pop(i)
            for i in range(len(file_name)):
                if file_name[i]==None:
                    file_name.pop(i)
            for i in range(len(locationaka)):
                if i<len(file_name):
                    locationaka[i]=locationaka[i][:-1]
                    file_name[i]=file_name[i][:-1]
                    tablecontent.append((locationaka[i],file_name[i]))
                else:
                    locationaka[i]=locationaka[i][:len(locationaka[i])-1]
                    tablecontent.append((locationaka[i],locationaka[i].split('\\')[-1].split('.')[0]))

            statement=f'''DELETE FROM username WHERE (name = '{username}');'''
            mycursor.execute(statement)
            db.commit()
            mycursor.execute(f'DROP TABLE {username};')
            try:
                mycursor.execute('INSERT INTO username(name,password) VALUES (%s,%s)',(username,password))
                db.commit()
                mycursor.execute(f'CREATE TABLE {username}(file_location VARCHAR(100) NOT NULL PRIMARY KEY,file_name VARCHAR(100));')
                db.commit()
            except:
                print('hello')
            sleep(1)
            for x in tablecontent:
                try:
                    mycursor.execute(f'INSERT INTO {username}(file_location,file_name) VALUE (%s,%s)',x)
                    db.commit()
                except:
                    pass
            dep.destroy()
            pathy.__python__('project.py')

        if password==None:
            password='0'

        dep.title('Project File manipulation')
        dep.geometry('1170x600')
        text = Label(dep,text = 'Project Management',font=('Times', 30, 'bold'),justify=CENTER,border=2,background='whitesmoke')
        text.pack()
        userid = Label(dep,text=username,font=('Times', 18, 'italic'),borderwidth=2,background='whitesmoke')
        userid.place(x=163,y=90)
        pword = Label(dep,text=password,font=('Times', 18, 'italic'),borderwidth=2,background='whitesmoke')
        pword.place(x=808,y=90)
        userlabel = Label(dep,text = 'Username:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        userlabel.place(x=50,y=90)
        passlabel = Label(dep,text = 'Password:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        passlabel.place(x=700,y=90)
        mycursor.execute(f'SELECT * FROM {username};')
        data=mycursor.fetchall()
        filenames=[x[1] for x in data]
        filelocation=[x[0] for x in data]
        file_name=Text(dep,width = 50,height= 15,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
        for i in filenames:
            file_name.insert(END,i+'\n')
        file_name.place(x=700,y=200)
        location=Text(dep,borderwidth=2,wrap= 'char',relief='groove',width = 70,height= 15,background='whitesmoke' )
        for i in filelocation:
            location.insert(END,i+'\n')

        location.place(x=30,y=200)
        change=Button(dep,text='Change',font=('Times',15,'bold'),command=lambda : changes())
        change.place(x=1025,y=470)
        records1=Label(text='Enter file location',font=('Times',18,'bold'))
        records1.place(x=30,y=167)
        records2=Label(text='Enter file name',font=('Times',18,'bold'))
        records2.place(x=700,y=167)

        dep.mainloop()
    def information(a):
        global dep
        global userid
        global password
        mycursor.execute('SELECT * FROM username;')
        data = mycursor.fetchall()
        userid = userid.get('1.0','end-1c')
        password = password.get('1.0','end-1c')
        if (userid,password) in data:
            if a==True:
                dep.destroy()
                editing(userid,password)
            elif a == False:
                dep.destroy()
                datadelete(userid,password)
            
        else:
            dep.destroy()
            Edit(False)
    text = Label(dep,text = 'Project Management',font=('Times', 30, 'bold'),justify=CENTER,border=2,background='whitesmoke')
    text.pack()
    userlabel = Label(dep,text = 'Username:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
    userlabel.place(x=190,y=90)
    passlabel = Label(dep,text = 'Password:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
    passlabel.place(x=190,y=190)
    userid = Text(dep,width = 50,height= 5,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
    userid.place(x=320,y=70)
    if a==False:
        allert=Label(dep,text = '(Incorrect Details)',fg='red',font=('Times', 10, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        allert.place(x=320,y=155)
    password = Text(dep,width = 50,height= 3,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
    password.place(x=320,y=180)
    enter = Button(dep,text = 'Procced',width=15,relief='sunken',bd=1, command = lambda: information(True))
    enter.place(x=320,y=290)
    enter = Button(dep,text = 'Delete',width=15,relief='sunken',bd=1, command = lambda: information(False))
    enter.place(x=610,y=290)
def dataenter(a):
    global mycursor
    global db
    def end():
        pathy= CallPy()
        pathy.__python__('project.py')

    def start():
        global userid
        global password
        global filen_ame
        global location
        dep=Tk()
        dep.title('Project File manipulation')
        dep.geometry('1170x600')
        def entery():
            global userid
            global password
            global filen_ame
            global location
            userid=userid.get('1.0','end-1c')
            password=password.get('1.0','end-1c')
            filen_ame=filen_ame.get('1.0','end-1c')
            location=location.get('1.0','end-1c')
            a=open('nouse.txt','w')
            a.write(location)
            a.close()
            a=open('nouse.txt','r')
            location=a.readlines()
            a.close()
            a=open('nouse.txt','w')
            a.write(filen_ame)
            a.close()
            a=open('nouse.txt','r')
            file_name=a.readlines()
            a.close()
            mycursor.execute('SELECT name FROM username')
            names=mycursor.fetchall()
            if (userid,) in names or userid=='nishant':
                dep.destroy()
                dataenter(False)
            mycursor.execute('INSERT INTO username(name,password) VALUES (%s,%s)',(userid,password))
            db.commit()
            mycursor.execute(f'CREATE TABLE {userid}(file_location VARCHAR(100) NOT NULL,file_name VARCHAR(100),PRIMARY KEY(file_location));')
            db.commit()
            for x in range(len(location)):
                if location[x]==None:
                    location.pop(x)
            for x in range(len(file_name)):
                if file_name[x]==None:
                    file_name.pop(x)
            for x in range(len(location)):
                mycursor.execute(f'INSERT INTO {userid}(file_location,file_name) VALUE (%s,%s)',(location[x][:-1],file_name[x][:-1]))
                db.commit()
            dep.destroy()
            end()
        text = Label(dep,text = 'Project Management',font=('Times', 30, 'bold'),justify=CENTER,border=2,background='whitesmoke')
        text.pack()
        userlabel = Label(dep,text = 'Username:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        userlabel.place(x=250,y=90)
        passlabel = Label(dep,text = 'Password:',font=('Times', 18, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        passlabel.place(x=250,y=190)
        userid = Text(dep,width = 50,height= 5,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
        userid.place(x=380,y=70)
        if a==False:
            allert=Label(dep,text = '(Choose another username)',fg='red',font=('Times', 10, 'italic'),justify=CENTER,border=2,background='whitesmoke')
            allert.place(x=380,y=155)
        password = Text(dep,width = 50,height= 3,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
        password.place(x=380,y=180)
        filen_ame=Text(dep,width = 50,height= 15,borderwidth=2,wrap ='char',relief='groove',background='whitesmoke')
        ScrollText = Scrollbar(dep,orient='vertical',command=filen_ame.yview)
        filen_ame.place(x=700,y=330)
        filen_ame['yscrollcommand']=ScrollText.set
        location=Text(dep,borderwidth=2,wrap= 'char',relief='groove',width = 50,height= 15,background='whitesmoke' )
        scrolllabel = Scrollbar(dep,orient='vertical',command=location.yview)
        location['yscrollcommand']=scrolllabel.set
        location.place(x=30,y=330)
        enter=Button(dep,text='procced',font=('Times',15,'bold'),command= entery)
        enter.place(x=380,y=250)
        records1=Label(text='Enter file location',font=('Times',18,'bold'))
        records1.place(x=30,y=297)
        records2=Label(text='Enter file name',font=('Times',18,'bold'))
        records2.place(x=700,y=297)

        dep.mainloop()

    start()
def wrong():
    pathy = CallPy()
    iExit = tkinter.messagebox.askyesno("YOU HAVE ENTERED WRONG USERNAME",
                                            "TO CONTINUE PRESS YES NO FOR LOGIN WITH NEW USERNAME")
    if iExit>0:
        page.destroy()
        login.destroy()
        pathy.__python__('project.py')
    else:
        page.destroy()
        login.destroy()
        dataenter(True)
def datas():
    global mycursor
    global db
    project = Tk()
    files = list()
    statement=f'SELECT * FROM {pb}'
    mycursor.execute(statement)
    files = mycursor.fetchall()
    def display(rea):
        pathy = CallPy()
        print(rea)
        project.destroy()
        pathy.__python__(rea)
        pathy.__python__('project.py')
    btn=list()
    i = 0
    project.title(pb)
    for k in range(len(files)):
            btn.append(Button(project,
                              width=18,
                              height=2,
                              bg='black',
                              fg='white',
                              font=('Helvetica', 15, 'bold'),
                              bd=4, text=files[k][1]))

    
            # set buttons in row & column and
            # separate them with a padding of 1 unit
            btn[i].pack()
    
            # put that number as a symbol on that button
            btn[i]["command"] = lambda x=files[k][0]: display(x)
            i += 1
    project.resizable= (False,False)
    project.mainloop()
def datadmin():
    global mycursor

    global db
    page.destroy()
    login.destroy()
    project = Tk()
    project.title('ADMIN SALUTE')
    def display(rea):
        pathy=CallPy()
        project.destroy()
        pathy.__python__(rea)
        pathy.__python__('project.py')
    btn=list()
    try:
        mycursor.execute('DROP TABLE admin;')
        db.commit()
    except:
        pass
    mycursor.execute('CREATE TABLE admin(PROGRAM VARCHAR(100) NOT NULL PRIMARY KEY,PROGRAM_NAME VARCHAR(100));')
    db.commit()
    mycursor.execute('SELECT * FROM username')
    users=mycursor.fetchall()
    for i in users:
        mycursor.execute(f'SELECT * FROM {i[0]}')
        inform=mycursor.fetchall()
        for t in inform:
            try:
                mycursor.execute(f'INSERT INTO admin(PROGRAM,PROGRAM_NAME) VALUE (%s,%s)',t)
                db.commit()
            except:
                pass
    mycursor.execute('SELECT * FROM admin')
    files = mycursor.fetchall()
    for k in range(len(files)):
            btn.append(Button(project,
                              width=18,
                              height=2,
                              bg='black',
                              fg='white',
                              font=('Helvetica', 15, 'bold'),
                              bd=4, text=files[k][1]))
    
            # set buttons in row & column and
            # separate them with a padding of 1 unit
            btn[k].pack()
    
            # put that number as a symbol on that button
            btn[k]["command"] = lambda x=files[k][0]: display(x)
    project.resizable= (False,False)
    project.mainloop()
def project(a):
    global mycursor
    global db
    run = CallPy()
    global login
    global page
    login = Tk()
    login.title('Login Page')
    page = Frame(login)
    login.geometry('450x450')
    login.resizable(False,False)
    page.grid()
    title = Label(page,text = 'Enter Your USERNAME',font = ('Times',25,'italic'))
    title.grid(row = 0,column =0,padx=40,pady=(60,40))
    def dataenter1():
        login.destroy()
        dataenter(True)
    def Edit1():
        login.destroy()
        Edit(True)
    if a==False:
        alert=Label(login,text = '(Incorrect username)',fg='red',font=('Times', 10, 'italic'),justify=CENTER,border=2,background='whitesmoke')
        alert.place(x=20,y=230)
    def data():
        global pb
        pb = txt.get('1.0','end-1c')
        mycursor.execute('SELECT name FROM username')
        a = mycursor.fetchall()
        a = [a[x][0] for x in range(len(a))]
        print('test')
        if pb=='nishant':
            print('ADMIN')
            datadmin()
        elif pb in a:
            page.destroy()
            login.destroy()
            datas()
        else:
            login.destroy()
            project(False)
    txt = Text(page,width = 45,bd=1,height=4,relief='sunken',font=('calibri',13))
    txt.grid(row = 1,column = 0,padx=(20,0))
    data_enter=Button(login,text = 'Register',fg='blue',width=25, command = lambda: dataenter1())
    data_enter.place(x=30,y=400)
    edit=Button(login,text = 'Sign in',fg='blue',width=25, command = lambda: Edit1())
    edit.place(x=250,y=400)
    enter = Button(page,text = 'Enter',width=15,relief='sunken',bd=1, command = lambda: data())
    enter.grid(row=2,column = 0,pady=30)
    login.mainloop()
if __name__=='__main__':
    try:
        db = sql.connect(host = 'localhost',user = 'root',passwd='040305ma' ,database='CS_Projects')
    except:
        db= sql.connect(host = 'localhost',user = 'root',passwd='040305ma')
        my=db.cursor()
        my.execute('CREATE DATABASE CS_Projects;')
        db.commit()
        db = sql.connect(host = 'localhost',user = 'root',passwd='040305ma' ,database='CS_Projects')
        my=db.cursor()
        my.execute('CREATE TABLE username(name VARCHAR(100) NOT NULL PRIMARY KEY,password VARCHAR(100));')
        db.commit()
    mycursor = db.cursor()
    project(True)