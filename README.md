# WeatherProjectAI

## Description

A powerful assistant that will help you know the weather conditions in various parts of the world and allows you to consult historical data in Boulder, Colorado (CO) between January 2023 and September 8, 2024.

### Flask App "WeatherBot"

- `main.py`: Main file of the Flask application.
- `requirements.txt`: Necessary dependencies.
- `test`: Folder that contains the tests.
- `static`: Folder that contains CSS, JS, PNG files.
- `templates`: Folder that contains HTML files.

### Docker

- `Dockerfile`: Contains the instructions to create the Docker image for the application.
- `docker-compose.yml`: Configuration of the services the project needs.

### Flowise on Hugging Face

- `WeatherChatH_v5`: The main ChatFlow which calls the different tools that are executed. This queries the [OpenWeatherMap API](https://api.openweathermap.org), the [time API](https://timeapi.io), and the *csv_history_v4* ChatFlow.
- `csv_history_v4`: Contains the CSV generated from the [Visualcrossing API](https://weather.visualcrossing.com).

## CI/CD in GitLab

This project includes a **GitLab CI** configuration to run tests and build the Docker image automatically on each push.

* .gitlab-ci.yml

## Required Commands

```bash
git clone https://gitlab.com/usuario/proyecto.git
docker-compose up --build
