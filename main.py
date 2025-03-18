import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt 

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_btn = QPushButton("Get Weather", self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox= QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_btn)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_btn.setObjectName("get_weather_btn")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        # self.setStyleSheet("""
        #                    Qlabel, QpushButton{
        #                        font-size: 20px;
        #                        font-family: Arial;
        #                        font-style: bold;
        #                    }
        #                    #city_label{
        #                        margin-top: 20px;
        #                    }
        #                    #city_input{
        #                        margin-top: 10px;
        #                    }
        #                    #get_weather_btn{
        #                        margin-top: 20px;
        #                    }
        #                    #temp_label{
        #                        margin-top: 20px;
        #                    }
        #                    #emoji_label{
        #                        font-family: Segoe UI Emoji;
        #                        margin-top: 10px;
        #                    }
        #                    #description_label{
        #                        margin-top: 10px;
        #                    }    
        #                    """)
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                    stop:0 #6dd5ed, stop:1 #2193b0);
    }
    
    QLabel, QPushButton {
        font-size: 20px;
        font-family: Arial;
        font-weight: bold;
        color: white;
    }

    QLineEdit {
        background-color: rgba(255, 255, 255, 0.2);
        border: 2px solid white;
        border-radius: 10px;
        padding: 8px;
        font-size: 18px;
        color: white;
    }

    QPushButton {
        background-color: #ff7e5f;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
    }
    
    QPushButton:hover {
        background-color: #feb47b;
    }

    #city_label {
        margin-top: 20px;
        font-size: 22px;
    }

    #city_input {
        margin-top: 10px;
    }

    #get_weather_btn {
        margin-top: 20px;
        background-color: #ff7e5f;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        color: white;
    }

    #get_weather_btn:hover {
        background-color: #feb47b;
    }

    #temp_label {
        margin-top: 20px;
        font-size: 24px;
    }

    #emoji_label {
        font-family: "Segoe UI Emoji";
        font-size: 40px;
        margin-top: 10px;
    }

    #description_label {
        margin-top: 10px;
        font-size: 18px;
    }
""")

        self.get_weather_btn.clicked.connect(self.get_weather)
    
    def get_weather(self):
        print("Getting weather")
        api_key = "964a03a2fa75534c7b49cc800318d3d9"    
        city = self.city_input.text()
        url= f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            # print(data)
            # if data["cod"] == "404": 
            self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_error:
                # print(response.status_code)
                match response.status_code:
                    case 400:
                        self.display_error("Bad request:\n Please check your input")
                    case 401:
                        self.display_error("Unauthorized:\n API key is invalid")    
                    case 403:
                        self.display_error("Forbidden:\n Access is denied")
                    case 404:
                        self.display_error("City not found:\n Please enter a valid city name")
                    case 500:
                        self.display_error("Internal server error:\n Please try again later")
                    case 502:
                        self.display_error("Bad gateway:\n Invalid response from the server")
                    case 503:
                        self.display_error("Service unavailable:\n SERVER IS DOWN")
                    case 504:
                        self.display_error("Gateway timeout:\n No response from the server")
                    case _:
                        self.display_error(f"HTTP error occurred:\n {http_error}")
        
        
        except requests.exceptions.ConnectionError:
            print("Connection error occurred\n Please check your internet connection")
        except requests.exceptions.Timeout:
            print("Request timed out\n Please try again later")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects\n Please try again later")
        except requests.exceptions.RequestException as req_error:
            print(f"Request error occurred\n {req_error}")
    def display_error(self, message):
        self.temp_label.setStyleSheet("font-size: 30px; color: red;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        temp = data["main"]["temp"]
        self.temp_label.setText(f"{temp}°C")
        # self.emoji_label.setText(self.get_emoji(temp))
        # print(data)
        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)
        weather_id = data["weather"][0]["id"] 
        self.emoji_label.setText(self.get_emoji(weather_id))
    @staticmethod    
    def get_emoji(weather_id):
        
        if weather_id >= 200 and weather_id <= 232:
            return "☔"
        elif weather_id >= 300 and weather_id <= 321:
            return "🌧"
        elif weather_id >= 500 and weather_id <= 531:
            return "🌧"
        elif weather_id >= 600 and weather_id <= 622:
            return "🌨"
        elif weather_id >= 701 and weather_id <= 781:
            return "🌫"
        elif weather_id == 800:
            return "☀"
        elif weather_id >= 801 and weather_id <= 804:
            return "🌤"
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())