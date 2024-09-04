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
  scene expression set_bg_manually() with fadeIn

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

