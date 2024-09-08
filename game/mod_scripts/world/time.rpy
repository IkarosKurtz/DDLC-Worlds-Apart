init -999 python:
  def update_time():
    global weather_steps
    global current_place
    global current_bg

    # persistent.current_weather[0] = 'Stormy'
    
    if persistent.world_time[1] + game_seconds >= 60:
      persistent.world_time[1] = 0
      persistent.world_time[0] += 1

      if persistent.world_time[0] + 1 >= 24:
        persistent.world_time[0] = 0

        persistent.current_date[0] += 1

      event_emitter.emit('weather')
      event_emitter.emit('bg')

      return

    persistent.world_time[1] += game_seconds

    event_emitter.emit('thunder')