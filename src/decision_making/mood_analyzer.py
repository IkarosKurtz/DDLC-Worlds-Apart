from ..openai_helpers.chat_completion import chat_completion
from ..character_data import CharacterDetails
from ..character_logging import CustomLogger

import textwrap

class MoodAnalyzer:
  def __init__(self, character_info: CharacterDetails, log_handler: CustomLogger) -> None:
    self._character_info = character_info
    self._log_handler = log_handler
    
    self.available_moods = {
      'neut': 'neutral',
      'angr': 'angry',
      'anno': 'annoyed',
      'cry': 'crying',
      'curi': 'curious',
      'dist': 'distant',
      'doub': 'doubtful',
      'flus': 'flustered',
      'happ': 'happy',
      'laug': 'laughing',
      'lsur': 'light surprised',
      'nerv': 'nervous',
      'pani': 'panicked',
      'pout': 'pouting',
      'sad': 'sad',
      'sedu': 'seductive',  
      'shoc': 'shocked',
      'vang': 'very angry',
      'vsur': 'very surprised',
      'worr': 'worried'
    }
    
    self.arm_positions = {
      'ldown': 'left arm down',
      'lpoint': 'left arm up',
      'rdown': 'right arm down',
      'rhip': 'right arm on hip',
    }
    
  def determine_pose(self, message: str) -> tuple[str, str]:  
    mood_list = '\n'.join([f'{key}: {value}' for key, value in self.available_moods.items()])
    
    pose_list = '\n'.join([f'{key}: {value}' for key, value in self.arm_positions.items()])
    
    self._log_handler.agent_info('Determining pose...')
    
    user_prompt = textwrap.dedent("""
    My message:
    {}

    Given the message above, what is the correct mood? Use the following list to choose:

    List of moods:
    {}

    Given the message above, what is the correct pose? Use the following list to choose:

    List of poses:
    {}

    Use the left value to select the correct mood (do not modify the value).

    Format:

    FullState: <MOOD> /*/ <POSE>
    """).format(
      message,
      mood_list,
      pose_list
    )
    
    response, _ = chat_completion('You are a helpful assistant', user_prompt)
    chosen_state = response.split(":")[1].strip()
    
    chosen_mood = chosen_state.split("/*/")[0].strip()
    chosen_pose = chosen_state.split("/*/")[1].strip()
    
    self._log_handler.agent_info(f'Determined pose: {chosen_pose}')
    
    return (chosen_mood, chosen_pose)
