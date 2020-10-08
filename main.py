from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/about/')
def about():
    return render_template('about.html')


# TODO: Phase I - Fetch book data from APIs
#       Phase II - Fetch book data from DB
@app.route('/books/', methods=['GET'])
def books():
    books = ['Beloved by Tony Morrison', 'The Magicians by Lev Grossman', 'Fluent Python by Luciano Ramalho']
    return render_template('books.html', books=books)


# TODO: Change route to use book id instead of book name in P.II
@app.route('/books/<string:book_name>')
def book_instance(book_name):
    book = dict()
    if book_name == 'beloved':
        book['title'] = ' '.join(book_name.split('-')).title()
    elif book_name == 'the-magicians':
        book['title'] = ' '.join(book_name.split('-')).title()
    else:
        book['title'] = ' '.join(book_name.split('-')).title()

    return render_template('book-instance.html', book=book)


# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors/', methods=['GET'])
def authors():
    authors = ['Tony Morrison', 'Lev Grossman', 'Luciano Ramalho']
    return render_template('authors.html', authors=authors)


# TODO: Change route to use author id instead of author name in P.II
@app.route('/authors/<string:author_name>')
def author_instance(author_name):
    author = dict()
    if author == 'toni-morrison':
        author['name'] = ' '.join(author_name.split('-')).title()
    elif author_name == 'lev-grossman':
        author['name'] = ' '.join(author_name.split('-')).title()
    else:
        author['name'] = ' '.join(author_name.split('-')).title()

    return render_template('author-instance.html', author=author)


# TODO: Phase I - Fetch pub data from APIs
#       Phase II - Fetch pub data from DB
@app.route('/publishers/', methods=['GET'])
def publishers():
    publishers = ['Alfred A. Knopf', 'Viking Press', "O'Reilly"]
    return render_template('publishers.html', publishers=publishers)


# TODO: Change route to use publisher id instead of publisher name in P.II
@app.route('/publishers/<string:pub_name>')
def publisher_instance(pub_name):
    pub = dict()
    if pub_name == 'alfred-a-knopf':
        pub['name'] = ' '.join(pub_name.split('-')).title()
    elif pub_name == 'viking-press':
        pub['name'] = ' '.join(pub_name.split('-')).title()
    else:
        pub['name'] = ' '.join(pub_name.split('-')).title()

    return render_template('publisher-instance.html', publisher=pub)


# TODO: Back-end work. Implement search algo
@app.route('/search/', methods=['GET', 'POST'])
def search():
    return "Search Results"


if __name__ == '__main__':
    app.run(debug=True)
