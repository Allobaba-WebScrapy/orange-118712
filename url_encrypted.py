import base64

class ENCRYPT:
    def __init__(self,url):
        self.url = url
    def encrypt_url(self):
        encoded_url = base64.b64decode(self.url).decode('utf-8')
        return encoded_url


