import tkinter as tk
from tkinter import filedialog
from code_analyzer import CodeAnalyzer
from gpt3_model import GPT3Model
from memory_card_generator import MemoryCardGenerator
from database import Database

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Code Analyzer")
        self.analyzer = CodeAnalyzer()
        self.gpt3_model = GPT3Model()
        self.memory_card_generator = MemoryCardGenerator()
        self.database = Database()
        self.upload_file_button()
        self.analysis_results_text = self.create_text_area()
        self.memory_cards_text = self.create_text_area()
        self.download_apkg_button()

    def upload_file_button(self):
        button = tk.Button(self.window, text="Upload Python File", command=self.upload_file)
        button.pack()

    def create_text_area(self):
        text = tk.Text(self.window)
        text.pack()
        return text

    def download_apkg_button(self):
        button = tk.Button(self.window, text="Download Memory Cards", command=self.download_apkg)
        button.pack()

    def upload_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        with open(filename, 'r') as file:
            code = file.read()
        self.analyze_and_display_results(code)
        self.generate_and_display_memory_cards(code)

    def analyze_and_display_results(self, code):
        self.analyzer.analyze_code(code)
        description = self.gpt3_model.describe_code(code)
        evaluation = self.gpt3_model.evaluate_code(code)
        knowledge_points = self.gpt3_model.list_knowledge_points(code)
        self.analysis_results_text.insert(tk.END, f"Description: {description}\n")
        self.analysis_results_text.insert(tk.END, f"Evaluation: {evaluation}\n")
        self.analysis_results_text.insert(tk.END, f"Knowledge Points: {knowledge_points}\n")

    def generate_and_display_memory_cards(self, code):
        knowledge_points = self.gpt3_model.list_knowledge_points(code).split(', ')
        for point in knowledge_points:
            self.memory_card_generator.add_card(point, point)
            self.memory_cards_text.insert(tk.END, f"Front: {point}, Back: {point}\n")
            self.database.store_memory_card(point, point)

    def download_apkg(self):
        self.memory_card_generator.save_deck_to_file()

    def start(self):
        self.window.mainloop()
