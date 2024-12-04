# Playfair

> :warning: Disclaimer: de code in deze folder gebruikt the infamous **BIG BALL OF MUD** pattern. Wees gewaarschuwd.

De oorsponkelijke foldersstructuur zag er als volgt uit:

```
│   bigram_test.png
│   decrypted.txt
│   graphic_generator.py
│   playfair.py
│   README.md
│   text_splitter.py
│   word_list_generator.py
│
├───corpus
│   │   corpus_preprocessing.py
│   │   links.txt
│   │   preprocessed_to_playfair.py
│   │
│   ├───original
│   │   ├───de
│   │   │       deu_news_1995_100K-sentences.txt
│   │   │
│   │   ├───en
│   │   │       eng-uk_web_2002_1M-sentences.txt
│   │   │       eng_news_2005_100K-sentences.txt
│   │   │
│   │   ├───es
│   │   │       spa_news_2006_100K-sentences.txt
│   │   │
│   │   ├───fr
│   │   │       fra_news_2005-2008_100K-sentences.txt
│   │   │
│   │   ├───it
│   │   │       ita_news_2005-2009_100K-sentences.txt
│   │   │
│   │   ├───la
│   │   │       lat_wikipedia_2014_100K-sentences.txt
│   │   │
│   │   └───nl
│   │           nld_mixed_2012_100K-sentences.txt
│   │
│   └───preprocessed
│       ├───de
│       │       deu_news_1995_100K-sentences.txt
│       │
│       ├───en
│       │       eng-uk_web_2002_1M-sentences.txt
│       │       eng_news_2005_100K-sentences.txt
│       │
│       ├───es
│       │       spa_news_2006_100K-sentences.txt
│       │
│       ├───fr
│       │       fra_news_2005-2008_100K-sentences.txt
│       │
│       ├───it
│       │       ita_news_2005-2009_100K-sentences.txt
│       │
│       ├───la
│       │       lat_wikipedia_2014_100K-sentences.txt
│       │
│       └───nl
│               nld_mixed_2012_100K-sentences.txt
│
├───stats
│   ├───de
│   │       bigram_frequency_de_part_1.png
│   │
│   ├───en
│   │       bigram_frequency_en_part_1.png
│   │       quadrams.txt
│   │
│   ├───es
│   │       bigram_frequency_es_part_1.png
│   │
│   ├───fr
│   │       bigram_frequency_fr_part_1.png
│   │
│   ├───it
│   │       bigram_frequency_it_part_1.png
│   │
│   ├───la
│   │       bigram_frequency_la_part_1.png
│   │       
│   ├───letters
│   │       bigram_frequency_de.png
│   │       bigram_frequency_en.png
│   │       bigram_frequency_fr.png
│   │       bigram_frequency_la.png
│   │       bigram_frequency_nl.png
│   │
│   └───nl
│           bigram_frequency_nl_part_1.png
│
├───tests
│       02-OPGAVE-playfair.txt
│       playfair-old.txt
│
├───word_lists
│   ├───without_frequency
│   │       de_deu_news_1995_100K-sentences.txt
│   │       en_eng_news_2005_100K-sentences.txt
│   │       es_spa_news_2006_100K-sentences.txt
│   │       fr_fra_news_2005-2008_100K-sentences.txt
│   │       it_ita_news_2005-2009_100K-sentences.txt
│   │       la_lat_wikipedia_2014_100K-sentences.txt
│   │       nl_nld_mixed_2012_100K-sentences.txt
│   │
│   └───with_frequency
│           de_deu_news_1995_100K-sentences.txt
│           en_eng_news_2005_100K-sentences.txt
│           es_spa_news_2006_100K-sentences.txt
│           fr_fra_news_2005-2008_100K-sentences.txt
│           it_ita_news_2005-2009_100K-sentences.txt
│           la_lat_wikipedia_2014_100K-sentences.txt
│           nl_nld_mixed_2012_100K-sentences.txt
```

Laten we eerst beginnen met de root folder. Naast deze ``README.md`` file kan je de volgende belangrijke bestanden vinden:

- ``bigram_test.png``: bigramverdeling van de ciphertext.
- ``decrypted.txt``: output van de vorige runs van de Playfair solver
- ``graphic_generator.py``: script dat ik heb gebruikt om de grafieken voor de bigramverdelingen te genereren
- ``playfair.py``: Playfair solvers (run die om de code te cracken!)
- ``text_splitter``: bevat een handig scriptje om een string in woorden te splitsen en dus wat spaties toe te voegen 

## Bepalen van de taal

Voor de opgave hebben we als een hint gekregen dat het originele bericht in het Nederlands, Frans, Duits, Engels, Italiaans of Spaans geschreven is.
Om te bepalen met welke van deze talen ik verder moet werken, heb ik frequentieanalyse toegepast.

### Frequentieanalyse

Aangezien dat Playfair een bericht bigram per bigram encrypt, vond ik logisch om een frequentietabel op te stellen voor elke van de gegeven talen en vergelijken of het min om meer hetzelfde patroon volgt als de gegeven ciphertext.
Hiervoor heb ik een dataset van 100000 zinnen van elke taal gepakt van https://wortschatz.uni-leipzig.de/en/download. In ``corpus/original`` folder kan je die datasets vinden. 
Daarna heb ik met ``corpus/corpus_preprocessing.py`` alle bestanden verwerkt zodat ze alleen lowercase letters bevatten (daarnaast heb ik j met i vervangen en en ook de letters met diakritische tekens met overeenstemmende letters van het Latijnse alfabet).
Het resultaat kan je in de ``corpus/preprocessed`` folder vinden.

Tot slot, heb ik grafieken van bigram frequentie gegenereerd met ``graphic_generator.py``. Voor de ciphertext zelf was de volgende afbeelding de output:

![Bigram verdeling voor ciphertext](./bigram_test.png)

Mijn conclusie was dat de meest waarschijnlijke taal het Engels is. 
Hier is de grafiek hiervan (voor andere talen kan je in de ``stats`` folder vinden):

![Bigram verdeling Engels](./stats/en/bigram_frequency_en_part_1.png)

## Simulated annealing

Simulated annealing is een optimalisatiealgoritme dat kan gebruikt worden om een globale extremum te vinden (in ons geval het globale maximum, maar daarover verder). 
Om gevallen te voorkomen waarbij het model in een lokaal extremum blijft hangen (wat zou in het geval van een hill climbing kunnen gebeuren), wordt er een concept van *temperatuur* geintroduceerd.
Hoe hoger de temperatuur, hoe groter de kans dat een key met een slechtere score geaccepteerd wordt.
In de loop van het werken van de simulated annealing algoritme daalt de temperatuur geleidelijk, wat tot een *greedier* search leidt. 

Samengevat, hier is een overzicht van hoe het algoritme werkt:

1. Begin met key *k*, * 

Een van de grootste struikelpunten voor mij was om een goed heuristic en parameters te vinden.
Helaas, van wat ik heb gelezen, zijn er geen vaste regels hoe je dat moet doen, waardoor mijn zoektocht naar de juiste oplossing een beetje langer was dan ik had verwacht.

#### Start key

Op zich speelt het geen grote rol, maar in het geval van deze ciphertext geeft het gemiddeld betere resultaten als je met de string ```abcdefghiklmnopqrstuvxyz``` dan een willekeurige sleutel. 
Maar opnieuw, door het aard van het algoritme, werkt het in beide gevallen.

#### Begintemperatuur

...

#### Aantal stappen

...

#### Aantal iteraties

...

#### Begintemperatuur

...

#### Temperatuurrooster

...

#### Neighbour generation function

...

#### Evaluatiefunctie

...

#### Oplossing

Bij een van de runs heb ik het volgende resultaat gekregen:

```text
1733165260.5431437
New best score: -7039.003283658883
Best key found: ['u', 'r', 's', 'o', 't', 'h', 'c', 'k', 'l', 'f', 'y', 'i', 'g', 'm', 'b', 'q', 'w', 'x', 'z', 'p', 'd', 'v', 'e', 'n', 'a']
Splitted text: you dont know about meu nl esx s you have read a box ok by the name of the adventures of tom sawyer 
that box ok was writ x ten by mark twain and he holds the truths mainly not all parts of the story are true 
but most of it is i dont know anyone who tel xl s the truth all the time except perhaps aunt polly or the widow 
douglas or tom sawyers x sister mary these people are written about in the adventures of tom sawyer that book 
ends like this to mandi find money that was x stolen and we are allowed to k exe pit we become rich we each have 
six thousand x do lx lars in gold i ud get hatcher put the money in a bank for us and we can have a dollar a day 
that is more money than a person can knowhow to spend the widow douglas to x ok me into her home to live but i did 
note nio y living in a nice house i put on my old clothes and ran away and was fr exe and hap xp y but x tom sawyer 
found me and said that if i wanted to io in his club and befriends i would have to return to live with the widow for 
this reason i returned to live with x her the widow cried over me and gave me new clothes to wear but i hated those 
new clothes i felt too warm in the mandi could not move my arms and legs f rex ely when supper was being served the 
widow always ran gabel xl and i had to come quickly i was happier when i could eat whenever i chose to thought his 
meant i had to make meals of the bits of food other people had thrown away when i asked permission to smoke the 
widow said no she thought x that smoking was a dirty habit and told me that i must not smoke her sister m is x 
swat son a woman who had never marx ried and who had no children of her own came to live with x her she thought 
x that she could change me and make me a bet xt er person by educating me and teaching me to sp el xl she worked 
with me for an hour until the widow made her stop miss watson complainedabout everything i did dont put your f 
ex et up there huckleberry sit straight in your chair why cant you improve the way x you act dont be so 
disrespectful to those who are trying to co rx rec t you x
```

Ziet er goed uit! Dit fragment komt uit ``The Adventures of Huckleberry Finn`` geschreven door Mark Twain. 

### Extra

Om de juiste decryptie gemakkelijker te kunnen herkennen, heb ik eens scriptje gemaakt dat gebaseerd is op Ziph's law en dat in een string met een gegeven taal spaties toevoegt.
Zoals je boven kan zien, werkt het best ok.

