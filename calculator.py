import pandas
import matplotlib.pyplot
import re

RACE_REGEX = re.compile(r"^(\d{1,2})$")
SPRINT_REGEX = re.compile(r"^S(\d{1,2})$")

class Calculator:
    def __init__(self, input:pandas.DataFrame) -> None:
        """Initialise le calculateur avec le dataframe"""
        self.df:pandas.DataFrame = input
        self.settings:dict = {
            "point_scale":[25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
            "sptint_point_scale":[3, 2, 1],
            "bonus":{"FL":(1, 10)}
        }

    def filter_df(self) -> None:
        """Applique la fonction de filtration au dataframe"""
        self.df = self.df.map(self.filter_function)
    
    def show_graph(self):
        """Affiche le graphique cumulatif"""
        self.df.cumsum().plot()
        matplotlib.pyplot.show()
    
    def get_df(self) -> pandas.DataFrame:
        """Renvoie le dataframe"""
        return self.df
    
    def filter_function(self, cell):
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
                race_point = Calculator.apply_scale(race_position, self.settings["point_scale"])
                point_result += race_point

            # Regex pour les résultats en sprint (format S12)
            regex_match = re.match(SPRINT_REGEX, element)
            if regex_match:
                sprint_position = int(regex_match[1])
                sprint_point = Calculator.apply_scale(sprint_position, self.settings["sptint_point_scale"])
                point_result += sprint_point

            # Points bonus tels que définis dans le dictionnaire
            if element in self.settings["bonus"]:
                point_result += self.settings["bonus"][element][0] if race_position <= self.settings["bonus"][element][1] or self.settings["bonus"][element][1] == -1 else 0
        
        return point_result
    
    @staticmethod
    def apply_scale(race_position:int, scale:list[int]) -> int:
        """Fonction pour convertir une position en points selon le barème passé en paramètre"""
        return scale[race_position-1] if race_position <= len(scale) else 0