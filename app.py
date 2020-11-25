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
            book_list.append(truncated_book(book))
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for book in books_collection.find().skip(page_number * per_page).limit(per_page):
            book_list.append(truncated_book(book))
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
            author_list.append(truncated_author(author))
        return render_template('authors.html', authors=author_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for author in authors_collection.find().skip(page_number * per_page).limit(per_page):
            author_list.append(truncated_author(author))
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
    return temp


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
            publisher_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)
    else:
        for publisher in publishers_collection.find().skip(page_number * per_page).limit(per_page):
            publisher_list.append(truncated_publisher(publisher))
        return render_template('publishers.html', publishers=publisher_list, pageNumber=page_number, perPage=per_page,
                               numPages=num_pages, sortType=sort_type)


@app.route('/publishers/<string:pub_id>')
def publisher_instance(pub_id):
    publisher = publishers_collection.find_one({"_id": ObjectId(pub_id)})
    pprint(publisher)
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
    filters = getActiveFilters()
    search_results = search_instances(search_type, search_query, page_num, per_page, sort_type, filters)
    num_pages = len(search_results) // per_page

    return render_template('search.html', searchResults=search_results, searchQuery=search_query,
                           searchType=search_type, pageNumber=page_num, perPage=per_page, numPages=num_pages,
                           sortType=sort_type)


def search_instances(search_type, query, page_num, per_page, sort_type, filters):
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
                        sort_type).skip(
                        page_num * per_page).limit(per_page):
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


def getActiveFilters():
    return None


@app.route('/filter', methods=['GET', 'POST'])
def filter():

    book_list = []
    selectedArray = []
    num_pages = 0
    keyNumber = 0
    field = ""

    for key, value in request.form.items():
        selectedArray.append(key)
        field = "genre"
        if not key.isalpha():
            if key.find(".") == -1:
                field = "pageCount"
                keyNumber = int(key)
            else:
                field = "rating"
                keyNumber = float(key)
        if field == "genre":
              for book in books_collection.find({"genre": {"$regex": key}}):
                  num_pages += 1
                  book_list.append(truncated_book(book))
        elif field == "rating":
              print("is a rating")
              x = (1.01)+keyNumber
              for book in books_collection.find({"rating": {"$lt":x, "$gt": keyNumber}}):
                  num_pages += 1
                  book_list.append(truncated_book(book))
        else:
              print("we get to page count")
              for book in books_collection.find({"pageCount": {"$gt":100 * keyNumber, "$lt": (100 * keyNumber) + 301}}):
                  num_pages += 1
                  book_list.append(truncated_book(book))

    num_pages = -(-num_pages//10)
    print(num_pages)
    print(len(book_list))
    if num_pages == 0:
        return render_template('noResults.html')
    return render_template('filterBooks.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages, gen=selectedArray)


@app.route('/filterBooks', methods=['GET', 'POST'])
def filterBooks():


    page_number = request.args.get('pageNumber')
    num_pages = int(request.args.get('numPages'))
    book_list = []
    selectedArray = []
    genre = request.args.get('gen')
    selected = genre.split()
    key2 = (selected[0])[2:-2]


    for i in range(len(selected)):
        if key2.isalpha():
            if i == 0:
                key = (selected[i])[2:-2]
            else:
                key = (selected[i])[1:-2]
            selectedArray.append(key)
            for book in books_collection.find({"genre": {"$regex": key} }):
                book_list.append(truncated_book(book))
        else:
            if i == 0:
                key = (selected[i])[2:-2]
            else:
                key = (selected[i])[1:-2]
            if key2.find(".") == -1:
                field = "pageCount"
                keyNumber = int(key)
            else:
                field = "rating"
                keyNumber = float(key)
            if field == "rating":
                x = (1.01) + keyNumber
                selectedArray.append(key2)
                if keyNumber == 9:
                    for book in books_collection.find({"rating": {"$gt": keyNumber-1}}):
                        book_list.append(truncated_book(book))
                else:
                    for book in books_collection.find({"rating": {"$lt":x, "$gt": keyNumber}}):
                        book_list.append(truncated_book(book))
            else:
                keyNumber = int(key)
                selectedArray.append(key)
                for book in books_collection.find({"pageCount": {"$gt": 100 * keyNumber, "$lt": (100 * keyNumber) + 301}}):
                    book_list.append(truncated_book(book))

    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterBooks.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages, gen=selectedArray)
    else:
        page_number = int(page_number)
        book_list = book_list[(int(page_number)*10):(10*int(page_number))+11]
        return render_template('filterBooks.html', books=book_list, pageNumber=page_number, perPage=10, numPages=num_pages,gen=selectedArray)

@app.route('/filterPub', methods=['GET', 'POST'])
def filterPub():
    publisher_list = []
    genreArray = []
    num_pages = 0
    page_number = request.args.get('pageNumber')
    if page_number is None:
        page_number = '0'
        for key, value in request.form.items():
            genreArray.append(key)
            if key == "Newyork":
                key = "New York"
            for publisher in publishers_collection.find({"hqLocation": {"$regex": key}}):
                num_pages+=1
                publisher_list.append(truncated_publisher(publisher))
        pprint(publisher_list)
        num_pages = -(-num_pages // 10)
    else:
        gen = request.args.get('gen')
        print(gen)
        selected = gen.split()
        print(len(selected))
        for i in range(len(selected)):
            if i == 0:
                key = (selected[i])[2:-2]
            else:
                key = (selected[i])[1:-2]
            print(key)
            genreArray.append(key)
            if key == "Newyork":
                key = "New York"
            num_pages = int(request.args.get('numPages'))
            for publisher in publishers_collection.find({"hqLocation": {"$regex": key}}):
                publisher_list.append(truncated_publisher(publisher))
        pprint(publisher_list)
    print(num_pages)
    print(len(publisher_list))
    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterPub.html', publishers=publisher_list, pageNumber=0, perPage=10, numPages=num_pages, gen=genreArray)
    else:
        print("we should be in this else")
        print(page_number)
        page_number = int(page_number)
        publisher_list = publisher_list[(int(page_number)*10):(10*int(page_number))+11]
        print("printing publisher list")
        pprint(publisher_list)
        return render_template('filterPub.html', publishers=publisher_list, pageNumber=page_number, perPage=10, numPages=num_pages,gen=genreArray)

@app.route('/filterAuthor', methods=['GET', 'POST'])
def filterAuthor():
    print(request.form)
    print(request.args)
    genreArray = []
    num_pages = 0
    author_list = []

    page_number = request.args.get('pageNumber')

    if page_number is None:
        page_number = '0'
        for key, value in request.form.items():
            genreArray.append(key)
            if key == "alive" or key == "dead":
                if key == "dead":
                    print("looking for dead peps")
                    key = None
                    for author in authors_collection.find({"dod": {"$ne":key}}):
                      num_pages+=1
                      author_list.append(truncated_author(author))
                else:
                    key = None
                    for author in authors_collection.find({"dod": key }):
                      num_pages+=1
                      author_list.append(truncated_author(author))

            else:
                for author in authors_collection.find({"genres": {"$regex": key}}):
                  num_pages+=1
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
            genreArray.append(key)
            num_pages = int(request.args.get('numPages'))
            if key == "alive" or key == "dead":
                if key == "dead":
                    print("loking for dead folk")
                    key = None
                    for author in authors_collection.find({"dod": {"$ne":key}}):
                      author_list.append(truncated_author(author))
                else:
                    key = None
                    for author in authors_collection.find({"dod": key }):
                      author_list.append(truncated_author(author))
            else:
                for author in authors_collection.find({"genres": {"$regex": key}}):
                    author_list.append(truncated_author(author))

    if num_pages == 0:
        return render_template('noResults.html')
    if int(page_number) == 0:
        return render_template('filterAuthor.html', authors=author_list, pageNumber=0, perPage=10, numPages=num_pages, gen=genreArray)
    else:
        page_number = int(page_number)
        author_list = author_list[(int(page_number) * 10):(10 * int(page_number)) + 11]
        return render_template('filterAuthor.html', authors=author_list, pageNumber=page_number, perPage=10,numPages=num_pages, gen=genreArray)


if __name__ == '__main__':
    app.run(debug=True)
