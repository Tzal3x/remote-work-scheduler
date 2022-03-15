# coding=utf-8
"""
Solver for the employee job scheduling problem.
"""
from ortools.sat.python import cp_model
from employees import (
    employees,
    teams,
    name_to_team_dict,
    special_requests_for_wfh,
)
from tabulate import tabulate
from datetime import datetime


"""--- Define parameters ----"""
num_days_wfh = 2
min_employees_in_office = 35
max_employees_in_office = 46
"""--------------------------"""


def main():
    """
    This is the main function
    """

    num_employees = len(employees)
    min_employees_home = num_employees - max_employees_in_office
    max_employees_home = num_employees - min_employees_in_office
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    print("##### Employee weekly work schedule #####")
    print(" Parameters: ")
    print("    Days working from home: %i" % num_days_wfh)
    print("    Total number of employees: %i" % num_employees)
    print("    Minimum number of employees allowed in office: %i" % min_employees_in_office)
    print("    Maximum number of employees allowed in office: %i" % max_employees_in_office)
    print("[#############################################")

    """Create the model"""
    model = cp_model.CpModel()

    """ 
    Create the variables:
    Explanation - wfh[(e, d)] equals 1 if an employee 'e', on day 'd' is working from home.
    """
    wfh = {}
    for name in employees:
        for day in days:
            wfh[(name, day)] = model.NewBoolVar('wfh_%s_d%s' % (name, day))

    """Create constraints"""
    # Each employee works X days from home.
    for name in employees:
        if not has_special_request(name):
            model.Add(sum(wfh[(name, d)] for d in days) == num_days_wfh)

    """
    We must have X people in the office at all times.
    Therefore Y (= total number of employees - X) wfh each day.
    """
    for day in days:
        model.Add(sum(wfh[(name, day)] for name in employees) >= min_employees_home)
    for day in days:
        model.Add(sum(wfh[(name, day)] for name in employees) <= max_employees_home)

    # Employees that are on the same team, should be working from home on the same days
    for team in teams:
        members = [member for member in teams[team] if not has_special_request(member)]
        for day in days:
            for i in range(len(members)-1):
                model.Add(wfh[(members[i], day)] == wfh[(members[i+1], day)])

    """Special Requests per person:"""
    for employee, requested_days in special_requests_for_wfh.items():
        for day in days:
            if day in requested_days:
                model.Add(wfh[(employee, day)] == 1)
            else:
                model.Add(wfh[(employee, day)] == 0)

    """Special Requests per team:"""
    # TEAM_5 must work 2 days in a row from office
    for employee in teams['TEAM_5']:
        if not has_special_request(employee):
            for day in ['monday', 'tuesday']:
                model.Add(wfh[(employee, day)] == 0)

    """Update solver parameters"""
    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    solver.parameters.enumerate_all_solutions = True

    """
    Maximize the total number of employees in the office <=>
    <=> Minimize the number of employees working from home.
    """
    model.Minimize(sum(wfh[(name, d)] for name in employees for d in days))

    print("Finding solution ... ")
    solver.parameters.max_time_in_seconds = 2
    solver.Solve(model)
    print("Done!")

    if 'INFEASIBLE' in solver.ResponseStats():
        print('[!] No feasible solution exists!')
        print(solver.ResponseStats())
        print('Terminating program.')
        return
    else:
        print('Solution found!')

    """ Display the solution """
    schedule = []
    for name in employees:
        row = [name]
        for day in days:
            res = solver.Value(wfh[(name, day)])
            if res:
                row.append("home")
            else:
                row.append("office")
        row.append(name_to_team_dict[name])
        schedule.append(row)

    # Calculate totals per day:
    employees_per_day = []
    headers = ['Name'] + days + ["TEAM"]
    for day in days:
        count_employees_wfh = 0
        count_employees_office = 0
        for name in employees:
            res = solver.Value(wfh[(name, day)])
            if res:
                count_employees_wfh += 1
            else:
                count_employees_office += 1
        employees_per_day.append("Office: %i - Home: %i" % (count_employees_office, count_employees_wfh))
    schedule.append(["TOTAL EMPLOYEES"] + employees_per_day)
    export_to_csv(schedule, headers)

    print(
        tabulate(schedule,
                 headers=headers,
                 tablefmt='orgtbl')
    )


def export_to_csv(schedule, headers):
    current_date = datetime.today().strftime('%Y-%m-%d-%H:%M')
    filename = 'employee_schedule_{}_wfh_{}_m{}_M{}.csv'.format(
        current_date,
        num_days_wfh,
        min_employees_in_office,
        max_employees_in_office
    )
    with open(filename, 'w') as f:
        lines = [','.join(row) for row in schedule]
        f.writelines(','.join([header for header in headers]))
        f.writelines('\n')
        for line in lines:
            f.writelines(line)
            f.writelines('\n')


def has_special_request(name):
    """
    If an employee has a special request, the rest of the constraints
    should not affect him/her.
    """
    return name in special_requests_for_wfh


if __name__ == '__main__':
    main()
