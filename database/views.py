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

def index(request):

    songs = Song.objects.all()
    return render(request, 'database/index.html', {
        "songs":songs
    })

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

def logout_view(request):
    logout(request)
    # redirect to a success page
    return HttpResponseRedirect(reverse("index"))

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

def song_view(request, id):
    song = {
        "title":"My Title",
        "author":"Mr Author",
        "meter":"8.8.8.8",
        "key":"C Major",
        "year":"1998",
        "content":"Mary had a little lamb whose fleece was white as snow"
    }

    song = Song.objects.get(id=id)
    return render(request, "database/song.html", {
        "song":song,
        "form":SongForm()
    })


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
            year = int(year) if year != None else ""
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

def fetch_songs(request):

    # Return a list of songs
    return JsonResponse({
        "success":"This worked",
        "song_list":[s.mini_serialize() for s in Song.objects.all()]
    })

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

def book_view(request, id):

    book = Book.objects.get(id=id)

    # Get all the song and relevant info
    songsinbook = Song_Book.objects.filter(book=book).select_related()

    return render(request, "database/book.html", {
        "songsinbook":songsinbook,
        "book":book
    })

def books_view(request):

    books = Book.objects.all()

    return render(request, "database/books.html", {
        "books":books
    })

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
    return HttpResponse("Edit book")

@login_required
@csrf_exempt
def song_to_book(request):
    if request.method != "POST":
        print(request)
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get new post data
    data = json.loads(request.body)
    print(data)


    # # SHould be able to add
    # # should be able to remove
    book_id = data.get("book_id")
    song_id = data.get("song_id")

    # Get the book to change
    book = Book.objects.get(id=book_id)

    # Get the song to change
    song = Song.objects.get(id=song_id)

    # Add the song to the book
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

    
@login_required
@csrf_exempt
def book_delete(request, id):
    book = Book.objects.get(id=id).delete()

    return HttpResponseRedirect(reverse("books"))


class BookForm(forms.Form):
    title =     forms.CharField(label='Title',      max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    year =      forms.IntegerField(label='Year',    required=False, widget=forms.TextInput(attrs={'class':'col-md-6 form-control'}))

class SongForm(forms.Form):
    title =     forms.CharField(label='Title',      max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    author =    forms.CharField(label='Author',     max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    composer =  forms.CharField(label='Composer',   max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    meter =     forms.CharField(label='Meter',      max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    key =       forms.CharField(label='Key',        max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    year =      forms.IntegerField(label='Year',    required=False, widget=forms.TextInput(attrs={'class':'col-md-6 form-control'}))
    content =   forms.CharField(label='Content',    max_length=1024, widget=forms.Textarea(attrs={'class':'form-control'}))



    