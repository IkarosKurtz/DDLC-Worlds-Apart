label do_bg_transition:
  $ renpy.with_statement(rain)

  with None
  return

init -998 python:
  def change_background():
    global current_bg
    
    if (bg := current_place.get_background(persistent.world_time)) != current_bg:
      current_bg = bg
      renpy.scene()
      renpy.show(bg)
      renpy.call_in_new_context('do_bg_transition')