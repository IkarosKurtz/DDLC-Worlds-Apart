init -999 python:
  from typing import Optional
  from enum import Enum

  class LocationType(Enum):
    Room = 'R'
    Corridor = 'C'
    Building = 'B'
    Street = 'S'
    World = 'W'

    @classmethod
    def list(cls) -> list[str]:
      return [e.value for e in cls if e != LocationType.World]

  
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
      self.is_indoor: bool = False
      self.type: Optional[LocationType] = None
      self._referencial_link: Optional[str] = None

      self.referenced_locations: list['BasicLocation'] = []
      self.sub_locations: list['BasicLocation'] = []

    def add_character(self, character: str) -> None:
      self.characters.append(character)

    def remove_character(self, character: str) -> None:
      self.characters.remove(character)

    def add_sub_location(self, sub_location: 'BasicLocation') -> None:
      self.sub_locations.append(sub_location)

      sub_location.parent_location = self

    def add_referenced_sub_location(self, sub_location: 'BasicLocation') -> None:
      self.referenced_locations.append(sub_location)

    def add_sub_locations(self, sub_locations: list['BasicLocation']) -> None:
      self.sub_locations.extend(sub_locations)

      for sub_location in sub_locations:
        sub_location.parent_location = self

    def sub_locations_here(self) -> str:
      return [
        sb.name for sb in self.referenced_locations + self.sub_locations
      ]

    def who_is_here(self) -> str:
      return ', '.join(self.characters)

    def all_sub_locations(self) -> list['BasicLocation']:
      return self.referenced_locations + self.sub_locations

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
      self.is_indoor = True
      self.type = LocationType.Room


  class Building(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)
      self.type = LocationType.Building


  class Street(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)
      self.type = LocationType.Street


  class Corridor(BasicLocation):
    def __init__(self,
                name: str,
                background_day: str,
                background_afternoon: str = None,
                background_night: str = None):
      super().__init__(name, background_day, background_afternoon, background_night)
      self.is_indoor = True
      self.type = LocationType.Corridor

  class World(BasicLocation):
    def __init__(self, name: str):
      super().__init__(name, ' ')
      self.type = LocationType.World
      self.loc_categories = {}
      self.all_locations: list[BasicLocation] = []

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

    def get_location(self, location_name: str, location_type: str, location: BasicLocation | None = None) -> BasicLocation | None:
      search_list = self.loc_categories.get(location_type, [])

      if len(search_list) == 0:
        return None

      for location in search_list:
        if location.name == location_name:
          return location

    def get_location_by_name(self, location_name: str) -> BasicLocation | None:
      for location in self.all_locations:
        if location.name == location_name:
          return location

    def get_characters(self, location: BasicLocation | None = None) -> list[str]:
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
      self._types = {
        "B": Building,
        "R": Room,
        "S": Street,
        "C": Corridor,
      }

    def _get_class(self, type: str):
      return self._types[type]

    def unpack(self) -> World:
      path = os.path.join(renpy.config.gamedir, "Nexis.json")

      with open(path, 'r', encoding='utf-8') as f:
        json_name = f.name
        data: dict[str, dict] = json.load(f)

      world_name = json_name.split('.')[0]
      world_name = ' '.join([w.capitalize() for w in world_name.split('_')])

      world = World(world_name)

      for i in LocationType.list():
        world.loc_categories[i] = []

      def wrapper(data: dict[str, dict]):
        locations = []

        for key, value in data.items():
          if key.count('-') != 1:
            continue

          location_type, location_name = key.split('-')

          if location_type not in LocationType.list():
            raise ValueError(f"Unknown location type: {location_type}")

          day_bg = value.get('day', None)

          if day_bg is None:
            raise ValueError(f"Missing day background for {key}")

          afternoon_bg = value.get('afternoon', day_bg)

          night_bg = value.get('night', day_bg)

          location_cls = self._get_class(location_type)

          location: BasicLocation = location_cls(location_name, day_bg, afternoon_bg, night_bg)

          world.loc_categories[location.type.value].append(location)

          if (referencial_links := value.get('to', None)) is not None:
            location._referencial_link = referencial_links

          sub_locations = wrapper(value)

          if sub_locations is None:
            continue

          location.add_sub_locations(sub_locations)
          world.all_locations.append(location)
          locations.append(location)

        return locations

      world.add_sub_locations(wrapper(data))

      def link_references(location: BasicLocation):
        if location._referencial_link is not None:
          for referencial_link in location._referencial_link:
            if referencial_link.count('-') != 1:
              raise ValueError(f"Invalid referencial link: {referencial_link}")

            location_type, location_name = referencial_link.split('-')

            if location_type not in LocationType.list():
              raise ValueError(f"Unknown location type: {location_type}")

            referenced_location = world.get_location(location_name, location_type)

            if referenced_location is None:
              raise ValueError(f"Referenced location not found: {referencial_link}")

            location.add_referenced_sub_location(referenced_location)

        for sub_location in location.sub_locations:
          link_references(sub_location)

      link_references(world)

      world.all_locations = world.all_locations[::-1]

      return world
