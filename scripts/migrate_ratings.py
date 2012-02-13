from foos.main.models import Outcome


def migrate_ratings():
    outcomes = Outcome.objects.all().order_by("created")
    for o in outcomes:
        o.update_rating()

