# Generated by Django 2.0.7 on 2018-08-12 10:50
from django.contrib.auth.hashers import make_password
import networkx as nx
from django.db import migrations
import json
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
from django.core.files import File
import numpy as np
from pygraphviz import *


def add_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'newadmin'
    superuser.email = 'admin@admin.net'
    superuser.password = make_password('adminadmin')
    superuser.save()


def remove_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.get(username="newadmin").delete()


def add_gamer(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    with open("teams") as data:
        teams = json.load(data)
        for name, password in teams.items():
            user = User(username=name, email=name + '@gamer.com')
            user.password = make_password(password)
            user.save()


def remove_gamer(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    gamers = User.objects.filter(is_staff=False)
    gamers.delete()


def add_game(apps, schema_editor):
    g = nx.DiGraph()
    size = 10
    tax = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    packets = [[0, 1, 1, 1, 0, 2, 0, 0, 1, 2],
               [0, 0, 1, 2, 1, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 2, 3, 2, 2, 0, 0],
               [2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 1, 1, 1, 1, 1],
               [1, 1, 0, 1, 1, 0, 0, 1, 0, 0],
               [0, 0, 1, 2, 2, 0, 0, 1, 1, 1],
               [0, 0, 0, 0, 0, 1, 0, 0, 1, 2],
               [2, 2, 0, 0, 3, 2, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 2, 2, 0, 0]]
    g.add_weighted_edges_from([(1, 0, tax[0]), (4, 0, tax[0]),
                               (0, 1, tax[1]), (2, 1, tax[1]), (4, 1, tax[1]),
                               (1, 2, tax[2]), (3, 2, tax[2]),
                               (2, 3, tax[3]), (4, 3, tax[3]),
                               (0, 4, tax[4]), (1, 4, tax[4]), (3, 4, tax[4]), (5, 4, tax[4]),
                               (4, 5, tax[5]), (6, 5, tax[5]), (7, 5, tax[5]), (8, 5, tax[5]),
                               (5, 6, tax[6]), (7, 6, tax[6]),
                               (5, 7, tax[7]), (6, 7, tax[7]), (9, 7, tax[7]),
                               (6, 8, tax[8]), (9, 8, tax[8]),
                               (7, 9, tax[9]), (8, 9, tax[9])])
    PricingGame = apps.get_model('main', 'Pricing_Game')
    Round = apps.get_model('main', 'Round')
    #  ,graph = nx.to_numpy_matrix(g).astype(int).tolist(), communication_matrix = packets
    print(nx.to_numpy_matrix(g).astype(int).tolist())
    print(packets)
    game = PricingGame(name="g1", finished=True, end=datetime.now(), graph=nx.to_numpy_matrix(g).astype(int).tolist(), communication_matrix=packets, players_number=10)
    game.save()
    G = AGraph(directed=True)
    for source, dest, params in g.edges(data=True):
        G.add_edge(source, dest, label=params["weight"])
    G.layout()
    G.draw("graph.png")
    with open('graph.png', 'rb') as f:   # use 'rb' mode for python3
        data = File(f)
        game.graph_graph.save('graph' + str(game.id) + ".png", data, True)
    round = Round(round_number=1, game=game)
    round.save()
    game = PricingGame(name="g2", graph=nx.to_numpy_matrix(g).tolist(), communication_matrix=packets)
    game.save()
    round = Round(round_number=1, game=game)
    round.save()

    size = 4
    tax = [1, 1, 1, 1]
    packets = [[0, 0, 0, 1],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [1, 0, 0, 0],
               ]
    adj = [[0, 1, 1, 0],
           [1, 0, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 0],
           ]
    g = nx.from_numpy_matrix(np.array(adj), nx.DiGraph())
    #  ,graph = nx.to_numpy_matrix(g).astype(int).tolist(), communication_matrix = packets
    print(nx.to_numpy_matrix(g).astype(int).tolist())
    print(packets)
    game = PricingGame(name="g3", finished=True, end=datetime.now(), graph=adj, communication_matrix=packets, players_number=4)
    game.save()
    G = AGraph(directed=True)
    for i in range(size):
        G.add_node(i, height=2)
    for source, dest, params in g.edges(data=True):
        G.add_edge(source, dest, label=params["weight"])
    G.layout()
    G.draw("graph.png")
    with open('graph.png', 'rb') as f:   # use 'rb' mode for python3
        data = File(f)
        game.graph_graph.save('graph' + str(game.id) + ".png", data, True)
    round = Round(round_number=1, game=game)
    round.save()

    size = 10
    tax = [1 for i in range(size)]
    packets = [[1 for i in range(size)] for j in range(size)]
    for i in range(size):
        packets[i][i] = 0
    g = nx.erdos_renyi_graph(size, 0.4, directed=True)
    print(nx.to_numpy_matrix(g).astype(int).tolist())
    print(packets)
    game = PricingGame(name="g4", finished=False, end=datetime.now(), graph=nx.to_numpy_matrix(g).astype(int).tolist(), communication_matrix=packets, players_number=size)
    game.save()
    G = AGraph(directed=True, pad=0.5, nodesep=1, ranksep=2)
    for i in range(size):
        G.add_node(i,height = 0.3, width = 0.3)
    for source, dest, params in g.edges(data=True):
        G.add_edge(source, dest, label=1)
    G.layout()
    G.draw("graph.png")
    with open('graph.png', 'rb') as f:   # use 'rb' mode for python3
        data = File(f)
        game.graph_graph.save('graph' + str(game.id) + ".png", data, True)
    round = Round(round_number=1, game=game)
    round.save()


def remove_game(apps, schema_editor):
    PricingGame = apps.get_model('main', 'Pricing_Game')
    games = PricingGame.objects.all()
    games.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_gamer, remove_gamer),
        migrations.RunPython(add_admin, remove_admin),
        migrations.RunPython(add_game, remove_game),
    ]
