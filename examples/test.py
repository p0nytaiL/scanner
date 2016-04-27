import requests

if __name__ == '__main__':
    response = requests.get('http://www.github.com')
    ip = response.raw._fp
    print response
