from .models import Period, Dashboard
from datetime import datetime, timedelta
from calendar import monthrange


def get_period(date=None):
        if not date:
            date = datetime.now()
        period = Period.objects.filter(start_date__lte=date, end_date__gte=date)
        if period.exists():
            return period[0]
        else:
            mrange = monthrange(date.year, date.month)
            start_date = datetime(year=date.year, month=date.month, day=1, hour=0)
            end_date = datetime(year=date.year, month=date.month, day=mrange[1], hour=0) + timedelta(days=1) - timedelta(microseconds=1)
            period = Period(month=date.strftime("%B"),
                            year=date.strftime("%Y"),
                            start_date=start_date,
                            end_date=end_date
                            )
            period.save()
            return period


def get_dashboard(period_id=None, profile_id=None):
    if not (period_id or profile_id):
        return None
    else:
        dashboard = Dashboard.objects.filter(profile_id=profile_id, period_id=period_id)
        if dashboard.exists():
            return dashboard.get()
        else:
            dashboard = Dashboard(profile_id=profile_id, period_id=period_id)
            dashboard.save()
            return dashboard
