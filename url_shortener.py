import random
import string
import datetime
import json
from flask import Flask, redirect, request

app = Flask(__name__)

# Function to generate a random string
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Route to handle form submission and generate short URL
@app.route('/generate_short_url', methods=['POST'])
def generate_short_url():
    # Retrieve the original URL from the form data
    original_url = request.form['original_url']
    
    # Generate a random short URL
    short_url = generate_random_string(6)
    
    # Save the short URL, original URL, and expiration date to the JSON file
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
    with open('short_urls.json', 'r') as f:
        short_urls = json.load(f)
    short_urls[short_url] = {'original_url': original_url, 'expiration_date': str(expiration_date)}
    with open('short_urls.json', 'w') as f:
        json.dump(short_urls, f)
    
    # Return the short URL to the user
    return f'sloth.me/{short_url}'

# Route to handle requests to the short URL and redirect to the original URL
@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    # Retrieve the original URL from the JSON file based on the short URL
    with open('short_urls.json', 'r') as f:
        short_urls = json.load(f)
    original_url = short_urls[short_url]['original_url']
    
    # Redirect to the original URL
    return redirect(original_url)

if __name__ == '__main__':
    app.run()