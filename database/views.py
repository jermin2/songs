from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms


from .models import User, Song

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
            "edit":True
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
            "edit":True
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
            year = int(year) if year != None else ""
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
            "form":form
        })

    return render(request, "database/add.html", {
        "form":SongForm()
    })
    


class SongForm(forms.Form):
    title =     forms.CharField(label='Title',      max_length=100, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    author =    forms.CharField(label='Author',     max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    composer =  forms.CharField(label='Composer',   max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    meter =     forms.CharField(label='Meter',      max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    key =       forms.CharField(label='Key',        max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'col-md-6 form-control'}))
    year =      forms.IntegerField(label='Year',    required=False, widget=forms.TextInput(attrs={'class':'col-md-6 form-control'}))
    content =   forms.CharField(label='Content',    max_length=1024, widget=forms.Textarea(attrs={'class':'form-control'}))



    