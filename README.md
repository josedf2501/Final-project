# Final-project
This is the Github repository for the Final project of Software Carpentry.

Members: Jose Daniel Fuentes, and Jiahang Yan

The code can be used to keep track of all the passwords that you use on other sites.

We build the graphical user interface (GUI) with the wxPython GUI toolkit. To be able to run the code you will need to install wxPython on your machine by doing the following:
                                          
                                          pip install wxpython
                                          
The program will first ask you for an account name and password to verify your identity, if the password does not match the account name, the program will end, if the password match the the account name, the program will then ask you for a key which is a number between 1 and 256 that will be used for encryption. this is for security purpose in case your account password get leaked. It is important that you always use the same number to be able to see the passwords that you stored. The username and password will be stored in a json file. To be able to run the program you will need to download the json.file that is in the repository.

When you access the main window, you will be able to add passwords from any site. There is also an option to update and delete a password. The application will tell you if the password that you are using is weak or strong and offers the possibility to search for a password that you registered just by introducing the name of the site.
