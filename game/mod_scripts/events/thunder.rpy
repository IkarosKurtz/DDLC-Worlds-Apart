init -999 python:
  def handle_thunder():
    global current_place

    if persistent.current_weather[0] == 'Stormy':
      rand = renpy.random.random()

      # 12.5% chance of a thunder
      if rand < thunder_chance:
        renpy.sound.play(thunder_sound, channel='thunder_sounds', relative_volume=0.8)
        if not current_place.is_indoor:
          renpy.show('thunder')