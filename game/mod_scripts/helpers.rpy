init -997 python:
  import threading
  
  def set_weather_music(music, volume=1.0, channel='weather_music'):
    current_music = renpy.music.get_playing(channel)
    if current_music == music:
      return

    print(f'Playing {music}')

    renpy.music.play(music, channel=channel, loop=True, relative_volume=volume, fadein=0.5)

  def set_weather_screen(screen):
    global active_effect
    current_screen = renpy.get_screen(screen)

    if current_screen is not None:
      return
    
    print(f'Showing {screen}')

    renpy.show_screen(screen)
    active_effect = screen

  def hide_weather_screen():
    global active_effect

    print(f'Hiding {active_effect}')

    if active_effect is None:
      print('ALERT: active_effect is None')
      return

    renpy.hide_screen(active_effect)
    active_effect = None

  def set_bg_manually():
    global current_place
    global current_bg
    bg = current_place.get_background(persistent.world_time)

    current_bg = bg

    return bg

  def set_music_manually():
    global previous_weather
    weather = persistent.current_weather[0]
    current_music = renpy.music.get_playing('music')

    if previous_weather == weather:
      return

    print(f'Music: {current_music}')
    if weather == 'Stormy' or weather == 'Rainy':
      set_weather_music(music.rain_ambient, channel='music')
    elif weather == 'Snowy':
      set_weather_music(music.snow_ambient, channel='music')
    else:
      set_weather_music(music.normal_ambient, channel='music', volume=1.3)
    

  def get_time(string: bool = True):
    if string:
      return f"{persistent.world_time[0]:02}: {persistent.world_time[1]:02}"

    return persistent.world_time

  def get_two_decimals(value):
    return f"{value:.2f}"

  def get_dokis_head(location):
    if location not in characters_in_location:
      return []

    return [character_heads[c.lower()] for c in characters_in_location[location]]

  def update_state(**props):
    RPC.update(**props)

  def get_date(full=False):
    day, month, year = persistent.current_date

    months = [
      ('January', 31),
      ('February', 28),
      ('March', 31),
      ('April', 30),
      ('May', 31),
      ('June', 30),
      ('July', 31),
      ('August', 31),
      ('September', 30),
      ('October', 31),
      ('November', 30),
      ('December', 31)
    ]

    month_name, days_in_month = months[month]

    if month_name == 'February':
      if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month += 1
      

    if day > days_in_month:
      day = 1
      month += 1
      month_name = months[month][0]

    if month > 12:
      month = 1
      year += 1

    return f"{month_name}/{day}/{year}" if full else f"{month + 1}/{day}/{str(year)[-2:]}"