import requests
from bs4 import BeautifulSoup
import csv

global_url = "https://polymerdatabase.com/polymer%20index/home.html"
ext = "html"

site_url = "https://polymerdatabase.com/polymer%20index/"

polymer_index = []

class Sub_Polymer:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.smiles = ""
        self.density = 0
        self.molar_volume = 0
        self.solubility = 0
        self.molar_cohesive_energy = 0
        self.glass_transition_temperature = 0
        self.molecular_weight_rep_unit = 0
        self.van_der_waals = 0
        self.entanglement_molecular_weigth = 0
        self.index_of_refraction = 0
        self.cas = 0
        self.curly_smiles = 0

    def __repr__(self):
        return f"polymer({self.name!r}, {self.url!r}, {self.smiles!r}, {self.density!r}, {self.molar_volume!r}, {self.solubility!r}, {self.molar_cohesive_energy!r},{self.glass_transition_temperature!r}, {self.molecular_weight_rep_unit!r}, {self.van_der_waals!r}, {self.entanglement_molecular_weight!r}, {self.index_of_refraction!r}, {self.cas!r}, {self.curly_smile!r}"
    
    def __iter__(self):
        return iter([self.name, self.url, self.smiles, self.density, self.molar_volume, 
            self.solubility, self.molar_cohesive_energy, self.glass_transition_temperature,
            self.molecular_weight_rep_unit, self.van_der_waals, self.entanglement_molecular_weigth,
            self.index_of_refraction, self.cas, self.curly_smiles])

    def add_density(self, density):
        self.density = density
    def add_smiles(self, smiles):
        self.smiles = smiles
    def add_molar_volume(self, mv):
        self.molar_volume = mv
    def add_sol_par(self, sol):
        self.solubility = sol
    def add_mol_coh_ene(self, mol_coh_ene):
        self.molar_cohesive_energy = mol_coh_ene
    def add_glass_trans_t(self, trans):
        self.glass_transition_temperature = trans
    def add_mol_weigth_rep_unit(self, mol_weight):
        self.molecular_weight_rep_unit = mol_weight
    def add_vdw(self, vdw):
        self.van_der_waals = vdw
    def add_ind_refraction(self, ind_refraction):
        self.index_of_refraction = ind_refraction
    def add_ent_mol(self, ent_mol):
        self.entanglement_molecular_weigth = ent_mol
    def add_cas(self, cas):
        self.cas = cas
    def add_curly_smiles(self, smiles):
        self.curly_smiles = smiles


class Polymer:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.sub_polymer = []
    def add_new_sub_polymer(self, name, url):
        self.sub_polymer.append(Sub_Polymer(name, url))

polymer_list = []


def write_to_csv(polymer_class):
    with open('polymers.csv', "w") as stream:
        writer = csv.writer(stream)
        writer.writerows(polymer_class)

def check_value_list(value):
    if value[-1].text:
        return value[-1]
    else:
        return value[-2]
def print_properties(polymer_class):
        print("{}. name = {}, smiles = {}, density = {}, molar volume = {}".format(len(polymer_class),
        polymer_class[-1].name, 
        polymer_class[-1].smiles,
        polymer_class[-1].density,
        polymer_class[-1].molar_volume
        ))
        print("{}. Solubility = {}, Molar Energy = {}, Glass Transition Temp = {}, Molecular Weight of Rep Unit = {}".format(len(polymer_class),
        polymer_class[-1].solubility,
        polymer_class[-1].molar_cohesive_energy,
        polymer_class[-1].glass_transition_temperature,
        polymer_class[-1].molecular_weight_rep_unit
        ))
        print("{}. vdw = {}, index of refraction = {}, entanglement molecular weight Me = {}, CAS = {}, CurlySmiles = {}".format(len(polymer_class),
        polymer_class[-1].van_der_waals,
        polymer_class[-1].entanglement_molecular_weigth,
        polymer_class[-1].index_of_refraction,
        polymer_class[-1].cas,
        polymer_class[-1].curly_smiles
        ))

def get_properties(url, ext, subpolymer_class):
    response = requests.get(url, ext)
    if response.ok:
        response_text = response.text
    else:
        return
    soup = BeautifulSoup(response_text, "html.parser")
    for property_node in soup.find_all("tr"):
        value = property_node.find_all("td")
        entry = value[0].text
        val = check_value_list(value)
        if value[0].text == "Density ρ":
            subpolymer_class[-1].add_density(val.text)
        if value[0].text == "SMILES":
            subpolymer_class[-1].add_smiles(val.text)
        if value[0].text == "Molar Volume Vm":
            subpolymer_class[-1].add_molar_volume(val.text)
        if value[0].text == "Solubility Parameter δ":
            subpolymer_class[-1].add_sol_par(val.text)
        if value[0].text == "Molar Cohesive Energy Ecoh":
            subpolymer_class[-1].add_mol_coh_ene(val.text)
        if value[0].text == "Glass Transition Temperature Tg":
            subpolymer_class[-1].add_glass_trans_t(val.text)
        if value[0].text == "Molecular Weight of Repeat unit, value":
            subpolymer_class[-1].add_mol_weight_rep_unit(val.text)
        if value[0].text == "Van-der-Waals Volume VvW":
            subpolymer_class[-1].add_vdw(val.text)
        if value[0].text == "Index of Refraction n":
            subpolymer_class[-1].add_ind_refraction(val.text)
        if value[0].text == "Entanglement Molecular Weight Me":
            subpolymer_class[-1].add_ent_mol(val.text)
        if value[0].text == "CAS":
            subpolymer_class[-1].add_cas(val.text)
        if value[0].text == "CurlySMILES":
            subpolymer_class[-1].add_curly_smiles(val.text)
        # print("-----> {}. name = {}, entry = {}, value = {}".format(len(subpolymer_class), 
        #     subpolymer_class[-1].name, value[0].text, val.text))
        
        
    #subpolymer_class.add_density(name=node.text, url=new_url)    

def get_sub_polymers(url, ext, polymer_class)   :
    response = requests.get(url, ext)
    if response.ok:
        response_text = response.text
    else:
        return
    soup = BeautifulSoup(response_text, "html.parser")
    polymer_data = soup.find("div", {"id": "content"})
    for node in polymer_data.find_all('a'):
        if node.get('href').endswith(ext):
            new_url = site_url + node.get("href")
            polymer_class.append(Sub_Polymer(name=node.text, url=new_url))   
            get_properties(polymer_class[-1].url, ext, polymer_class)
            print_properties(polymer_class)

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
            #polymer_index.append(new_url)
            #polymer_list.append(Polymer(name=node.text, url=new_url))
            get_sub_polymers(url=new_url, ext=ext, polymer_class=polymer_list)
            #print("-------------------------------------------------------------------------------")
            #print("{}. name = {}, url = {}".format(len(polymer_list), polymer_list[-1].name, polymer_list[-1].url))
            #print("-------------------------------------------------------------------------------")
    write_to_csv(polymer_list)

    next_button = soup.find(id="menu2")
    if next_button:
        for node in next_button.find_all('a'):
            if node.get('href').endswith(ext):
                next_page = site_url + node.get("href")
                get_all_files_recursively(next_page, ext)
    else:
        return

get_all_files_recursively(global_url, ext)
