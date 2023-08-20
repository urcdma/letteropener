import genanki
from typing import List, Tuple

class MemoryCardGenerator:
    def __init__(self, deck_name: str = 'Python Basics'):
        self.model = genanki.Model(
            1607392319,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ])
        self.deck = genanki.Deck(2059400110, deck_name)

    def add_card(self, front: str, back: str):
        note = genanki.Note(
            model=self.model,
            fields=[front, back])
        self.deck.add_note(note)

    def generate_deck(self) -> genanki.Deck:
        return self.deck

    def save_deck_to_file(self, filename: str = 'output.apkg'):
        genanki.Package(self.deck).write_to_file(filename)
