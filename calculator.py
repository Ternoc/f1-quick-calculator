import pandas
import matplotlib.pyplot
import re

RACE_REGEX = re.compile(r"^(\d{1,2})$")
SPRINT_REGEX = re.compile(r"^S(\d{1,2})$")

class Calculator:
    def __init__(self, input:pandas.DataFrame) -> None:
        """Initialise le calculateur avec le dataframe"""
        self.input:pandas.DataFrame = input.copy()
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
        self.settings = self.settings | settings

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
                point_result += self.settings["bonus"][element][0] if 0 < race_position <= self.settings["bonus"][element][1] or self.settings["bonus"][element][1] == -1 else 0
        
        return point_result
    
    def calculate_statistics(self):
        """Calcul les statistiques pour chaque pilotes"""
        positions = list(range(1, len(self.settings["point_scale"]))) + ["FL", "DNF", "DNS", "DSQ", "DNQ", "DNPQ"] # Position sur lesquels on calcul les statistiques
        data = {}

        # On itère chaque colomne
        for driver in self.df.columns:
            # Initialisation du dictionnaire pour chaque pilote
            data[driver] = {}
            for position in positions:
                data[driver][str(position)] = 0

            # On itère chaque ligne
            for results in self.input[driver]:
                # On itère chaque résultat (séparés par +)
                results = str(results).split("+")
                for result in results:
                    # Si un résultat correspond à une des statistiques on incrémente
                    if result in data[driver]:
                        data[driver][result] += 1

        return pandas.DataFrame(data)

    def get_cumulative_max(self) -> pandas.Series:
        return self.df.sum()
    
    def get_champion(self) -> tuple[str, float|int]:
        """Renvoie un tuple (champion, points)"""
        sum = self.get_cumulative_max() # pandas series avec les points cumulés pour chaque pilote
        max = sum.max() # Points maximums marqués

        driver_at_max = [] # Pilotes qui ont marqués le maximum de points

        for index, item in sum.items():
            if item == max:
                driver_at_max.append(index)

        # S'il n'y a qu'un pilote avec le nombre max de points, il est champion
        if len(driver_at_max) == 1:
            return (driver_at_max[0], max)
        
        # Sinon on doit départager au maximum de victoire, puis de 2nde place etc...
        drivers_stats = self.calculate_statistics()
        
        # On itère chaque ligne (soit la place) du df de statistiques
        for index, row in drivers_stats.iterrows():
            row_max = row.max() # Maximum du nombre de place
            driver_at_row_max = [] # Pilotes qui ont le nombre max pour cette place

            # On itère sur chaques pilotes que l'on départage
            for driver in driver_at_max:
                # Si le pilote a le nombre max de pilote on l'ajoute à la liste
                if row[driver] == row_max:
                    driver_at_row_max.append(driver)

            # S'il n'y a qu'un pilote qui a ce nombre de place c'est bon le départage est fait
            if len(driver_at_row_max) == 1:
                return (driver_at_row_max[0], max)
        
        # Si on a pas réussi à départager
        return("", 0)

    @staticmethod
    def apply_scale(race_position:int, scale:list[int]) -> int:
        """Fonction pour convertir une position en points selon le barème passé en paramètre"""
        return scale[race_position-1] if race_position <= len(scale) else 0