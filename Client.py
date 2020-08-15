import json
import requests

class Client:
    base_url = 'https://lichess.org'

    def __init__(self, team_id, token):
        self.team_id = team_id
        self.token = token
        self._headers = { 
            'Accept': 'application/vnd.lichess.v3+json',
            'Authorization': 'Bearer ' + self.token
        }

    def _get(self, location):
        return requests.get(self.base_url + location, headers=self._headers)

    def _post(self, location, **kwargs):
        return requests.post(self.base_url + location, headers=self._headers, **kwargs)

    def get_top_10(self):
        res = self._get('/player')
        return res.json()

    def get_100_swiss(self):
        res = self._get(f'/api/team/{self.team_id}/swiss')
        for line in res.text.splitlines():
            yield json.loads(line)

    def create_swiss(self, clock_limit, clock_increment, rounds, name=None, starts_at=None,
            round_interval=None, variant=None, description=None, rated=None, chat_for=None):
        data = {
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'nbRounds': rounds,
        }

        if name is not None:
            data['name'] = name

        if starts_at is not None:
            data['startsAt'] = starts_at

        if round_interval is not None:
            data['roundInterval'] = round_interval

        if variant is not None:
            data['variant'] = variant

        if description is not None:
            data['description'] = description

        if rated is not None:
            data['rated'] = rated

        if chat_for is not None:
            data['chatFor'] = chat_for

        print(data)
        return self._post(f'/api/swiss/new/{self.team_id}', data=data)
