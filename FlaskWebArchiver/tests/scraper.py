import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlparse
import os
import datetime

def save_file(name, raw_data):
    try:
        with open(name, "wb") as f:
            f.write(raw_data)  
    except:
        print(f"an error occured when saving file called {name}")
        


def scrape(url):
    netloc = urlsplit(url)[1]
    scheme = urlsplit(url)[0]
    query = urlsplit(url)[3].split(".")
    print(netloc)
    if netloc not in os.listdir("./FlaskWebArchiver/website_saves"):
        os.mkdir(f"./FlaskWebArchiver/website_saves/{netloc}")
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}")
    else:
        os.chdir(f"./FlaskWebArchiver/website_saves/{netloc}")
    
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
            f.write(soup.prettify())  


scrape("https://harlington.org")


    # todo: 
    #  - parse soup to find all src tags DONE
    #  - then download them DONE
    #  - then replace the tag in the soup with the local path to same file DONE
    #  - write the changed soup into the index.html file DONE

    # AHH THIS TOOK 4 HOURS. SO WORTH IT.