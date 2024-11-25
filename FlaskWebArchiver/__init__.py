import sqlite3
import os
import random
import string
import yaml

# ----- TO DO -----
#   > maybe make a config file to store the database names, admin password for the website, etc 
#     (this could be done in docker maybe??)
#   > research if previous idea is possible
#   > work on the theory too

def start():
    
    if "cfg.yml" not in os.listdir():
        f = open("cfg.yml", "w")
        f.write(f"""SECRET_KEY: '{"".join(random.choices(string.ascii_letters, k=20))}'
                database_name: 'database.db' # default: database.db
                MAIL_ACCOUNT: ''
                MAIN_PASS: ''""")
        f.close()

    with open('cfg.yml', 'r') as cfg:
        settings = yaml.safe_load(cfg)
        MAIN_DB_NAME = settings["database_name"]

    
    # creates table for user data
    con = sqlite3.connect(MAIN_DB_NAME)
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS stats(
               stat_id INTEGER PRIMARY KEY ,
               total_searches INT,
               total_saves INT
               )""")
    #creates main userdata table
    cursor.execute("""CREATE TABLE IF NOT EXISTS userdata(
                   uid INTEGER PRIMARY KEY,
                   username TEXT NOT NULL,
                   phash TEXT NOT NULL,
                   email TEXT NOT NULL,
                   stat_id INT NOT NULL,
                   vercode INT,
                   FOREIGN KEY(stat_id) REFERENCES stats(stat_id)
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS sites(
                   site_id INTEGER PRIMARY KEY,
                   scraped_by INT NOT NULL,
                   FOREIGN KEY(scraped_by) REFERENCES userdata(uid)
                   )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS sites_data (
                   site_id INTEGER PRIMARY KEY,
                   url TEXT NOT NULL,
                   timestamp RFLOATEAL NOT NULL,
                   local_path TEXT NOT NULL,
                   FOREIGN KEY(site_id) REFERENCES sites(site_id)
                   )""")
    con.commit()
    cursor.close()
    con.close()

    
    # creates folder for website save data
    try:
        os.mkdir("FlaskWebArchiver/website_saves")
    except:
        print("[!] website_saves folder already exists")
    
    
    print("[!] starting program")
    from FlaskWebArchiver.routes import app
    app.run(host="0.0.0.0", port="5000",debug=True)