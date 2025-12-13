import pandas
import argparse
import typing

from calculator import Calculator

class MainArgs(typing.Protocol):
    input: str
    output: str|None
    show_graph: bool

def main(args: MainArgs):
    caclulator = Calculator(pandas.read_csv(args.input, index_col=0))

    caclulator.filter_df()

    print(f"Le champion est {caclulator.get_df().sum().idxmax()} avec {caclulator.get_df().sum().max()}")

    if args.output is not None:
        caclulator.get_df().to_csv(args.output)

    if args.show_graph:
        caclulator.show_graph()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Ouvre le fichier csv fourni")
    parser.add_argument("-o", "--output", required=False, type=str, help="Sauvegarde le résultat dans un fichier")
    parser.add_argument("-g", "--show-graph", required=False, action='store_true', help="Affiche le graphique cumulatif")

    args = parser.parse_args()

    main(args)  # type: ignore