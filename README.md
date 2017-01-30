# Item Catalog Project - Jake Gornall
 
## This application was designed for Udacity's Item Catalog course by Jake Gornall.
## Application allows users to sign in using their facebook accounts, create items to sell, update the item info or delete the item.

**Language** = Python 2.7
if not installed, click [here](https://www.python.org/download/releases/2.7/).

### Installing Dependencies:
1. Run "install_requirements.sh"
2. Follow the install instructions [here](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm) to install Sqlite3.



### Running Application on localhost:

1. clone repository to your machine by opening Git Bash and using the command ```git clone https://github.com/jakegornall/ItemCatalogProject```

2. before you can run the application you need to create an account with facebook as a developer.

3. To do so, go to https://developers.facebook.com if you do not have an account go ahead and create one.

4. Once you have an account, create a new application call ItemCatalog. 

5. When your new application is registered, go to the dashboard and you will see your API version, App ID, and App Secret. 
   Take note of these, we'll use them in the following steps.

6. In the root directory of ItemCatalogProject you will find a file called "fb_client_secrets.json". Open it
   in your text editor and replace the app_id and app_secret with the numbers you found in step 5. Make sure the numbers 
   are wrapped in quotation marks (as strings).

7. You are now ready to run the application. Navigate to the root directory in Git Bash. Run the command "python webserver.py". 

8. Open a browser of your choice (preferably Chrome). In the address bar enter "http://localhost:5000".

9. If port 5000 is already in use on your machine, open webserver.py and go to the last line in the program. Where is says "port=5000", change to
   your desired port number. Make sure you make the appropriate change in your browser address as well. 
