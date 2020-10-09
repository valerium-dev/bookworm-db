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
        book['author'] = "Lev Grossman"
        book['publisher'] = "Penguin"
        book['published_date'] = "2009-08-11"
        book['description'] = "The New York Times bestselling novel about a young man practicing magic in the real world, now an original series on SYFY “The Magicians is to Harry Potter as a shot of Irish whiskey is to a glass of weak tea. . . . Hogwarts was never like this.” —George R.R. Martin “Sad, hilarious, beautiful, and essential to anyone who cares about modern fantasy.” —Joe Hill “A very knowing and wonderful take on the wizard school genre.” —John Green “The Magicians may just be the most subversive, gripping and enchanting fantasy novel I’ve read this century.” —Cory Doctorow “This gripping novel draws on the conventions of contemporary and classic fantasy novels in order to upend them . . . an unexpectedly moving coming-of-age story.” —The New Yorker “The best urban fantasy in years.” —A.V. Club Quentin Coldwater is brilliant but miserable. A high school math genius, he’s secretly fascinated with a series of children’s fantasy novels set in a magical land called Fillory, and real life is disappointing by comparison. When Quentin is unexpectedly admitted to an elite, secret college of magic, it looks like his wildest dreams have come true. But his newfound powers lead him down a rabbit hole of hedonism and disillusionment, and ultimately to the dark secret behind the story of Fillory. The land of his childhood fantasies turns out to be much darker and more dangerous than he ever could have imagined. . . . The prequel to the New York Times bestselling book The Magician King and the #1 bestseller The Magician's Land, The Magicians is one of the most daring and inventive works of literary fantasy in years. No one who has escaped into the worlds of Narnia and Harry Potter should miss this breathtaking return to the landscape of the imagination."
        book['isbn13'] = "9781101082287"
        book['genre'] = "Fiction"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=d84AspgFjSwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

    else:
        book['title'] = 'Fluent Python '.join(book_name.split('-')).title()
        book['author'] = "Lucian Ramalho"
        book['publisher'] = "O'Reilly Media, Inc."
        book['published_date'] = "2015-07-30"
        book['description'] = "Python’s simplicity lets you become productive quickly, but this often means you aren’t using everything it has to offer. With this hands-on guide, you’ll learn how to write effective, idiomatic Python code by leveraging its best—and possibly most neglected—features. Author Luciano Ramalho takes you through Python’s core language features and libraries, and shows you how to make your code shorter, faster, and more readable at the same time. Many experienced programmers try to bend Python to fit patterns they learned from other languages, and never discover Python features outside of their experience. With this book, those Python programmers will thoroughly learn how to become proficient in Python 3. This book covers: Python data model: understand how special methods are the key to the consistent behavior of objects Data structures: take full advantage of built-in types, and understand the text vs bytes duality in the Unicode age Functions as objects: view Python functions as first-class objects, and understand how this affects popular design patterns Object-oriented idioms: build classes by learning about references, mutability, interfaces, operator overloading, and multiple inheritance Control flow: leverage context managers, generators, coroutines, and concurrency with the concurrent.futures and asyncio packages Metaprogramming: understand how properties, attribute descriptors, class decorators, and metaclasses work"
        book['isbn13'] = "9781491946251"
        book['genre'] = "Computers"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=bIZHCgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

    return render_template('book-instance.html', book=book)


# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors/', methods=['GET'])
def authors():
    authors = ['Toni Morrison', 'Lev Grossman', 'Luciano Ramalho']
    return render_template('authors.html', authors=authors)


# TODO: Change route to use author id instead of author name in P.II
@app.route('/authors/<string:author_name>')
def author_instance(author_name):
    author = dict()
    if author_name == 'toni-morrison':
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] ="Lorain, Ohio"
        author['born']= "February 18, 1931"
        author['died'] = "August 05, 2019"
        author['other_books'] = "Beloved, The Bluest Eye, Song of Solomon, Sula, Paradise, Jazz, A Mercy, God Help the Child, Tar Baby, Home"
        author['thumbnail_url'] ="https://images.gr-assets.com/authors/1494211316p5/3534.jpg"
        author['history']= "Chloe Anthony Wofford Morrison known as Toni Morrison, was an American novelist, essayist, book editor, and college professor. Her first novel, The Bluest Eye, was published in 1970. The critically acclaimed Song of Solomon (1977) brought her national attention and won the National Book Critics Circle Award. In 1988, Morrison won the Pulitzer Prize for Beloved (1987); she gained worldwide recognition when she was awarded the Nobel Prize in Literature in 1993.Born and raised in Lorain, Ohio, Morrison graduated from Howard University in 1953 with a B.A. in English. In 1955, she earned a master's in American Literature from Cornell University. In 1957 she returned to Howard University, was married, and had two children before divorcing in 1964. In the late 1960s, she became the first black female editor in fiction at Random House in New York City. In the 1970s and 1980s, she developed her own reputation as an author, and her perhaps most celebrated work, Beloved, was made into a 1998 film.\nIn 1996, the National Endowment for the Humanities selected her for the Jefferson Lecture, the U.S. federal government's highest honor for achievement in the humanities. Also that year, she was honored with the National Book Foundation's Medal of Distinguished Contribution to American Letters. On May 29, 2012, President Barack Obama presented Morrison with the Presidential Medal of Freedom. In 2016, she received the PEN/Saul Bellow Award for Achievement in American Fiction"
    elif author_name == 'lev-grossman':
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] =" Concord, Massachusetts"
        author['born'] ="June 26, 1969"
        author['died'] = "Still Alive"
        author['other_books'] = "The Magicians(The Magicians, #1), The Magician King (The Magicians, #2), The Magician's Land (The Magicians,#3), Codex, The Magicians Trilogy Boxed Set, The Magicians and the Mafician King, The Magicians: Alice's Story, Warp, The Silver Arrow, The Connector"
        author['history'] ="Lev Grossman is an American novelist and journalist, who wrote The Magicians Trilogy: The Magicians (2009), The Magician King (2011), and The Magician's Land (2014). He was the book critic and lead technology writer at Time magazine from 2002 to 2016."
        author['thumbnail_url'] ="https://images.gr-assets.com/authors/1386343699p5/142270.jpg"
    else:
        author['name'] = ' '.join(author_name.split('-')).title()
        author['place_of_birth'] =""
        author['died'] = "Still alive"
        author['other_books'] = "NONE"
        author['thumbnail_url'] ="http://books.google.com/books/content?id=bIZHCgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

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
