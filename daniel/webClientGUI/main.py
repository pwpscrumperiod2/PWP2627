#initialize the database
import initialize_db

#start the account management
#this opens the login window and waits until it is closed
import accountGUI
#run the main GUI if logged in successfully
if accountGUI.loggedIn:
    import home
