init -999 python:
  from typing import Optional
  
  class LocationBackground:
    def __init__(self, day: str, afternoon: str = None, night: str = None):
      self.day: str = day
      self.afternoon: str = afternoon if afternoon is not None else day
      self.night: str = night if night is not None else day

    def get_backgrounds(self) -> str:
      return (self.day, self.afternoon, self.night)

    def get_background(self, time: tuple[int, int]) -> str:
      hour, minute = time

      if 7 <= hour < 17:
        return self.day
      elif 17 <= hour < 19:
        return self.afternoon
      else:
        return self.night


  class BasicLocation(LocationBackground):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(background_day, background_afternoon, background_night)

      self.name = name
      self.characters: list[str] = []
      self.sub_locations: list['BasicLocation'] = []
      self.parent_location: Optional['BasicLocation'] = None

    def add_character(self, character: str) -> None:
      self.characters.append(character)

    def remove_character(self, character: str) -> None:
      self.characters.remove(character)

    def add_sub_location(self, sub_location: 'BasicLocation') -> None:
      self.sub_locations.append(sub_location)

      sub_location.parent_location = self

    def add_sub_locations(self, sub_locations: list['BasicLocation']) -> None:
      self.sub_locations.extend(sub_locations)

      for sub_location in sub_locations:
        sub_location.parent_location = self

    def sub_locations_here(self) -> str:
      return [
        sb.name for sb in self.sub_locations
      ]

    def who_is_here(self) -> str:
      return ', '.join(self.characters)

    def __str__(self) -> str:
      sub_locations = '\n\t'.join(str(sl) for sl in self.sub_locations)
      return f"Location: {self.name}\nSub Locations: {sub_locations}\n"

    def __repr__(self) -> str:
      return self.name

    def __iter__(self):
      self._location_idx = 0
      return self

    def __next__(self):
      if len(self.sub_locations) == 0:
        raise StopIteration

      if self._location_idx >= len(self.sub_locations):
        raise StopIteration

      location = self.sub_locations[self._location_idx]
      self._location_idx += 1

      return location

  class Room(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)


  class Building(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)


  class GenericConnection(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)


  class Town(BasicLocation):
    def __init__(self, name: str):
      super().__init__(name, ' ')

    def _rec(self, loc: BasicLocation, character: str):
      if character in loc.characters:
        return f"{character} is in {loc.name}"

      a = None

      for sub_location in loc.sub_locations:
        a = self._rec(sub_location, character)

        if a is not None:
          return a

    def __str__(self) -> str:
      sub_locations = '\t\t'.join(str(sl) for sl in self.sub_locations)
      return f"Location: {self.name}\n\tSub Locations: {sub_locations}"

    def __repr__(self) -> str:
      return super().__str__()

    def get_location(self, location_name: str, location: BasicLocation = None) -> BasicLocation:
      if location is None:
        location = self

      if location.name == location_name:
        return location

      a = None

      for sub_location in location.sub_locations:
        a = self.get_location(location_name, sub_location)

        if a is not None:
          return a

    def get_characters(self, location: BasicLocation = None) -> list[str]:
      characters = {}

      if location is None:
        location = self

      if len(location.characters) > 0:
        characters[location.name] = location.characters

      for sub_location in location.sub_locations:
        characters.update(self.get_characters(sub_location))

      return characters

    def where_is(self, character: str) -> str:
      return self._rec(self, character)

  
  class WorldParser:
    def __init__(self) -> None:
      self._path = os.path.join(renpy.config.gamedir, "schema.json")

      self._types = {
        "T": Town,
        "B": Building,
        "R": Room,
        "GC": GenericConnection
      }
    def _get_class(self, type: str):
      if type in self._types:
        return self._types[type]

      raise ValueError(f"Unknown type: {type}")

    def get_locations(self, location: BasicLocation) -> list[BasicLocation]:
      locations = []

      for sbl in location:
        if len(sbl.sub_locations) > 0:
          locations.extend(self.get_locations(sbl))

        locations.append(sbl)

      return locations

    def unpack(self) -> Town:
      with open(self._path, 'r', encoding='utf-8') as f:
        data: dict[str, dict] = json.load(f)

      def wrapper(data: dict[str, dict]):
        locations = []
        for key, value in data.items():
          if any(key.startswith(t) for t in self._types):

            if day := value.get('day', None) is None:
              raise ValueError(f"Missing day background for {key}")

            day = value['day']
            afternoon = value.get('afternoon', day)
            night = value.get('night', day)

            type, name = key.split('-')
            location = self._get_class(type)(name, day, afternoon, night)

            more = wrapper(value)

            if more is not None:
              location.add_sub_locations(more)

              locations.append(location)

          continue

        return locations

      town = None
      for key, value in data.items():
        if key.startswith("T"):
          town = Town(key.split('-')[1])

        town.add_sub_locations(wrapper(value))
        return town

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

    def transition_weather(self, initial_conditions, final_conditions, duration_hours):
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
        transition_duration = renpy.random.randint(2, 6)

        if (remaining_hours - transition_duration) < 0:
          transition_duration = remaining_hours

        # Choose the next weather based in the actual weather
        new_weather = renpy.random.choice(self.posible_transitions[current_weather])
        print(f"Weather transition: {current_weather} -> {new_weather}")
        final_conditions = self._generate_weather(new_weather)

        # Perform the transition
        transition_gen = self.transition_weather(current_conditions, final_conditions, transition_duration)

        steps.extend(transition_gen)

        # Update for the next transition
        current_conditions = final_conditions
        remaining_hours -= transition_duration
        current_weather = new_weather

      return steps