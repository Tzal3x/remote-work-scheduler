# Remote work scheduler 👨‍💻🏠

Let's say you are working in the human resources department in a company that hybrid remote work is the status quo, and you need to create a weekly schedule for the employees.

The aim is to **define which days of the week each employee has to come in the office**, taking into account a set of constraints (e.g. all members of a team should have the same schedule, in order to meet at the office the same days, each employee should work from home 3 days a week etc).

This is what this script is doing, created as a proof of concept with some artificial constraints and data.

The output can also be exported to a csv file in order to be loaded in your favorite excel-like editor.

# Brief theory

Since all we care for in this problem is whether a solution is feasible or not given our set of constraints, this problem can be classified into the [constraint programming](https://en.wikipedia.org/wiki/Constraint_programming) category. 

Google has a very convenient solver, the [CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver) from the or-tools library for those kinds of problems. 

All that I had to do was to create the correct model in order to feed it to the solver.

## The model 

First step to construct our model, is to define our variables:

- Let `wfh_X_Y` be **1** if _the employee with name X is working from home the day Y_, else 0. 
e.g. `wfh_Alex_friday` == "Alex is working from home on Friday". 

Then we add constraints to the `cp_model.CpModel()` by expressing those constraints in relation to those variables: 

**Constraints**:

1. Each employee should work **n** days from home per week, where `0 < n <= 5`

2. The number of employees in office should not be less than **m**, where `0 < m <= total_number_of_employees`

3. The number of employees in office should not exceed **M**, where `0 < M <= total_number_of_employees`

4. Every employee of the same team should have the same schedule.

5. Other requests or exceptions such as: "Team 1 should be in office on Mondays", "Employee 41 is always working from office" etc.

From that point on, to express those constraints in a language that the model can understand, we write the equations as sums of the variables `wfh_X_Y`.

For example constraint 1 can be expressed as:

```python
for name in employees:
    if not has_special_request(name):
        model.Add(sum(wfh[(name, d)] for d in days) == n)
```

# Installation

> Python **3.8**

Create virtual environment: `python -m virtualenv env`

Activate virtual environment: `source env/bin/activate`

Install dependencies: `pip install -r requirements.txt`

Run program: `python main.py`


# Example 

```bash
##### Employee weekly work schedule #####
 Parameters: 
    Days working from home: 2
    Total number of employees: 67
    Minimum number of employees allowed in office: 35
    Maximum number of employees allowed in office: 46
#############################################
Finding solution ... 
Done!
Solution found!
| Name            | monday                | tuesday               | wednesday             | thursday              | friday                | TEAM    |
|-----------------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+---------|
| employee_y_3    | office                | office                | office                | office                | office                | TEAM_4  |
| employee_y_4    | office                | office                | office                | office                | office                | TEAM_4  |
| employee_10     | office                | office                | home                  | office                | home                  | TEAM_4  |
| employee_11     | office                | office                | office                | home                  | home                  | TEAM_5  |
| employee_12     | office                | office                | office                | home                  | home                  | TEAM_5  |
| employee_y_5    | office                | office                | office                | office                | office                | TEAM_6  |
| employee_13     | office                | office                | home                  | office                | home                  | TEAM_6  |
| employee_14     | office                | office                | home                  | office                | home                  | TEAM_6  |
| employee_x_6    | home                  | home                  | home                  | office                | office                | TEAM_6  |
| employee_y_6    | office                | office                | office                | office                | office                | TEAM_6  |
| employee_15     | office                | office                | home                  | office                | home                  | TEAM_6  |
| employee_16     | office                | office                | home                  | office                | home                  | TEAM_6  |
| employee_17     | office                | office                | home                  | office                | home                  | TEAM_6  |
| employee_x_7    | home                  | home                  | home                  | office                | office                | TEAM_6  |
| employee_18     | office                | office                | home                  | home                  | office                | TEAM_7  |
| employee_19     | office                | office                | home                  | home                  | office                | TEAM_7  |
| employee_x_2    | home                  | office                | home                  | office                | office                | NO_TEAM |
| employee_x_3    | office                | office                | office                | office                | home                  | NO_TEAM |
| employee_47     | office                | office                | home                  | home                  | office                | NO_TEAM |
| employee_x_5    | office                | office                | home                  | office                | home                  | NO_TEAM |
| admin_1         | office                | office                | office                | office                | office                | NO_TEAM |
| admin_2         | office                | office                | office                | office                | office                | NO_TEAM |
| admin_3         | office                | office                | office                | office                | office                | NO_TEAM |
| admin_4         | office                | office                | office                | office                | office                | NO_TEAM |
| admin_5         | office                | office                | office                | office                | office                | NO_TEAM |
| admin_6         | office                | office                | office                | office                | office                | NO_TEAM |
| employee_1      | office                | office                | office                | home                  | home                  | TEAM_1  |
| employee_2      | office                | office                | office                | home                  | home                  | TEAM_1  |
| employee_3      | office                | office                | office                | home                  | home                  | TEAM_1  |
| employee_4      | office                | office                | office                | home                  | home                  | TEAM_1  |
| employee_x_1    | office                | home                  | office                | home                  | office                | TEAM_2  |
| employee_x_8    | home                  | home                  | home                  | home                  | home                  | TEAM_2  |
| employee_5      | office                | office                | home                  | office                | home                  | TEAM_2  |
| employee_6      | office                | office                | home                  | office                | home                  | TEAM_2  |
| employee_7      | office                | office                | home                  | home                  | office                | TEAM_3  |
| employee_8      | office                | office                | home                  | home                  | office                | TEAM_3  |
| employee_9      | office                | office                | home                  | home                  | office                | TEAM_3  |
| employee_20     | office                | office                | home                  | home                  | office                | TEAM_8  |
| employee_21     | office                | office                | home                  | home                  | office                | TEAM_8  |
| employee_22     | office                | office                | office                | home                  | home                  | TEAM_9  |
| employee_23     | office                | office                | office                | home                  | home                  | TEAM_9  |
| employee_37     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_38     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_39     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_40     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_41     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_42     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_43     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_44     | home                  | home                  | office                | office                | office                | TEAM_16 |
| employee_y_1    | office                | office                | office                | office                | office                | TEAM_17 |
| employee_45     | home                  | home                  | office                | office                | office                | TEAM_17 |
| employee_y_2    | office                | office                | office                | office                | office                | TEAM_17 |
| employee_46     | home                  | home                  | office                | office                | office                | TEAM_17 |
| employee_35     | home                  | office                | office                | office                | home                  | TEAM_14 |
| employee_36     | home                  | home                  | office                | office                | office                | TEAM_15 |
| employee_27     | home                  | home                  | office                | office                | office                | TEAM_12 |
| employee_28     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_29     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_30     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_31     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_32     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_33     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_34     | home                  | home                  | office                | office                | office                | TEAM_13 |
| employee_24     | office                | home                  | office                | home                  | office                | TEAM_10 |
| employee_25     | office                | home                  | office                | home                  | office                | TEAM_10 |
| employee_x_4    | office                | office                | office                | office                | home                  | TEAM_10 |
| employee_26     | office                | home                  | office                | home                  | office                | TEAM_11 |
| TOTAL EMPLOYEES | Office: 43 - Home: 24 | Office: 41 - Home: 26 | Office: 46 - Home: 21 | Office: 46 - Home: 21 | Office: 46 - Home: 21 |         |
```

