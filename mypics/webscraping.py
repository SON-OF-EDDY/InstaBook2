from bs4 import BeautifulSoup
import requests

def find_course():

    my_url = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=RUB'

    result = requests.get(my_url)

    soup = BeautifulSoup(result.text, 'html.parser')

    output = soup.find("p", class_="result__BigRate-sc-1bsijpp-1 iGrAod")

    if output != None:
        output = output.text
    else:
        output = 'Not Found'

    return output


def find_weather():

    my_url = 'https://www.tomorrow.io/weather/'

    result = requests.get(my_url)

    soup = BeautifulSoup(result.text, 'html.parser')

    # location_box = str(soup.find("h1", class_="PFnzkD"))

    location = (soup.find("h1", class_="PFnzkD")).string

    temperature = (soup.find("div", class_="_9oCDP5 DsY3vz")).string

    weather_description = (soup.find("div", class_="TMYuez")).string

    weather_description = weather_description.lower()

    icon_dictionary = {

        'mostly cloudy':'<i class="fa-solid fa-cloud fa-3x"></i>',
        'partly cloudy':'<i class="fa-solid fa-cloud fa-3x"></i>',
        'cloudy': '<i class="fa-solid fa-cloud fa-3x"></i>',

        'clear': '<i class="fa-solid fa-sun fa-3x"></i>',
        'mostly clear': '<i class="fa-solid fa-sun fa-3x"></i>',

        'light rain': '<i class="fa-solid fa-cloud-rain fa-3x"></i>',
        'drizzle': '<i class="fa-solid fa-cloud-rain fa-3x"></i>',
        'rainy': '<i class="fa-solid fa-cloud-showers-heavy fa-3x"></i>',

                       }

    if weather_description in icon_dictionary.keys():
        pic = icon_dictionary[weather_description]
    else:
        pic = ''

    output = [location, temperature, weather_description,pic]

    return output


def find_trending():

    my_url = 'https://www.theguardian.com/world'

    result = requests.get(my_url)

    soup = BeautifulSoup(result.text, 'html.parser')

    my_box = soup.find_all("div",class_='most-popular__link',limit=5)

    final_list = []

    for _ in my_box:
        a_tag = _.find("a")
        final_list.append([a_tag.text,a_tag.get("href")])

    return final_list


def most_watched():

    my_url = 'https://kworb.net/youtube/'

    result = requests.get(my_url)

    soup = BeautifulSoup(result.text, 'html.parser')

    my_box = soup.find_all("td", class_='text', limit=5)

    final_list = []

    for _ in my_box:
        a_tag = _.find("a")
        hyperlink = a_tag.get("href")
        if hyperlink.startswith("https://www.youtube.com/watch?v="):
            final_list.append([a_tag.text, hyperlink])
        else:
            hyperlink = hyperlink.replace("video/", "")
            hyperlink = hyperlink.replace(".html", "")
            hyperlink = "https://www.youtube.com/watch?v=" + hyperlink
            final_list.append([a_tag.text, hyperlink])

    return final_list




