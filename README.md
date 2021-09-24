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

All pages are mobile responsive

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


## Files and Directories
* `Songs` - Main application directory
  * `database` - Main app directory
    * `static\database`
      * `database.js` - Contains the javascript code for loading songs, adding and removing songs from books, and deleting books
      * `sidebar.css` - Styling for sidebar 
      * `styles.css` - Empty
    * `templates\database` 
      * `add.html` - template for adding or editing a song
      * `index.html` - template for showing all the songs
      * `song.html` - template for showing a single song
      * `book_add.html` - template for adding or remove songs from a book
      * `book.html` - template for showing the songs in a book
      * `books.html` - template for showing the list of books
      * `favourites.html` - template for showing the favourited songs
      * `layout.html` - Contains the top-nav and side-nav components and used as a base for the other files
      * `login.html` - template for logging in
      * `register.html` - template for registering a user for the site
    * `admin.py` - registered the User, Book, and Song models
    * `models.py` - contains the three models (User, Book, Song), defines some functions for them, and a custom ManyToMany relationship between Book and Song
    * `urls.py` - all the application URLS
    * `views.py` - Contains the handlers for the url and json requests
*   `db.sqlite3` - the database used by the application



## How to run
You will need to install `django`. You will need to `python manage.py makemigrations` and `python manage.py migrate` before you run
`python manage.py runserver`.
You can optionally create a superuser using `python manage.py createsuperuser`if you want to use the admin interface.

## Future Work
The next stage is to support the display of chords in the chordpro format, along with instant transpose. Books should have an index, and Songs in a Book should also be retrievable by their index
