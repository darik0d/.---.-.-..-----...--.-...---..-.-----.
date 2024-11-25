# ADFGVX

Om deze code te ontcijferen heb ik in drie stappen gewerkt.

## 1. Mogelijkheden transpositie uitschrijven
We hadden gekregen dat de sleutel maximaal van lengte 10 zou zijn.
Daarom waren er voor de kolomtranspositie *slechts* $\sum_{k=1}^{10} k!=4.037.913$  mogelijkheden: voor elke mogelijke sleutellengte de mogelijke volgordes van de kolommen.

Als eerste idee heb ik geprobeerd deze mogelijkheden allemaal te overlopen en de digramfrequenties uit te schrijven naar een bestand om later te kunnen analyseren. Dit bleek ineens al goed genoeg te werken (zie volgende stap)

Met `frequency_calculator.py` doe ik dit in een 50tal minuten op mijn PC.
Het resultaat is een bestand van 1,51GB.

## 2. Digramfrequenties transpositie onderzoeken
Bij het onderzoeken van de digramfrequenties heb ik rekening gehouden met het volgende:
- Bij een juiste transpositie zou de hoogste frequentie veel hoger zijn dan bij de meeste foute transposities, die een meer gelijkmatige verdeling zouden produceren.
- Bij een juiste transpositie zou het ook logisch zijn dat er bepaalde digrammen niet voorkwamen (bv. het is onwaarschijnlijk dat in een literaire tekst, alle getallen zouden voorkomen).


In enkele minuten vind ik met `frequency_analyzer` vier ordeningen waarbij de maximale frequentie mijn *threshold* overschrijdt. De threshold is experimenteel bepaald.
Van de vier ordeningen is er één die hoogstwaarschijnlijk de juiste was: 
(4, 2, 5, 0, 7, 1, 6, 8, 3). Bij deze volgorde kwamen 12 digrams niet voor, terwijl bij de andere transposities alle digrams minstens één keer voorkwamen.
Deze volgorde heb ik bij de substitutie verder gebruikt en bleek uiteindelijk de juiste te zijn. 

Toen ik eenmaal de plaintext had teruggevonden en wist over welke tekst het ging(zie volgende stap), kon ik de sleuteltekst voor de transpositie gemakkelijk raden: `GENTLEMAN` komt overeen met de gevonden kolomvolgorde. 

## 3. Digramsubstitutie ongedaan maken

De substitutie bleek moeilijker te zijn.
Ik heb eerst een aantal varianten van bruteforce uitgeprobeerd, met beperkingen op de lengte van de tekst of het aantal digrams om mogelijkheden voor uit te proberen, om de runtime enigzins te beperken. Ik gebruikte woordenlijsten om met het aantal gematchte woorden te berekenen hoe hard de gesubstitueerde tekst leek op een juiste tekst.
Dit gaf geen goede resultaten.

Ook heb ik geprobeerd te vertrekken vanuit een frequentietabel en van daar de n (n=2, n=3) meest waarschijnlijke mappings van digram naar letter uit te proberen. Ook hierbij geen succes en een zeer lange runtime om iets betekenisvols te kunnen uitproberen.

Ten slotte besefte ik dat ik een meer gestructureerde aanpak nodig had. Ik ben gegaan voor het Hill Climbing algoritme. Voor de fitness-functie leek de woordenlijst-aanpak mij niet geschikt aangezien deze geen duidelijk verschil zou geven in score bij één aanpassing aan de substitutie, wat net belangrijk is voor Hill Climbing.

Daarom heb ik gekozen voor een variant op de fitness functie hier beschreven: http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/. 

Met deze aanpak kon ik de plaintext vinden.

Aangezien mijn implementatie Stochastic Hill Climbing gebruikt geeft het script (`substitution_solver.py`) niet telkens dezelfde output. Meestal kom ik met een fitness score van 75.12 op deze tekst:
```
LETRANFEVOXAFEILAVAITSIGIENCOMMENCECEPENDANTPOURMAPARTZENENBISZAMAISQUISANNONCATSOUSDEPLUSHEUREUJAUSPICESLAPROVENCEESTUNTRANSATLANTIQUERAPIDECONBORTAGLECOMMANDEPARLEPLUSABBAGLEDESHOMMESLASOCIETELAPLUSCHOISIESXTROUVAITREUNIEDESRELATIONSSEBORMAIENTDESDIVERTISSEMENTSSORFANISAIENTNOUSAVIONSCETTEIMPRESSIONEJQUISEDETRESEPARESDUMONDEREDUITSANOUSMEMESCOMMESURUNEILEINCONNUEOGLIFESPARCONSEQUENTDENOUSRAPPROCHERLESUNSDESAUTRESETNOUSNOUSRAPPROCHIONSAVEYVOUSZAMAISSONFEACEQUILXADORIFINALETDIMPREVUDANSCEFROUPEMENTDETRESQUILAVEILLEENCORENESECONNAISSAIENTPASETQUIDURANTQUELQUESZOURSENTRELECIELINBINIETLAMERIMMENSEVONTVIVREDELAVIELAPLUSINTIMEENSEMGLEVONTDEBIERLESCOLERESDELOCEANLASSAUTTERRIBIANTDESVAFUESETLECALMESOURNOISDELEAUENDORMIECESTAUBONDVECUEENUNESORTEDERACCOURCITRAFIQUELAVIEELLEMEMEAVECSESORAFESETSESFRANDEURSSAMONOTONIEETSADIVERSITEETVOILAPOURQUOIPEUTETREONFOUTEAVECUNEHATEBIEVREUSEETUNEVOLUPTEDAUTANTPLUSINTENSECECOURTVOXAFEDONTONAPERCOITLABINDUMOMENTMEMEOUILCOMMENCEMAISDEPUISPLUSIEURSANNEESQUELQUECHOSESEPASSEQUIAZOUTESINFULIEREMENTAUJEMOTIONSDELATRAVERSEELAPETITEILEBLOTTANTEDEPENDENCOREDECEMONDEDONTONSECROXAITABBRANCHIUNLIENSUGSISTEQUINESEDENOUEQUEPEUAPEUENPLEINOCEANETPEUAPEUENPLEINOCEANSERENOUELETELEFRAPHESANSBILAPPELSDUNAUTREUNIVERSDOULONRECEVRAITDESNOUVELLESDELABACONLAPLUSMXSTERIEUSEQUISOITLIMAFINATIONNAPLUSLARESSOURCEDEVOQUERDESBILSDEBERAUCREUJDESQUELSFLISSELINVISIGLEMESSAFELEMXSTEREESTPLUSINSONDAGLEENCOREPLUSPOETIQUEAUSSIETCESTAUJAILESDUVENTQUILBAUTRECOURIRPOUREJPLIQUERCENOUVEAUMIRACLEAINSILESPREMIERESHEURESNOUSSENTIMESNOUSSUIVISESCORTESPRECEDESMEMEPARCETTEVOIJLOINTAINEQUIDETEMPSENTEMPSCHUCHOTAITALUNDENOUSQUELQUESPAROLESDELAGASDEUJAMISMEPARLERENTDIJAUTRESVINFTAUTRESNOUSENVOXERENTATOUSATRAVERSLESPACELEURSADIEUJATTRISTESOUSOURIANTSORLESECONDZOURACINQCENTSMILLESDESCOTESBRANCAISESPARUNAPRESMIDIORAFEUJLETELEFRAPHESANSBILNOUSTRANSMETTAITUNEDEPECHEDONTVOICILATENEURARSENELUPINAVOTREGORDPREMIERECLASSECHEVEUJGLONDSGLESSUREAVANTGRASDROITVOXAFESEULSOUSLENOMDERACEMOMENTPRECISUNCOUPDETONNERREVIOLENTECLATADANSLECIELSOMGRELESONDESELECTRIQUESBURENTINTERROMPUESLERESTEDELADEPECHENENOUSPARVINTPASDUNOMSOUSLEQUELSECACHAITARSENELUPINONNESUTQUELINITIALESILSEBUTAFIDETOUTEAUTRENOUVELLEZENEDOUTEPOINTQUELESECRETENEUTETESCRUPULEUSEMENTFARDEPARLESEMPLOXESDUPOSTETELEFRAPHIQUEAINSIQUEPARLECOMMISSAIREDUGORDETPARLECOMMANDANTMAISILESTDECESEVENEMENTSQUISEMGLENTBORCERLADISCRETIONLAPLUSRIFOUREUSELEZOURMEMESANSQUONPUTDIRECOMMENTLACHOSEAVAITETEEGRUITEENOUSSAVIONSTOUSQUELEBAMEUJARSENELUPINSECACHAITPARMINOUS
```

en dit met substitutie
|   | A | D | F | G | V | X |
|---|---|---|---|---|---|---|
| A | Y | G | J | Q | T | C |
| D | M |   |   | D | V |   |
| F | F | X | R | U |   |   |
| G |   | O |   | B |   |   |
| V |   | E |   | I |   | L |
| X | A | H | S | P | N | Z |

met 12 lege vakken voor de 12 ontbrekende digrams.

Deze substitutie was nog niet perfect maar leek wel hard op een Franse tekst, en kon dus gemakkelijk manueel verbeterd worden:

| Digram | Waarde gevonden dmv hill climbing | Manuele verbetering |
|--------|-----------------------------------|---------------------|
| FA     | f                                 | g                   |
| GG     | b                                 | f                   |
| AD     | g                                 | b                   |
| AF     | j                                 | x                   |
| FD     | x                                 | y                   |
| XX     | z                                 | j                   |
| AA     | y                                 | z                   |

met 
|   | A | D | F | G | V | X |
|---|---|---|---|---|---|---|
| A | Z | B | X | Q | T | C |
| D | M |   |   | D | V |   |
| F | G | Y | R | U |   |   |
| G |   | O |   | F |   |   |
| V |   | E |   | I |   | L |
| X | A | H | S | P | N | J |

Dit geeft de volgende tekst:
```
letrangevoyageilavaitsibiencommencecependantpourmapartjenenfisjamaisquisannoncatsousdeplusheureuxauspiceslaprovenceestuntransatlantiquerapideconfortablecommandeparleplusaffabledeshommeslasocietelapluschoisiesytrouvaitreuniedesrelationsseformaientdesdivertissementssorganisaientnousavionscetteimpressionexquisedetreseparesdumondereduitsanousmemescommesuruneileinconnueobligesparconsequentdenousrapprocherlesunsdesautresetnousnousrapprochionsavezvousjamaissongeacequilyadoriginaletdimprevudanscegroupementdetresquilaveilleencoreneseconnaissaientpasetquidurantquelquesjoursentrelecielinfinietlamerimmensevontvivredelavielaplusintimeensemblevontdefierlescoleresdeloceanlassautterrifiantdesvaguesetlecalmesournoisdeleauendormiecestaufondvecueenunesortederaccourcitragiquelavieellememeavecsesoragesetsesgrandeurssamonotonieetsadiversiteetvoilapourquoipeutetreongouteavecunehatefievreuseetunevoluptedautantplusintensececourtvoyagedontonapercoitlafindumomentmemeouilcommencemaisdepuisplusieursanneesquelquechosesepassequiajoutesingulierementauxemotionsdelatraverseelapetiteileflottantedependencoredecemondedontonsecroyaitaffranchiunliensubsistequinesedenouequepeuapeuenpleinoceanetpeuapeuenpleinoceanserenoueletelegraphesansfilappelsdunautreuniversdoulonrecevraitdesnouvellesdelafaconlaplusmysterieusequisoitlimaginationnapluslaressourcedevoquerdesfilsdeferaucreuxdesquelsglisselinvisiblemessagelemystereestplusinsondableencorepluspoetiqueaussietcestauxailesduventquilfautrecourirpourexpliquercenouveaumiracleainsilespremieresheuresnoussentimesnoussuivisescortesprecedesmemeparcettevoixlointainequidetempsentempschuchotaitalundenousquelquesparolesdelabasdeuxamismeparlerentdixautresvingtautresnousenvoyerentatousatraverslespaceleursadieuxattristesousouriantsorlesecondjouracinqcentsmillesdescotesfrancaisesparunapresmidiorageuxletelegraphesansfilnoustransmettaitunedepechedontvoicilateneurarsenelupinavotrebordpremiereclassecheveuxblondsblessureavantbrasdroitvoyageseulsouslenomderacemomentprecisuncoupdetonnerreviolenteclatadanslecielsombrelesondeselectriquesfurentinterrompueslerestedeladepechenenousparvintpasdunomsouslequelsecachaitarsenelupinonnesutquelinitialesilsefutagidetouteautrenouvellejenedoutepointquelesecreteneutetescrupuleusementgardeparlesemployesdupostetelegraphiqueainsiqueparlecommissairedubordetparlecommandantmaisilestdecesevenementsquisemblentforcerladiscretionlaplusrigoureuselejourmemesansquonputdirecommentlachoseavaiteteebruiteenoussavionstousquelefameuxarsenelupinsecachaitparminous
```

Deze komt uit de verzameling verhalen van Maurice Leblanc `Arsène Lupin, gentleman-cambrioleur`, specifiek het deel `L'arrestation d'Arsène Lupin`.