import Model_x
import sys
import os


def welcomePage(dbase):
    #os.system('cls')
    print("Welcome to my books Library checkout/Checkin System")
    print()
    print()
    print("Please select an option to login or to register")
    print()
    print("[1]: Login")
    print("[2]: Register")
    print("[3]: Run Setup")
    print("[0]: Quit")
    menuOption=int(input("Enter option: "))
    if menuOption == 1:       
        loginId=(input("Please enter your login id (Case Sensitive) >:"))
        userId=Model_x.checkLoginId(dbase,loginId)        
        if userId is None:
            print("User Not found, please register")
            
        else:    
            passWord=(input("Now enter your password (Case Sensitive) >:"))
            passStatus=Model_x.checkPassword(dbase,loginId, passWord)
            print("passstatsu ",passStatus)
            if passStatus == 1:
                print("Invalid password entered")
            else:
                userType=Model_x.checkUserType(dbase,userId)
                if userType == "user":
                    mainMenu_user(dbase, userId)
                else:       
                    mainMenu_lib(dbase, userId)        
    elif menuOption == 2:
        print("Please Provide the following data to continue registeration process")
        print()
        print()
        loginId=(input("Enter a Login Id >:"))
        passWord=(input("Enter a Password >:"))
        fName=(input("Enter your First Name >:"))
        sName=(input("Enter your Surname >:"))
        emailId=(input("nter your Email Address>:"))
        phoneNum=(input("Enter a contact number >:"))
        role=(input("Enter 1 if you are a user or 2 if this is a contact for a librarian >:"))
        if (role == "1"):
            userRole="user"        
        else:
            userRole="librarian"

        Model_x.registerUser(dbase,loginId,passWord,fName,sName,emailId,phoneNum,userRole)        
    elif menuOption == 3:
        Model_x.setUp(dbase)        
    elif menuOption == 0:
        sys.exit()
    else:
        print("Invalid menu item chosen. Enter 0 - 3 only")
    welcomePage(dbase)
    

def mainMenu_lib(dbase,userId):
    
    print()
    print("Please select an option to continue")
    print()
    print("[1]: Add a book")
    print("[2]: Display all books")
    print(" ")
    print("[3]: Delete a Book")
    print("[4]: Update a Book")
    print(" ")
    print("[5]: Delete a User")    
    print("[6]: Add a new User")
    print("[7]: Update a User")
    print("[8]: Display all Users")
    print()
    print("[0]: Quit")
    menuOption=int(input("Enter option: "))
    if menuOption == 1:
        title=(input("Enter title of book to add >:"))
        pubName=(input("Enter the books publication_name >:"))
        author=(input("Enter the authors name >:"))
        Model_x.add_book(dbase,title,pubName,author)
    elif menuOption == 2:
        Model_x.display_books(dbase,"All")
    elif menuOption == 3:
        Model_x.display_books(dbase,"Available")
        bookId=(input("Enter book id of book to delete >:"))
        delStatus=Model_x.delete_book(dbase, bookId)
        if delStatus == 0:
            print("Book deleted")
        else:
            print("There was an error deleting the book, with id ",bookId)
    elif menuOption == 4:
        bookId=(input("Enter book id of book to update >:"))
        print("Book atrribute that can be updated >:")
        print("[1]: Title")
        print("[2]: Publication Company")
        print("[3]: Author")
        attrib=(input("Enter user atrribute to update >:"))
        newVal=(input("Now Enter New Value >:"))
        Model_x.update_book(dbase,bookId,attrib,newVal)
    elif menuOption == 5:
        Model_x.display_users(dbase)
        userId=(input("Enter user Id to delete >:"))
        deleteStatus=Model_x.delete_user(dbase, userId)
        if deleteStatus == 0:
            print("User deleted")
        elif deleteStatus == 0:
            print("Cannot delete users as they have books rented out")
        else:
            print("Error occured in deleting user")
    elif menuOption == 6:
        print("Please Provide the following data to a new user")
        print()
        print()
        loginId=(input("Enter a Login Id >:"))
        passWord=(input("Enter a Password >:"))
        fName=(input("Enter a First Name >:"))
        sName=(input("Enter a Surname >:"))
        emailId=(input("nter the Email Address>:"))
        phoneNum=(input("Enter a contact number >:"))
        role=(input("Enter 1 if its for a new user or 2 if person is a new librarian >:"))
        if (role == "1"):
            userRole="user"        
        else:
            userRole="librarian"

        Model_x.registerUser(dbase,loginId,passWord,fName,sName,emailId,phoneNum,userRole)        

    elif menuOption == 7:
        loginId=(input("Enter login Id to update >:"))
        print("User atrributes that can be updated >:")
        print("[1]: First Name")
        print("[2]: Surname")
        print("[3]: Email Address")
        print("[4]: Phone Number")
        print("[5]: Role")
        print("[6]: Login Id")
        print("[7]: Password")
        attrib=(input("Enter user atrribute to update >:"))
        if (attrib == 6 or attib - 7):
            Model_x.update_login(dbase, loginId,attrib,newVal)
        else:
            newVal=(input("Now Enter New Value >:"))
            Model_x.update_user(dbase, loginId,attrib,newVal)
    elif menuOption == 8:
            Model_x.display_users(dbase)                    
    elif menuOption == 0:
        welcomePage(dbase)
    else:
        print("Invalid menu item chosen. Enter 1 - 6 only")
    mainMenu_lib(dbase,userId)
    

def mainMenu_user(dbase,userId):
    print()
    print("Please select an option to continue")
    print()
    print("[1]: Checkout a book")
    print("[2]: Checkin a book")
    print("[3]: Display Available books")
    print("[4]: View total Fine Amt")
    print()
    print("[0]: Quit")
    menuOption=int(input("Enter option: "))
    if menuOption == 1:
        Model_x.display_books(dbase,"Available")
        bookId=(input("Enter book id of book to checkout >:"))
        Model_x.checkoutBook(dbase, userId, bookId)        
    elif menuOption == 2:
        Model_x.display_books_user(dbase,userId)
        bookId=(input("Enter book id of book to check-in >:"))
        fineAmt = Model_x.checkinBook(dbase, bookId, userId)
        if fineAmt != 0:
            print("This book was overdue and has incured a fine of ",fineAmt) 
    elif menuOption == 3:
        Model_x.display_books(dbase,"Available")
    elif menuOption == 4:
        FineAmt=Model_x.display_fine_total(dbase, userId)
        if FineAmt != 0:
            print("The total Fine accumlated by you is ",FineAmt)
        else:
            print("You have not incurred any fines for this return")
    elif menuOption == 0:
        welcomePage(dbase)
    else:
        print("Invalid menu item chosen. Enter 1 - 3 only")        
    mainMenu_user(dbase,userId)
