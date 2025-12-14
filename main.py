import pandas
import argparse
import typing
import json

from calculator import Calculator

class MainArgs(typing.Protocol):
    input: str
    output: str|None
    settings: str|None
    show_wdc_graph: bool
    wcc: bool
    show_wcc_graph: bool

def load_settings_file(file_name:str) -> dict:
    with open(file_name) as file:
        settings = json.load(file)
    
    return settings

def main(args: MainArgs):
    calculator = Calculator(pandas.read_csv(args.input, index_col=0))

    # Chargement du fichier de réglage si argument donné
    if args.settings is not None:
        calculator.set_settings(load_settings_file(args.settings))

    calculator.calculate_drivers()

    print("Points marqués par weekend :")
    print(calculator.get_drivers_df())

    print("Statistiques de la saison :")
    print(calculator.calculate_statistics())

    print("Total de points :")
    print(calculator.get_cumulative_max())

    champion, champion_points = calculator.get_champion()
    print(f"Le champion est {champion} avec {champion_points}")

    if args.wcc:
        calculator.calculate_constructors()
        print("Championnat constructeur")
        print(calculator.get_constructors_df())

        if args.show_wcc_graph:
            calculator.show_constructor_graph()

    if args.output is not None:
        calculator.get_drivers_df().to_csv(args.output)

    if args.show_wdc_graph:
        calculator.show_driver_graph()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Ouvre le fichier csv fourni")
    parser.add_argument("-o", "--output", required=False, type=str, help="Sauvegarde le résultat dans un fichier")
    parser.add_argument("-s", "--settings", required=False, type=str, help="Fichiers de paramètres pour la saison")
    parser.add_argument("-g", "--show-wdc-graph", required=False, action='store_true', help="Affiche le graphique cumulatif")
    parser.add_argument("--wcc", required=False, action='store_true', help="Calcul le championnat constructeur")
    parser.add_argument("--show-wcc-graph", required=False, action='store_true', help="Affiche le graphique cumulatif pour les constructeurs")

    args = parser.parse_args()

    main(args)  # type: ignore