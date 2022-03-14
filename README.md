# Reseptikirjasto
Sovellus löytyy osoitteesta https://tsoha-reseptikirjasto.herokuapp.com.

## Ominaisuuksia
- [x] käyttäjä voi kirjautua sisään ja ulos
  - [x] Käyttäjätunnuksen luominen onnistuu käyttäjän toimesta
- etusivulta voi navigoida selailemaan reseptejä
  - [x] kaikki reseptit tulostuvat yhdelle listalle
  - [x] reseptejä voi hakea/suodattaa listalta
  - [x] resepteillä on tagit/tunnisteet, joiden perusteella voi suodattaa
- pääkäyttäjä voi tehdä muutoksia käyttöliittymällä
  - [x] tällä hetkellä kuka vain käyttäjä voi lisätä reseptejä
  - [x] pääkäyttäjä voi poistaa
    - [x] käyttäjiä
    - [x] reseptejä
    - [x] kommentteja
  - [x] pääkäyttäjä voi muokata
    - [x] reseptejä
      - etusivulta voi piilottaa reseptejä, reseptiselailusta voi muokata yksityiskohtia
    - [x] ainesosia
    - [x] yksiköitä
    - [x] tunnisteita
- [x] reseptejä voi kommentoida
- [x] istunnon aikana voi muodostaa "ostoslistan", jolle voi merkitä useamman reseptin, joiden aineisosat sovellus tallentaa yhdelle listalle 
  - [x] listalta voi poistaa jo kaapista löytyviä asioita helposti
  - [x] lista poistetaan uloskirjautumisen yhteydessä

## Backlog (ei prioriteettijärjestyksessä)
- Sovellus on nyt Tsoha-kurssin näkökulmasta valmis.

 
### Laajempia ideoita / täsmennyksiä (tehdään ehkä kurssin jälkeen)
- Finelin sivuilta voisi tuoda ruoka-aineiden ravintoarvot ja sovellus voisi sitten laskea annosten ravintosisällön
- Hakutulosten sivuttaminen. Tämä tuskin on tarpeen, koska ei palveluun olla lisäämässä älyttömiä määriä reseptejä
- tilavuusyksiköiden tunnistaminen (esim. 1 rkl = 15 ml) ja yhteenlasku yhdenmukaisesti, esim. 1 tl + 1 rkl suolaa = 20 ml
- reseptien lisäämisen parannukset
  - lisätieto-kenttä tai kenttä alkuperäisen reseptin lähteelle
  - syötteiden validoinnin tehostus
  - Reseptiä lisätessä käydään katsomassa mitkä kaikki ainesosat, yksiköt ja tunnisteet on jo kannassa. Käyttäjältä kysytään haluaako lisätä niitä mitä ei ole, vai haluaako muuttaa syötettä -> vältetään yksiköt "sipuli, sipulia" yms.
- valmistusajat pudotusvalikoksi suoran tekstisyötteen sijaan, voisi ehkä tallentaa omaan tauluunsa
