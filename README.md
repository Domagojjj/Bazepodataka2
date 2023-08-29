Ovaj projekt demonstrira primjenu upotrebe međuspremnika (cache) za pohranu podataka koristeći Docker,a unutur Dockera i Redis poslužitelj. Projekt uključuje Python aplikaciju koja koristi SQLAlchemy za komunikaciju s bazom podataka i Redis za međuspremanje podataka.
Struktura Projekta:

- main.py: Glavna Python skripta koja sadrži definiciju baze podataka, interakciju s Redisom te primjer korištenja međuspremnika za dohvaćanje podataka.
- Dockerfile: Dockerfile je tekstualna datoteka koja se koristi za definiranje koraka i postavki za izgradnju Docker kontejnera.
- docker-compose.yaml: Konfiguracijska datoteka za pokretanje Redis kontejnera.