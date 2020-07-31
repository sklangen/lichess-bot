from Tournament import tournaments 
from Client import Client
from pprint import pprint
import datetime
import locale

def get_next_tournament(date):
    for _ in range(7):
        date += datetime.timedelta(days=1)
        for tour in tournaments:
            appointment = tour.appointment(date.year, date.month)
            if appointment.date() == date:
                return appointment, tour
    return None, None

def schedule_next_tournament(client):
    today = datetime.date.today()
    app, tour = get_next_tournament(today)

    if app is None:
        print('No tournament to be scheduled within the next seven days. Exiting...')
        return

    starts_at = int(app.timestamp())*1000
    name = app.strftime('%B ') + tour.name

    description = f'Erstellt von OSHs Bot um {datetime.datetime.utcnow()}'
    if not tour.rated:
        description += '\n\nKeine Saisonwertung'

    print(f'Creating {repr(name)}={tour} at {app}')
    res = client.create_swiss(tour.clock_limit, tour.clock_increment,
        tour.rounds, name=name, description=description, starts_at=starts_at)

    if res.status_code != 200:
        print('Error:', res.json())

def main():
    locale.setlocale(locale.LC_ALL, 'de_DE')
    
    with open('lichess.token') as f:
        token = f.read().strip()
    client = Client(team_id='schachklub-langen-e-v', token=token)

    schedule_next_tournament(client)

if __name__ == '__main__':
    main()
