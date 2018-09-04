from django import forms
from main import models
from django.forms.utils import ErrorDict, ErrorList, pretty_name  # NOQA
from django.core.exceptions import NON_FIELD_ERRORS


class PricingPlayForm(forms.Form):
    # form for charging wallets
    amount = forms.IntegerField(min_value=1, label='قیمت جدید')
    current_round = {}
    current_strategy_table_data = {}
    current_profit_table_data = {}

    def __init__(self, *args, **kwargs):
            #     print("in init")
        self.user = kwargs.pop("user")
        self.game = kwargs.pop("game")
        print("game in init")
        print(self.game)
        self.action = None
        self.round_number = PricingPlayForm.get_current_round(self.game.id).round_number
        self.strategy_table_data = PricingPlayForm.current_strategy_table_data.get(self.game.id)
        self.profit_table_data = PricingPlayForm.current_profit_table_data.get(self.game.id)
        super(PricingPlayForm, self).__init__(*args,  **kwargs)
    #     print("done")
    #     # return temp

    @staticmethod
    def get_current_round(game_id):
        print("in get current tound")
        if not PricingPlayForm.current_round.get(game_id):
            print("in if")
            game = models.Pricing_Game.objects.get(id=game_id)
            print(game)
            print(models.Round.objects.filter(game=game).order_by('-round_number').first())
            PricingPlayForm.current_round[game_id] = models.Round.objects.filter(game=game).order_by('-round_number').first()
        print("game_is")
        print(PricingPlayForm.current_round[game_id])
        return PricingPlayForm.current_round[game_id]

    def clean(self):
        print("in the start of clean")
        temp = super().clean()
        price = self.cleaned_data["amount"]
        self.action = models.Pricing_Game_Data(round=PricingPlayForm.get_current_round(self.game.id), source=self.user, new_price=price)
        print(self.action.__dict__)
        self.action.full_clean()
        print("end of clean")
        return temp

    def update_db(self):
        # updates db
        self.action.save()
        this_round = PricingPlayForm.get_current_round(self.game.id)
        if (len(models.Pricing_Game_Data.objects.filter(round=this_round)) >= self.game.players_number):
            next_round = this_round.get_next_round()
            PricingPlayForm.current_round[self.game.id] = next_round
            this_round.finished = True
            this_round.set_profits_and_save()
            this_round.save()
            next_round.save()
            temp = self.game.get_last_strategies_profits()
            PricingPlayForm.current_strategy_table_data[self.game.id] = temp[0]
            PricingPlayForm.current_profit_table_data[self.game.id] = temp[1]
