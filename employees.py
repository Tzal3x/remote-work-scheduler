"""
Here are defined the employees of each team,
plus special requests for work from home.
"""


teams = {
    'TEAM_1': [
        'employee_1',
        'employee_2',
        'employee_3',
        'employee_4'
    ],
    'TEAM_2': [
        'employee_x_1',
        'employee_x_8',
        'employee_5',
        'employee_6'
    ],
    'TEAM_3': [
        'employee_7',
        'employee_8',
        'employee_9'
    ],
    'TEAM_4': [
        'employee_y_3',
        'employee_y_4',
        'employee_10'
    ],
    'TEAM_5': [
        'employee_11',
        'employee_12'
    ],
    'TEAM_6': [
        'employee_y_5',
        'employee_13',
        'employee_14',
        'employee_x_6',
        'employee_y_6',
        'employee_15',
        'employee_16',
        'employee_17',
        'employee_x_7'
    ],
    'TEAM_7': [
        'employee_18',
        'employee_19'
    ],
    'TEAM_8': [
        'employee_20',
        'employee_21'
    ],
    'TEAM_9': [
        'employee_22',
        'employee_23'
    ],
    'TEAM_10': [
        'employee_24',
        'employee_25',
        'employee_x_4'
    ],
    'TEAM_11': [
        'employee_26'
    ],
    'TEAM_12': [
        'employee_27'
    ],
    'TEAM_13': [
        'employee_28',
        'employee_29',
        'employee_30',
        'employee_31',
        'employee_32',
        'employee_33',
        'employee_34'
    ],
    'TEAM_14': [
        'employee_35'
    ],
    'TEAM_15': [
        'employee_36'
    ],
    'TEAM_16': [
        'employee_37',
        'employee_38',
        'employee_39',
        'employee_40',
        'employee_41',
        'employee_42',
        'employee_43',
        'employee_44'
    ],
    'TEAM_17': [
        'employee_y_1',
        'employee_45',
        'employee_y_2',
        'employee_46'
    ],
    'NO_TEAM': [
        'employee_x_2',
        'employee_x_3',
        'employee_47',
        'employee_x_5',
        'admin_1',
        'admin_2',
        'admin_3',
        'admin_4',
        'admin_5',
        'admin_6'
    ]
}

special_requests_for_wfh = {
    'employee_x_1': [
        'tuesday',
        'thursday'
    ],
    'employee_x_2': [
        'monday',
        'wednesday'
    ],
    'employee_x_3': [
        'friday'
    ],
    'employee_x_4': [
        'friday'
    ],
    'employee_x_5': [
        'wednesday',
        'friday'
    ],
    'employee_x_6': [
        'monday',
        'tuesday',
        'wednesday'
    ],
    'employee_x_7': [
        'monday',
        'tuesday',
        'wednesday'
    ],
    'employee_x_8': [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday'
    ],

    # --- Never wfh ---
    # - Developers
    'employee_y_1': [],
    'employee_y_2': [],
    'employee_y_3': [],
    'employee_y_4': [],
    'employee_y_5': [],
    'employee_y_6': [],

    # - Admins
    'admin_1': [],
    'admin_2': [],
    'admin_3': [],
    'admin_4': [],
    'admin_5': [],
    'admin_6': [],
}

name_to_team_dict = {name: team for team in teams for name in teams[team]}
employees = [name for team in teams for name in teams[team]]
