from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from pprint import pprint

app = Flask(__name__)

atlas_user = os.getenv("ATLAS_USER")
atlas_pwd = os.getenv("ATLAS_PASSWD")
mongo = MongoClient(
    f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
books_collection = mongo.book_worm_database.SharBooks
authors_collection = mongo.book_worm_database.SharAuthorsv2
publishers_collection = mongo.book_worm_database.SharPub


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/books', methods=['GET'])
def books():
    page_number = request.args.get('pageNumber')
    per_page = request.args.get('perPage')
    if page_number is None and per_page is None:
        num_pages = books_collection.estimated_document_count() // 10
        book_list = []
        for book in books_collection.find().limit(10):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['rating'] = book['rating']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = books_collection.estimated_document_count() // per_page
        book_list = []
        for book in books_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


@app.route('/books/<string:book_id>')
def book_instance(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    pprint(book)
    return render_template('book-instance.html', book=book)


# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors', methods=['GET'])
def authors():
    page_number = request.args.get('pageNumber')
    per_page = request.args.get('perPage')
    if page_number is None and per_page is None:
        num_pages = authors_collection.estimated_document_count() // 10
        author_list = []
        for author in authors_collection.find().limit(10):
            temp = dict()
            temp['_id'] = author['_id']
            temp['name'] = author['name']
            temp['age'] = author['age'] if author['age'] else "___"
            temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
            temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static', filename='/avi'
                                                                                                               '/avi.png')
            author_list.append(temp)
        return render_template('authors.html', authors=author_list, pageNumber=0, perPage=10, numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = authors_collection.estimated_document_count() // per_page
        author_list = []
        for author in authors_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = author['_id']
            temp['name'] = author['name']
            temp['age'] = author['age'] if author['age'] else "___"
            temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
            temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static',
                                                                                            filename='/avi/avi.png')
            author_list.append(temp)
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


# TODO: Change route to use author id instead of author name in P.II
@app.route('/authors/<string:author_id>')
def author_instance(author_id):
    author = authors_collection.find_one({"_id": ObjectId(author_id)})
    author['thumbnail'] = author['thumbnail'] if author['thumbnail'] else url_for('static', filename='/avi/avi.png')
    pprint(author)
    return render_template('author-instance.html', author=author)


# TODO: Phase I - Fetch pub data from APIs
#       Phase II - Fetch pub data from DB
@app.route('/publishers', methods=['GET'])
def publishers():
    page_number = request.args.get('pageNumber')
    per_page = request.args.get('perPage')
    if page_number is None and per_page is None:
        num_pages = publishers_collection.estimated_document_count() // 10
        publisher_list = []
        for publisher in publishers_collection.find().limit(10):
            temp = dict()
            temp['_id'] = publisher['_id']
            temp['name'] = publisher['name']
            temp['logo'] = publisher['logo']
            temp['hq_location'] = publisher['hqLocation']
            temp['estYear'] = publisher['estYear']
            publisher_list.append(temp)
        return render_template('publishers.html', publishers=publisher_list, pageNumber=0, perPage=10,
                               numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = publishers_collection.estimated_document_count() // per_page
        publisher_list = []
        for publisher in publishers_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = publisher['_id']
            temp['name'] = publisher['name']
            temp['logo'] = publisher['logo']
            temp['hq_location'] = publisher['hqLocation']
            temp['estYear'] = publisher['estYear']
            publisher_list.append(temp)
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=10,
                               numPages=num_pages)


# TODO: Change route to use publisher id instead of publisher name in P.II
@app.route('/publishers/<string:pub_id>')
def publisher_instance(pub_id):
    publisher = publishers_collection.find_one({"_id": ObjectId(pub_id)})
    pprint(publisher)
    return render_template('publisher-instance.html', publisher=publisher)


# TODO: Back-end work. Implement search algo
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
