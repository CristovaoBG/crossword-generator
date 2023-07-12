
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
``` individualismo
incandescencia
espectroscopia
desnutricao
coerencia
microbiota
leucocitos
poesia
nervoso
isometrica
independencia
enredo
catalise
opep
etica
rad

```
##### Layout file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|I|N|D|I|V|I|D|U|A|L|I|S|M|O|
|N| |S| |E| |E| |L| | | |I| |
|C|A|T|A|L|I|S|E| |E|T|I|C|A|
|A| | | | | |N| |P| | | |R| |
|N|A| | |L|E|U|C|O|C|I|T|O|S|
|D| | | | | |T| |E| |S| |B| |
|E|S|P|E|C|T|R|O|S|C|O|P|I|A|
|S| | | |L| |I| |I| |M| |O| |
|C|O|E|R|E|N|C|I|A| |E|S|T|E|
|E| |N| |R| |A| | | |T| |A| |
|N|E|R|V|O|S|O| |O|U|R|O| | |
|C| |E| | | | | |P| |I| |R| |
|I|N|D|E|P|E|N|D|E|N|C|I|A| |
|A| |O| |I| | | |P| |A| |D| |

##### Directions file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|+|─|+|─|+|─|+|─|+|─|─|─|+|─|
|\|| |\|| |\| ||\|| |\|| | | |\| |
|+|─|+|─|+|─|+|─| |─|─|─|+|─|
|\| | | | | ||\|| |\|| | | |\| |
|+|─| | |─|─|+|─|+|─|+|─|+|─|
|\| | | | | ||\|| |\|| |\|| |\| |
|+|─|─|─|+|─|+|─|+|─|+|─|+|─|
|\|| | | |\|| |\|| |\|| |\|| |\| ||
|+|─|+|─|+|─|+|─|+| |+|─|+|─|
|\|| |\|| |\|| |\|| | | |\|| |\|| |
|+|─|+|─|+|─|+| |+|─|+|─| | |
|\|| |\|| | | | | |\|| |\|| |\|| |
|+|─|+|─|+|─|─|─|+|─|+|─|+| |
|\|| |\|| |\|| | | |\|| |\|| |\|| |

##### Descriptor file:
The first two numbers of each line of the descriptor indicates the X and Y origin of the given word, then the following character (before the actual word) indicates if the word is oriented in the vertically ("|") or horizontally ("-").
```
individualismo
incandescencia
espectroscopia
desnutricao
coerencia
microbiota
leucocitos
poesia
nervoso
isometrica
independencia
enredo
catalise
opep
etica
rad
```

Scpecial characters that indicates direction, end of word and blank spaces can easily be changed in the code.

### TODO
- Optimize some time consuming functions in Cython
- Handle bad usage exceptions 

    
Created by Cristóvão B. Gomes
cristovao@live.com