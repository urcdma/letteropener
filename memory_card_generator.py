import genanki
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='memory_card_generator.log', filemode='w')

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
        logging.info(f"Adding card with front: {front} and back: {back}.")
        note = genanki.Note(
            model=self.model,
            fields=[front, back])
        self.deck.add_note(note)
        logging.info(f"Card added successfully.")

    def generate_deck(self) -> genanki.Deck:
        logging.info("Generating deck.")
        return self.deck

    def save_deck_to_file(self, filename: str = 'output.apkg'):
        logging.info(f"Saving deck to file: {filename}.")
        genanki.Package(self.deck).write_to_file(filename)
        logging.info("Deck saved successfully.")
