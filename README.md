
# Crossword Generator
This program takes a dictionary list and finds solutions to a crosswords with a given width and height specified in the header. 

### Input
the program takes a dictionary as input, the program searches for every .txt file in the "data/input" folder, separated by line feed such as shown bellow:
```
teatro
agua
anelideos
anfibios
base
codigo
digestivo
dna
...
```
### output
Three types of output are generated for every generated crossword:
| File | Description |
|------|------|
| Words | List of every word used in the crossword. This file is (the only one) used internaly to generate  new crosswords and not use this words again next time the program is run.|
| Layouts | ASCII visual representation of the crossword, usefull for seeing the results and for debugging. |
| Directions | ASCII visual representation of the direction of every block that forms the crossword. Have no real internal usage, but it's useful to visualize and debug. |
| Descriptor | Contains a list with all of the above information synthesized in a struct, not very useful for visualization, but can be useful to pass the structure to another program. See following example for clarification.|

### Output example
for a given dictionary set of words in the input folder, a typical output for it would look something like the following, for a 14/14 crossword:
##### Words file:
``` proparoxitona
isovolumetrica
totalitarismo
aguapotavel
centrifugacao
digestivo
ondulatoria
parasitose
frio
otan
solo
nuclear
al
oxitona
pb
fusao
mmc
isotopo
ele
```
##### Layout file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|P|R|O|P|A|R|O|X|I|T|O|N|A| |
|I| | | |G| |T| |S| |X| |S| |
| |O|N|D|U|L|A|T|O|R|I|A| | |
|A| |U| |A| |N| |V| |T| |P| |
|M|M|C| |P|B| |S|O|L|O| |A|L|
|P| |L| |O| |D| |L| |N| |R| |
| |C|E|N|T|R|I|F|U|G|A|C|A|O|
|I| |A| |A| |G| |M| | | |S| |
|S|E|R| |V| |E|L|E| |F|R|I|O|
|O| | | |E| |S| |T| |U| |T| |
|T|O|T|A|L|I|T|A|R|I|S|M|O| |
|O| |R| | | |I| |I| |A| |S| |
|P|R|E|S|E|R|V|A|C|A|O| |E|U|
|O| |S| |M| |O| |A| | | | | |

##### Directions file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|+|─|─|─|+|─|+|─|+|─|+|─|+| |
|\|| | | |\|| |\|| |\|| |\|| |\|| |
| |─|+|─|+|─|+|─|+|─|+|─| | |
|\|| |\|| |\|| |\|| |\|| |\|| |\|| |
|+|─|+| |+|─| |─|+|─|+| |+|─|
|\|| |\|| |\|| |\|| |\|| |\|| |\|| |
| |─|+|─|+|─|+|─|+|─|+|─|+|─|
|\|| |\|| |\|| |\|| |\|| | | |\|| |
|+|─|+| |\|| |+|─|+| |+|─|+|─|
|\|| | | |\|| |\|| |\|| |\|| |\|| |
|+|─|+|─|+|─|+|─|+|─|+|─|+| |
|\|| |\|| | | |\|| |\|| |\|| |\|| |
|+|─|+|─|+|─|+|─|+|─|+| |+|─|
|\|| |\|| |\|| |\|| |\|| | | | | |

##### Descriptor file:
The first two numbers of each line of the descriptor indicates the X and Y origin of the given word, then the following character (before the actual word) indicates if the word is oriented in the vertically ("|") or horizontally ("-").
```
0 0 | proparoxitona
0 8 - isovolumetrica
10 0 | totalitarismo
0 4 - aguapotavel
6 1 | centrifugacao
5 6 - digestivo
2 1 | ondulatoria
3 12 - parasitose
8 10 | frio
0 6 - otan
4 7 | solo
2 2 - nuclear
4 12 | al
0 10 - oxitona
4 4 | pb
8 10 - fusao
4 0 | mmc
7 0 - isotopo
8 6 | ele
10 2 - tres
12 0 | preservacao
3 0 - amp
8 0 | ser
0 0 - pi
12 12 | eu
0 12 - as
12 4 - em

```

Scpecial characters that indicates direction, end of word and blank spaces can easily be changed in the code.

    
Created by Cristóvão B. Gomes
cristovao@live.com