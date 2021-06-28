import sqlite3
##from sqlite3 import Error
import datetime

def create_connection(dbase):
    conn = None
    try:
        conn = sqlite3.connect(dbase)
        return conn
    except Error as e:
        print(e)
    return conn

def close_connection(conn):
    try:
        if conn:
           conn.close()
           conn = None
    except Error as e:
        print("error in operation close connection")
        print(e)        
    return 0

def search_book(dbase, title):
    try:
        conn = create_connection(dbase)
        cur=conn.cursor()
        cur.execute("SELECT * from books where title = ?",(title))
        record = cur.fetchall()
        if (len(record[0]) == 0):
            print("book not found")
        else:
            for row in record:
                print(row[0])
            close_connection(conn)
    except Error as e:
        print("error in operation search book")
        print(e)  

def display_books(dbase,searchType):
    try:
        conn = create_connection(dbase)
        cur=conn.cursor()
        if searchType == "Available":
            cur.execute("SELECT  * from books where status = 'Available'")
        elif searchType == "Rented":
            cur.execute("SELECT  * from books where status = 'Rented'")
        else:
            cur.execute("SELECT  * from books")    
        booklist = cur.fetchall()
        for record in booklist:
            print(record)
        close_connection(conn)        
    except Error as e:
        print("error in operation close connection")
        print(e)  

def display_users(dbase):
    try:
        conn = create_connection(dbase)
        cur=conn.cursor()

        cur.execute("SELECT  * from userDetails ")    
        booklist = cur.fetchall()
        for record in booklist:
            print(record)
        close_connection(conn)        
    except Error as e:
        print("error in operation close connection")
        print(e)  

def display_books_user(dbase,userId):
    try:
        conn = create_connection(dbase)
        cur=conn.cursor()
        sql="SELECT bk.book_id, bk.title from books bk INNER JOIN rental rr ON rr.book_id = bk.book_id and bk.status='Rented' and rr.user_id = ?"""
        cur.execute(sql,[userId])
        booklist = cur.fetchall()
        for record in booklist:
            print(record)
        close_connection(conn)        
    except Error as e:
        print("error in operation close connection")
        print(e) 
            
def add_book(dbase, bkTitle,pubName,bkAuthor):
    try:
        conn = create_connection(dbase)
        cur=conn.cursor()
        bkstatus="Available"
        cur.execute("INSERT INTO books VALUES (null,?,?,?,?)",(bkTitle,pubName,bkAuthor,bkstatus))
        conn.commit()
        close_connection(conn)
    except Error as e:
        print("error in operation add_book")
        print(e)
        conn.rollback()
        close_connection(conn)

def create_login(dbase, loginId, passWord, userId):
    try:       
       conn=create_connection(dbase)
       cur = conn.cursor()
       cur.execute("INSERT INTO userLogin VALUES (null,?,?,?)",(loginId, passWord, userId))
       conn.commit()
       close_connection(conn)
    except sqlite3.Error as e:
        print(e)
        print ("error in operation create_login")
        conn.rollback()
        close_connection(conn)

def checkLoginId(dbase,loginId):
    try:
        userId=1
        conn=create_connection(dbase)
        cur = conn.cursor()               
        cur.execute("SELECT  user_id from userLogin where login_id =?",[loginId])         
        record = cur.fetchone()[0]
        if len(record) != 0:
              userId=record
        close_connection(conn)
        return userId
    except sqlite3.Error as error:
       print ("error in operation checkLoginId")
       close_connection(conn)

def checkPassword(dbase,loginId, passWord):
    try:
        status=1
        conn=create_connection(dbase)
        cur = conn.cursor()
        sql="""SELECT login_id,login_password from userLogin where login_id = ?"""
        cur.execute(sql,[loginId])
        record = cur.fetchone()[1]
        if len(record) != 0:
            if record == passWord:
                status=0
        close_connection(conn)
        return status
    except sqlite3.Error as error:
       print ("error in operation checkPassword")
       close_connection(conn)

def checkUserType(dbase,userId):
    try:
        userType="user"
        #default to User incase of issue.
        conn=create_connection(dbase)
        cur = conn.cursor()
        cur.execute("SELECT user_type from userDetails where user_id = ?",(userId))
        booklist = cur.fetchall()
        for record in booklist:
            print(record)
            userType=record[0]
        close_connection(conn)
        return userType
    except sqlite3.Error as error:
       print ("error in operation checkUserType")
       close_connection(conn)       
       
       
def checkoutBook(dbase, userId, bookId):
    try:
        conn=create_connection(dbase)
        cur = conn.cursor()
        bkstatus="Available"
        cur.execute("SELECT status from books where book_id = ?",(bookId))
        record = cur.fetchone()[0]
        print("CheckOut ",record)
        if record == bkstatus:
            myDate=datetime.date.today()
            aDate=myDate.strftime('%Y-%m-%d')
            print("aDate ",aDate)
            bkstatus="Active"
            cur.execute("INSERT INTO rental VALUES (null,?,null,null,?,?,?)",(aDate,bkstatus,bookId,userId))
            cur.execute("UPDATE books SET status = 'Rented' WHERE book_id= ?",(bookId))
            conn.commit()               
        close_connection(conn)
    except sqlite3.Error as error:
       print ("error in checkoutBook")
       conn.rollback()
       close_connection(conn)

def checkinBook(dbase, bookId, userId):
    try:
        fineAmt=0
        conn=create_connection(dbase)
        cur = conn.cursor()
        cur.execute("SELECT rental_id, start_rental_date from rental where book_id = ? and user_id = ?",(bookId, userId))
        record = cur.fetchone()
        if record is None:
            print("rental not found")
        else:
            rentalId=record[0]
            rental_start_date = record[1]
            myDate=datetime.date.today()
            aDate=myDate.strftime('%Y-%m-%d')
            cur.execute("UPDATE rental SET return_date =?, rental_status = ? WHERE rental_id= ?",(aDate,'Inactive',rentalId))           
            cur.execute("UPDATE books SET status = ? WHERE book_id=?",('Available',bookId))
            #check if a fine is due

            cur.execute("SELECT (strftime(?, return_date) - strftime(?, start_rental_date)) / 86400.0 FROM rental where rental_id = ?",("""%s""", """%s""", rentalId))
            record = cur.fetchone()[0]
            if record != None:
                if record != 0:
                    if (record > 19) and (record <20):
                        print("send message to ", userId, " that book, ", bookId, " is over due")
                    elif (record >= 20):
                        fineAmt=0
                        OverDueDays=int(record)-20
                        NumMultiples=int(OverDueDays)//5
                        for index in range(0,NumMultiples):
                            fineAmt=int(fineAmt) + 20 + (5 * index)
                        cur.execute("UPDATE rental SET Fine =? WHERE rental_id= ?",(fineAmt,rentalId))
                    else:
                        cur.execute("UPDATE rental SET Fine =? WHERE rental_id= ?",('0',rentalId))                   
        conn.commit()
        close_connection(conn)
        return fineAmt
    except sqlite3.Error as error:
       print ("error in checkin Book")
       print(error)
       conn.rollback()
       close_connection(conn)

              
def add_user(dbase,firstName,lastName,emailAddress,phoneNum,userRole):
    try:
        conn=create_connection(dbase)
        cur=conn.cursor()
        cur.execute("INSERT INTO userDetails VALUES (null,?,?,?,?,?)", (firstName,lastName,emailAddress,phoneNum,userRole))
        sql='SELECT user_id from userDetails where email_address = ?'
        cur.execute(sql,[emailAddress])         
        userId = cur.fetchone()[0]
        conn.commit()
        close_connection(conn)
        return userId
    except sqlite3.Error as e:
       print(e) 
       print ("error in operation add_user")
       conn.rollback()
       close_connection(conn)

def update_login(dbase, loginId,attrib,newVal):
    try:
        conn=create_connection(dbase)
        cur=conn.cursor()
      
        if attrib == "4":
            cur.execute("UPDATE userLogin SET login_id =? WHERE login_id= ?",(newVal,loginId))          
        elif attrib == "5":    
            cur.execute("UPDATE userLogin SET login_password =? WHERE login_id= ?",(newVal,loginId))
        else:
            print("invalid Option Selected")
        conn.commit()
        close_connection(conn)
    except sqlite3.Error as e:
       print(e) 
       print ("error in operation add_user")
       conn.rollback()
       close_connection(conn)
    

def update_user(dbase,loginId,attrib,newVal):
    try:
        conn=create_connection(dbase)
        cur=conn.cursor()

        sql='SELECT user_id from userlogin where login_id = ?'
        cur.execute(sql,[loginId])         
        userId = cur.fetchone()[0]
        
        if attrib == "1":    
            cur.execute("UPDATE userDetails SET first_name =? WHERE user_id= ?",(newVal,userId))
        elif attrib == "2":
            cur.execute("UPDATE userDetails SET last_name =? WHERE user_id= ?",(newVal,userId))
        elif attrib == "3":
            cur.execute("UPDATE userDetails SET email_address =? WHERE user_id= ?",(newVal,userId))
        elif attrib == "4":
            cur.execute("UPDATE userDetails SET phone_number =? WHERE user_id= ?",(newVal,userId))          
        elif attrib == "5":    
            cur.execute("UPDATE userDetails SET user_type =? WHERE user_id= ?",(newVal,userId))
        elif attrib == "4":
            cur.execute("UPDATE userLogin SET login_id =? WHERE user_id= ?",(newVal,userId))          
        elif attrib == "5":    
            cur.execute("UPDATE userLogin SET login_password =? WHERE user_id= ?",(newVal,userId))
        else:
            print("invalid Option Selected")
        conn.commit()
        close_connection(conn)
    except sqlite3.Error as e:
       print(e) 
       print ("error in operation add_user")
       conn.rollback()
       close_connection(conn)

def update_book(dbase, bookId,attrib,newVal):
    try:
        conn=create_connection(dbase)
        cur=conn.cursor()
        if attrib == "1":    
            cur.execute("UPDATE books SET title =? WHERE book_id= ?",(newVal,bookId))
        elif attrib == "2":
            cur.execute("UPDATE books SET publication_name =? WHERE book_id= ?",(newVal,bookId))
        elif attrib == "3":
            cur.execute("UPDATE books SET author =? WHERE book_id= ?",(newVal,bookId))
        else:
            print("invalid Option selected")
        conn.commit()
        close_connection(conn)
    except Error as e:
        print("error in operation add_book")
        print(e)
        conn.rollback()
        close_connection(conn)       

def registerUser(dbase,loginId,passWord,firstName,lastName,emailAddress,phoneNum,userRole):
    try:
       conn=create_connection(dbase)
       userId=add_user(dbase,firstName,lastName,emailAddress,phoneNum,userRole)
       create_login(dbase,loginId, passWord, userId)
    except sqlite3.Error as error:
       print ("error in registerUser")

def delete_book(dbase, bookId):
    try:
        #Assumed only available books to be deleted
        conn = create_connection(dbase)
        cur=conn.cursor()
        bkStatus="Available"
        cur.execute("DELETE FROM books WHERE status = ? and book_id = ?",(bkStatus,bookId,))
        conn.commit()
        return 0
    
    except sqlite3.Error as error:
       print ("error in delete_book")
       conn.rollback()
       close_connection(conn)
       return 1

def delete_user(dbase, userId):
    try:
        count=0
        conn=create_connection(dbase)
        cur = conn.cursor()
        bkStatus="Rented"
        cur.execute("SELECT * from rental where status = 'Rented' and user_id = ?",(userId))
        userslist = cur.fetchall()
        for record in userslist:
            print(record)
            count=int(count)+1
            if count > 0:
                return 9
            else:
                sql="""SELECT * FROM Rental WHERE user_id = ?"""      
                cur.execute(sql,(userId))
                if cur3.fetchone()[0] != 0:
                    cur.execute("DELETE FROM rental where user_id = ?",(userId,))
                    
                sql="""SELECT * FROM userLogin WHERE user_id = ?"""      
                cur.execute(sql,(userId))
                if cur3.fetchone()[0] != 0:
                    cur.execute("DELETE FROM userLogin where user_id = ?",(userId,))

                sql="""SELECT * FROM userDetails WHERE user_id = ?"""      
                cur.execute(sql,(userId))
                if cur3.fetchone()[0] != 0:                
                    cur.execute("DELETE FROM userDetails where user_id = ?",(userId,))
                conn.commit()  
        close_connection(conn)
        return 0
    except sqlite3.Error as error:
        print ("error in delete_user")
        conn.rollback()
        close_connection(conn)
        return 1

def display_fine_total(dbase, userId):
    try:
        fineAmt=0
        conn=create_connection(dbase)
        cur=conn.cursor()
        sql="""SELECT SUM(Fine) FROM Rental WHERE user_id = ? GROUP BY user_id"""      
        cur.execute(sql,(userId))
        fineAmt = cur.fetchone()[0]
        close_connection(conn)
        return fineAmt
    except sqlite3.Error as e:
       print(e) 
       print ("error in operation add_user")
       conn.rollback()
       close_connection(conn)

def display_fine_book(dbase, userId, bookId):
    try:        
        conn=create_connection(dbase)
        cur=conn.cursor()
        sql="""SELECT Fine FROM Rental WHERE user_id = ? and book_id = ?"""      
        cur.execute(sql,(userId,bookId))
        fineAmt = cur.fetchone()[0]
        close_connection(conn)
        return fineAmt
    except sqlite3.Error as e:
       print(e) 
       print ("error in operation add_user")
       conn.rollback()
       close_connection(conn)    

def setUp(dbase):
#Create database structure
    try:
        conn=create_connection(dbase)
        cur = conn.cursor()

        sql= """CREATE TABLE IF NOT EXISTS books (                                
		book_id              INTEGER    NOT NULL PRIMARY KEY, 
		title                CHAR(255)  NOT NULL,  
                publication_name     CHAR(255) NOT NULL, 
                author               TEXT       NOT NULL,
                status               Text       NOT NULL );"""

        conn.execute(sql)
        conn.commit()

        sql= """CREATE TABLE IF NOT EXISTS userLogin (
                id              INTEGER    NOT NULL PRIMARY KEY , 
                login_id        CHAR(255)  NOT NULL, 
                login_Password  CHAR(255)  NOT NULL, 
                user_id         CHAR(255)  NOT NULL );"""
       

        cur.execute(sql)
        conn.commit()

        sql= """CREATE TABLE IF NOT EXISTS userDetails ( 
                user_id         INTEGER  NOT NULL PRIMARY KEY, 
                first_name      TEXT  NOT NULL, 
                last_name       TEXT  NOT NULL, 
                email_address   CHAR(100) NOT NULL, 
                phone_number    CHAR(100) NOT NULL, 
                user_type       TEXT  NOT NULL);"""

        cur.execute(sql)
        conn.commit()

        sql= """CREATE TABLE IF NOT EXISTS rental (     
                rental_id          INTEGER  NOT NULL PRIMARY KEY,     
                start_Rental_date  Text  NOT NULL,  
                return_date        Text,   
		Fine		   Text,
                rental_status      TEXT NOT NULL,         
                book_id            INTEGER   NOT NULL,     
                user_id            INTEGER   NOT NULL );"""

        cur.execute(sql)
        conn.commit()
        close_connection(conn)
    except sqlite3.Error as error:
       print ("error in SetUp Block")
       conn.rollback()
       close_connection(conn)   
             

