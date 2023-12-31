from ..openai_helpers.chat_completion import chat_completion
from ..character_data import CharacterDetails
from ..custom_logger import CustomLogger

import textwrap


class MoodAnalyzer:
  """ Analyzes the mood and pose based on given messages. """

  def __init__(self, character_data: CharacterDetails, logger: CustomLogger) -> None:
    """
    Initializes the MoodAnalyzer.

    Parameters
    ----------
    character_data : CharacterDetails
        An instance of CharacterDetails containing details about the character.

    logger : CustomLogger
        An instance of CustomLogger for logging information.
    """
    self._character_data = character_data
    self._logger = logger

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
      'rhip': 'right arm on hip'
    }

    self._mood_list = '\n'.join([f'{key}: {value}' for key, value in self.available_moods.items()])
    self._pose_list = '\n'.join([f'{key}: {value}' for key, value in self.arm_positions.items()])

  def determine_pose(self, message: str) -> str:
    """
    Determines the pose of the character based on the given message.

    Parameters
    ----------
    message : str
        The message based on which the pose is to be determined.

    Returns
    -------
    str
        The determined pose of the character.
    """
    self._logger.agent_info('Determining pose...')

    prompt = textwrap.dedent("""
    My message:
    {}

    Given the message above, what is the correct mood? Use the following list to choose:

    List of moods:
    {}

    Given the message above, what is the correct pose? Use the following list to choose:

    List of poses:
    {}
    
    Example:
    neut: neutral # use neut as value, do the same for the rest of the values 

    Format:

    FullState: <MOOD> /*/ <POSE>
    """).format(
      message,
      self._mood_list,
      self._pose_list
    )

    response, _ = chat_completion(prompt)
    chosen_state = response.split(":")[1].strip()

    chosen_mood = chosen_state.split("/*/")[0].strip()
    chosen_pose = chosen_state.split("/*/")[1].strip()

    chosen_mood = chosen_mood if self.available_moods.get(chosen_mood) else 'neut'
    chosen_pose = chosen_pose if self.arm_positions.get(chosen_pose) else 'ldown'

    self._logger.agent_info(f'Determined pose: {chosen_pose}')

    return f'{chosen_mood} {chosen_pose}'
