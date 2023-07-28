# BrewAdjustment

This is a Python script for brewing adjustment. It provides solutions for water chemistry problems and helps adjust the water profile for brewing to better match beer styles. It's based on the following concepts:

- Different styles of beer require different water profiles. For example, an Oktoberfest style beer has different ion concentration requirements compared to a Blonde ale.
- The ratio of chloride to sulfate has a significant effect on the perception of beer. High chloride to sulfate ratios make the beer sweeter while high sulfate to chloride ratios make the beer more bitter.
- Chemicals like baking soda, gypsum, calcium chloride, epsom salt, and chalk can be added to water to adjust the ion concentrations.

## How it works

The script generates possible combinations of chemical additions (adjustments) and target ion concentrations within the defined ranges. It then evaluates each combination and selects the optimal one based on the following criteria:

- The total absolute difference between the ion concentrations after the adjustment and the target ion concentrations.
- The difference between the chloride to sulfate ratio after the adjustment and the desired ratio.

Each of these criteria are given a weight when calculating the total difference for a combination. The combination with the smallest total difference is selected as the optimal solution. The ratio difference is multiplied by a weight to increase its significance in the evaluation. Adjusting the weight can give more or less importance to achieving the desired ratio.

## Usage

To use this script, instantiate the `BrewAdjustment` class with the volume of water in gallons and call the `adjust_water()` method:

```python
volume = 5  # volume of water in gallons
brew = BrewAdjustment(volume)
brew.adjust_water()

This will output the optimal adjustments for the water and a comparison between the initial, target, and final ion concentrations.

## Customization

You can adjust the following parameters to customize the script to your needs:

- initial_values: This is a dictionary containing the initial concentrations of the ions in ppm.
- target_ranges: This is a dictionary containing the target ranges for the ion concentrations. The ranges are sliced using numpy's linspace function, which increases or decreases the search precision and time.
- ion_weights: This is a dictionary containing the ion contributions of each chemical per gram in ppm.
- ratio: This is the desired chloride to sulfate ratio.