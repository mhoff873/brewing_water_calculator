import itertools
import numpy as np
from tabulate import tabulate
import time

class BrewAdjustment:
    def __init__(self, volume):
        self.volume = volume * 3.78541  # Convert volume from gallons to liters

        # Initial values for common ions in ppm
        self.initial_values = {
            "calcium": 0.1,
            "sulfate": 3,
            "chloride": 30,
            "sodium": 5,
            "magnesium": 0.1,
            "bicarbonate": 50
        }

        #Target Water Profile Ranges
        # add ion targets in the following format:
        # np.linespace(lower_bound, upper_bound, slices)
        # slicing the range more can increase the precision but also increases the search time.

        # Oktoberfest
        self.target_ranges = {
            "calcium": np.linspace(50, 75, 2),
            "sulfate": np.linspace(50, 80, 2),
            "chloride": np.linspace(50, 100, 2),
            "sodium": np.linspace(10, 20, 2),
            "magnesium": np.linspace(5, 10, 2),
            "bicarbonate": np.linspace(50, 150, 2)
        }

        # Blonde ale
        """self.target_ranges = {
            "calcium": np.linspace(60, 65, 2),
            "sulfate": np.linspace(60, 75, 2),
            "chloride": np.linspace(60, 75, 2),
            "sodium": np.linspace(10, 20, 2),
            "magnesium": np.linspace(5, 10, 2),
            "bicarbonate": np.linspace(50, 100, 2)
        }"""

        # Weight of ions contributed by each chemical per gram in ppm
        self.ion_weights = {
            "baking_soda": {"sodium": 273, "bicarbonate": 191},
            "gypsum": {"calcium": 232, "sulfate": 556},
            "calcium_chloride": {"calcium": 272, "chloride": 482},
            "epsom_salt": {"magnesium": 98, "sulfate": 388},
            "chalk": {"calcium": 1056, "bicarbonate": 1584}
        }

        # Desired chloride to sulfate ratio
        self.ratio = 1

    def adjust_water(self):
        best_diff = float('inf')
        best_order = None
        best_adjustments = None
        best_updated_values = None
        best_goals = None
        ratio_weight = 100  # Adjust this value to give more or less weight to the ratio
        dash = "\n" + ("*" * 75)
        num_checked = 0

        start_time = time.time()  # Record the start time

        # Try all possible orders of adding the chemicals
        for order in itertools.permutations(self.ion_weights.keys()):
            for goal_values in itertools.product(*self.target_ranges.values()):
                goal_values = dict(zip(self.target_ranges.keys(), goal_values))
                adjustment_weights = {}
                updated_values = self.initial_values.copy()

                for chem in order:
                    ions = self.ion_weights[chem]
                    adjustment = 0

                    for ion, weight in ions.items():
                        num_checked += 1
                        if goal_values[ion] > updated_values[ion]:
                            ion_diff = goal_values[ion] - updated_values[ion]
                            adjustment = ion_diff / weight * self.volume

                            # Update other ions based on this adjustment
                            for ion_adj, weight_adj in ions.items():
                                updated_values[ion_adj] += adjustment * weight_adj / self.volume

                            # Break after adjusting for one ion as the same compound can't be added twice
                            break  

                    adjustment_weights[chem] = round(adjustment, 2)

                # Calculate the total difference from the goal values and the chloride to sulfate ratio
                total_diff = 0
                for ion, value in updated_values.items():
                    total_diff += abs(value - goal_values[ion])
                total_diff += abs((updated_values['chloride'] / updated_values['sulfate']) - self.ratio) * ratio_weight

                # Update the best order if this order is better
                if total_diff < best_diff:
                    best_diff = total_diff
                    best_order = order
                    best_adjustments = adjustment_weights
                    best_updated_values = updated_values
                    best_goals = goal_values

        print(dash)
        
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time

        print(f"Checked {num_checked} possible solutions in {execution_time} seconds!\n")

        print("The optimal adjustments for " + str(self.volume / 3.78541) + " gallons:")
        for chem, adjustment in best_adjustments.items():
            if adjustment != 0:  # Only print non-zero adjustments
                print(f"  {chem}: {adjustment} grams")

        # Prepare table data
        table_data = [
            ['Initial'] + list(self.initial_values.values()),
            ['Target'] + list(best_goals.values()),
            ['Final'] + list(best_updated_values.values()),
        ]
        print("")
        # Print table
        print(tabulate(table_data, headers=[""] + list(self.initial_values.keys())))

        print(dash)

        return best_adjustments


if __name__ == "__main__":
    # volume of water in gallons, converted to liters in the constructor
    volume = 5

    brew = BrewAdjustment(volume)
    brew.adjust_water()