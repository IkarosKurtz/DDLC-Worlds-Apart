init -997 python:
  
  class WorldWeather:
    def __init__(self) -> None:
      self.weather = {
          'Sunny': {'temperature': (25, 35), 'humidity': (10, 30), 'wind': (0, 10), 'clouds': (0, 20)},
          'Cloudy': {'temperature': (15, 25), 'humidity': (40, 60), 'wind': (5, 15), 'clouds': (60, 100)},
          'Rainy': {'temperature': (10, 20), 'humidity': (70, 90), 'wind': (10, 20), 'clouds': (80, 100)},
          'Stormy': {'temperature': (8, 18), 'humidity': (80, 100), 'wind': (20, 40), 'clouds': (90, 100)},
          'Snowy': {'temperature': (-5, 5), 'humidity': (60, 80), 'wind': (5, 15), 'clouds': (70, 100)}
      }

      self.posible_transitions = {
        'Sunny': ['Cloudy', 'Rainy'],
        'Cloudy': ['Sunny', 'Rainy', 'Stormy', 'Snowy'],
        'Rainy': ['Cloudy', 'Stormy'],
        'Stormy': ['Rainy', 'Cloudy'],
        'Snowy': ['Cloudy']
      }

    def _interpolate(self, initial_value: float, final_value: float, step: int, max_steps: int) -> float:
      return initial_value + (final_value - initial_value) * (step / max_steps)

    def _generate_weather(self, weather) -> None:
      conditions = self.weather[weather]
      temperature = random.uniform(*conditions['temperature'])
      humidity = random.uniform(*conditions['humidity'])
      wind = random.uniform(*conditions['wind'])
      clouds = random.uniform(*conditions['clouds'])
      return {'weather': weather, 'temperature': temperature, 'humidity': humidity, 'wind': wind, 'clouds': clouds}

    def _transition_weather(self, initial_conditions, final_conditions, duration_hours):
      hours = []
      for hour in range(duration_hours):
        temperature = self._interpolate(
            initial_conditions['temperature'], final_conditions['temperature'], hour, duration_hours)
        humidity = self._interpolate(
            initial_conditions['humidity'], final_conditions['humidity'], hour, duration_hours)
        wind = self._interpolate(
            initial_conditions['wind'], final_conditions['wind'], hour, duration_hours)
        clouds = self._interpolate(
            initial_conditions['clouds'], final_conditions['clouds'], hour, duration_hours)
        print(
            f"Hour {hour}: Weather: {final_conditions['weather']}, Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%, Wind: {wind:.2f} km/h, Clouds: {clouds:.2f}%")

        hours.append({
            'weather': final_conditions['weather'],
            'data': {
              'temperature': temperature,
              'humidity': humidity,
              'wind': wind,
              'clouds': clouds
            }
        })

      return hours

    def simulate_weather_with_transitions(self, total_duration_hours: int, last_weather: str = 'Sunny'):
      current_conditions = self._generate_weather(last_weather)
      remaining_hours = total_duration_hours
      current_weather = last_weather

      steps = []

      while remaining_hours > 0:
        # Define the duration of the next transition
        transition_duration = renpy.random.randint(weather_period_transition[0], weather_period_transition[1])

        if (remaining_hours - transition_duration) < 0:
          transition_duration = remaining_hours

        # Choose the next weather based in the actual weather
        new_weather = renpy.random.choice(self.posible_transitions[current_weather])
        print(f"Weather transition: {current_weather} -> {new_weather}")
        final_conditions = self._generate_weather(new_weather)

        # Perform the transition
        transition_gen = self._transition_weather(current_conditions, final_conditions, transition_duration)

        steps.extend(transition_gen)

        # Update for the next transition
        current_conditions = final_conditions
        remaining_hours -= transition_duration
        current_weather = new_weather

      return steps