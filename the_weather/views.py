from django.shortcuts import render
import requests
from .forms import CityForm
from the_weather.models import City

# Create your views here.


def index(request):

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=090ffecfae05341a427634840e247205'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    weather_data = []

    cities = City.objects.all()
    for city in cities:
        response = requests.get(url.format(city)).json()


        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure'],
            'wind': response['wind']['speed']
        }

        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form
    }
    return render(request, 'the_weather/index.html', context)
