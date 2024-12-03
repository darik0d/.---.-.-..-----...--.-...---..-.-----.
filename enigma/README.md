# Enigma

### PermutatieMatrix
de file ``PermutatieMatrix.py`` bevat de implementatie van de permutatie matrix. Deze matrix volgt het algorithm van de 
geavanceerde Turing Bombe. Stroom wordt gesimuleerd door op elke positie van de matrix een ``PermutationNode`` te plaatsen.
Ieder node object heeft een lijst van connections (``propagations``). Deze lijst bevat alle andere nodes, waarmee de 
gegeven node verbonden is (verbindingen worden gemaakt volgens het algoritme van de cursus). Voor het onder stroom zetten van een node,
wordt de ``trigger()`` method gebruikt. Dit zet de gegeven node 'onder stroom', en zet recursief alle connecties onder 
stroom. Indien deze node al onder stroom stond, zal die deze trigger negeren. Dit voorkomt hetzelfde werk meerdere keren te  
doen en oneindige recursie. Er is een ``clear()`` method, om alle stroom te laten verdwijnen.
Het is makkelijk te checken welke nodes onder stroom worden gezet, indien er 1 node van de gegeven rij onder stroom staat,
zal de rotors en rotorposities juist zijn.


