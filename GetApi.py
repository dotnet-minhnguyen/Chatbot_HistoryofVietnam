import json
import requests

# url_api_wiki = "https://vi.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&search="
url_api_wiki = "https://vi.wikipedia.org/w/api.php"
url_google = "https://www.google.com/search?q="


def getLinkWiki(text):

    api_url = '{0}{1}'.format(url_api_wiki, text)
    PARAMS = {
        'action': 'opensearch',
        'limit': '1',
        'namespace': '0',
        'format': 'json',
        'search': text
    }
    response = requests.get(url=url_api_wiki, params=PARAMS)

    if response.status_code == 200:
        if len(json.loads(response.content.decode('utf-8'))[3]):
            return json.loads(response.content.decode('utf-8'))[3][0]
        else:
            return "Tôi thấy tranng wiki này :("
    else:
        return "Get link failed!"


def getLinkGoogle(text):
    return url_google + text
