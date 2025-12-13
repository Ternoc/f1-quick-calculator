import pandas
import matplotlib.pyplot
import argparse
import typing
import re

# Barèmes
POINT_SCALE = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
SPRINT_POINT_SCALE = [3, 2, 1]

# Points bonus
# Format :
# {"BONUS":(points bonus, position maximale)}
# points bonus : Points attribués par le bonus
# position maximale : Position au delà delaquelle le point bonus n'est pas attribué. -1 pour désactiver
BONUS = {"FL":(1, 10)}

# Patterns pour les regex
RACE_REGEX = re.compile(r"^(\d{1,2})$")
SPRINT_REGEX = re.compile(r"^S(\d{1,2})$")

class MainArgs(typing.Protocol):
    input: str
    output: str|None
    show_graph: bool

def apply_scale(race_position:int, scale:list[int]) -> int:
    """Fonction pour convertir une position en points selon le barème passé en paramètre"""
    return scale[race_position-1] if race_position <= len(scale) else 0

def filter_function(cell):
    """Fonction pour convertir une cellule avec les points correspondants"""
    cell = str(cell)
    cell_elements = cell.split("+") # Découpe la cellule en élements séparés par un +

    point_result = 0
    race_position = 0
    sprint_position = 0
    
    for element in cell_elements:
        # Regex pour les résultats en course (format 11)
        regex_match = re.match(RACE_REGEX, element)
        if regex_match:
            race_position = int(regex_match[1])
            race_point = apply_scale(race_position, POINT_SCALE)
            point_result += race_point

        # Regex pour les résultats en sprint (format S12)
        regex_match = re.match(SPRINT_REGEX, element)
        if regex_match:
            sprint_position = int(regex_match[1])
            sprint_point = apply_scale(sprint_position, SPRINT_POINT_SCALE)
            point_result += sprint_point

        # Points bonus tels que définis dans le dictionnaire
        if element in BONUS:
            point_result += BONUS[element][0] if race_position <= BONUS[element][1] or BONUS[element][1] == -1 else 0
    
    return point_result

def show_graph(df:pandas.DataFrame):
    df.cumsum().plot()
    matplotlib.pyplot.show()

def main(args: MainArgs):
    input = pandas.read_csv(args.input, index_col=0)

    output = input.map(filter_function)
    print(output)
    print(output.sum())

    if args.output is not None:
        output.to_csv(args.output)

    if args.show_graph:
        show_graph(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", type=str, help="Ouvre le fichier csv fourni")
    parser.add_argument("-o", "--output", required=False, type=str, help="Sauvegarde le résultat dans un fichier")
    parser.add_argument("-g", "--show-graph", required=False, action='store_true', help="Affiche le graphique cumulatif")

    args = parser.parse_args()

    main(args)  # type: ignore