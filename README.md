# Reseptikirjasto
Tällä hetkellä sovelluksen perusominaisuudet toimivat MVP-tasolla. Mukavaan käyttökokemukseen on vielä paljon kehitettävää, mutta kokonaisuus on periaatteessa nyt toimiva. Sovellus löytyy https://tsoha-reseptikirjasto.herokuapp.com.

Huom! Rivien poistaminen ostoslistalta vaikuttaa toimivan varsin vaihtelevasti ja saattaa vaatia useampia yrityksiä/selainsivun päivityksiä. Chrome-selaimella vaikuttaisi toimivan vähän paremmin kuin esim. Firefoxilla.

## Ominaisuuksia
- käyttäjä voi kirjautua sisään ja ulos (toteutettu)
  - Käyttäjätunnuksen luominen onnistuu joko käyttäjän (toteutettu) tai pääkäyttäjän toimesta
    - jälkimmäinen vain, jos tarkoituksena jaella rajatun pääsyn reseptejä rajatulle joukolle
- etusivulta voi navigoida aiheittain tai tekstihaun avulla selailemaan reseptejä
  - kaikkien reseptien selaus yhdeltä listalta on toteutettu
  - resepteillä on siis tagit/tunnisteet
- pääkäyttäjä voi lisätä reseptin ja muokata olemassaolevaa
  - tällä hetkellä kuka vain käyttäjä voi lisätä
- reseptejä voi kommentoida
- istunnon aikana voi muodostaa "ostoslistan", jolle voi merkitä useamman reseptin, joiden aineisosat sovellus tallentaa yhdelle listalle (toteutettu, mutta ei ole istuntokohtainen...)
  - listalta voi poistaa jo kaapista löytyviä asioita helposti (toteutettu)

## Backlog (ei prioriteettijärjestyksessä)
- ulkoasun siistimistä
- ostoslista istuntokohtaiseksi
- reseptien lisäämisen parannukset
  - syötteiden validoinnin tehostus
  - käyttöoikeuksien rajaus
  - ainesosien tarkistus / kirjoitusvirheiden eliminointi
  - ainesosien lisäys murto- tai liukulukuina
- käyttöoikeushallinta
  - tällä hetkellä ei varsinaisesti tee mitään
  - käyttäjien / reseptien poisto pääkäyttäjäoikeuksien taakse
- reseptien listauksen parannukset
  - aihetunnisteet/tagit
  - lisätieto-kenttä tai kenttä alkuperäisen reseptin lähteelle
- kommentointimahdollisuus resepteihin

### Laajempia ideoita / täsmennyksiä
- Finelin sivuilta voisi tuoda ruoka-aineiden ravintoarvot ja sovellus voisi sitten laskea annosten ravintosisällön
- tilavuusyksiköiden tunnistaminen (esim. 1 rkl = 15 ml) ja yhteenlasku litroissa

