### Edgars Laķis
### DatZ5057 : Datu apstrādes sistēmas
### 3. mājas darbs (MongoDB skripts Python valodā, izmantojot PyMongo draiveri)

import sys, requests, csv, pprint
import pymongo
from pymongo.mongo_client import MongoClient

# Izveido jaunu klientu un savienojas ar MongoDB serveri
uri = "mongodb+srv://edgarslakis:qXg26KFBoDnh5yZo@puduris0.93lsbgq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
# Izveido šablona datubāzi "myDatabase" ar vienu kolekciju "proteins"
db = client.myDatabase
my_collection = db["proteins"]
# drop, ja kolekcija jau eksistē
try:
  my_collection.drop()  
# return a friendly error if an authentication error is thrown
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are your username and password correct in your connection string?")
  sys.exit(1)

def main():
  # Ping
  try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      print(e)
      sys.exit(1)
  # Pievieno vienu dokumentu
  #mongoAdd(uniprot("P01583"))

  # Izveido (doc_list funkcija) un pievieno (mongoAddMany funkcija) 100 dokumentus
  dokumenti = doc_list("acs.csv")
  mongoAddMany(dokumenti)
  print("############")
  
  # 1. atrast vienu dokumentu pēc viena ieraksta vērtības (primaryAccession) vai apakšvērtības (sequence[molWeight])
  result = my_collection.find_one({"primaryAccession": "O60882"})
  #result = my_collection.find_one({'sequence': {'molWeight': 35015}})
  if result is not None:
    print("1. Atrasts dokuments pēc molWeight 35015")
    pprint.pprint(result)
    print("############")
  else:
    print("Nav atrasts ieraksts")
  
  # 2. Atrast ierakstus ar mol_weight vērtību mazāk par 20'000 Da
  results = my_collection.find({'sequence.molWeight': {'$lt': 20000}})
  if results:
    print("2. Ieraksti ar molWeight vērtību < 20 000")
    for doc in results:
      pprint.pprint(doc['sequence'])
    print("############")
  else:
    print("Nav atrasti dokumenti")

  # 3. Saskaitīt, cik dokumentu mol_weight vērtība ir lielāka par 50000
  query_many = {'sequence.molWeight': {'$gt': 50000}}
  results = my_collection.count_documents(query_many)
  print("3. Dokumentu skaits ar molWeight > 50 000: ", results)
  print("############")

  # 4. izmaina mol_weight vērtību par 1000 Da
  add_to_mass = {"$inc": {"sequence.molWeight": 1000}}
  filter = {"primaryAccession": "O60882"}
  update = my_collection.update_one(filter, add_to_mass)
  # Pārbaudām, vai ir izmainīts ieraksts
  result = my_collection.find_one({"primaryAccession": "O60882"})
  if result is not None:
    print("4. Izmainīta molWeight vērtība vienam dokumentam (primaryAccession: O60882)")
    pprint.pprint(result)
    print("############")
  else:
    print("Nav atrasts ieraksts")

  # 5. Aprēķina vidējo mol_weight massu tiem ierakstiem mol_weight ir lielāks par 10'000 Da
  pipeline = [{
    "$group": {
      "_id": None,
      "videjais": {"$avg": "$sequence.molWeight"}      
      }
    }]
  
  result = list(my_collection.aggregate(pipeline))
  if result:
    print("5. Pipeline rezultāts: Vidējā molWeight vērtība: ", result[0]["videjais"])
    print("############")

  # 6. Izdzēst dokumentus ar O60882 VAI P08253
  my_result = my_collection.delete_many({ "$or": [{"primaryAccession": "O60882"}, {"primaryAccession": "P08253"}]})
  print("6. Izdzēsti dokumenti ar O60882 VAI P08253", my_result)
  print("############")


def doc_list(csvFile):
    ac = []
    with open(csvFile, "r") as lane_acs:
        reader = csv.reader(lane_acs)
        next(reader)
        for row in reader:
            dokuments = uniprot(row[2])
            ac.append(dokuments)
    # print("Trīs dokumenti", ac[5:7])
    return ac

def mongoAdd(entry):
  try: 
    result = my_collection.insert_one(entry)

  # return a friendly error if the operation fails
  except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  #else:
  #  inserted_count = len(result.inserted_ids)
  #print("I inserted %x documents." %(inserted_count))
  #print("\n")
  print(result.inserted_id)

def mongoAddMany(entryList):
  try: 
    result = my_collection.insert_many(entryList)

  # return a friendly error if the operation fails
  except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  else:
    inserted_count = len(result.inserted_ids)
  print("Ievietoto dokumentu skaits:", inserted_count)


def uniprot(accession):
    #accession = "P01583"
    #https://rest.uniprot.org/uniprotkb/P01583?fields=ft_carbohyd&fields=ft_mod_res&fields=ft_lipid&fields=mass

    WEBSITE_API = "https://rest.uniprot.org/"

    def get_url(url, **kwargs):
        response = requests.get(url, **kwargs)

        if not response.ok:
            print(response.text)
            response.raise_for_status()
            sys.exit()

        return response

    ecodict = {
        "ECO:0000269": "EXP: Inferred from Experiment",
        "ECO:0000314": "IDA: Inferred from Direct Assay",
        "ECO:0000353": "IPI: Inferred from Physical Interaction",
        "ECO:0000315": "IMP: Inferred from Mutant Phenotype",
        "ECO:0000316": "IGI: Inferred from Genetic Interaction",
        "ECO:0000270": "IEP: Inferred from Expression Pattern",
        "ECO:0000250": "ISS: Inferred from Sequence or Structural Similarity",
        "ECO:0000255": "ISM: Inferred from Sequence Model",
    }

    r = get_url(
        f"{WEBSITE_API}/uniprotkb/{accession}?fields=ft_carbohyd&fields=ft_mod_res&fields=ft_lipid&fields=mass"
    )
    data = r.json()
    while True:
        try:
            if data["sequence"]["molWeight"] > 1:
                return data
        except KeyError:
            print(f"{accession} no uniprot entry found")
            return None

if __name__ == "__main__":
    main()