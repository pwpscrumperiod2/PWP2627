#imports web application library
from flask import Flask, request, render_template
#imports the secondary files
#each file runs as soon as it is imported

#initialize the database
import initialize_db

#start the account management
#this opens the login window and waits until it is closed
import account
#run the main GUI if logged in successfully
if account.loggedIn:
    import home


