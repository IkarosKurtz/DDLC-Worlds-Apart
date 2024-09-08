init python:
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

  def check_ai():
    global llm_model_online
    global embedding_model_online

    llm_model_online = llm_online()
    embedding_model_online = embedding_online()

label before_main_menu:
  # $ config.main_menu_music = audio.t1
  if override_pre_load:
    return

  if not llm_model_online:
    call screen dialog("The LLM model from ollama is offline, please check it out", [
      Function(check_ai),
      Jump("before_main_menu")
    ])

  if not embedding_model_online:
    call screen dialog("The embedding model from ollama is offline, please check it out",[
      Function(check_ai),
      Jump("before_main_menu")
    ])

  return