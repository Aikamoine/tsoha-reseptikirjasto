# Reseptikirjasto
Sovellus löytyy osoitteesta https://tsoha-reseptikirjasto.herokuapp.com.

## Ominaisuuksia
- [x] käyttäjä voi kirjautua sisään ja ulos
  - [x] Käyttäjätunnuksen luominen onnistuu käyttäjän toimesta
- etusivulta voi navigoida selailemaan reseptejä
  - [x] kaikki reseptit tulostuvat yhdelle listalle
  - [x] reseptejä voi hakea/suodattaa listalta
  - [ ] resepteillä on tagit/tunnisteet, joiden perusteella voi suodattaa
- pääkäyttäjä voi lisätä reseptin ja muokata olemassaolevaa
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
- [x] reseptejä voi kommentoida
- [x] istunnon aikana voi muodostaa "ostoslistan", jolle voi merkitä useamman reseptin, joiden aineisosat sovellus tallentaa yhdelle listalle 
  - [x] listalta voi poistaa jo kaapista löytyviä asioita helposti

## Backlog (ei prioriteettijärjestyksessä)
- reseptien lisäämisen parannukset
  - syötteiden validoinnin tehostus
  - ainesosien tarkistus / kirjoitusvirheiden eliminointi
   - aihetunnisteet/tagit
  - lisätieto-kenttä tai kenttä alkuperäisen reseptin lähteelle
- reseptien lisäämisen parannukset
- tilavuusyksiköiden tunnistaminen (esim. 1 rkl = 15 ml) ja yhteenlasku yhdenmukaisesti, esim. 1 tl + 1 rkl suolaa = 20 ml
 
### Laajempia ideoita / täsmennyksiä
- Finelin sivuilta voisi tuoda ruoka-aineiden ravintoarvot ja sovellus voisi sitten laskea annosten ravintosisällön

