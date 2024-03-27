import base64

def encrypt_url(url):
    encoded_url = base64.b64decode(url).decode('utf-8')
    return encoded_url