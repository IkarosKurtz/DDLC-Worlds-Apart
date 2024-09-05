label do_transition:
  $ renpy.with_statement(fadeIn)

init -1 python:
  active_effect = None
  previous_weather = None
  current_bg = None

  def init_weather():
    global weather_steps
    
    time = day_duration - persistent.world_time[0]
    print(f'Time to weather: {time} = {day_duration} - {persistent.world_time[0]}')

    weather_steps = weather.simulate_weather_with_transitions(time, persistent.current_weather[0])

  def set_weather_music(music, volume=1.0):
    current_music = renpy.music.get_playing('weather_music')
    if current_music == music:
      return

    print(f'Playing {music}')

    renpy.music.play(music, channel='weather_music', loop=True, relative_volume=volume, fadeout=0.3)

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


  def set_weather_effect():
    global current_place
    global active_effect
    global previous_weather

    weather = persistent.current_weather[0]

    is_soft_rain = weather == 'Rainy'
    is_hard_rain = weather == 'Stormy'
    is_raining = is_soft_rain or is_hard_rain

    is_snowing = weather == 'Snowy'

    is_some_weather = is_raining or is_snowing

    if previous_weather != weather and active_effect is not None:
      hide_weather_screen()

      if not is_some_weather:
        renpy.music.stop('weather_music', fadeout=1.0)

      previous_weather = weather

    if not is_some_weather and active_effect is not None:
      renpy.music.stop('weather_music', fadeout=1.0)
      return

    if is_snowing:
      set_weather_screen('snow')
      renpy.music.stop('weather_music', fadeout=1.0)
      return

    if is_raining and not current_place.is_indoor:
      if is_soft_rain:
        set_weather_screen('rain')
        set_weather_music(rain_sound.soft_rain)
      else:
        set_weather_screen('stormy')
        set_weather_music(rain_sound.hard_rain, 0.7)
    elif is_raining and current_place.is_indoor:
      renpy.hide_screen('rain')
      renpy.hide_screen('stormy')
      set_weather_music(rain_sound.soft_indoor_rain, volume=0.5)

      active_effect = 'rain'

  def set_bg_manually():
    global current_place
    global current_bg
    bg = current_place.get_background(persistent.world_time)

    current_bg = bg

    return bg

  def handle_thunder():
    if persistent.current_weather[0] == 'Stormy':
      rand = renpy.random.random()

      # 20% chance of thunder
      if rand < 0.2:
        renpy.sound.play(thunder_sound, channel='thunder_sounds', relative_volume=0.8)
        if not current_place.is_indoor:
          renpy.show('thunder')

  def update_time():
    global weather_steps
    global current_place
    global current_bg

    # if persistent.world_time[1] % 10 == 0:
    #   persistent.current_weather[0] = renpy.random.choice(['Rainy', 'Stormy', 'Snowy'])

    # persistent.current_weather[0] = 'Stormy'
    
    if persistent.world_time[1] + game_seconds >= 70:
      persistent.world_time[1] = 0
      persistent.world_time[0] += 1

      if persistent.world_time[0] + 1 >= 24:
        persistent.world_time[0] = 0

        persistent.current_day += 1

      if len(weather_steps) == 0:
        init_weather()

      new_weather = weather_steps.pop(0)
      print(f'New weather: {new_weather}')

      if new_weather['weather'] != persistent.current_weather[0]:
        persistent.current_weather[0] = new_weather['weather']
        persistent.current_weather[1] = new_weather['data']

      if (bg := current_place.get_background(persistent.world_time)) != current_bg:
        current_bg = bg
        renpy.scene()
        renpy.show(bg)

        renpy.call_in_new_context('do_transition')

      renpy.restart_interaction()

      return

    persistent.world_time[1] += game_seconds

    handle_thunder()

    renpy.restart_interaction()

  def llm_online():
    try:
      __response = chat_completion("You are online??", "You can only say yes or no")
      return True
    except:
      return False

  def embedding_online():
    try:
      __response = get_embedding("You are online??")
      return True
    except:
        return False

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

  def get_characters_locations():
    return nexis.get_characters()

  def update_state(**props):
    RPC.update(**props)