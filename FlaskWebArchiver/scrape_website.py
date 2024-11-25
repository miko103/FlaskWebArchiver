import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlsplit
import datetime
from FlaskWebArchiver.func import Database
import yaml

def save_file(name, raw_data):
    try:
        with open(name, "wb") as f:
            f.write(raw_data)  
    except:
        print(f"an error occured when saving file called {name}")

def scrape(url, scraped_by_user):

    with open("cfg.yml") as f:
        DB = Database(yaml.safe_load(f)["database_name"])


    netloc = urlsplit(url)[1]
    scheme = urlsplit(url)[0]
    query = urlsplit(url)[3].split(".")
    timestamp = datetime.datetime.now().timestamp()
    print(netloc)
    if netloc not in os.listdir("./FlaskWebArchiver/website_saves"):
        os.mkdir(f"./FlaskWebArchiver/website_saves/{netloc}_{timestamp}")
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}_{timestamp}")
    else:
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}_{timestamp}")
    
    #save scrape url as "index.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    src_elements = soup.find_all(src=True)
    for element in src_elements:
        element_src = element['src'].split(".")[0]
        element_extension = element['src'].split(".")[-1] # gets last item in list aka file extension
        element_src_filename = os.path.basename(element['src'])
        if not element_src.startswith("http"):
            print("src doesnt start with 'html' appending netlocation")
            to_fetch = f"{scheme}://{netloc}{element_src}{element_extension}"
        else:
            to_fetch = f'{element["src"]}'
    
    
        try:
            file_raw_data = requests.get(to_fetch).content
        except:
            print("something heppened oops")
            pass
        

        save_file(element_src_filename,file_raw_data)
        element["src"] = element_src_filename
    
    #saves the edited soup to the index.html file which will be located in the same.
    # cant use function save_file() as that one writes raw binary and i need to write html into file blah blah
    with open("index.html", "w") as f:
            f.write(soup.prettify().replace("{#", "{ #"))
    
    indexpath = f"./FlaskWebArchiver/website_saves/{netloc}_{timestamp}/index.html" # this is what will be saved in the database

    DB.create_website_save(url, indexpath, timestamp, scraped_by_user)
    return indexpath
