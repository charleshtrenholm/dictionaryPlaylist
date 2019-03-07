from django.shortcuts import render, redirect
from bs4 import BeautifulSoup, Tag, NavigableString
import re, requests, bcrypt, random, json, os
from .models import User, Playlist, URI
from django.contrib import messages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

client_credentials_manager = SpotifyClientCredentials(client_id = os.getenv('SPOTIFY_CLIENT_ID'), client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def index(request):
    url = 'https://www.merriam-webster.com/word-of-the-day/sentient-2019-03-03'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    word = soup.h1.string
    print("WORD:", word)
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

    saved_playlist = Playlist.objects.check_db_for_playlist(word = word)
    if saved_playlist: 
        print('The playlist has been saved', saved_playlist.uris)
        uris = URI.objects.filter(playlist = saved_playlist)
        print('URIS', uris)
        track = uris[0].string_val
    else:
        results = sp.search(q=word, limit=20, type="track")
        print('RESULTS:::::::::>', results)
        uris = [i['uri'] for i in results['tracks']['items']] #todo: revise this arraye
        print("URIS:::::::::>", uris)
        track = uris[0]
        p = Playlist(word = word)
        p.save()
        for uri in uris: 
            u = URI(string_val = uri, playlist = p)
            u.save()

    context = {
        'word' : word,
        'defs' : defs,
        'track' : track
    }

    return render(request, 'streaming/index.html', context)

def newSong(request):
    word = request.GET.get('word', None)
    uris = URI.objects.filter(playlist=word)
    newURI = uris[random.randInt(1, len(playlist.uris) - 1)].string_val
    result = {'value' : newURI}
    return json.dumps(result)

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
    
                            