from django.db import models
import json

# Create your models here.


MPO = "MPO"
FPO = "FPO"
MP40 = "MP40"
MA1 = "MA1"


DIVISION_CHOICES = (
    (MPO, "MPO"),
    (FPO, "FPO"),
    (MP40, "MP40"),
    (MA1, "MA1"),
)


class Round(models.Model):
    roundScores = models.CharField(max_length=200)

    def setRoundScores(self, lst):
        self.roundScores = json.dumps(lst)

    def getRoundScores(self):
        return json.loads(self.roundScores)


class Event(models.Model):
    roundNumber = models.PositiveSmallIntegerField()
    eventId = models.CharField(max_length=8)
    division = models.CharField(max_length=5,
                  choices=DIVISION_CHOICES,
                  default=MPO)