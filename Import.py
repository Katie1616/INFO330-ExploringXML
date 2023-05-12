import sqlite3
import sys
import xml.etree.ElementTree as ET

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>


# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")

conn = sqlite3.connect('pokemon.sqlite')
cursor = conn.cursor()

for i, arg in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue


try:
    tree = ET.parse(arg)
except ET.ParseError():
    print("Error")

poke = tree.getroot()
pokedexNumber = poke.get('pokedex', None)
generation = poke.get('generation', '')
classification = poke.get('classification', '')
name = poke.get('name', '')
hp = poke.findtext('hp', '')
type1 = poke.get('type', '')
type2 = poke.get('type', '')
attack = poke.findtext('attack', '')
defense = poke.findtext('defense', '')
speed = poke.findtext('speed', '')
sp_attack = poke.findtext('sp_attack', '')
sp_defense = poke.findtext('sp_defense', '')
height = poke.findtext('height/m', '')
weight = poke.findtext('weight/kg', '')
abilities = poke.gettext('ability', '')

cursor.execute('SELECT COUNT(*) FROM Pokemon WHERE name=?', (name,))
check = cursor.fetchone()[0]

if check > 0:
        print(f"Pokemon {name} already exists in the database")
else:
    cursor.execute('''INSERT INTO Pokemon (pokedex_number, generation, classification, name, hp, 
        type1, type2, attack, defense, speed, sp_attack, sp_defense, height, weight, abilities) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (pokedexNumber, generation, classification, name, hp, type1, type2,
            attack, defense, speed, sp_attack, sp_defense, height, weight, abilities))

conn.commit()
conn.close()
