from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pricing_Game(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    players_number = models.IntegerField(default=2)
    # graph = models.Arr
    # def __init__(self, *args, **kwargs):
    #     # self.last_round = Round(round_number=1, game=self)
    #     super().__init__(*args, **kwargs)

    def get_last_strategies_profits(self):
        rounds = Round.objects.filter(game=self, finished=True).order_by('-round_number')
        print("printing rounds")
        print(rounds)
        actions = []
        profits = []
        for round in rounds:
            temp = round.get_strategies_profits()
            actions.append(temp[0])
            profits.append(temp[1])
        print(actions)
        return (actions, profits)


class Pricing_Game_Data(models.Model):
    source = models.ForeignKey(User, related_name="actions", on_delete=models.CASCADE)
    round = models.ForeignKey("main.Round", related_name="round", on_delete=models.CASCADE)
    new_price = models.IntegerField()
    profit = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = (('source', 'round'),)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('source', 'round'):
            return 'شما مبلغ خود برای این راند را اعلام کرده‌اید.'
        else:
            return super(Pricing_Game_Data, self).unique_error_message(model_class, unique_check)


class Round(models.Model):
    round_number = models.IntegerField()
    game = models.ForeignKey(Pricing_Game, related_name="round", on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = (('round_number', 'game'),)

    def get_next_round(self):
        return Round(game=self.game, round_number=self.round_number + 1)

    def set_profits_and_save(self):
        actions = Pricing_Game_Data.objects.filter(round=self)
        for action in actions:
            action.profit = 1
            action.save()
        print("herher")

    def get_strategies_profits(self):
        data = Pricing_Game_Data.objects.filter(round=self).order_by('-source')
        actions = [self.round_number]
        profits = [self.round_number]

        for action in data:
            actions.append(action.new_price)
            profits.append(action.profit)
        return (actions, profits)
