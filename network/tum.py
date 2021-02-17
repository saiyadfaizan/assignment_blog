import pytumblr
from tumblr_keys import *    #this imports the content in our tumblr_keys.py file

# Authenticate via OAuth
client = pytumblr.TumblrRestClient(
    YarI8mnIJG3e5IfvmOkkqr0kVviLkAQv7SoWeXUHQFfhZGhQS0,
    3sE6qJ9Tz9NRFlUGQsEGxD1TI22quLpcJpprBQWoytfCE0ZiBS,
    g7wkKGZ9AdPUaW7dlOy6MbsE5tRjtRaYZiZFRroNZtLGeqzogP,
    X69ZFcrjA5QpH9StmmOaHj83Hd4uyXMosX7YmLRiLyPueyJoyf
)

#Posts an image to your tumblr.
#Make sure you point an image in your hard drive. Here, 'image.jpg' must be in the 
#same folder where your script is saved.
#From yourBlogName.tumblr.com should just use 'yourBlogName'
#The default state is set to "queue", to publish use "published"
#client.create_photo('saiyadfaizan.tumblr.com', state="published", tags=["testing", "ok"], data="image.jpg")
client.create_photo(saiyadfaizan, state="published", tags=["testing", "ok"],
                    tweet="Woah this is an incredible sweet post [URL]",
                    data="/rails/Downloads/user.jpg")

# client.posts('saiyadfaizan.tumblr.com')