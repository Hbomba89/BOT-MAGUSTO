from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from pip._vendor import requests
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

def index(request):

    error = ''
    if request.method == "POST":
        form = CityForm(request.POST)
        City.objects.all().delete()
        if form.is_valid():
            form.save()
            return redirect('home')

    form = CityForm()

    city = City.objects.all()
    for el in city:

        city = str(el).title()

        url_geo = "https://geocode.search.hereapi.com/v1/geocode"
        api_key = 'vqqbNX_YP6VlEPX3kbhcKT41v_lNt1v5NWhN12hp3UU'
        PARAMS = {'apikey': api_key, 'q': city}
        r = requests.get(url=url_geo, params=PARAMS)
        data = r.json()
        if data == {'items': []}:
            latitude = 51.50643
            longitude = -0.12719
            city = 'London'
            error = 'Nie znam takiego miasta'
        else:
            latitude = data['items'][0]['position']['lat']
            longitude = data['items'][0]['position']['lng']

        appid = '6ea601f81b4da9c3799fb4f096c33b9f'
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(latitude) + '&lon=' + str(
            longitude) + '&exclude=minutely, alerts, current&units=metric&lang=pl&appid=' + appid
        res = requests.get(url.format()).json()

        all_info = []

        for i in range(0, 8):
            unix_time = res["daily"][i]["dt"]
            norm_time = time.strftime("%a, %d %b %Y %H:%M", time.localtime(unix_time))
            temp = str(res["daily"][i]["temp"]["day"])
            temp_nig = str(res["daily"][i]["temp"]["night"])
            description = str(res["daily"][i]["weather"][0]["description"])
            icon = str(res["daily"][i]["weather"][0]["icon"])

            all_info.append([city, norm_time, temp, temp_nig, description, icon])

            context = {
                'all_info': all_info,
                'form': form,
                'error': error,
                }

    return render(request, 'main/index.html', context)

def about(request):


    return render(request, 'main/about.html')
