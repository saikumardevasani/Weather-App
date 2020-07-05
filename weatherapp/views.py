import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=enteryourkey'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Enter valid city !'   
            else:
                err_msg = 'City already exits in the database !'

        if err_msg:
            message = err_msg
            message_class = 'alert alert-danger'
        else:
            message = 'City added successfully !'
            message_class = 'alert alert-success'    


    form = CityForm()


    cities = City.objects.all()

    Weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
    

        city_weather = {
            'city' : city.name,
            'country' : r['sys']['country'],
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],        
        }

        Weather_data.append(city_weather)  

    context = {
        'Weather_data' : Weather_data,
        'form': form,
        'message' : message,
        'message_class' : message_class
        }

    return render(request, 'index.html',context)

def delete_city(request, city_name):

    City.objects.get(name=city_name).delete()
    
    return redirect('index')
