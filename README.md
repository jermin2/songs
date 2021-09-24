# Songs
An online database to find/store/edit songs, and sort them into songbooks.

A project written in Python, JavaScript, Django as a Final Project for CS50W Web Programming Course 2021

## Features:
Songs can have the following meta-data
- Author
- Composer
- Meter
- Key
- Year

Songs can also be grouped via a Book. 

A Book can have many songs (but only one of each). User must be able to click through to a song from a book. A book also has a title and a year

Authenticated users are able to add/remove/edit Songs and Books. They are also able to favourite songs to a favourites list which is displayed on the side-nav. Unauthenticated users can view songs and books.

# Distinctiveness and Complexity
This application is more complex than previous projects due to the relationship and requirement for users to be able to modify Books, which contain Songs. Users must not only be able to add/remove/edit Songs, but users must be able to add and remove songs from Books. Each song can only appear once in a Book.
Another feature is the search bar, which adds a keyup listener to real-time filter through the titles.

## Features:
Models:
* User
* Book
* Song

## JSON Queries:
* Add/remove favourites
* Add/remove songs from books
* "search as you type" style search bar
* Loading of songs and sidebar lists


## File Contents
### Song
* **add.html** - Form for adding/editing a Song
* **index.html** - Show all the songs in the database
* **song.html** - Show a song
* 
### Book
* **book_add.html** - Form for adding a Songs to a Book
* **book.html** - Show the contents of a book
* **books.html** - Show the list of all the books

### Misc
* **favourites.html** - Show all the favourited songs of a user
* **layout.html** - Contains the top-nav and side-nav components and used as a base for the other files
* **login.html** - Form for logging into the site
* **register.html** - Form for registering for the site

### Styling and Javascript
* **database.js** - Contains the javascript code for loading songs, adding and removing songs from books, and deleting books
* **sidebar.css** - Styling for sidebar 
* **styles.css** - Empty
* **views.py** - Contains the handlers for the url and json requests

## How to run
No need to install any additional files. You will need to <code>makemigrations</code> and <code>migrate</code> before you run
<code>python manage.py runserver</code>

## Future Work
The next stage is to support the display of chords in the chordpro format, along with instant transpose. Books should have an index, and Songs in a Book should also be retrievable by their index
