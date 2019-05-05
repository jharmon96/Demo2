global driver, URL, username, password, direction, cost_Structure


# Values that provide information necessary for the script to run

# export templates
settings_file = r"export templates\project_expense_account.csv"
summary_file = r"export templates\cost_structure_summary.csv"
labor_cost_file = r"export templates\labor_cost.csv"
ODC_cost_file = r"export templates\ODC_Costs.csv"
indirect_cost_file = r"export templates\indirect_costs.csv"
indirect_cost_rates_file = r"export templates\indirect_cost_rates.csv"

# DB tables
expense_types_file = r"tables\expense_types.csv"
cost_elements_file = r"tables\cost_elements.csv"

# Login info
URL = "http://sites.unanet.com/demo_jharmon"
username = "fcontroller"
password = "welcome"

# Import / Export
direction = "Export"

cost_structure = "Division A"
cost_structure_key = "1"