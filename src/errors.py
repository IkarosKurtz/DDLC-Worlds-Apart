class InvalidVersion(Exception):
  def __init__(self, version) -> None:
    self.message = f"{version} is not a valid version. Valid versions are: ['4k', '16k']"
    super().__init__(self.message)
