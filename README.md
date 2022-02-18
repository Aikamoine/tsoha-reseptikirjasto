# Reseptikirjasto
Sovellus löytyy osoitteesta https://tsoha-reseptikirjasto.herokuapp.com.
(Vertais)arviointia varten on tehty käyttäjätunnus admin-oikeuksin.
Tunnus (ilman lainausmerkkejä): "testadmin"
Salasana (ilman lainausmerkkejä): "salasanaonPassword1"

## Ominaisuuksia
- [x] käyttäjä voi kirjautua sisään ja ulos
  - [x] Käyttäjätunnuksen luominen onnistuu käyttäjän toimesta
- etusivulta voi navigoida selailemaan reseptejä
  - [x] kaikki reseptit tulostuvat yhdelle listalle
  - [x] reseptejä voi hakea/suodattaa listalta
  - [x] resepteillä on tagit/tunnisteet, joiden perusteella voi suodattaa
  - KYSYMYS ARVIOIJALLE: onko käyttäjän kannalta kivempi, että on vain yksi hakukenttä, vai että jokaisella "otsikolla" on oma hakunsa?
- pääkäyttäjä voi tehdä muutoksia käyttöliittymällä
  - [x] tällä hetkellä kuka vain käyttäjä voi lisätä reseptejä
  - [x] pääkäyttäjä voi poistaa
    - [x] käyttäjiä
    - [x] reseptejä
    - [x] ainesosia
    - [x] yksiköitä
    - [ ] kommentteja
  - [x] pääkäyttäjä voi muokata
    - [ ] kommentteja
    - [ ] reseptejä
    - [ ] ainesosia
    - [ ] yksiköitä
    - [ ] tunnisteita
- [x] reseptejä voi kommentoida
- [x] istunnon aikana voi muodostaa "ostoslistan", jolle voi merkitä useamman reseptin, joiden aineisosat sovellus tallentaa yhdelle listalle 
  - [x] listalta voi poistaa jo kaapista löytyviä asioita helposti
  - [x] lista poistetaan uloskirjautumisen yhteydessä

## Backlog (ei prioriteettijärjestyksessä)
- reseptien lisäämisen parannukset
  - lisätieto-kenttä tai kenttä alkuperäisen reseptin lähteelle
- eri tietueiden muokkausominaisuudet kuntoon

 
### Laajempia ideoita / täsmennyksiä (tehdään ehkä kurssin jälkeen)
- Finelin sivuilta voisi tuoda ruoka-aineiden ravintoarvot ja sovellus voisi sitten laskea annosten ravintosisällön
- Hakutulosten sivuttaminen. Tämä tuskin on tarpeen, koska ei palveluun olla lisäämässä älyttömiä määriä reseptejä
- tilavuusyksiköiden tunnistaminen (esim. 1 rkl = 15 ml) ja yhteenlasku yhdenmukaisesti, esim. 1 tl + 1 rkl suolaa = 20 ml
- syötteiden validoinnin tehostus
- Reseptiä lisätessä käydään katsomassa mitkä kaikki ainesosat, yksiköt ja tunnisteet on jo kannassa. Käyttäjältä kysytään haluaako lisätä niitä mitä ei ole, vai haluaako muuttaa syötettä -> vältetään yksiköt "sipuli, sipulia" yms.
