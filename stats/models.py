from django.db import models

class Update(models.Model):
    update_text = models.CharField(max_length=255)
    update_url = models.CharField(max_length=127)
    created = models.DateTimeField(null=True,blank=True)

class OutcomeUpdate(Update):
    text_template = "%s beat %s with a score %s - %s"
    url_template = "/stats/view/outcome/?oid=%s"

    def save(self):
        return super(OutcomeUpdate,self).save()


class ScoreUpdate(Update):
    text_template = "%s scored against %s. Score is now %s-%s"
    url_template = ""

    def save(self):
        return super(ScoreUpdate,self).save()
