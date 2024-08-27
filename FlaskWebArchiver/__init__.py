import sqlite3
import os
# ----- TO DO -----
#   > maybe make a config file to store the database names, admin password for the website, etc 
#     (this could be done in docker maybe??)
#   > research if previous idea is possible
#   > work on the theory too

def start():
    USER_DB_NAME = "user.db"
    WEBSITE_DB_NAME = "website_data.db"

    if USER_DB_NAME not in os.listdir():
        os.system(f'echo > {USER_DB_NAME}')
        print("[+] user database created")
        c = sqlite3.connect(USER_DB_NAME)
        cursor = c.cursor()

        # creates table for user data
        cursor.execute("CREATE TABLE userdata(user_id INTEGER PRIMARY KEY,username STRING,phash STRING,email STRING,vercode STRING)")
        c.commit()
        print("[+] table 'ud' created in user table")
        c.close()
        
        if WEBSITE_DB_NAME not in os.listdir():
            os.system(f'echo > {WEBSITE_DB_NAME}')
            print("[+] website database created")

        else:
            print(["[!] website database already exists"])
            quit()

    else:
        print("[!] user database already exists\n")
        
    print("[!] starting program")
    from FlaskWebArchiver.routes import app
    app.run(host="0.0.0.0", port="5000",debug=True)