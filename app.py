from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from pprint import pprint

app = Flask(__name__)


atlas_user = os.getenv("ATLAS_USER")
atlas_pwd = os.getenv("ATLAS_PASSWD")
mongo = MongoClient(f'mongodb+srv://{atlas_user}:{atlas_pwd}@cluster0.rh1w0.mongodb.net/book_worm_database?retryWrites=true&w=majority')
books_collection = mongo.book_worm_database.Books
authors_collection = mongo.book_worm_database.Authors
publishers_collection = mongo.book_worm_database.Publishers

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
        for book in books_collection.find({"_id":ObjectId("5f932cb187f700c50ebb04cd")}).limit(10):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=0, perPage=10, numPages=num_pages)
    else:
        page_number = int(page_number)
        per_page = int(per_page)
        num_pages = books_collection.estimated_document_count() // per_page
        book_list = []
        for book in books_collection.find({"_id":ObjectId("5f932cb187f700c50ebb04cd")}).skip(page_number * per_page).limit(per_page):
            temp = dict()
            temp['_id'] = book['_id']
            temp['title'] = book['title']
            temp['authors'] = book['authors']
            temp['genre'] = book['genre']
            temp['thumbnail_url'] = book['thumbnail']
            book_list.append(temp)
        return render_template('books.html', books=book_list, pageNumber=page_number, perPage=per_page, numPages=num_pages)



@app.route('/books/<string:book_id>')
def book_instance(book_id):

    book = books_collection.find_one({"_id":ObjectId(book_id)})
    pprint(book)
    return render_template('book-instance.html', book=book)


# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors', methods=['GET'])
def authors():
    authors = ['Toni Morrison', 'Lev Grossman', 'George Orwell']
    return render_template('authors.html', authors=authors)

# TODO: Change route to use author id instead of author name in P.II
@app.route('/authors/<string:author_name>')
def author_instance(author_name):
    author = dict()
    if author_name == 'toni-morrison':
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] = "Lorain, Ohio"
        author['born'] = "February 18, 1931"
        author['died'] = "August 05, 2019"
        author[
            'other_books'] = "Beloved, The Bluest Eye, Song of Solomon, Sula, Paradise, Jazz, A Mercy, God Help the Child, Tar Baby, Home"
        author['thumbnail_url'] = "https://images.gr-assets.com/authors/1494211316p5/3534.jpg"
        author[
            'history'] = "Chloe Anthony Wofford Morrison known as Toni Morrison, was an American novelist, essayist, book editor, and college professor. Her first novel, The Bluest Eye, was published in 1970. The critically acclaimed Song of Solomon (1977) brought her national attention and won the National Book Critics Circle Award. In 1988, Morrison won the Pulitzer Prize for Beloved (1987); she gained worldwide recognition when she was awarded the Nobel Prize in Literature in 1993.Born and raised in Lorain, Ohio, Morrison graduated from Howard University in 1953 with a B.A. in English. In 1955, she earned a master's in American Literature from Cornell University. In 1957 she returned to Howard University, was married, and had two children before divorcing in 1964. In the late 1960s, she became the first black female editor in fiction at Random House in New York City. In the 1970s and 1980s, she developed her own reputation as an author, and her perhaps most celebrated work, Beloved, was made into a 1998 film.\nIn 1996, the National Endowment for the Humanities selected her for the Jefferson Lecture, the U.S. federal government's highest honor for achievement in the humanities. Also that year, she was honored with the National Book Foundation's Medal of Distinguished Contribution to American Letters. On May 29, 2012, President Barack Obama presented Morrison with the Presidential Medal of Freedom. In 2016, she received the PEN/Saul Bellow Award for Achievement in American Fiction"
    elif author_name == 'lev-grossman':
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] = " Concord, Massachusetts"
        author['born'] = "June 26, 1969"
        author['died'] = "Still Alive"
        author[
            'other_books'] = "The Magicians(The Magicians, #1), The Magician King (The Magicians, #2), The Magician's Land (The Magicians,#3), Codex, The Magicians Trilogy Boxed Set, The Magicians and the Mafician King, The Magicians: Alice's Story, Warp, The Silver Arrow, The Connector"
        author[
            'history'] = "Lev Grossman is an American novelist and journalist, who wrote The Magicians Trilogy: The Magicians (2009), The Magician King (2011), and The Magician's Land (2014). He was the book critic and lead technology writer at Time magazine from 2002 to 2016."
        author['thumbnail_url'] = "https://images.gr-assets.com/authors/1386343699p5/142270.jpg"
    else:
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] = ""
        author['born'] = "June 25, 1903"
        author['died'] = "January 21, 1950"
        author['history'] = "Eric Arthur Blair (25 June 1903 \u2013 21 January 1950), known by his pen name George Orwell,  was an English novelist, essayist, journalist and critic. His work is characterised by lucid prose, biting social criticism, opposition to totalitarianism, and outspoken support of democratic socialism.As a writer, Orwell produced literary criticism and poetry, fiction and polemical journalism; and is best known for the allegorical novella Animal Farm (1945) and the dystopian novel Nineteen Eighty-Four (1949). His non-fiction works, including The Road to Wigan Pier (1937), documenting his experience of working-class life in the north of England, and Homage to Catalonia (1938), an account of his experiences soldiering for the Republican faction of the Spanish Civil War (1936\u20131939), are as critically respected as his essays on politics and literature, language and culture."
        author['other_books'] = "1984, Animal Farm, Down and Out in Paris and London, Homage to Catalonia, Burmese Days, The Road to Wigan Pier, Keep the Aspidistra Flying, Coming Up fo Air, Shootin an Elephant"
        author['thumbnail_url'] = "http://www.thomaswictor.com/wp-content/uploads/2015/04/george-orwell.jpg"

    return render_template('author-instance.html', author=author)


# TODO: Phase I - Fetch pub data from APIs
#       Phase II - Fetch pub data from DB
@app.route('/publishers', methods=['GET'])
def publishers():
    publishers = ['Alfred A. Knopf', 'Penguin', "Houghton Mifflin Harcourt"]
    return render_template('publishers.html', publishers=publishers)


# TODO: Change route to use publisher id instead of publisher name in P.II
@app.route('/publishers/<string:pub_name>')
def publisher_instance(pub_name):
    pub = dict()
    if pub_name == 'alfred-a-knopf':
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location'] = "New York City, New York, United States"
        pub['description'] = "Alfred A. Knopf, Inc. is an American publishing house that was founded by Alfred A. Knopf Sr. and Blanche Knopf in 1915.[1] Blanche and Alfred traveled abroad regularly and were known for publishing European, Asian, and Latin American writers in addition to leading American literary trends. It was acquired by Random House in 1960, and is now part of the Knopf Doubleday Publishing Group division of Penguin Random House which is owned by the German conglomerate Bertelsmann.[2][3] The Knopf publishing house is associated with its borzoi colophon, which was designed by co-founder Blanche Knopf in 1925."
        pub['logo_url'] = url_for('static', filename='/publisher-logos/Knopf.png')
    elif pub_name == 'penguin':
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location'] = "City of Westminster, London, England"
        pub['description'] = "Penguin Books is a British publishing house. It was co-founded in 1935 by Sir Allen Lane with his brothers Richard and John,[3] as a line of the publishers The Bodley Head, only becoming a separate company the following year.[4] Penguin revolutionised publishing in the 1930s through its inexpensive paperbacks, sold through Woolworths and other high street stores for sixpence, bringing high-quality paperback fiction and non-fiction to the mass market.[5] Penguin's success demonstrated that large audiences existed for serious books. Penguin also had a significant impact on public debate in Britain, through its books on culture, politics, the arts, and science"
        pub['logo_url'] = url_for('static', filename='/publisher-logos/penguin.jpg')
    else:
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location'] = "Boston, MA, United States"
        pub['description'] = "As a global learning company, HMH specializes in pre-K–12 education content, services and cutting edge technology solutions for today’s changing landscape.\nHMH creates engaging, dynamic and effective educational content and experiences from early childhood to K-12 and beyond the classroom, serving more than 50 million students in more than 150 countries. Available through multiple media, our content meets the needs of students, teachers, parents and lifelong learners, no matter where and how they learn.\nOur renowned and awarded children's books, novels, nonfiction, and reference titles are enjoyed by readers throughout the world. Our distinguished author list, from Ralph Waldo Emerson to Philip Roth, and brands from Curious George to The Lord of the Rings, includes 10 Nobel Prize winners, 48 Pulitzer Prize winners, 15 National Book Award winners, and more than 100 Caldecott, Newbery, Printz and Sibert Medal and Honor recipients. "
        pub['logo_url'] = url_for('static', filename='/publisher-logos/hmh.jpg')

    return render_template('publisher-instance.html', publisher=pub)


# TODO: Back-end work. Implement search algo
@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
