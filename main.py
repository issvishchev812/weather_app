from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = '1ec1bdec54c33d103df3d41e43b237e1'
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(API_URL, params)
        if response.status_code != 200:
            err_msg = f"Произошла ошибка при загрузке данных ({response.status_code}). Попробуйте снова."
            if 'cod' in response.json():
                err_msg += f"\nСообщение API: {response.json()['message']}"
            raise Exception(err_msg)
        data = response.json()
        temperature = data['main']['temp']
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        weather = {
            'city': city,
            'temp': f'{temperature}°C',
            'desc': description,
            'hum': f'Влажность воздуха: {humidity}%',
            'wind': f'Скорость ветра: {wind_speed} м/с'
        }

        return render_template('index.html', weather=weather)

    except Exception as e:
        return render_template('index.html', error=e)


if __name__ == "__main__":
    app.run(debug=True)

