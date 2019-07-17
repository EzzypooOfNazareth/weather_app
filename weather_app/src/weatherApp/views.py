import requests
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import get_template
from database.models import City
from database.forms import CityForm


def home_page(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=8e1196000bc1f959aa972f7744c8f591'

    if request.method == 'POST':
        try:
            form = CityForm(request.POST)
            city = form['name'].value()
            r = requests.get(url.format(city)).json()
            city_weather = {
                'city' : city,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description']
            }
        except:
            raise Http404
    else:
        city = 'Philadelphia'
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description']
        }

    form = CityForm()
    image = city_weather.get('description')
    print(image)
    print(city_weather)
    context = {"city_weather" : city_weather, "form" : form}
    return render(request, "base.html", context)
