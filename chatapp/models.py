from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)


    def __str__(self):
        return "Room : "+ self.name


class Message(models.Model):
    sender = models.CharField(max_length=255)
    user_id = models.CharField(max_length=25)
    content = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    read_message = models.BooleanField(default=False)


    def __str__(self):
        return "Message is :- "+ self.content
    

class Contact(models.Model):
    name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=13)
    user_id = models.CharField(max_length=13)
    # profile = models.ImageField(upload_to='/profile_pics', null=True, blank=True)

    def __str__(self):
        return self.mobile_number
