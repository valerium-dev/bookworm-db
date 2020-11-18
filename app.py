from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from pprint import pprint

app = Flask(__name__)

atlas_user = os.getenv("ATLAS_USER")
atlas_pwd = os.getenv("ATLAS_PASSWD")
mongo = MongoClient(
    f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
books_collection = mongo.book_worm_database.Golden_Books
authors_collection = mongo.book_worm_database.Golden_Authors
publishers_collection = mongo.book_worm_database.Golden_Publishers


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
        return render_template('books.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages,
                               sortType=None)
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
            temp['rating'] = book['rating']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=None)


@app.route('/books', methods=['POST'])
def books_form_submit():
    form_values = request.form
    per_page = int(form_values['perPage'])

    try:
        page_number = int(form_values['pageNumber'])
    except KeyError:
        page_number = 0

    num_pages = books_collection.estimated_document_count() // per_page
    sort_type = form_values['sort-type'] if form_values['sort-type'] != 'Default' else None

    book_list = []
    if sort_type is not None:
        for book in books_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['rating'] = book['rating']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for book in books_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['rating'] = book['rating']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/books/<string:book_id>')
def book_instance(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    pprint(book)
    return render_template('book-instance.html', book=book)


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
            temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
            temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static',
                                                                                            filename='/avi/avi.png')
            author_list.append(temp)
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


@app.route('/authors', methods=['POST'])
def authors_form_submit():
    form_values = request.form
    per_page = int(form_values['perPage'])

    try:
        page_number = int(form_values['pageNumber'])
    except KeyError:
        page_number = 0

    num_pages = authors_collection.estimated_document_count() // per_page
    sort_type = form_values['sort-type'] if form_values['sort-type'] != 'Default' else None

    author_list = []
    if sort_type is not None:
        for author in authors_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = author['_id']
            temp['name'] = author['name']
            temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
            temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static',
                                                                                            filename='/avi/avi.png')
            author_list.append(temp)
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for author in authors_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = author['_id']
            temp['name'] = author['name']
            temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
            temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static',
                                                                                            filename='/avi/avi.png')
            author_list.append(temp)
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/authors/<string:author_id>')
def author_instance(author_id):
    author = authors_collection.find_one({"_id": ObjectId(author_id)})
    author['thumbnail'] = author['thumbnail'] if author['thumbnail'] else url_for('static', filename='/avi/avi.png')
    pprint(author)
    return render_template('author-instance.html', author=author)


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
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


@app.route('/publishers', methods=['POST'])
def publishers_form_submit():
    form_values = request.form
    per_page = int(form_values['perPage'])

    try:
        page_number = int(form_values['pageNumber'])
    except KeyError:
        page_number = 0

    num_pages = publishers_collection.estimated_document_count() // per_page
    sort_type = form_values['sort-type'] if form_values['sort-type'] != 'Default' else None

    publisher_list = []
    if sort_type is not None:
        for publisher in publishers_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = publisher['_id']
            temp['name'] = publisher['name']
            temp['logo'] = publisher['logo']
            temp['hq_location'] = publisher['hqLocation']
            temp['estYear'] = publisher['estYear']
            publisher_list.append(temp)
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for publisher in publishers_collection.find().skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = publisher['_id']
            temp['name'] = publisher['name']
            temp['logo'] = publisher['logo']
            temp['hq_location'] = publisher['hqLocation']
            temp['estYear'] = publisher['estYear']
            publisher_list.append(temp)
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


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
