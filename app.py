from flask import Flask, render_template, url_for, request
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

app = Flask(__name__)

atlas_user = os.getenv("ATLAS_USER")
atlas_pwd = os.getenv("ATLAS_PASSWD")
mongo = MongoClient(
    f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
books_collection = mongo.book_worm_database.Golden_Books
authors_collection = mongo.book_worm_database.Golden_Authors_Mrugank_copy
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
            book_list.append(truncated_book(book))
        return render_template('books.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages,
                               sortType=None)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = books_collection.estimated_document_count() // per_page
        book_list = []
        for book in books_collection.find().skip(page_number * per_page).limit(per_page):
            book_list.append(truncated_book(book))
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=None)


def truncated_book(book):
    temp = dict()
    temp['_id'] = book['_id']
    temp['title'] = book['title']
    temp['authors'] = book['authors']
    temp['genre'] = book['genre']
    temp['rating'] = book['rating']
    temp['thumbnail_url'] = book['thumbnail']
    return temp


@app.route('/books', methods=['POST'])
def books_sort():
    per_page = int(request.form['perPage'])

    try:
        page_number = int(request.form['pageNumber'])
    except KeyError:
        page_number = 0

    sort_type = request.form['sort-type'] if request.form['sort-type'] != 'Default' else None

    num_pages = books_collection.estimated_document_count() // per_page
    sorted_list = []
    if sort_type is not None:
        for book in books_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_book(book))
        return render_template('books.html', books=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for book in books_collection.find().skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_book(book))
        return render_template('books.html', books=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/books/<string:book_id>')
def book_instance(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    return render_template('book-instance.html', book=book)


@app.route('/authors', methods=['GET'])
def authors():
    page_number = request.args.get('pageNumber')
    per_page = request.args.get('perPage')
    if page_number is None and per_page is None:
        num_pages = authors_collection.estimated_document_count() // 10
        author_list = []
        for author in authors_collection.find().limit(10):
            author_list.append(truncated_author(author))
        return render_template('authors.html', authors=author_list, pageNumber=0, perPage=10, numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = authors_collection.estimated_document_count() // per_page
        author_list = []
        for author in authors_collection.find().skip(page_number * per_page).limit(per_page):
            author_list.append(truncated_author(author))
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


def truncated_author(author):
    temp = dict()
    temp['_id'] = author['_id']
    temp['name'] = author['name']
    temp['genres'] = author['genres']
    # temp['age'] = author['age'] if author['age'] else "___"
    temp['hometown'] = author['hometown'] if author['hometown'] else "Someplace, Earth"
    temp['thumbnail_url'] = author['thumbnail'] if author['thumbnail'] else url_for('static', filename='/avi/avi.png')
    temp['followers'] = author['followers']
    temp['website'] = author['website']
    return temp


@app.route('/authors', methods=['POST'])
def authors_sort():
    per_page = int(request.form['perPage'])

    try:
        page_number = int(request.form['pageNumber'])
    except KeyError:
        page_number = 0

    sort_type = request.form['sort-type'] if request.form['sort-type'] != 'Default' else None

    num_pages = authors_collection.estimated_document_count() // per_page
    sorted_list = []
    if sort_type is not None:
        for author in authors_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_author(author))
        return render_template('authors.html', authors=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for author in authors_collection.find().skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_author(author))
        return render_template('authors.html', authors=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/authors/<string:author_id>')
def author_instance(author_id):
    author = authors_collection.find_one({"_id": ObjectId(author_id)})
    author['thumbnail'] = author['thumbnail'] if author['thumbnail'] else url_for('static', filename='/avi/avi.png')
    return render_template('author-instance.html', author=author)


@app.route('/publishers', methods=['GET'])
def publishers():
    page_number = request.args.get('pageNumber')
    per_page = request.args.get('perPage')
    if page_number is None and per_page is None:
        num_pages = publishers_collection.estimated_document_count() // 10
        publisher_list = []
        for publisher in publishers_collection.find().limit(10):
            publisher_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=publisher_list, pageNumber=0, perPage=10,
                               numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = publishers_collection.estimated_document_count() // per_page
        publisher_list = []
        for publisher in publishers_collection.find().skip(page_number * per_page).limit(per_page):
            publisher_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages)


def truncated_publisher(publisher):
    temp = dict()
    temp['_id'] = publisher['_id']
    temp['name'] = publisher['name']
    temp['logo'] = publisher['logo']
    temp['hq_location'] = publisher['hqLocation']
    temp['estYear'] = publisher['estYear']
    temp['website'] = publisher['website']
    return temp


@app.route('/publishers', methods=['POST'])
def publishers_sort():
    per_page = int(request.form['perPage'])

    try:
        page_number = int(request.form['pageNumber'])
    except KeyError:
        page_number = 0

    sort_type = request.form['sort-type'] if request.form['sort-type'] != 'Default' else None

    num_pages = publishers_collection.estimated_document_count() // per_page
    sorted_list = []
    if sort_type is not None:
        for publisher in publishers_collection.find().sort(sort_type).skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for publisher in publishers_collection.find().skip(page_number * per_page).limit(per_page):
            sorted_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=sorted_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/publishers/<string:pub_id>')
def publisher_instance(pub_id):
    publisher = publishers_collection.find_one({"_id": ObjectId(pub_id)})
    return render_template('publisher-instance.html', publisher=publisher)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('error.html', message="Search Error <hr> Please use the search bar to submit a request.")

    search_input = request.form
    if search_input['origin'] == 'navbar':
        # Default search params
        per_page = 12
        page_num = 0
        search_type = 'books'
        sort_type = 'Default'
    else:
        # Use user selected inputs
        per_page = int(search_input['perPage'])
        page_num = int(search_input['pageNumber'])
        search_type = search_input['search-type']
        sort_type = search_input['sort-type']

    search_query = search_input['search-text']
    search_results = search_instances(search_type, search_query, page_num, per_page, sort_type)
    num_pages = len(search_results) // per_page

    return render_template('search.html', searchResults=search_results, searchQuery=search_query,
                           searchType=search_type, pageNumber=page_num, perPage=per_page, numPages=num_pages,
                           sortType=sort_type)


def search_instances(search_type, query, page_num, per_page, sort_type, filters=None):
    search_results = []

    if search_type == 'books':
        if filters:
            pass

        else:
            if sort_type != 'Default':
                for book in books_collection.find({"title": {"$regex": query, "$options": 'i'}}).sort(sort_type).skip(
                        page_num * per_page).limit(per_page):
                    search_results.append(truncated_book(book))

            else:
                for book in books_collection.find({"title": {"$regex": query, "$options": 'i'}}).skip(
                        page_num * per_page).limit(per_page):
                    search_results.append(truncated_book(book))

    elif search_type == 'authors':
        if filters:
            pass

        else:
            if sort_type != 'Default':
                for author in authors_collection.find({"name": {"$regex": query, "$options": 'i'}}).sort(
                        sort_type).skip(page_num * per_page).limit(per_page):
                    search_results.append(truncated_author(author))

            else:
                for author in authors_collection.find({"name": {"$regex": query, "$options": 'i'}}).skip(
                        page_num * per_page).limit(per_page):
                    search_results.append(truncated_author(author))

    elif search_type == 'publishers':
        if filters:
            pass

        else:
            if sort_type != 'Default':
                for publisher in publishers_collection.find({"name": {"$regex": query, "$options": 'i'}}).sort(
                        sort_type).skip(page_num * per_page).limit(per_page):
                    search_results.append(truncated_publisher(publisher))
            else:
                for publisher in publishers_collection.find({"name": {"$regex": query, "$options": 'i'}}).skip(
                        page_num * per_page).limit(per_page):
                    search_results.append(truncated_publisher(publisher))

    return search_results


@app.route('/filter', methods=['GET', 'POST'])
def filter_instances():
    book_list = []
    selected_array = []
    num_pages = 0
    key_number = 0

    for key, value in request.form.items():
        selected_array.append(key)
        field = "genre"
        if not key.isalpha():
            if key.find(".") == -1:
                field = "pageCount"
                key_number = int(key)
            else:
                field = "rating"
                key_number = float(key)
        if field == "genre":
            for book in books_collection.find({"genre": {"$regex": key}}):
                num_pages += 1

                book_list.append(truncated_book(book))

        elif field == "rating":

            x = 1.01 + key_number
            for book in books_collection.find({"rating": {"$lt": x, "$gt": key_number}}):
                num_pages += 1

                book_list.append(truncated_book(book))

        else:

            for book in books_collection.find({"pageCount": {"$gt": 100 * key_number,
                                                             "$lt": (100 * key_number) + 301}}):
                num_pages += 1
                book_list.append(truncated_book(book))

    num_pages = -(-num_pages // 10)

    if num_pages == 0:
        return render_template('noResults.html')
    return render_template('filterBooks.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages,
                           gen=selected_array)


@app.route('/filterBooks', methods=['GET', 'POST'])
def filter_books():
    page_number = request.args.get('pageNumber')
    num_pages = int(request.args.get('numPages'))
    book_list = []
    selected_array = []
    request_argument = request.args.get('gen')
    request_argument = request_argument.split()

    for i in range(len(request_argument)):
        if (request_argument[0])[2:-2].isalpha():
            if i == 0:
                key = (request_argument[i])[2:-2]
            else:
                key = (request_argument[i])[1:-2]
            selected_array.append(key)
            for book in books_collection.find({"genre": {"$regex": key}}):
                book_list.append(truncated_book(book))

        else:
            if i == 0:
                key = (request_argument[i])[2:-2]
            else:
                key = (request_argument[i])[1:-2]
            if (request_argument[0])[2:-2].find(".") == -1:
                field = "pageCount"
                key_number = int(key)
            else:
                field = "rating"
                key_number = float(key)
            if field == "rating":
                x = 1.01 + key_number
                selected_array.append((request_argument[0])[2:-2])
                if key_number == 9:
                    for book in books_collection.find({"rating": {"$gt": key_number - 1}}):
                        book_list.append(truncated_book(book))
                else:
                    for book in books_collection.find({"rating": {"$lt": x, "$gt": key_number}}):
                        book_list.append(truncated_book(book))
            else:
                key_number = int(key)
                selected_array.append(key)
                for book in books_collection.find(
                        {"pageCount": {"$gt": 100 * key_number, "$lt": (100 * key_number) + 301}}):
                    book_list.append(truncated_book(book))

    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterBooks.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages,
                               gen=selected_array)
    else:
        page_number = int(page_number)
        book_list = book_list[(int(page_number) * 10):(10 * int(page_number)) + 11]
        return render_template('filterBooks.html', books=book_list, pageNumber=page_number, perPage=10,
                               numPages=num_pages, gen=selected_array)

@app.route('/filterPub', methods=['GET', 'POST'])
def filter_pub():
    publisher_list = []
    selected_array = []
    num_pages = 0
    page_number = request.args.get('pageNumber')
    if page_number is None:
        page_number = '0'
        for key, value in request.form.items():
            selected_array.append(key)
            if key == "Newyork":
                key = "New York"
            for publisher in publishers_collection.find({"hqLocation": {"$regex": key}}):
                num_pages += 1
                publisher_list.append(truncated_publisher(publisher))

        num_pages = -(-num_pages // 10)
    else:
        gen = request.args.get('gen')
        selected = gen.split()
        for i in range(len(selected)):
            if i == 0:
                key = (selected[i])[2:-2]
            else:
                key = (selected[i])[1:-2]
            selected_array.append(key)
            if key == "Newyork":
                key = "New York"
            num_pages = int(request.args.get('numPages'))
            for publisher in publishers_collection.find({"hqLocation": {"$regex": key}}):
                publisher_list.append(truncated_publisher(publisher))

    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterPub.html', publishers=publisher_list, pageNumber=0, perPage=10,
                               numPages=num_pages, gen=selected_array)
    else:
        page_number = int(page_number)
        publisher_list = publisher_list[(int(page_number) * 10):(10 * int(page_number)) + 11]
        return render_template('filterPub.html', publishers=publisher_list, pageNumber=page_number, perPage=10,
                               numPages=num_pages, gen=selected_array)


@app.route('/filterAuthor', methods=['GET', 'POST'])
def filter_author():
    selected_array = []
    num_pages = 0
    author_list = []
    page_number = request.args.get('pageNumber')

    if page_number is None:
        page_number = '0'
        for key, value in request.form.items():
            selected_array.append(key)
            if key == "alive" or key == "dead":
                if key == "dead":
                    key = None
                    for author in authors_collection.find({"dod": {"$ne": key}}):
                        num_pages += 1
                        author_list.append(truncated_author(author))
                else:
                    key = None
                    for author in authors_collection.find({"dod": key}):
                        num_pages += 1
                        author_list.append(truncated_author(author))

            else:
                for author in authors_collection.find({"genres": {"$regex": key}}):
                    num_pages += 1
                    author_list.append(truncated_author(author))
        num_pages = -(-num_pages // 10)
    else:
        gen = request.args.get('gen')
        selected = gen.split()
        for i in range(len(selected)):
            if i == 0:
                key = (selected[i])[2:-2]
            else:
                key = (selected[i])[1:-2]
            selected_array.append(key)
            num_pages = int(request.args.get('numPages'))
            if key == "alive" or key == "dead":
                if key == "dead":
                    key = None
                    for author in authors_collection.find({"dod": {"$ne": key}}):
                        author_list.append(truncated_author(author))
                else:
                    key = None
                    for author in authors_collection.find({"dod": key}):
                        author_list.append(truncated_author(author))
            else:
                for author in authors_collection.find({"genres": {"$regex": key}}):
                    author_list.append(truncated_author(author))

    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterAuthor.html', authors=author_list, pageNumber=0, perPage=10, numPages=num_pages,
                               gen=selected_array)
    else:
        page_number = int(page_number)
        author_list = author_list[(int(page_number) * 10):(10 * int(page_number)) + 11]
        return render_template('filterAuthor.html', authors=author_list, pageNumber=page_number, perPage=10,
                               numPages=num_pages, gen=selected_array)


if __name__ == '__main__':
    app.run(debug=True)
