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
    books = ['Beloved by Tony Morrison', 'The Magicians by Lev Grossman']
    return render_template('books.html', books=books)

# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors/', methods=['GET'])
def authors():
    authors = ['Author Instance 1', 'Author Instance 2']
    return render_template('authors.html', authors=authors)

# TODO: Phase I - Fetch pub data from APIs
#       Phase II - Fetch pub data from DB
@app.route('/publishers/', methods=['GET'])
def publishers():
    pubs = ['Publisher Instance 1', 'Publisher Instance 2']
    return render_template('publishers.html', pubs=pubs)

# TODO: Back-end work. Implement search algo
@app.route('/search/', methods=['GET', 'POST'])
def search():
    return "Search Results"

if __name__ == '__main__':
    app.run(debug=True)