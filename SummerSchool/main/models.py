from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class PricingGame(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        # self.last_round = Round(round_number=1, game=self)
        super().__init__(*args, **kwargs)

    def update_last_round():
        if (self.last_round):
            self.last_round = Round(round_number=self.last_round.round_number + 1, game=self)


class PricingGameData(models.Model):
    source = models.ForeignKey(User, related_name="actions", on_delete=models.CASCADE)
    round = models.ForeignKey(User, related_name="rouund", on_delete=models.CASCADE)
    new_price = models.IntegerField()
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = (('source', 'round'),)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # Call the real save() method
        self.round.number_of_submits += 1
        self.round.save()


class Round(models.Model):
    round_number = models.IntegerField(primary_key=True)
    game = models.ForeignKey(PricingGame, related_name="round", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        temp = super().__init__(*args, **kwargs)
        self.number_of_players = len(User.objects.filter(is_staff=False))
        self.number_of_submits = 0
        return temp

    def save(self, *args, **kwargs):
        if (self.number_of_submits >= self.number_of_players):
            self.finished = True
            self.game.update_last_round()
            self.game.save()

        super().save(*args, **kwargs)  # Call the real save() method
