import pandas
import argparse
import typing
import json

from calculator import Calculator

class MainArgs(typing.Protocol):
    input: str
    output: str|None
    settings: str|None
    show_graph: bool

def load_settings_file(file_name:str) -> dict:
    with open(file_name) as file:
        settings = json.load(file)
    
    return settings

def main(args: MainArgs):
    calculator = Calculator(pandas.read_csv(args.input, index_col=0))

    # Chargement du fichier de réglage si argument donné
    if args.settings is not None:
        calculator.set_settings(load_settings_file(args.settings))

    calculator.apply_filters()

    print(calculator.get_df())

    print(calculator.calculate_statistics())

    champion, champion_points = calculator.get_champion()
    print(f"Le champion est {champion} avec {champion_points}")

    if args.output is not None:
        calculator.get_df().to_csv(args.output)

    if args.show_graph:
        calculator.show_graph()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Ouvre le fichier csv fourni")
    parser.add_argument("-o", "--output", required=False, type=str, help="Sauvegarde le résultat dans un fichier")
    parser.add_argument("-s", "--settings", required=False, type=str, help="Fichiers de paramètres pour la saison")
    parser.add_argument("-g", "--show-graph", required=False, action='store_true', help="Affiche le graphique cumulatif")

    args = parser.parse_args()

    main(args)  # type: ignore