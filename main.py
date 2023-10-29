# Jon Person
# Pet_Chooser

# Let's import a Python package that reads SQL from MySQL. The package pymsql seems to be the most popular.
import pymysql

# This will hide our password. Nobody likes a shoulder surfer.
import pyautogui

# If you don't already have either of these packages installed, you will need to install them.
# Use the function 'pip install <package_name>' to install them.
# Alternatively, type 'import <package name>' in PyCharm. If it isn't already installed, a red lightbulb will appear,
# and PyCharm will recognize that it is not already installed. Click the lightbulb and it will prompt you to install it.

# Ken suggested making Pets its own class during, well, class. It makes perfect sense to work with our SQL data.
# I tried making 'Pets' a class, but it absolutely wouldn't work unless I made it its own sheet. Import it separately.
from Class_Pets import Pet

# This is an SQL Command that will pull our desired data from the SQL database, and also join the appropriate lists
# This took a little trial and error separately in MySQL, but this code works.
# Don't forget to go into MySQL and add the appropriate databases
petdbConnector = """
    select 
        pets.id,
        pets.name as petName,
        pets.age,
        owners.name as ownerName, 
        types.animal_type as petType
    from pets 
        join owners on pets.owner_id = owners.id 
        join types on pets.animal_type_id = types.id;
    """

# I had a LOT of trouble with the quit function last time. Instead of a list, I should have used a tuple.
# These are our entry options to exit the program.
quitOptions = {"q", "quit"}

# It also helps to define a quit function that executes just like you want it to instead of trying to make it do it all
# at once like I did with Number Guessing Game v1
# This is the quit function
def quitPets():
    print("Thank you for using the Pet Chooser! Come back soon!")
    exit()

# This is the input function
def petInput():
    try:
        input("Press [ENTER] to continue.")
    # Error messages in case the user tries something odd with the pet Input message
    except EOFError:
        print("Whatever you're doing, I don't like it. If you come back, be on your best behavior.")
        quitPets()
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting for safety.")
        quitPets()

# This asks for your MySQL credentials to start the program.
try:
    # This asks for your MySQL password in a separate window, creates a connection to mySQL, and
    # hides your password from prying eyes using 'pyautogui'. In addition, you can still use any of the quit commands
    # from quitOptions. Incorrect passwords or invalid entries will exit. I'm kinda proud of this one :).
    password = pyautogui.password(text='Please enter your MySQL password or type q to quit. Invalid entries will exit.',
                                  title='MySQL Password',
                                  default='',
                                  mask='*')
    if password.lower() in quitOptions:
        quitPets()
    # This defines connection so that we can automatically connect to MySQL database through a pymysql function
    connection = pymysql.connect(host="localhost",
                                   user="root",
                                   password=password,
                                   db="pets",
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)
# You must define possible errors and exceptions and make the program quit nicely like we went over in class
except EOFError:
    print("Quitting. Come back soon!")
    quitPets()
except Exception as e:
    print(f"Error: {e}. Exiting Pet_Chooser.")
    exit()



# According to Ken and many wise men on YouTube, this executes the SQL command that we wrote above. Everything that
# we wrote will be put into a dictionary (petDict) that we can use to populate each list below.
# A cursor in MySQL is used to retrieve rows from your SQL data set and then perform operations on that data. The cursor
# enables you to iterate over returned rows from an SQL query.
# ^^^^ proof that I can read
with connection.cursor() as cursor:
    cursor.execute(petdbConnector)
    petDict = cursor.fetchall()

# make listOfPets an empty list
# name each row in the dictionary 'pet', and append your empty list with the contents of petDict
listOfPets = list()
for pet in petDict:
    listOfPets.append(Pet(pet["petName"],
                          pet["ownerName"],
                          pet["age"],
                          pet["petType"]))

# Now we start the actual loop! Begin with a 'while True' statement
while True:
    # Let's start with an initial greeting
    print("Please choose one of our lovely (if somewhat exotic in some cases) pets:")
    # This is a tricky bit of code that gets a list of the pets names. A lot of trial and error made this... also tears
    # Don't overthink it like me. You can append your list just like we did before in the other assignments.
    # Essentially, you're printing each entry (pet) in the list as its own line
    # Use "i + 1" in the print function so that the objects are numbered starting at 1, and not 0
    for i in range(0, len(listOfPets)):
        print("[", i+1, "]", listOfPets[i].petName)
    # Remind the use of the option to enter a quit command at the end after your list
    print("[ Q ] Quit")

    # At this point, a list should be printed on screen and the user should choose from that list.

    # Let's get the user's input.
    try:
        choice = input()
        # First check if the input is a quit command. using 'choice.lower' reads all the input as lower-case so even
        # if they enter 'Q' or 'Quit', it will still be interpreted as a viable input
        if choice.lower() in quitOptions:
            quitPets()
        # This will cover any input that might not be in the choices listed, and return a Value Error
        # Go through each one and make sure that each pet is properly linked with its owner, pet ID, age, etc.
        # I can't get Rex to work. I'm going insane.
        # NVM, all I had to do was add +1 to length. I can't believe that was all.
        choice = int(choice)
        if choice not in range(1, len(listOfPets) + 1):
            raise ValueError
    # Instead of a ValueError making the program quit, write an exception for it
    # Make sure to put petInput after the error message so that the loop starts over
    except ValueError:
        print("Invalid input. Remember, you have to enter the number next to the pet name, but not their actual name.")
        print()
        petInput()
    # This lets us use Ctrl-D to quit
    except EOFError:
        print("Oh shoot, you're using the ejector seat! Program better, Jon! ABANDON SHIP!")
        quitPets()
    # This should handle any other potential errors
    except Exception as e:
        print(f"Exception error: {e}. Quitting Pet Chooser.")
        quitPets()
    # This next portion covers everything that we want to happen if we get a proper input like we want.
    # According to a lot of sources I read, we're supposed to do all the exceptions we want first, then use 'else' to
    # cover the proper input. There's other ways to make the code work but this is supposedly proper syntax 'grammar'
    # Remember to put perInput at the end so that the loop starts over!
    # I tried to this using 'print(f"blah_function_blah")' but it didn't go well
    else:
        print("You have chosen " + listOfPets[choice - 1].petName + " the " + listOfPets[choice - 1].petType + ".",
              listOfPets[choice - 1].petName + " is " + str(listOfPets[choice - 1].petAge) + " years old.",
              listOfPets[choice - 1].petName + "'s owner is " + listOfPets[choice - 1].ownerName + ".")
        print()
        petInput()
