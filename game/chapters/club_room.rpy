label test:
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

    renpy.music.play(music, channel='weather_music', loop=True, relative_volume=volume)

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

    if previous_weather != weather:
      hide_weather_screen()

      if not is_some_weather:
        renpy.music.stop('weather_music')

      previous_weather = weather

    if not is_some_weather and active_effect is not None:
      renpy.music.stop('weather_music')
      return

    if is_snowing:
      set_weather_screen('snow')
      renpy.music.stop('weather_music')
      return

    if is_raining and not current_place.is_indoor:
      if is_soft_rain:
        set_weather_screen('rain')
        set_weather_music(soft_rain_sound)
      else:
        set_weather_screen('stormy')
        set_weather_music(hard_rain_sound, 0.7)
    elif is_raining and current_place.is_indoor:
      renpy.hide_screen('rain')
      renpy.hide_screen('stormy')
      set_weather_music(indor_rain_sound, volume=0.5)

      active_effect = 'rain'

  def update_time():
    global weather_steps
    global current_place
    global current_bg

    # if persistent.world_time[1] % 10 == 0:
    #   persistent.current_weather[0] = renpy.random.choice(['Rainy', 'Stormy', 'Snowy'])
    
    if persistent.world_time[1] + game_seconds >= 60:
      persistent.world_time[1] = 0
      persistent.world_time[0] += 1

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
        renpy.call_in_new_context('test')

    if persistent.world_time[0] + 1 >= 24:
      persistent.world_time[0] = 0

      persistent.current_day += 1

    persistent.world_time[1] += game_seconds

    renpy.restart_interaction()

# This label is used to charge the location
label charge_location:
  python:
    global current_place
    update_state(details=f"Location: {persistent.location}")

    # To avoid of getting the same location twice
    if current_place is None or current_place.name != persistent.location:
      current_place = nexis.get_location_by_name(persistent.location)

    if current_place is not None and len(current_place.characters) > 0:
      update_state(state="Dokis: " + ', '.join(current_place.characters))
    else:
      update_state(state="No dokis in this location")

  # Show the background of the current location, it supports day, afternoon and night
  scene expression current_place.get_background(persistent.world_time) with fadeIn

  show screen game_info
  call screen location_info(current_place.characters, current_place.sub_locations_here(), current_place.parent_location)
  
  # When changed the location, we need to charge it again
  jump charge_location 

# This label is used to handle the responses from the selected doki
label callback:
  $ counter = 0
  $ max_counter = len(dialogues)

  $ renpy.show(selected_char + ' om', at_list=[t11])

  while counter < max_counter:
    $ dialogue = dialogues[counter][1]
    $ mood = dialogues[counter][0]

    $ counter += 1

    $ show_character(selected_char, normal_pos, mood)

    $ characters[selected_char](dialogue)

  $ renpy.show(selected_char + ' cm', at_list=[t11])

  jump chat_lobby

# This label is used to wait for an input from the user
label chat_lobby:
  $ normal_pos = 'turned' if selected_char != 'monika' else 'forward'

  $ update_state(state=f"Talking with {selected_char.capitalize()}")

  $ renpy.show(selected_char + f' {normal_pos}', at_list=[t11]) 

  call screen inputma

  if _return == "exit":
    $ renpy.transition(nothing, always=True)
    return 

  $ message = message.strip()

  mc "[message]"

  # $ asyncchat(message, player)
  $ dialogues = None


  $ idx = 0
  $ dots = "."

  while dialogues is None:
    $ characters[selected_char]("[dots] {w=.5}{nw}")
     
    $ dots += "."

    if len(dots) == 9:
      $ dialogues = [('happ', 'LOREM IPSUM DOLOR SIT AMET, CONSECTETUR ADIPISCING ELIT, SED DO EIUSMOD TEMPORTrigge')]
      $ dots = "."

  $ message = ""
  jump callback

