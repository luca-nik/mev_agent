import sys
import os
import json
from matplotlib import pyplot as plt

# Add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import mev_project_interface as interface

# Json file containing the liquidities of the pools at the time I executed the code
json_file = 'my_data.json'
    
# Maximize the surplus with the new json file
interface.main(json_file, plot_strategy=True)


