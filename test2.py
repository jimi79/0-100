#!/usr/bin/python3
import minmax
import importlib

a=minmax.AI('/tmp/ai.db')
a.init_db()
a.init_state('coucou', ['1', '2', '3'], False)
a.init_state('coucou2', ['1', '2', '3'], True)
a.init_path('coucou', 1, 'coucou2', False)
a.init_path('coucou2', 2, 'coucou3', True)
