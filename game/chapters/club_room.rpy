init -1 python:
  global weather_steps

  def init_weather():
    global weather_steps
    
    time = day_duration - persistent.world_time[0]
    print(f'Time to weather: {time} = {day_duration} - {persistent.world_time[0]}')

    weather_steps = weather.simulate_weather_with_transitions(time, persistent.current_weather[0])

  def update_time():
    global weather_steps
    
    if persistent.world_time[1] + game_seconds >= 60:
      persistent.world_time[1] = 0
      persistent.world_time[0] += 1

      if len(persistent.weather_steps) == 0:
        init_weather()

      new_weather = weather_steps.pop(0)
      print(f'New weather: {new_weather}')

      if new_weather['weather'] != persistent.current_weather[0]:
        persistent.current_weather[0] = new_weather['weather']
        persistent.current_weather[1] = new_weather['data']

    if persistent.world_time[0] + 1 >= 24:
      persistent.world_time[0] = 0

      persistent.current_day += 1

    persistent.world_time[1] += game_seconds

    renpy.restart_interaction()



label charge_location:
  python:
    print(f'\n{persistent.location}')

    RPC.update(state=f"Location: {persistent.location}")

    if current_place is None or current_place.name != persistent.location:
      print('Next location')
      current_place = nexis.get_location(persistent.location)

  # Show the background of the current location, it supports day, afternoon and night
  scene expression current_place.get_background(persistent.world_time) with fadeIn

  show screen game_info
  call screen location_info(current_place.characters, current_place.sub_locations_here(), current_place.parent_location)
  
  
  jump charge_location 

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

label chat_lobby:
  $ normal_pos = 'turned' if selected_char != 'monika' else 'forward'

  $ RPC.update(state=f"Location: {persistent.location} -- Talking with {selected_char}")

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
      $ dialogues = [('happ', 'sd')]
      $ dots = "."

  $ message = ""
  jump callback

