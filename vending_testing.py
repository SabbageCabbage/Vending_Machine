import pytest
import vending
import pathlib
import csv

def test_decrement_inventory():
    inventory = {'A1': {'item': "Double-Chunk Chocolate Chip Cookie", 'price_usd': 2.49, 'quantity':2}}
    result = vending.decrementInventory(inventory, 'A1')
    assert result is True
    assert inventory['A1']['quantity'] == 1
def test_display_inventory(capsys):
     inventory = {
        'A1': {'item': 'Soda', 'price_usd': 1.50, 'quantity': 5},
        'B2': {'item': 'Chips', 'price_usd': 2.00, 'quantity': 0},
        'C3': {'item': 'Juice', 'price_usd': 2.50, 'quantity': 3},
    }
     vending.displayInventory(inventory)
     captured = capsys.readouterr() #huh, it captures the outputs how cool!!! the more you know!!
     assert "A1 - $1.50 Soda" in captured.out
     assert "B2 - SOLD OUT" in captured.out
     assert "C3 - $2.50 Juice" in captured.out