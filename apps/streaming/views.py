from django.shortcuts import render, redirect
from bs4 import BeautifulSoup, Tag, NavigableString
import re, requests, bcrypt
from .models import User, Playlist
from django.contrib import messages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials(client_id ="client id", client_secret ="client secret")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def index(request):
    url = 'https://www.merriam-webster.com/word-of-the-day'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    word = soup.h1.string
    defTable = soup.find('div', attrs = {'class' : 'wod-definition-container'})

    if 'login' not in request.session:
        request.session['login'] = False

    defs = ''
    runner = defTable.find('h2')

    while runner.next_element != 'Did You Know?':
        if isinstance(runner, Tag):
            defs += str(runner)
            if runner.children:
                for child in runner.children:
                    if not isinstance(runner.next_element, Tag):
                        runner = runner.next_element.next_element
                    else:
                        runner = runner.next_element
        runner = runner.next_element

    print (isinstance(word, str))

    # results = sp.search(q="songs:" + word, limit = 20, type="song")
    # print(results)

    context = {
        'word' : word,
        'defs' : defs
    }

    return render(request, 'streaming/index.html', context)

def create(request):
    if 'word' not in request.session:
        request.session['word'] = request.POST['word']
    else:
        request.session['word'] = request.POST['word']
    return redirect('/result')

def result(request):
    context = {
        'word' : request.session['word']
    }
    return render(request, 'streaming/result.html', context)

def signup(request):
    errors = User.objects.checkRegistration(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/#userSignup')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'],
                            last_name = request.POST['last_name'],
                            email = request.POST['email'],
                            password = pw_hash.decode('utf-8'),
                            email_option = request.POST['email_option'])
        request.session['login'] = True
        if 'id' not in request.session:
            request.session['id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/success')

def success(request):
    context = {
        'loggedUser' : User.objects.get(id=request.session['id']),
        'users' : User.objects.all()
    }

    return render(request, "streaming/success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')
    
                            