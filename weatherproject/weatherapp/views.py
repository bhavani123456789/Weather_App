from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    # Default city
    default_city = 'indore'
    # Check if city is provided in POST request
    city = request.POST.get('city', default_city)

    # OpenWeatherMap API URL
    weather_api_key = 'c507439a89dea4553e1e833a3d2ce72b'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}'
    PARAMS = {'units': 'metric'}

    # Google Custom Search API setup
    API_KEY = 'AIzaSyBrTa3so4VL9XdehTjpiz1i2LpGimMaUf8'  # Your Google API key
    SEARCH_ENGINE_ID = 'a4a1a9c666a284fb9'  # Your search engine ID

    # Prepare query for image search
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Fetching image data
    try:
        response = requests.get(city_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        search_items = data.get("items")

        # Check if search_items is not None or empty
        if search_items:
            image_url = search_items[0]['link']  # Use the first image link
        else:
            print("No images found for the query.")
            image_url = 'https://via.placeholder.com/1920x1080.png?text=No+Image+Available'  # Default image

    except Exception as e:
        print(f"Error fetching image data: {e}")
        image_url = 'https://via.placeholder.com/1920x1080.png?text=Error+Fetching+Image'  # Default error image

    # Fetching weather data
    try:
        weather_response = requests.get(url, params=PARAMS)
        weather_response.raise_for_status()  # Raise an error for bad responses
        data = weather_response.json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError as e:
        print(f"KeyError: {e}")
        messages.error(request, 'Entered city is not available in the API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': default_city,
            'exception_occurred': True,
            'image_url': image_url
        })
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        messages.error(request, 'Error fetching weather data. Please try again.')
        day = datetime.date.today()
        
        return render(request, 'weatherapp/index.html', {
            'description': 'Error fetching data',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': default_city,
            'exception_occurred': True,
            'image_url': image_url
        })
