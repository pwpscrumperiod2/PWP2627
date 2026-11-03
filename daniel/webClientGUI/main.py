#initialize the database
import initialize_db

#start the account management
#this opens the login window and waits until it is closed
import account
#run the main GUI if logged in successfully
if account.loggedIn:
    import home
