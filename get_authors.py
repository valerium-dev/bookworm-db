import pymongo
import wikipedia
import goodreads_api_client as gr
import requests
import xml.etree.ElementTree as ET
from collections import OrderedDict 

myclient = pymongo.MongoClient("mongodb+srv://moogie:sdl_bookworm%402020@cluster0.rh1w0.mongodb.net/test")
mydb = myclient["book_worm_database"]
authors_col = mydb["Authors"]
goodreads_api_key = "pckNQ3X39wTpCyFRM7EBeQ"
gr_client = gr.Client(developer_key=goodreads_api_key)
index = False
PARAMS = {'key': goodreads_api_key}

for x in authors_col.find():
    if x['name'] == "Tuttle Publishing":
        index = True
    print(x['name'])
    if index:
        URL = "https://www.goodreads.com/api/author_url/"
        id_query = x['_id']
        author = x['name']
        if len(author) > 1:
            if author[0] == " ":
                author = author[1:]
            if author[len(author)-1] == " ":
                author = author[0:len(author)-1]
        else:
            continue
        author = author.replace(" ", "+")

        
        print(author)
        URL += author
        r = requests.get(url = URL, params=PARAMS)
        root = ET.fromstring(r.content)
        for child in root.iter('author'):
            author_id = child.attrib['id']
        try:
            od = gr_client.Author.show(author_id)
            about = od['about']
            if about:
                authors_col.find_and_modify(query={'_id': id_query}, update={"$set": {'biography':about}}
                , upsert=False, full_response=True)
                print(about)

            hometown = od['hometown']
            if hometown:
                authors_col.find_and_modify(query={'_id': id_query}, update={"$set": {'hometown':hometown}}
                , upsert=False, full_response=True)
                print(hometown)

            dob = od['born_at']
            if dob:
                authors_col.find_and_modify(query={'_id': id_query}, update={"$set": {'dob':dob}}
                , upsert=False, full_response=True)
                print(dob)

            dod = od['died_at']
            if dod:
                authors_col.find_and_modify(query={'_id': id_query}, update={"$set": {'dod':dod}}
                , upsert=False, full_response=True)
                print(dod)

            print("\n")
        except Exception as e:
            print(author + " not found")

    
    


    
    


    
