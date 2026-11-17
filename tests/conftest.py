import pytest
from unittest.mock import patch
from io import StringIO

from src import main

@pytest.fixture
def game():
    g = main.MontyHallGame()
    g.doors = ['goat', 'car', 'goat']
    return g
