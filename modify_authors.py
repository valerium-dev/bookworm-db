import pymongo



myclient = pymongo.MongoClient("mongodb+srv://moogie:sdl_bookworm%402020@cluster0.rh1w0.mongodb.net/test")
mydb = myclient["book_worm_database"]
authors_col = mydb["Authors"]
books_dict_arr = []
flag = False
book = ""
for x in authors_col.find({"books" : { "$type" : 4}}):
    id_query = x['_id']
    if x['name'] == "Brad Nichols " or flag == True:
        flag = True
        if isinstance(x["books"], list):
            if len(x["books"]):
                book_array = x["books"][0]
                while True:
                    if (isinstance(book_array, list)):
                        if book_array:
                            book_array = book_array[0]
                        else: 
                            break
                    else:
                        book = book_array 
                        break
                if book:
                    book_names = book.keys()
                    book_ids = book.values()
                    for y in range(len(book_names)):
                        my_dict = {"name" : list(book_names)[y], "_id":list(book_ids)[0]}
                        books_dict_arr.append(my_dict)
                    authors_col.update({'_id': id_query}, {"$set": {"books": books_dict_arr}})
                    books_dict_arr = []
            else:
                continue
        else:
            continue

