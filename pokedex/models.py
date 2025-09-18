from django.db import models

class PokemonType(models.Model):
    name = models.CharField(max_length=20, unique=True, default=None)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    CHOICES = (
    ('grass', 'Grass'),
    ('fire', 'Fire'),
    ('water', 'Water'),
    ('bug', 'Bug'),
    ('dark', 'Dark'),
    ('dragon', 'Dragon'),
    ('electric', 'Electric'),
    ('fairy', 'Fairy'),
    ('fighting', 'Fighting'),
    ('flying', 'Flying'),
    ('ghost', 'Ghost'),
    ('ground', 'Ground'),
    ('ice', 'Ice'),
    ('normal', 'Normal'),
    ('poison', 'Poison'),
    ('psychic', 'Psychic'),
    ('rock', 'Rock'),
    ('steel', 'Steel'),
    ('shadow', 'Shadow'),
)

    pokedex_id = models.IntegerField(unique=True, default=None)
    name = models.CharField(max_length=15, unique=True, default=None)
    types = models.ManyToManyField(PokemonType)
    sprite = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.name
