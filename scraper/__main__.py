import requests
from bs4 import BeautifulSoup

global_url = "https://polymerdatabase.com/polymer%20index/home.html"
ext = "html"

site_url = "https://polymerdatabase.com/polymer%20index/"

polymer_index = []

class Sub_Polymer:
    def __init__(self, name, url):
        self.name = name
        self.url = url
    def add_density(self, density):
        self.density = density

class Polymer:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.sub_polymer = []
    def add_new_sub_polymer(self, name, url):
        self.sub_polymer.append(Sub_Polymer(name, url))

polymer_list = []

def get_properties(url, ext, subpolymer_class):
    try:
        response = requests.get(url, ext)
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        polymer_data = soup.find("div", {"id": "content"})
        for node in polymer_data.find_all('a'):
            if node.get('href').endswith(ext):
                new_url = site_url + node.get("href")
                subpolymer_class.add_density(name=node.text, url=new_url)    
                print("{}. name = {}, url = {}".format(len(polymer_class.sub_polymer),
                        polymer_class.sub_polymer[-1].name, polymer_class.sub_polymer[-1].url))
    except:
        # should implement better error handling but OK for now (most likely a 404!)
        print(response)    

def get_sub_polymers(url, ext, polymer_class):
    try:
        response = requests.get(url, ext)
        response_text = response.text
        soup = BeautifulSoup(response_text, "html.parser")
        polymer_data = soup.find("div", {"id": "content"})
        for node in polymer_data.find_all('a'):
            if node.get('href').endswith(ext):
                new_url = site_url + node.get("href")
                polymer_class.add_new_sub_polymer(name=node.text, url=new_url)    
                print("{}. name = {}, url = {}".format(len(polymer_class.sub_polymer),
                        polymer_class.sub_polymer[-1].name, polymer_class.sub_polymer[-1].url))
    except:
        # should implement better error handling but OK for now (most likely a 404!)
        print(response)
            
def get_all_files_recursively(url, ext):
    response = requests.get(url, ext)
    if response.ok:
        response_text = response.text
    else:
        response.raise_for_status()
    soup = BeautifulSoup(response_text, "html.parser")
    polymer_data = soup.find("div", {"id": "tablestyle"})
    for node in polymer_data.find_all('a'):
        if node.get('href').endswith(ext):
            new_url = site_url + node.get("href")
            polymer_index.append(new_url)
            polymer_list.append(Polymer(name=node.text, url=new_url))
            print("-------------------------------------------------------------------------------")
            print("{}. name = {}, url = {}".format(len(polymer_list), polymer_list[-1].name, polymer_list[-1].url))
            print("-------------------------------------------------------------------------------")
            get_sub_polymers(url=new_url, ext=ext, polymer_class=polymer_list[-1])

    next_button = soup.find(id="menu2")
    if next_button:
        for node in next_button.find_all('a'):
            if node.get('href').endswith(ext):
                next_page = site_url + node.get("href")
                get_all_files_recursively(next_page, ext)
    else:
        return

get_all_files_recursively(global_url, ext)