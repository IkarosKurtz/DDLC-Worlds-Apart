init -998 python:
  import textwrap

  class MoodAnalyzer:
    """ Analyzes the mood and pose based on given messages. """

    def __init__(self, agent_details: AgentDetails, logger: CustomLogger) -> None:
      """
      Initializes the MoodAnalyzer.

      Parameters
      ----------
      agent_details : AgentDetails
          An instance of AgentDetails containing details about the character.

      logger : CustomLogger
          An instance of CustomLogger for logging information.
      """
      self._agent_details = agent_details
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

      Given the message above, what is the correct combination of mood and pose? Don't explain just fill the format.
      Use the following list to choose (if there is no match, use the closest one, but always use one of the options):

      List of moods:
      {}

      List of poses:
      {}
      
      Example:
      neut: neutral # use neut as value, do the same for the rest of the values 

      Examples of format:
      happ /*/ rhip
      angr /*/ ldown
      dist /*/ rdown

      Fill in:
      <MOOD> /*/ <POSE>
      """).format(
        message,
        self._mood_list,
        self._pose_list
      )
      
      chosen_state, _ = chat_completion(prompt)
      chosen_mood = chosen_state.split("/*/")[0].strip()
      chosen_pose = chosen_state.split("/*/")[1].strip()
      
      self._logger.agent_info(f'Determined pose: {chosen_pose} and mood: {chosen_mood}')
      
      return f'{chosen_mood} {chosen_pose}'