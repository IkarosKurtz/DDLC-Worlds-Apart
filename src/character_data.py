class CharacterDetails:
  """ Represents the details of a character including name, bio, traits, abilities, and position. """

  def __init__(self, name: str, bio: str, traits: str, abilities: str, position: str) -> None:
    """
    Initializes the CharacterDetails.

    Parameters
    ----------
    name : str
        The name of the character.

    bio : str
        The biography of the character.

    traits : str
        The traits of the character.

    abilities : str
        The abilities of the character, separated by semicolons.

    position : str
        The current position of the character.
    """
    self._name = name
    self._bio = bio
    self._status = None
    self._position = position
    self._traits = traits
    abilities = [ability.strip() for ability in abilities.split(';')]
    self._abilities = '\n'.join([f'{ability}' for ability in abilities])

  @property
  def name(self) -> str:
    return self._name

  @property
  def bio(self) -> str:
    return self._bio

  @bio.setter
  def bio(self, new_bio: str) -> None:
    self._bio = new_bio

  @property
  def status(self) -> str:
    return self._status

  @status.setter
  def status(self, new_status: str) -> None:
    self._status = new_status

  @property
  def position(self) -> str:
    return self._position

  @position.setter
  def position(self, new_position: str) -> None:
    self._position = new_position

  @property
  def traits(self) -> str:
    return self._traits

  @property
  def abilities(self) -> str:
    return self._abilities
