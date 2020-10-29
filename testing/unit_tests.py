import unittest
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://moogie:sdl_bookworm%402020@cluster0.rh1w0.mongodb.net/test")
mydb = myclient["book_worm_database"]
authors_col = mydb["Authors"]
publishers_col = mydb["Publishers"]
books_col = mydb["books_testing"]

def update_document(query, values):
    update_result = books_col.update_one(query, values)
    return update_result.modified_count

def find_one(query, values):
    find_result = books_col.find_one({query:values})
    return find_result

def insert_one(insert_dict):
    insert_one_result = books_col.insert_one(insert_dict)
    return insert_one_result

def delete_one(new_dict):
    delete_one_result = books_col.delete_one(new_dict)
    return delete_one_result.deleted_count 

class crud_tests(unittest.TestCase):
    query_dict = {}
    new_dict = {}

    find_key = ""
    val_key = ""

    insert_dict = {}
    def __init__(self, testname, query_dict, new_dict, find_key, val_key, insert_dict):
        super(crud_tests, self).__init__(testname)
        self.query_dict = query_dict
        self.new_dict = new_dict
        self.find_key = find_key
        self.val_key = val_key
        self.insert_dict

    def update_test(self):
        result = update_document(query_dict, new_dict)
        self.assertEqual(result, 1, "nothing updated")

    def read_test(self):
        result = find_one(find_key, val_key)
        self.assertTrue(result)

    def insert_test(self):
        result = insert_one(self.insert_dict)
        self.assertTrue(result)
    
    def delete_test(self):
        result = delete_one(new_dict)
        self.assertEqual(result, 1, "nothing updated")

if __name__ == '__main__':
    query_dict = {}
    new_dict = {}
    test_name = input("enter a test_name: ")
    read_dict = {}
    if test_name == "update_test":
        query = input("enter a query: ")
        value = input("enter the value for the query: ")
        newValue = input("enter the new value for the query: ")
        query_dict = {query: value}
        new_dict = {"$set": {query : newValue}}
    elif test_name == "read_test":
        find_key = input("enter the query key: ")
        val_key = input("enter the value for the key: ")
    elif test_name == "delete_test":
        query = input("enter a key: ")
        value = input("enter a value: ")
        new_dict = {query:value}
       
    

    suite = unittest.TestSuite()
    suite.addTest(crud_tests(test_name, query_dict, new_dict, find_key, val_key, read_dict))
    
    unittest.TextTestRunner(verbosity=2).run(suite)

