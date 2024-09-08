init -999 python:
  def show_character(char, outfit, mood):
    renpy.show("{0} {1} {2}".format(char, outfit, mood), at_list=[t11])
    return
  
  def chat(message):
    return monika_agent.chat('Ikaros', message)

  dialogues = None

  def asyncchat(message, player):
    def run():
      global dialogues
      dialogues = monika_agent.chat(player, message)

    thread = threading.Thread(target=run, name="Monika Chat")
    thread.start()
