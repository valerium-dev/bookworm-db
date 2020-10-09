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
    books = ['Beloved by Tony Morrison', 'The Magicians by Lev Grossman', '1984 by George Orwell']
    return render_template('books.html', books=books)


# TODO: Change route to use book id instead of book name in P.II
@app.route('/books/<string:book_name>')
def book_instance(book_name):
    book = dict()
    if book_name == 'beloved':
        book['title'] = ' '.join(book_name.split('-')).title()
        book['author'] = "Toni Morrison"
        book['page_count']="352"
        book['maturity']="NOT_MATURE"
        book['lang']= "en"
        book['publisher'] = "Alfred A. Knopf"
        book['published_date'] = "2019"
        book['description'] = "Upon the original publication of Beloved, John Leonard wrote in the Los Angeles Times: \"I can't imagine American literature without it.\" Nearly two decades later, The New York Times chose Beloved as the best American novel of the previous fifty years. Toni Morrison's magnificent Pulitzer Prize-winning work--first published in 1987--brought the wrenching experience of slavery into the literature of our time, enlarging our comprehension of America's original sin. Set in post-Civil War Ohio, it is the story of Sethe, an escaped slave who has lost a husband and buried a child; who has withstood savagery and not gone mad. Sethe, who now lives in a small house on the edge of town with her daughter, Denver, her mother-in-law, Baby Suggs, and a disturbing, mesmerizing apparition who calls herself Beloved. Sethe works at \"beating back the past,\" but it makes itself heard and felt incessantly: in her memory; in Denver's fear of the world outside the house; in the sadness that consumes Baby Suggs; in the arrival of Paul D, a fellow former slave; and, most powerfully, in Beloved, whose childhood belongs to the hideous logic of slavery and who has now come from the \"place over there\" to claim retribution for what she lost and for what was taken from her. Sethe's struggle to keep Beloved from gaining possession of the present--and to throw off the long-dark legacy of the past--is at the center of this spellbinding novel. But it also moves beyond its particulars, combining imagination and the vision of legend with the unassailable truths of history."
        book['isbn13'] = "9780525659273"
        book['genre'] = "Fiction"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=5xG_DwAAQBAJ&printsec=frontcover&img=1&source=gbs_api"
    elif book_name == 'the-magicians':
        book['title'] = ' '.join(book_name.split('-')).title()
        book['author'] = "Lev Grossman"
        book['maturity'] = "NOT_MATURE"
        book['page_count']="416"
        book['lang'] = "en"
        book['publisher'] = "Penguin"
        book['published_date'] = "2009-08-11"
        book['description'] = "The New York Times bestselling novel about a young man practicing magic in the real world, now an original series on SYFY “The Magicians is to Harry Potter as a shot of Irish whiskey is to a glass of weak tea. . . . Hogwarts was never like this.” —George R.R. Martin “Sad, hilarious, beautiful, and essential to anyone who cares about modern fantasy.” —Joe Hill “A very knowing and wonderful take on the wizard school genre.” —John Green “The Magicians may just be the most subversive, gripping and enchanting fantasy novel I’ve read this century.” —Cory Doctorow “This gripping novel draws on the conventions of contemporary and classic fantasy novels in order to upend them . . . an unexpectedly moving coming-of-age story.” —The New Yorker “The best urban fantasy in years.” —A.V. Club Quentin Coldwater is brilliant but miserable. A high school math genius, he’s secretly fascinated with a series of children’s fantasy novels set in a magical land called Fillory, and real life is disappointing by comparison. When Quentin is unexpectedly admitted to an elite, secret college of magic, it looks like his wildest dreams have come true. But his newfound powers lead him down a rabbit hole of hedonism and disillusionment, and ultimately to the dark secret behind the story of Fillory. The land of his childhood fantasies turns out to be much darker and more dangerous than he ever could have imagined. . . . The prequel to the New York Times bestselling book The Magician King and the #1 bestseller The Magician's Land, The Magicians is one of the most daring and inventive works of literary fantasy in years. No one who has escaped into the worlds of Narnia and Harry Potter should miss this breathtaking return to the landscape of the imagination."
        book['isbn13'] = "9781101082287"
        book['genre'] = "Fiction"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=d84AspgFjSwC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

    else:
        book['title'] = '1984'.join(book_name.split('-')).title()
        book['author'] = "George Orwell"
        book['page_count']="648"
        book['maturity'] = "NOT_MATURE"
        book['lang'] = "en"
        book['publisher'] = "Houghton Mifflin Harcourt"
        book['published_date'] = "1983-10-17"
        book['description'] = "George Orwell’s 1984 takes on new life with extraordinary relevance and renewed popularity. “Orwell saw, to his credit, that the act of falsifying reality is only secondarily a way of changing perceptions. It is, above all, a way of asserting power.”—The New Yorker In 1984, London is a grim city in the totalitarian state of Oceania where Big Brother is always watching you and the Thought Police can practically read your mind. Winston Smith is a man in grave danger for the simple reason that his memory still functions. Drawn into a forbidden love affair, Winston finds the courage to join a secret revolutionary organization called The Brotherhood, dedicated to the destruction of the Party. Together with his beloved Julia, he hazards his life in a deadly match against the powers that be. Lionel Trilling said of Orwell’s masterpiece, “1984 is a profound, terrifying, and wholly fascinating book. It is a fantasy of the political future, and like any such fantasy, serves its author as a magnifying device for an examination of the present.” Though the year 1984 now exists in the past, Orwell’s novel remains an urgent call for the individual willing to speak truth to power."
        book['isbn13'] = "9780547249643"
        book['genre'] = "Fiction"
        book['thumbnail_url'] = "http://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

    return render_template('book-instance.html', book=book)


# TODO: Phase I - Fetch author data from APIs
#       Phase II - Fetch author data from DB
@app.route('/authors/', methods=['GET'])
def authors():
    authors = ['Toni Morrison', 'Lev Grossman', 'George Orwell']
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
        author['born']= "June 25, 1903"
        author['died'] = "January 21, 1950"
        author['history'] = "Eric Arthur Blair (25 June 1903 \u2013 21 January 1950), known by his pen name George Orwell,  was an English novelist, essayist, journalist and critic. His work is characterised by lucid prose, biting social criticism, opposition to totalitarianism, and outspoken support of democratic socialism.As a writer, Orwell produced literary criticism and poetry, fiction and polemical journalism; and is best known for the allegorical novella Animal Farm (1945) and the dystopian novel Nineteen Eighty-Four (1949). His non-fiction works, including The Road to Wigan Pier (1937), documenting his experience of working-class life in the north of England, and Homage to Catalonia (1938), an account of his experiences soldiering for the Republican faction of the Spanish Civil War (1936\u20131939), are as critically respected as his essays on politics and literature, language and culture."
        author['other_books'] = "1984, Animal Farm, Down and Out in Paris and London, Homage to Catalonia, Burmese Days, The Road to Wigan Pier, Keep the Aspidistra Flying, Coming Up fo Air, Shootin an Elephant"
        author['thumbnail_url'] ="http://books.google.com/books/content?id=kotPYEqx7kMC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

    return render_template('author-instance.html', author=author)


# TODO: Phase I - Fetch pub data from APIs
#       Phase II - Fetch pub data from DB
@app.route('/publishers/', methods=['GET'])
def publishers():
    publishers = ['Alfred A. Knopf', 'Penguin', "Houghton Mifflin Harcourt"]
    return render_template('publishers.html', publishers=publishers)


# TODO: Change route to use publisher id instead of publisher name in P.II
@app.route('/publishers/<string:pub_name>')
def publisher_instance(pub_name):
    pub = dict()
    if pub_name == 'alfred-a-knopf':
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location']="New York City, New York, United States"
        pub['description']="Alfred A. Knopf, Inc. is an American publishing house that was founded by Alfred A. Knopf Sr. and Blanche Knopf in 1915.[1] Blanche and Alfred traveled abroad regularly and were known for publishing European, Asian, and Latin American writers in addition to leading American literary trends. It was acquired by Random House in 1960, and is now part of the Knopf Doubleday Publishing Group division of Penguin Random House which is owned by the German conglomerate Bertelsmann.[2][3] The Knopf publishing house is associated with its borzoi colophon, which was designed by co-founder Blanche Knopf in 1925."
    elif pub_name == 'penguin':
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location']="City of Westminster, London, England"
        pub['description']="Penguin Books is a British publishing house. It was co-founded in 1935 by Sir Allen Lane with his brothers Richard and John,[3] as a line of the publishers The Bodley Head, only becoming a separate company the following year.[4] Penguin revolutionised publishing in the 1930s through its inexpensive paperbacks, sold through Woolworths and other high street stores for sixpence, bringing high-quality paperback fiction and non-fiction to the mass market.[5] Penguin's success demonstrated that large audiences existed for serious books. Penguin also had a significant impact on public debate in Britain, through its books on culture, politics, the arts, and science"
    else:
        pub['name'] = ' '.join(pub_name.split('-')).title()
        pub['location']=" Sebastopol, CA, United States"
        pub['description']="One of the world's leading computer and technical book publishers. O’Reilly Media spreads the knowledge of innovators through its books, online services, magazines, research, and conferences. Since 1978, O’Reilly has been a chronicler and catalyst of leading-edge development, homing in on the technology trends that really matter and galvanizing their adoption by amplifying “faint signals” from the alpha geeks who are creating the future. An active participant in the technology community, the company has a long history of advocacy, meme-making, and evangelism"

    return render_template('publisher-instance.html', publisher=pub)


# TODO: Back-end work. Implement search algo
@app.route('/search/', methods=['GET', 'POST'])
def search():
    return "Search Results"


if __name__ == '__main__':
    app.run(debug=True)
