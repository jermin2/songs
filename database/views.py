from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django import forms
from django.http import JsonResponse
import json

from .models import User, Song, Book, Song_Book

# Get the list of all the songs
def index(request):

    songs = Song.objects.all()
    return render(request, 'database/index.html', {
        "songs":songs
    })

# The Login View
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirecto to a success page.
            return HttpResponseRedirect(reverse("index"))
        else:
            # return an 'invalid login' error message
            return render(request, "database/login.html", {
                "message": "Invalid username and/or password. "
            })
    else:
        return render(request, "database/login.html")

# The Logout function
def logout_view(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect(reverse("index"))

# The register view
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "database/register.html", {
                "message":"Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "database/register.html", {
                "message":"Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "database/register.html")

# View a single song
def song_view(request, id):

    song = Song.objects.get(id=id)
    favourite = False

    # If user is logged in, return the favourite status in JSON payload
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        favourite = user.favourites.filter(id=id).exists()

    return render(request, "database/song.html", {
        "song":song,
        "form":SongForm(),
        "favourite":favourite
    })

# View favourites
@login_required
def favourites_view(request):

    # Get the user object
    user = User.objects.get(id=request.user.id)

    # Get all the song and relevant info
    favourites = user.favourites.all()

    return render(request, "database/favourites.html", {
        "favourites":favourites,
    })

# Edit a song
@login_required
def edit(request, id):
    if request.method=="POST":
        # Take in the data the user submitted and save it as form
        form = SongForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Isolate the data from the 'cleaned' version
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            composer = form.cleaned_data["composer"]
            key = form.cleaned_data["key"]
            meter = form.cleaned_data["meter"]
            year = form.cleaned_data["year"]
            year = int(year) if year != None else None
            content = form.cleaned_data["content"]

            try:
                song = Song.objects.get(id=id)
                song.title = title
                song.author = author
                song.composer = composer
                song.key = key
                song.meter = meter
                song.year = year
                song.content = content

                song.save()

                return HttpResponseRedirect(reverse("song", args=(song.id,)))
            except Exception as e:
                print(e)
                print("caught exception")
                return HttpResponse(e)
        
        # If form is invalid
        print("Form is invalid")
        return render(request, "database/add.html", {
            "id":id,
            "form":form,
            "route":"edit",
            "title":"Edit Song"
        })
    
    # GET request
    else:
        song = Song.objects.get(id=id)

        form = SongForm(initial={
            "title": song.title,
            "author":song.author,
            "composer":song.composer,
            "meter":song.meter,
            "key":song.key,
            "year":song.year,
            "content":song.content
        })
        
        return render(request, "database/add.html",{ 
            "id":id,
            "form":form,
            "route":"edit",
            "title":"Edit Song"
        })

# Add a new song
@login_required
def add(request):

    if request.method=="POST":
        # Take in the data the user submitted and save it as form
        form = SongForm(request.POST)

        # Check if form is valid
        if form.is_valid():

            # Isolate the data from the 'cleaned' version
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            composer = form.cleaned_data["composer"]
            key = form.cleaned_data["key"]
            meter = form.cleaned_data["meter"]
            year = form.cleaned_data["year"]
            year = int(year) if year != None else None
            content = form.cleaned_data["content"]

            try:
                song = Song.objects.create(
                    title=title, 
                    author=author, 
                    composer=composer, 
                    key=key, 
                    meter=meter,
                    year=year,
                    content=content)
                song.save()

                # Link back to the page
                return HttpResponseRedirect(reverse("song", args=(song.id,)))
            except Exception as e:
                print(e)
                return HttpResponse(e)
            
        # If form is invalid
        return render(request, "database/add.html", {
            "form":form,
            "title": "Add Song",
        })

    return render(request, "database/add.html", {
        "form":SongForm(),
        "title": "Add Song",
    })

# JSON Response to get all the songs
def fetch_songs(request):

    # Return a list of songs
    return JsonResponse({
        "success":"Success",
        "song_list":[s.mini_serialize() for s in Song.objects.all()]
    })

# Add a new book
@login_required
def add_book(request):

    if request.method=="POST":
        # Take in the data the user submitted and save it as form
        form = BookForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            # Isolate the data from the 'cleaned' version
            title = form.cleaned_data["title"]
            year = form.cleaned_data["year"]

            try:
                book = Book.objects.create(
                    title=title,
                    year=year
                )
                book.save()
                return HttpResponseRedirect(reverse("index"))

            except Exception as e:
                print(e)
                return HttpResponse(e)

        # If form is invalid
        return render(request, "database/add.html", {
            "form":form,
            "title": "New Book",
            "route": "add_book"
        })

    return render(request, "database/add.html", {
        "title": "New Book",
        "form":BookForm(),
        "route": "add_book"
    })

# View a book with all it's songs
def book_view(request, id):

    book = Book.objects.get(id=id)

    # Get all the song and relevant info
    songsinbook = Song_Book.objects.filter(book=book).select_related()

    return render(request, "database/book.html", {
        "songsinbook":songsinbook,
        "book":book,
    })

# View all the books
def books_view(request):

    books = Book.objects.all()

    return render(request, "database/books.html", {
        "books":books
    })

# Edit a book
@login_required
def book_edit(request, id):

    book = Book.objects.get(id=id)
    # Get all the song and relevant info
    songsinbook = Song_Book.objects.filter(book=book).select_related()

    return render(request, "database/book_add.html", {
        "songsinbook":songsinbook,
        "songs":Song.objects.all(),
        "book":book
    })

# JSON Request to put a song in a book
@login_required
@csrf_exempt
def song_to_book(request):
    if request.method != "POST":
        print(request)
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get new post data
    data = json.loads(request.body)

    # Get the book to change
    book = Book.objects.get(id=data.get("book_id"))

    # Get the song to change
    song = Song.objects.get(id=data.get("song_id"))

    # Add or remove the song from the book
    try:
        if data.get("method") == "add":
            book.songs.add(song)
        elif data.get("method") == "remove":
            book.songs.remove(song)
        book.save()

    except Exception as e:
        return JsonResponse({
            "fail":e
        })

    # Return JsonResponse of new book list
    return JsonResponse({
        "success":"Adding song to book",
        "songs":[book.mini_serialize() for book in book.songs.all()],
        "song":song.mini_serialize()
    })

# Delete a book
@login_required
@csrf_exempt
def book_delete(request, id):
    book = Book.objects.get(id=id).delete()

    return HttpResponseRedirect(reverse("books"))

# JSON Request to favourite a book
@login_required
@csrf_exempt
def favourite(request):
    if request.method != "POST":
        print(request)
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get new post data
    data = json.loads(request.body)

    # Get the user
    user = User.objects.get(id=request.user.id)

    # Get the song
    song = Song.objects.get(id = int(data.get('song_id')))

    # Add or remove the song from the user's favourites
    try:
        if data.get("method") == "favourite":
            user.favourites.add(song)
        elif data.get("method") == "unfavourite":
            user.favourites.remove(song)
        user.save()

    except Exception as e:
        return JsonResponse({
            "fail":str(e)
        })

    # Return JsonResponse of new favourites list
    return JsonResponse({
        "success":"Success",
        "id": data.get("song_id"),
        "favourite": user.favourites.filter(id=song.id).exists(),
        "favourites_list": [song.mini_serialize() for song in user.favourites.all()]
    })

# JSON request to grab the sidebar data
def sidebar(request):

    favourites = False
    # Only send favourites data if user is logged in
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        favourites = [song.mini_serialize() for song in user.favourites.all()]

    return JsonResponse({
        "books":[book.serialize() for book in Book.objects.all()],
        "favourites": favourites
    })


    
# DJANGO Form for Book Class
class BookForm(forms.Form):
    title =     forms.CharField(label='Title',      max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    year =      forms.IntegerField(label='Year',    required=False, widget=forms.TextInput(attrs={'class':'col-md-6 form-control'}))

# DJANGO Form for Song Class
class SongForm(forms.Form):
    title =     forms.CharField(label='Title',      max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    author =    forms.CharField(label='Author',     max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    composer =  forms.CharField(label='Composer',   max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    meter =     forms.CharField(label='Meter',      max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    key =       forms.CharField(label='Key',        max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    year =      forms.IntegerField(label='Year',    required=False, widget=forms.TextInput(attrs={'class':'col-md-6 form-control'}))
    content =   forms.CharField(label='Content',    max_length=1024, widget=forms.Textarea(attrs={'class':'form-control'}))



    