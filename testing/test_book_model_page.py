import unittest
import os

from selenium import webdriver
from pymongo import MongoClient


class BookModelPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup selenium driver
        cls.driver = webdriver.Firefox(executable_path=os.getenv("GECKO_PATH"))
        cls.base_url = 'http://127.0.0.1:5000/books'

        # Connect to database
        # Testing the GUI requires knowing the number of documents in our database
        atlas_user = os.getenv("ATLAS_USER")
        atlas_pwd = os.getenv("ATLAS_PASSWD")
        cls.mongo = MongoClient(
    f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
        cls.books_collection = cls.mongo.book_worm_database.SharBooks
        cls.books_per_page = 10
        cls.num_pages = cls.books_collection.estimated_document_count() // cls.books_per_page

    def tearDown(self):
        self.driver.close()

    def test_entries_number(self):
        # Testing first page
        self.driver.get(f'{self.base_url}?pageNumber=0&perPage={self.books_per_page}')
        entries_elem = self.driver.find_element_by_id('entriesText')
        output = entries_elem.text
        self.assertEqual('Showing entries 1-10', output)

        # Testing last page
        self.driver.get(f'{self.base_url}?pageNumber={self.num_pages}&perPage={self.books_per_page}')
        entries_elem = self.driver.find_element_by_id('entriesText')
        output = entries_elem.text
        self.assertEqual(f'Showing entries {self.num_pages * self.books_per_page}-{self.books_collection.estimated_document_count()}',
                         output, "Last page entries test failed")

    def test_next_page(self):
        # From the first page
        self.driver.get(f'{self.base_url}?pageNumber=0&perPage={self.books_per_page}')

        # From an arbitrary page
        self.driver.get(f'{self.base_url}?pageNumber=6&perPage={self.books_per_page}')

        # From the last page
        self.driver.get(f'{self.base_url}?pageNumber={self.num_pages}&perPage={self.books_per_page}')

    def test_prev_page(self):
        # From the first page
        self.driver.get(f'{self.base_url}?pageNumber=0&perPage={self.books_per_page}')

        # From an arbitrary page
        self.driver.get(f'{self.base_url}?pageNumber=6&perPage={self.books_per_page}')

        # From the last page
        self.driver.get(f'{self.base_url}?pageNumber={self.num_pages}&perPage={self.books_per_page}')


if __name__ == '__main__':
    unittest.main()
