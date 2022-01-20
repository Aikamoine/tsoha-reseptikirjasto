# Reseptikirjasto
Otsikko on ehkä vähän harhaanjohtava, koska sovelluksen ei ole tarkoitus olla pelkkä kirjasto, vaan moniulotteisempi ruuonlaiton apuväline.

## Ominaisuuksia
- käyttäjä voi kirjautua sisään ja ulos
  - Käyttäjätunnuksen luominen onnistuu joko käyttäjän tai pääkäyttäjän toimesta
    - jälkimmäinen vain, jos tarkoituksena jaella rajatun pääsyn reseptejä rajatulle joukolle
- etusivulta voi navigoida aiheittain tai tekstihaun avulla selailemaan reseptejä
  - resepteillä on siis tagit/tunnisteet
- pääkäyttäjä voi lisätä reseptin ja muokata olemassaolevaa
- reseptejä voi kommentoida
- istunnon aikana voi muodostaa "ostoslistan", jolle voi merkitä useamman reseptin, joiden aineisosat sovellus tallentaa yhdelle listalle
  - listalta voi poistaa jo kaapista löytyviä asioita helposti

### Laajempia ideoita / täsmennyksiä
- jokainen aineisosa on oma tietueensa
- jokainen resepetin vaihe on oma tietueensa
- Finelin sivuilta voisi tuoda ruoka-aineiden ravintoarvot ja sovellus voisi sitten laskea annosten ravintosisällön

## Alustava tietokantakuvaus
- users
- ingredients
- cooking_steps
- recipes
- comments
- tags
