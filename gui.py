import tkinter as tk
from tkinter import filedialog
from code_analyzer import CodeAnalyzer
from gpt3_model import GPT3Model
from memory_card_generator import MemoryCardGenerator
from database import Database
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='gui.log', filemode='w')

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
        logging.info("User initiated file upload.")
        filename = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
        self.analyze_and_display_results(code)
        self.generate_and_display_memory_cards(code)
        logging.info("File upload and processing completed.")

    def analyze_and_display_results(self, code):
        logging.info("Analyzing code and displaying results.")
        self.analyzer.analyze_code(code)
        description = self.gpt3_model.describe_code(code)
        evaluation = self.gpt3_model.evaluate_code(code)
        knowledge_points = self.gpt3_model.list_knowledge_points(code)
        self.analysis_results_text.insert(tk.END, f"Description: {description}\n")
        self.analysis_results_text.insert(tk.END, f"Evaluation: {evaluation}\n")
        self.analysis_results_text.insert(tk.END, f"Knowledge Points: {knowledge_points}\n")
        logging.info("Analysis and display completed.")

    def generate_and_display_memory_cards(self, code):
        logging.info("Generating and displaying memory cards.")
        knowledge_points = self.gpt3_model.list_knowledge_points(code).split(', ')
        for point in knowledge_points:
            description_cn, description_en = self.gpt3_model.get_knowledge_point_description(point)
            self.memory_card_generator.add_card(description_cn, description_en)
            self.memory_cards_text.insert(tk.END, f"Front: {description_cn}, Back: {description_en}\n")
            self.database.store_memory_card(description_cn, description_en)
        logging.info("Memory cards generation and display completed.")

    def download_apkg(self):
        logging.info("User initiated memory cards download.")
        self.memory_card_generator.save_deck_to_file()
        logging.info("Memory cards download completed.")

    def start(self):
        self.window.mainloop()
