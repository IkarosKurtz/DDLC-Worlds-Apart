init -998 python:
  def init_weather():
    global weather_steps
    
    time = day_duration - persistent.world_time[0]
    print(f'Time to weather: {time} = {day_duration} - {persistent.world_time[0]}')

    weather_steps = world_weather.simulate_weather_with_transitions(time, persistent.current_weather[0])

  def set_weather():
    global weather_steps
    global previous_weather

    if len(weather_steps) == 0:
        init_weather()

    new_weather = weather_steps.pop(0)
    print(f'New weather: {new_weather["weather"]}')

    if new_weather['weather'] != persistent.current_weather[0]:
      previous_weather = persistent.current_weather[0]
      persistent.current_weather[0] = new_weather['weather']
      persistent.current_weather[1] = new_weather['data']


  def set_weather_effect():
    global current_place
    global active_effect
    global previous_weather

    weather = persistent.current_weather[0]

    is_soft_rain = weather == 'Rainy'
    is_hard_rain = weather == 'Stormy'
    is_raining = is_soft_rain or is_hard_rain

    is_snowing = weather == 'Snowy'

    set_music_manually()

    is_some_weather = is_raining or is_snowing

    if previous_weather != weather and active_effect is not None:
      hide_weather_screen()

      if not is_some_weather:
        renpy.music.stop('weather_music')

      previous_weather = weather

    if not is_some_weather and active_effect is not None:
      renpy.music.stop('weather_music')
      return

    if is_snowing and not current_place.is_indoor:
      set_weather_screen('snow')
      renpy.music.stop('weather_music')
      return
    elif is_snowing and current_place.is_indoor:
      renpy.hide_screen('snow')
      renpy.music.stop('weather_music')

    if is_raining and not current_place.is_indoor:
      if is_soft_rain:
        set_weather_screen('rain')
        set_weather_music(rain_sound.soft_rain)
      else:
        set_weather_screen('stormy')
        set_weather_music(rain_sound.hard_rain, 0.7)
    elif is_raining and current_place.is_indoor:
      if is_soft_rain:
        renpy.hide_screen('rain')
        set_weather_music(rain_sound.soft_indoor_rain, 1.2)
      else:
        renpy.hide_screen('stormy')
        set_weather_music(rain_sound.hard_indoor_rain, 0.65)

      active_effect = 'rain'
