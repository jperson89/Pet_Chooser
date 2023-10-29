# This is our class for Pet. Not only do we need to keep it in a separate file per the instructions, it won't
# work unless we do.

# This works like it did before when we made the bike class, but let's make it a little easier on ourselves by
# making sure everything is either a string or integer where needed.
class Pet:
    def __init__(self, petName, ownerName, petAge, petType):
        self.petName = str(petName)
        self.ownerName = str(ownerName)
        self.petAge = int(petAge)
        self.petType = str(petType)
