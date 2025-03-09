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
        
        self.setStyleSheet("""
                           Qlabel, QpushButton{
                               font-size: 20px;
                               font-family: Arial;
                               font-style: bold;
                           }
                           #city_label{
                               margin-top: 20px;
                           }
                           #city_input{
                               margin-top: 10px;
                           }
                           #get_weather_btn{
                               margin-top: 20px;
                           }
                           #temp_label{
                               margin-top: 20px;
                           }
                           #emoji_label{
                               font-family: Segoe UI Emoji;
                               margin-top: 10px;
                           }
                           #description_label{
                               margin-top: 10px;
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
    
    def display_weather(self, data):
        print(data)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())