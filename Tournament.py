import calendar
import datetime

cal = calendar.Calendar()
def fridays(year, month):
    monthcal = cal.monthdatescalendar(year, month)
    return [day for week in monthcal for day in week if \
                day.weekday() == calendar.FRIDAY and \
                day.month == month]

@dataclass
class Tournament:
    name: str
    week: int
    rated: bool
    clock_limit: int
    clock_increment: int
    rounds: int

    def appointment(self, year, month):
        date = fridays(year, month)[self.week]
        time = datetime.time(20, 30, 0)
        return datetime.datetime.combine(date, time)

schnell_15plus0 = Tournament('Schnellschach 15 Plus 0', week=1, rated=True,
        clock_limit=60*15, clock_increment=0, rounds=5)

blitz_3plus2 = Tournament('Blitzschach 3 Plus 2', week=2, rated=True,
        clock_limit=60*3, clock_increment=2, rounds=15)

blitz_5plus0 = Tournament('Blitzschach 5 Plus 0', week=-1, rated=True,
        clock_limit=60*5, clock_increment=0, rounds=15)

tournaments = [schnell_15plus0, blitz_3plus2, blitz_5plus0]
