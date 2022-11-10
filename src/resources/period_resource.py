from src import db
from src.models.period import Period


class PeriodResource:
    def __int__(self):
        pass

    @staticmethod
    def add_new_period(year, semester, day, start_hr, start_min, end_hr, end_min):
        period = Period(year=year,
                        semester=semester,
                        day=day,
                        start_hr=start_hr,
                        start_min=start_min,
                        end_hr=end_hr,
                        end_min=end_min)
        db.session.add(period)
        db.session.commit()

    @staticmethod
    def get_period_id(year, semester, day, start_hr, start_min, end_hr, end_min):
        return db.session.query(Period.id).filter_by(year=year,
                                                     semester=semester,
                                                     day=day,
                                                     start_hr=start_hr,
                                                     start_min=start_min,
                                                     end_hr=end_hr,
                                                     end_min=end_min).first()
