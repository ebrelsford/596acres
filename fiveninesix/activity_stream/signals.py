from django.dispatch import Signal

# Define our own signal, difficult to disconnect handler for
# actstream.signals.action 

action = Signal(providing_args=[
    'actor',
    'verb',
    'action_object',
    'place',
    'target',
    'description',
    'timestamp',
])
