from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def checkRegistration(self, data):
        emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        userEmails = User.objects.all()
        errors = {}
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            errors['name'] = "Sorry: email must contain at least 2 characters"
        elif bool(re.search(r'\d', data['first_name'])) == True:
            errors['name'] = "Sorry: name must not contain a number"
        elif bool(re.search(r'\d', data['last_name'])) == True:
            errors['name'] = "Sorry name must not contain a number"
        elif not emailRegex.match(data['email']):
            errors['email'] = "Sorry: invalid email address"
        for email in userEmails:
            if data['email'] == email.email:
                errors['email'] = "Sorry: email already in use!"
        if bool(re.search(r'\d', data['password'])) == False:
            errors['password'] = "Sorry: Password must contain at least 1 number"
        elif len(data['password']) < 8:
            errors['password'] = "Sorry: Password Must contain at least 8 Characters"
        elif data['password'] != data['pw_confirm']:
            errors['password'] = "Sorry: Password and confirmation do not match"
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    email_option = models.CharField(max_length = 15)
    objects = UserManager()
    def __repr__(self):
        return "<user first name: {}, last name: {}, email: {}, email option: {}>".format(self.first_name, self.last_name, self.email, self.email_option)

class PlaylistManager(models.Manager):
    def check_db_for_playlist(self, word):
        playlists = Playlist.objects.all()
        for playlist in playlists:
            if playlist.word == word:
                return playlist
        return False

class Playlist(models.Model):
    word = models.CharField(max_length = 255)
    objects = PlaylistManager()

class URI(models.Model):
    string_val = models.CharField(max_length = 255)
    playlist = models.ForeignKey(Playlist, related_name = 'uris', on_delete = models.PROTECT)





# Create your models here.
