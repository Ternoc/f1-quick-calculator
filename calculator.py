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
            "sprint_point_scale":[3, 2, 1],
            "bonus":{"FL":(1, 10)}
        }

    def apply_filters(self) -> None:
        """Applique la fonction de filtration au dataframe"""
        # Modificateurs de barèmes pour certaines courses
        scales = self.settings["modified_scales"] if "modified_scales" in self.settings else {}

        # On itère chaque ligne du dataframe 
        for index, row in self.df.iterrows():
            index = str(index) # Index de la ligne
            
            # Si la course (index de la ligne) est dans les modificateurs de barème sinon pas de modification
            scale = scales[index] if index in scales else 1

            # On applique la fonction de filtrage sur chaque cellule
            self.df.loc[index] = row.apply(self.filter_cell, args=(scale,))

    def show_graph(self):
        """Affiche le graphique cumulatif"""
        self.df.cumsum().plot()
        matplotlib.pyplot.show()
    
    def get_df(self) -> pandas.DataFrame:
        """Renvoie le dataframe"""
        return self.df
    
    def set_settings(self, settings:dict) -> None:
        """Modifie les settings"""
        del self.settings
        self.settings = settings

    def filter_cell(self, cell, race_scale):
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
                point_result += race_point*race_scale

            # Regex pour les résultats en sprint (format S12)
            regex_match = re.match(SPRINT_REGEX, element)
            if regex_match:
                sprint_position = int(regex_match[1])
                sprint_point = Calculator.apply_scale(sprint_position, self.settings["sprint_point_scale"])
                point_result += sprint_point

            # Points bonus tels que définis dans le dictionnaire
            if element in self.settings["bonus"]:
                point_result += self.settings["bonus"][element][0] if race_position <= self.settings["bonus"][element][1] or self.settings["bonus"][element][1] == -1 else 0
        
        return point_result
    
    @staticmethod
    def apply_scale(race_position:int, scale:list[int]) -> int:
        """Fonction pour convertir une position en points selon le barème passé en paramètre"""
        return scale[race_position-1] if race_position <= len(scale) else 0