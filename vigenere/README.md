# Cracking the Vigenere Cipher

## Hoe uit te voeren
Voer de pythonfile ``main.py`` uit. Verslag is hieronder te vinden.

## Oplossing

Rauwe ontcijferde tekst:
```text
DOEMAARGEWOONALSOFIKERNIETBENZEIIKTEGENHETKINDDATVANDEHONGERAANHETSTERVENWASENDATIKPROBEERDETEFOTOGRAFERENIKWASZENUWACHTIGENWOUDATIKEENPILTESLIKKENHADDIEHETBEVENVANMIJNHANDENZOUSTOPPENERGENSVOELDEIKDATDITMIJNFOTOZOUWORDENDEFOTODIEFOTODIEMIJNGROTEDOORBRAAKZOUINLUIDENWAARDOORIKMIJNMARKTWAARDEKONOPDRIJVENDIEHETMIJZOUTOESTAANDEGROTEBAASVANREUTERSTEVRAGENOFHIJMIJEENSTERUGKONBELLENWANNEERHETMIJBETERPASTEEENFOTOGRAAFVOELTZOIETSDEWERELDBEROEMDEHENRICARTIERBRESSONVOELDEHETTOENHIJDATJONGETJEMETDETWEEWIJNFLESSENINDEPARIJSERUEMOUFFETARDVASTLEGDEELLIOTERWITTVOELDEHETTOENDIENEGERVOORHETOOGVANDECAMERAZIJNTONGUITSTAKALFREDSTIEGLITZVOELDEHETTOENDATMOOIEMEISJEMETDENOGMOOIEREVINGERSHAARJASHADDICHTGEKNOOPTOPHETJUISTEMOMENTENEDWARDSTEICHENHADHONDERDENKIEKJESVANGRETAGARBOGESCHOTENMAARHADNOGTIJDENSHETSCHERPSTELLENVANZIJNLENSGEVOELDDITWORDTHETENIGEWARESCHONEULTIEMEPORTRETVANDEGODINHETZELFDEALSWATIKVOELDEMETHETUITGEHONGERDEKINDINMIJNVIZIERZALIGOPAVONDENDIENERGENSVOORDEUGENDANVOORFLAUWEKULHOORJEWELEENSBEWERENDATFOTOGRAFIEVEELZONIETALLESMETGELUKVANDOENHEEFTENDANBEGINNENZEOVERDEMAKERVANDEFOTODIEIEDEREENKENTHETNAAKTEMEISJEVERBRANDRENNENDMETDEARMENOPENCHRISTUSMETEENKUTALSDEFOTOGRAAFNIETTOEVALLIGOPDEPLAATSVANHETNAPALMBOMBARDEMENTWASGEWEESTZOREDENERENZEDANHADHIJNOOITDIEFOTOKUNNENSCHIETENENDUSHEEFTHETTEMAKENMETGELUKTJAUGAATTOCHNIETMOPPERENDATIKHETGELUKHADDATERVOORMIJNOGENEENKINDLAGTECREPERENIKHADDATGELUKNIETIKHADDATTALENTZOALSROBERTCAPAHETTALENTHADDENEUSHADMETZIJNCAMERAOPDEPLAATSTEZIJNWAAREENSOLDAATDEHERSENENUITDEKOPWERDENGESCHOTENGELUKZEGGENBERGBEKLIMMERSDIEEENMOORDENDESTEENLAWINEOPDRIECENTIMETERVANHUNSMIKKELZAGENVOORBIJRAZENGELUKISOPDENDUUREENKWESTIEVANBEKWAAMHEIDIKWEETDATZEDAARGELIJKINHEBBENI
```

Ontcijferde tekst (met spaties):
```text
DOE MAAR GEWOON ALSOF IK ER NIET BEN ZEI IK TEGEN 
HET KIND DAT VAN DE HONGER AAN HET STERVEN WAS EN DAT IK PROBEERDE 
TE FOTOGRAFEREN IK WAS ZENUWACHTIG EN WOU DAT
IK EEN PIL TE SLIKKEN HAD DIE
HET BEVEN VAN MIJN HANDEN ZOU STOPPEN ERGENS VOELDE IK DAT DIT MIJN FOTO ZOU WORDEN DE FOTO
DIE FOTO DIE MIJN GROTE DOORBRAAK ZOU INLUIDEN WAARDOOR IK MIJN MARKTWAARDE KON OPDRIJVEN DIE HET MIJ ZOU 
TOESTAAN DE GROTE BAAS VAN REUTERSTE VRAGEN OF HIJ MIJ EENS TERUG KON BELLEN WANNEER HET MIJ BETER PAST 
EEEN FOTOGRAAF VOELT ZOIETS DE WERELD BEROEMDE HENRI CARTIER BRESSON VOELDE HET TOEN HIJ DAT JONGETJE MET 
DE TWEE WIJNFLESSEN IN DE PARIJSE RUE MOUFFETARD VASTLEGDE ELLIOT ERWITT VOELDE HET TOEN DIE NEGER VOOR HET OOG 
VAN DE CAMERA ZIJN TONG UIT STAK ALFRED STIEGLITZ
VOELDE HET TOEN DAT MOOIE MEISJE MET DE NOG MOOIERE VINGERS HAAR JAS
HAD DICHTGEKNOOPT OP HET JUISTE MOMENT EN EDWARD STEICHEN HAD HONDERDEN KIEKJES VAN GRETA GARBO GESCHOTEN MAAR 
HAD NOG TIJDENS HET SCHERPSTELLEN VAN ZIJN LENS GEVOELD DIT WORDT HET ENIGE WARE SCHONE ULTIEME PORTRET 
VAN DE GOD IN HET ZELFDE ALS WAT IK VOELDE MET HET UITGEHONGERDE KIND IN MIJN 
VIZIER ZALIG OP AVOND EN DIE NERGENS VOOR DEUGEN DAN VOOR FLAUWEKUL HOOR JE WELEENS 
BEWEREN DAT FOTOGRAFIE VEEL ZONIET ALLES MET GELUK VAN DOEN HEEFT EN DAN BEGINNEN ZE OVER DE MAKER 
VAN DE FOTO DIE IEDEREEN KENT HET NAAKTE MEISJE VERBRAND RENNEND MET DE ARMEN OPEN CHRISTUS MET 
EEN KUT ALS DE FOTOGRAAF NIET TOEVALLIG OP DE PLAATS VAN HET NAPALMBOMBARDEMENT WAS GEWEEST 
ZO REDENEREN ZE DAN HAD HIJ NOOIT DIE FOTO KUNNEN SCHIETEN EN DUS HEEFT 
HET TE MAKEN MET GELUK TJAU GAAT TOCH NIET MOPPEREN DAT IK HET GELUK HAD DAT ER VOOR MIJN OGEN EEN 
KIND LAG TE CREPEREN IK HAD DAT GELUK NIET IK HAD DAT TALENT ZOALS ROBERT CAPAHET TALENT HADDENEUS HAD MET ZIJN
CAMERA OP DE PLAATS TE ZIJN WAAR EEN SOLDAAT DE HERSENEN UIT DE KOP WERDEN GESCHOTEN 
GELUK ZEGGEN BERG BE KLIMMERS DIE EEN MOORDENDE STEENLAWINE OP DRIE CENTIMETER VAN HUN SMIKKEL ZAGEN
VOORBIJ RAZEN GELUK IS OP DEN DUUR EEN KWESTIE VAN BEKWAAMHEID IK WEET DAT ZE DAAR GELIJK IN HEBBEN I
```

Van het boek 'Problemski Hotel' van 'Dimitri Verhulst'

## Oplossingsmethode
Eerst heb ik de enkel-kolomtranspositie achterhaald.
Vervolgens heb ik [Simon Singh cracking the vigenere cipher](https://www.simonsingh.net/The_Black_Chamber/vigenere_cracking_tool.html)
gebruikt om de laatste sleutel (VERHULST) en de tekst te achterhalen.

Tot slot, heb ik een gelijkwaardig systeem geïmplementeerd, zodat het automatisch de tekst
ontcijfert zodat de website van Simon Singh niet meer nodig is.

### Enkel kolomtranspositie
Een eigenschap van Vigenere is dat deze cipher veel herhaling heeft (vooral woorddelen van lengte 3).
Deze eigenschap word geëxploiteerd voor het oplossen van de enkel kolomtranspositie.
Hierbij wordt elke enkel-kolomtranspositie uitgevoerd. Vervolgens word er door middel van **Suffix Arrays** ([suffix array explanation](https://cp-algorithms.com/string/suffix-array.html))
makkelijk gezocht naar common prefixes (CP) in de tekst. Als metric pakken we de CP van de enkel-kolomtranspositie. We nemen de decryption dat de hoogste CP-hoeveelheid heeft van 
lengte 3. Gelukkig voor ons kwam dit na de eerste poging uit op de ontcijfering van de enkel-kolomtranspositie.

### Vigenere Cipher
De Vigenere cipher voert steeds een Caesar Cipher uit, zodat voor iedere groep posities (met dezelfde mod key lengte), het meest voorkomende karakter gelijkgesteld is aan 'E'.
We maken wel gebruik van het feit dat we de key lengte weten (kan via trial and error/ Simon Singh tool). Door steeds het meest frequente karakter te linken aan het karakter 'E', komen we snel tot het juiste antwoord.

### Concrete functies

- ``CommonPrefixCounter.py`` zorgt ervoor, dat gegeven een string, het makkelijk is te tellen hoe vaak dat een zekere 3-letter combinatie voorkomt.
- ``TranspositionCipher.py`` voert de enkel kolomtranspositie encryptie en decryptie uit.
- ``VigenereSolver.py`` kraakt de vigenere zelf, door steeds Caesar ciphers uit te voeren, en steeds het meest frequente karakter gelijk te stellen aan 'E'
- ``main.py`` hier is de functie ``find_highest_cp``, deze functie voert alle mogelijke enkel-kolomtransposities uit, en behoudt de key van de resulterende transpositie decryptie die de meeste common prefixes heeft. Deze file voert ook de hele decryptie uit.

### Moeilijkheden
Niet aanwezig, het werkte na de eerste poging.

### References
- Course Material Code Theory from Professor S. Symens
- Vigenere cracking tool (https://www.simonsingh.net/The_Black_Chamber/vigenere_cracking_tool.html) from Simon Singh 
- Suffix Array (https://cp-algorithms.com/string/suffix-array.html) Mainly from Jakobkogler
