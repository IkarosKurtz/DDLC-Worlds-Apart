class CharacterDetails:
  def __init__(self, name: str, bio: str, traits: str, habilites: str, status: str, position: str) -> None:
    self._name = name
    self._bio = bio
    self._status = status
    self._position = position
    self._traits = traits
    self._habilites = habilites
      
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
  def activity(self, new_status: str) -> None:
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
  def habilites(self) -> str:
    return self._habilites