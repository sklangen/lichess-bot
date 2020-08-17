from Tournament import tournaments 
from Client import Client
from pprint import pprint
import datetime
import locale


class Scheduler:
    def __init__(self, client):
        self.client = client
        self.scheduled_on_server = list(client.get_100_swiss())

    def get_tournaments_of_date(self, date):
        for tour in self.scheduled_on_server:
            if datetime.date.fromisoformat(tour['startsAt'][:10]) == date:
                return tour 
        return None

    def get_unscheduled_tournaments(self):
        date = datetime.date.today()
        for _ in range(30):
            date += datetime.timedelta(days=1)
            for tour in tournaments:
                appointment = tour.appointment(date.year, date.month)
                if appointment.date() == date:
                    on_server = self.get_tournaments_of_date(date)
                    if on_server is None:
                        yield appointment, tour
                    else:
                        print('Tournament', tour.name, 'for', date, 'is already scheduled:', on_server)

    def schedule_future_tournaments(self):
        for app, tour in self.get_unscheduled_tournaments():
            starts_at = int(app.timestamp())*1000
            name = app.strftime('%b ') + tour.name

            description = f'Erstellt von OSHs Bot um {datetime.datetime.utcnow()}'
            if not tour.rated:
                description += '\n\nKeine Saisonwertung'

            print(f'Scheduling {repr(name)}={tour} at {app}')
            res = self.client.create_swiss(tour.clock_limit, tour.clock_increment,
                tour.rounds, name=name, description=description, starts_at=starts_at)

            if res.status_code == 200:
                self.scheduled_on_server.append(res.json())
            else:
                print('Error:', res.json())

def main():
    locale.setlocale(locale.LC_ALL, 'de_DE')
    
    with open('lichess.token') as f:
        token = f.read().strip()
    client = Client(team_id='schachklub-langen-e-v', token=token)

    Scheduler(client).schedule_future_tournaments()

if __name__ == '__main__':
    main()
