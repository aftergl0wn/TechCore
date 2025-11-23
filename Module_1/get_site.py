import requests


def get_site(URL):
    response = requests.get(URL)
    data = response.json()
    return data


if __name__ == "__main__":
    print(get_site("https://httpbin.org/get"))
