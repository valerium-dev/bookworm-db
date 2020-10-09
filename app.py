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
        book['author'] = "Toni Morrison"
        book['publisher'] = "Alfred A. Knopf"
        book['published_date'] = "2019"
        book['description'] = "Upon the original publication of Beloved, John Leonard wrote in the Los Angeles Times: \"I can't imagine American literature without it.\" Nearly two decades later, The New York Times chose Beloved as the best American novel of the previous fifty years. Toni Morrison's magnificent Pulitzer Prize-winning work--first published in 1987--brought the wrenching experience of slavery into the literature of our time, enlarging our comprehension of America's original sin. Set in post-Civil War Ohio, it is the story of Sethe, an escaped slave who has lost a husband and buried a child; who has withstood savagery and not gone mad. Sethe, who now lives in a small house on the edge of town with her daughter, Denver, her mother-in-law, Baby Suggs, and a disturbing, mesmerizing apparition who calls herself Beloved. Sethe works at \"beating back the past,\" but it makes itself heard and felt incessantly: in her memory; in Denver's fear of the world outside the house; in the sadness that consumes Baby Suggs; in the arrival of Paul D, a fellow former slave; and, most powerfully, in Beloved, whose childhood belongs to the hideous logic of slavery and who has now come from the \"place over there\" to claim retribution for what she lost and for what was taken from her. Sethe's struggle to keep Beloved from gaining possession of the present--and to throw off the long-dark legacy of the past--is at the center of this spellbinding novel. But it also moves beyond its particulars, combining imagination and the vision of legend with the unassailable truths of history."
        book['isbn13'] = "9780525659273"
        book['genre'] = "Fiction"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=5xG_DwAAQBAJ&printsec=frontcover&img=1&source=gbs_api"
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
    publishers = ['Alfred A. Knopf', 'Penguin', "O'Reilly"]
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
