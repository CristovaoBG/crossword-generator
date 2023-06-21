
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
``` contemporanea
eletroquimica
perpendicular
agropecuaria
hidrografia
capitalismo
dissertacao
coplanares
procarionte
narracao
teatro
celular
lua
raio
pac
aves
vol
pol
os
pa
pi
gene
sr
ds
ldc
```
##### Layout file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|C|A|P|I|T|A|L|I|S|M|O|.|P|A|
|O| |E| |E| |U| |R| |S| |R| |
|N|A|R|R|A|C|A|O|.| |.|P|O|L|
|T| |P| |T| |.| |D| |H| |C| |
|E|L|E|T|R|O|Q|U|I|M|I|C|A|.|
|M| |N| |O| |.| |S| |D| |R| |
|P|.|D|S|.|A|V|E|S|.|R|A|I|O|
|O| |I| |.| |O| |E| |O| |O| |
|R|.|C|E|L|U|L|A|R|.|G|E|N|E|
|A| |U| |D| |.| |T| |R| |T| |
|N| |L|.|C|O|P|L|A|N|A|R|E|S|
|E| |A| |.| |A| |C| |F| |.| |
|A|G|R|O|P|E|C|U|A|R|I|A|.| |
|.| |.| |I| |.| |O| |A| | | |

##### Directions file:
|||||||||||||||
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
+|-|+|-|+|-|+|-|+|-|+| |+|-|
|\||| |\||| |\||| |\||| |\||| |\||| |\||| |
|+|-|+|-|+|-|+|-| | | |-|+|-|
|\||| |\||| |\||| | | |\||| |\||| |\||| |
|+|-|+|-|+|-|-|-|+|-|+|-|+| |
|\||| |\||| |\||| | | |\||| |\||| |\||| |
|\||| |+|-| |-|+|-|+| |+|-|+|-|
|\||| |\||| | | |\||| |\||| |\||| |\||| |
|\||| |+|-|+|-|+|-|+| |+|-|+|-|
|\||| |\||| |\||| | | |\||| |\||| |\||| |
|\||| |\||| |+|-|+|-|+|-|+|-|+|-|
|\||| |\||| | | |\||| |\||| |\||| | | |
|+|-|+|-|+|-|+|-|+|-|+|-| | |
| | | | |\||| | | |\||| |\||| | | |

##### Descriptor file:
The first two numbers of each line of the descriptor indicates the X and Y origin of the given word, then the following character (before the actual word) indicates if the word is oriented in the vertically ("|") or horizontally ("-").
```
0 0 | contemporanea
0 4 - eletroquimica
2 0 | perpendicular
0 12 - agropecuaria
10 3 | hidrografia
0 0 - capitalismo
8 3 | dissertacao
4 10 - coplanares
12 0 | procarionte
0 2 - narracao
4 0 | teatro
2 8 - celular
6 0 | lua
10 6 - raio
6 10 | pac
5 6 - aves
6 6 | vol
11 2 - pol
10 0 | os
12 0 - pa
4 12 | pi
10 8 - gene
8 0 | sr
2 6 - ds
4 8 | ldc
```

Scpecial characters that indicates direction, end of word and blank spaces can easily be changed in the code.

### TODO
- Optimize some time consuming functions in Cython

    
Created by Cristóvão B. Gomes
cristovao@live.com