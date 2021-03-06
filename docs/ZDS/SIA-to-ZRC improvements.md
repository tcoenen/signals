# Pijnpunten in het ZRC/DRC/ZTC

1. **De api ziet er to omslachtig uit.**

    Er zijn te veel stappen die niet logisch aan voelen. Het maken van een zaak zou je verwachten
    dat je de koppeling naar het object zou kunnen mee geven. Dit moet nu in een losse call
    gebeuren. Dit voelt niet heel logisch aan.
    Hezelfde geldt hier ook voor het enkelvoudiginformatieobject. Dit is ook niet met 1 call aan de
    zaak te koppelen.

    [issue](https://github.com/VNG-Realisatie/gemma-zaken/issues/523)

2. **De documentatie in de api specs zou uitgebreider kunnen.**

    Zo was het niet meteen duidelijk waar een objectinformatieobject precies voor was. De spec zelf
    zegt hier niets over. Pas bij de list komt er een uitleg naar voren. Deze is echter nog al vaag.

    > Beheer relatie tussen InformatieObject en OBJECT.

    Wat is een object? Bij het ZRC werd er naar een object verwezen van een externe
    applicatie. Is dat hier ook het geval? Antwoord, nee; als je bij de create call kijkt zie je dat
    het gaat om een zaak of besluit. Dit zou ook in de documentatie kunnen. Of mogelijk een
    referentie naar de documentatie die over dit onderdeel gaat. Zonder dat de developer het zelf zou
    hoeven zoeken.

    [issue](https://github.com/VNG-Realisatie/gemma-zaken/issues/522)

3. **Rollen.**

    > Opvragen en bewerken van ROLrelatie tussen een ZAAK en een BETROKKENE.

    Waar komt de BETROKKENE vandaan?

    [issue](https://github.com/VNG-Realisatie/gemma-zaken/issues/522)

4. **authenticatie**

    Zonder authenticatie kan dit niet bij amsterdam in productie draaien. Dit betekent dat het
    systeem pas in gebruik genomen kan worden nadat de authenticatie is toegevoegd.

    Wordt aan gewerkt

5. **Filter status**

    Er is geen filter op status. Hierdoor is het niet op een restfull manier mogelijk om alle
    statussen op te halen bij een zaak.

    [issue](https://github.com/VNG-Realisatie/gemma-zaken/issues/518)

