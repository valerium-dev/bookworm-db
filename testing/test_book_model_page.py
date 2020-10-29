import unittest
import os

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from pymongo import MongoClient


class BookModelPage(unittest.TestCase):

    def setUp(self):
        # Setup selenium driver
        self.driver = webdriver.Firefox(executable_path=os.getenv("GECKO_PATH"))
        self.base_url = 'http://127.0.0.1:5000/books'

        # Connect to database
        # Testing the GUI requires knowing the number of documents in our database
        atlas_user = os.getenv("ATLAS_USER")
        atlas_pwd = os.getenv("ATLAS_PASSWD")
        self.mongo = MongoClient(
    f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
        self.books_collection = self.mongo.book_worm_database.SharBooks
        self.books_per_page = 10
        self.num_pages = self.books_collection.estimated_document_count() // self.books_per_page

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
        self.assertEqual(f'Showing entries {self.num_pages * self.books_per_page + 1}-{self.books_collection.estimated_document_count()}',
                         output, "Last page entries test failed")

    def test_next_page(self):
        # From the first page
        self.driver.get(f'{self.base_url}?pageNumber=0&perPage={self.books_per_page}')
        next_btn = self.driver.find_element_by_id('nextPage')
        next_btn.click()
        self.assertEqual(f'{self.base_url}?pageNumber=1&perPage={self.books_per_page}', self.driver.current_url)

        # From an arbitrary page
        self.driver.get(f'{self.base_url}?pageNumber=6&perPage={self.books_per_page}')
        next_btn = self.driver.find_element_by_id('nextPage')
        next_btn.click()
        self.assertEqual(f'{self.base_url}?pageNumber=7&perPage={self.books_per_page}', self.driver.current_url)

        # From the last page
        self.driver.get(f'{self.base_url}?pageNumber={self.num_pages}&perPage={self.books_per_page}')
        next_btn = self.driver.find_element_by_id('nextPage')
        with self.assertRaises(ElementClickInterceptedException):
            next_btn.click()

    def test_prev_page(self):
        # From the first page
        self.driver.get(f'{self.base_url}?pageNumber=0&perPage={self.books_per_page}')
        prev_btn = self.driver.find_element_by_id('prevPage')
        with self.assertRaises(ElementClickInterceptedException):
            prev_btn.click()

        # From an arbitrary page
        self.driver.get(f'{self.base_url}?pageNumber=6&perPage={self.books_per_page}')
        prev_btn = self.driver.find_element_by_id('prevPage')
        prev_btn.click()
        self.assertEqual(f'{self.base_url}?pageNumber=5&perPage={self.books_per_page}', self.driver.current_url)

        # From the last page
        self.driver.get(f'{self.base_url}?pageNumber={self.num_pages}&perPage={self.books_per_page}')
        prev_btn = self.driver.find_element_by_id('prevPage')
        prev_btn.click()
        self.assertEqual(f'{self.base_url}?pageNumber={self.num_pages - 1}&perPage={self.books_per_page}',
                         self.driver.current_url)


if __name__ == '__main__':
    unittest.main()
