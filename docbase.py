import sys, requests, csv, pprint
import pymongo
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://edgarslakis:qXg26KFBoDnh5yZo@puduris0.93lsbgq.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)
# use a database named "myDatabase"
db = client.myDatabase
# use a collection named "recipes"
my_collection = db["proteins"]
# drop the collection in case it already exists
try:
  my_collection.drop()  
# return a friendly error if an authentication error is thrown
except pymongo.errors.OperationFailure:
  print("An authentication error was received. Are your username and password correct in your connection string?")
  sys.exit(1)

def main():
  # Send a ping to confirm a successful connection
  try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
  except Exception as e:
      print(e)
      sys.exit(1)
  # Pievieno vienu dokumentu
  #mongoAdd(uniprot("P01583"))

  # Pievieno 100 dokumentus no csv faila
  dokumenti = doc_list("acs.csv")
  pprint.pprint(len(dokumenti))
  mongoAddMany(dokumenti)

  query_one = {"primaryAccession": "P01583"}
  # 1 atrast pēc unikāla vārda
  result = my_collection.find_one(query_one)

  if result is not None:
    pprint.pprint(result)
  else:
    print("Nav atrasts ieraksts")

  query_many = {"sequence": {"molWeight": {"$gt": 10000}}}
  # 2 mol_weight ir lielāks par 10'000 Da
  results = my_collection.find(query_many)

  if results:
    for column in results:
      features = column['features']
      features_count = len(column['features'])
      mass = column['sequence']
      pprint.pprint("Pretty print:", features_count, features)
      print()      
  else:
    print("Nav atrasti dokumenti")

def doc_list(csvFile):
    ac = []
    with open(csvFile, "r") as lane_acs:
        reader = csv.reader(lane_acs)
        next(reader)
        for row in reader:
            dokuments = uniprot(row[2])
            ac.append(dokuments)
    print("Trīs dokumenti", ac[5:7])
    return ac

def mongoAdd(entry):
  # INSERT DOCUMENT
  #
  # You can insert individual documents using collection.insert_one().
  # In this example, we're going to create four documents and then 
  # insert them all with insert_many().
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
  # INSERT DOCUMENTS
  #
  # You can insert individual documents using collection.insert_one().
  # In this example, we're going to create four documents and then 
  # insert them all with insert_many().

  try: 
    result = my_collection.insert_many(entryList)

  # return a friendly error if the operation fails
  except pymongo.errors.OperationFailure:
    print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
  else:
    inserted_count = len(result.inserted_ids)
  print("ievietotais dokumentu skaits:", inserted_count)

def mongo(myDatabase):
  

  # UPDATE A DOCUMENT
  #
  # You can update a single document or multiple documents in a single call.
  # 
  # Here we update the prep_time value on the document we just found.
  #
  # Note the 'new=True' option: if omitted, find_one_and_update returns the
  # original document instead of the updated one.

  my_doc = my_collection.find_one_and_update({"ingredients": "potato"}, {"$set": { "prep_time": 72 }}, new=True)
  if my_doc is not None:
    print("Here's the updated recipe:")
    print(my_doc)
  else:
    print("I didn't find any recipes that contain 'potato' as an ingredient.")
  print("\n")

  # DELETE DOCUMENTS
  #
  # As with other CRUD methods, you can delete a single document 
  # or all documents that match a specified filter. To delete all 
  # of the documents in a collection, pass an empty filter to 
  # the delete_many() method. In this example, we'll delete two of 
  # the recipes.
  #
  # The query filter passed to delete_many uses $or to look for documents
  # in which the "name" field is either "elotes" or "fried rice".

  my_result = my_collection.delete_many({ "$or": [{ "name": "elotes" }, { "name": "fried rice" }]})
  print("I deleted %x records." %(my_result.deleted_count))
  print("\n")

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