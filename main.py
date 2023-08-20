import logging
from gui import GUI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='w')

def main():
    logging.info("Application started.")
    gui = GUI()
    gui.start()
    logging.info("Application closed.")

if __name__ == "__main__":
    main()
