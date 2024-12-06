# Enigma

## Hoe uit te voeren
Voer de pythonfile ``main.py`` uit.

## Oplossing

```
alice della rocca odiava la scuola di sci odiava la sveglia alle sette e mezzo del mattino anche nelle vacanze 
di natale e suo padre che a colazione la fissava e sotto il tavolo faceva ballare la gamba nervosa mente come a dire 
su s briga ti odiava la calza maglia di lana che la punge va sulle cosce lem off o le che non le lasciavano muovere 
le dita il casco che le schiaccia vale guance e puntava con il ferro sulla mandibola e poi quegli scarponi sempre 
troppo stretti che la facevano camminare come un gorilla
```
Deze tekst komt uit `La solitudine dei numeri primi` door Paolo Giordano.

Rotors: ``[1, 3, 4]``, ``['E', 'F', 'I']``

Plug mapping: ``KBCXEUGNSWALMHOPQRITFVJDYZ``

## Oplossingsmethode
Enigma wordt ontcijferd door het implementeren van de Advanced Turing Bombe.

### PermutatieMatrix
De file ``PermutatieMatrix.py`` bevat de implementatie van de permutatiematrix. Deze matrix volgt het algoritme van de 
geavanceerde Turing Bombe. Stroom wordt gesimuleerd door op elke positie van de matrix een ``PermutationNode`` te plaatsen.
Ieder node object heeft een lijst van connections (``propagations``). Deze lijst bevat alle andere nodes, waarmee de 
gegeven node verbonden is (verbindingen worden gemaakt volgens het algoritme van de cursus). Voor het onder stroom zetten van een node,
word de ``trigger()`` method gebruikt. Dit zet de gegeven node 'onder stroom', en zet recursief alle connecties onder 
stroom. Indien deze node al onder stroom stond, zal die deze trigger negeren. Dit voorkomt hetzelfde werk meerdere keren te  
doen en vermijdt ook oneindige recursie. Er is een ``clear()`` method, om alle stroom te laten verdwijnen.
Het is makkelijk te checken welke nodes onder stroom worden gezet: indien er 1 node van de gegeven rij onder stroom staat,
zullen de rotors en rotorposities juist zijn.

### Moeilijkheden
Het evenredig verdelen van Enigma, zodat iedereen een deel kon bijdragen aan het oplossen van deze cipher.

### References
- Course Material Code Theory from Professor S. Symens
- Enigma tool from https://atlas.uantwerpen.be/~ssymens/enigma.php
