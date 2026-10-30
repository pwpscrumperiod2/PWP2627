#imports web application library
from flask import Flask, request, render_template
#imports the secondary files

#initialize the database
import initialize_db

#imports the functions for rover communication
import rover

"""now we have to manage the account apge and the main page"""
#start the account management
import account
if account.loggedIn:
    #run the main gui if logged in successfully
    import home


