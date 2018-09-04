from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from django.core.files import File
from pygraphviz import *
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Pricing_Game(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    players_number = models.IntegerField(default=2)
    graph = ArrayField(
        ArrayField(
            models.IntegerField(blank=True),
        ),
    )
    communication_matrix = ArrayField(
        ArrayField(
            models.IntegerField(blank=True),
        ),
    )
    graph_graph = models.ImageField(null=True, upload_to="SummerSchool/photo")
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
        actions = Pricing_Game_Data.objects.filter(round=self).order_by('source')
        for action in actions:
            print(action.source.id)
        tax = [action.new_price for action in actions]
        # for
        print("tax")
        print(tax)
        matrix = np.array(self.game.graph)
        print(matrix)
        for i in range(self.game.players_number):
            matrix[:, i] *= tax[i]
        graph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph())
        print(matrix)
        G = AGraph(directed=True)
        for source, dest, params in graph.edges(data=True):
            G.add_edge(source, dest, label=params["weight"])
        G.layout()
        G.draw("graph.png")
        # plt.clf()
        # pos = nx.spring_layout(graph)
        # labels = dict([((u, v,), d['weight']) for u, v, d in graph.edges(data=True)])
        # print("edge data")
        # print(labels)
        # print(graph.edges(data=True))
        # nx.draw_networkx_edges(graph, pos, width=6, alpha=0.5, edge_color='black')
        # nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        # nx.draw(graph, pos, with_labels=True, node_size=700, node_color="blue")
        # plt.draw()
        # plt.savefig("graph.png")
        with open('graph.png', 'rb') as f:   # use 'rb' mode for python3
            data = File(f)
            self.game.graph_graph.save('graph'+str(self.game.id)+".png", data, True)
        paths = dict(nx.all_pairs_dijkstra_path(graph))
        print("path")
        print(paths)
        profits = [0] * self.game.players_number
        print("profit")
        print(profits)
        size = self.game.players_number
        value = 100
        packets = self.game.communication_matrix

        def calc_price(i, j):
            price = 0
            print("salam")
            print(i)
            print(j)
            print(paths)
            print(paths[i][j])
            print(paths[i][j])
            temp = len(paths[i][j]) - 1
            if (temp == 0):
                temp = 1
            for k in paths[i][j][1:temp]:
                print("baba")
                print(k)
                price += tax[k]
            return price

        def calc_profits(packet_value, i, j):
            price = calc_price(i, j)
            if price <= packet_value:
                profits[i] += packet_value - price
                for k in paths[i][j][1:len(paths[i][j]) - 1]:
                    profits[k] += tax[k]

        def calc_all():
            for i in range(size):
                for j in range(size):
                    for k in range(packets[j][i]):
                        calc_profits(value, i, j)
        calc_all()
        for action in actions:
            action.profit = profits[action.source.id-1]
            action.save()

    def get_strategies_profits(self):
        data = Pricing_Game_Data.objects.filter(round=self).order_by('-source')
        actions = [self.round_number]
        profits = [self.round_number]

        for action in data:
            actions.append(action.new_price)
            profits.append(action.profit)
        return (actions, profits)
