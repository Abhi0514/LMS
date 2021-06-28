import View_x
import os


def main_menu(db_name):
   #os.system('cls')
    choice ='0'
    while choice =='0':
        print("Library Database Management System")
        print(" ")
        print(" ")
        print("Please Note this program wil only work if the database file exists ")
        print(" ")
        print(" ")
        print("Choose 1 to continue")
        print(" ")
        
        choice = input ("OR Choose Any other key to quit: ")

        if choice == "1":
            View_x.welcomePage(db_name)     
        else:
            exit()    

if __name__ == '__main__':
    main_menu(r"C:\Users\Ankur\Desktop\LMS\lib22.db")

