from urllib.parse import urlparse

def get_host(url):
    return urlparse(url).netloc

def get_path(url):
    return urlparse(url).path