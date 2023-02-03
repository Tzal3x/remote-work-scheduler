# coding=utf-8
"""
Solver for the employee job scheduling problem.
"""
import argparse
from ortools.sat.python import cp_model
from employees import (
    employees,
    teams,
    name_to_team_dict,
    special_requests_for_wfh,
)
from tabulate import tabulate
from datetime import datetime
from halo import Halo


def main(args):
    """
    This is the main function
    """
    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

    info = GeneralInfoStruct(args=args, total_employees=len(employees))
    print(info)

    """Create the model"""
    model = cp_model.CpModel()

    """ 
    Create the variables:
    Explanation - wfh[(e, d)] equals 1 if an employee 'e', on day 'd' is working from home.
    """
    wfh = {}
    for name in employees:
        for day in DAYS:
            wfh[(name, day)] = model.NewBoolVar('wfh_%s_d%s' % (name, day))

    """Create constraints"""
    # Each employee works X days from home.
    for name in employees:
        if not has_special_request(name):
            model.Add(sum(wfh[(name, d)] for d in DAYS) == info.num_days_wfh)

    """
    We must have X people in the office at all times.
    Therefore Y (= total number of employees - X) wfh each day.
    """
    for day in DAYS:
        model.Add(sum(wfh[(name, day)] for name in employees) >= info.min_employees_home)
    for day in DAYS:
        model.Add(sum(wfh[(name, day)] for name in employees) <= info.max_employees_home)

    # Employees that are on the same team, should be working from home on the same days
    for team in teams:
        members = [member for member in teams[team] if not has_special_request(member)]
        for day in DAYS:
            for i in range(len(members)-1):
                model.Add(wfh[(members[i], day)] == wfh[(members[i+1], day)])

    """Special Requests per person:"""
    for employee, requested_days in special_requests_for_wfh.items():
        for day in DAYS:
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
    model.Minimize(sum(wfh[(name, d)] for name in employees for d in DAYS))

    solver.parameters.max_time_in_seconds = 2
    spinner = Halo(text="Finding solution ... ", spinner='dots')
    spinner.start()
    solver.Solve(model)
    spinner.stop()

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
        for day in DAYS:
            res = solver.Value(wfh[(name, day)])
            if res:
                row.append("home")
            else:
                row.append("office")
        row.append(name_to_team_dict[name])
        schedule.append(row)

    # Calculate totals per day:
    employees_per_day = []
    headers = ['Name'] + DAYS + ["TEAM"]
    for day in DAYS:
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

    if args.print:
        print(
            tabulate(schedule,
                    headers=headers,
                    tablefmt='orgtbl')
        )


class GeneralInfoStruct:
    def __init__(
        self,
        args,
        total_employees
    ) -> None:
        self.num_days_wfh = args.num_days_wfh
        self.min_employees_in_office = args.min_employees_in_office 
        self.max_employees_in_office = args.max_employees_in_office 
        self.num_employees = total_employees
        self.min_employees_home = self.num_employees - args.max_employees_in_office
        self.max_employees_home = self.num_employees - args.min_employees_in_office

    def __repr__(self) -> str:
        return f""">> Employee Weekly Work Scheduler <<\nParameters:
    🏠 Days working from home per week: {self.num_days_wfh}
    🧑‍💻 Total number of employees: {self.num_employees}
    📉 Minimum number of employees allowed in office: {self.min_employees_in_office}
    📈 Maximum number of employees allowed in office: {self.max_employees_in_office}
    """


def export_to_csv(schedule, headers):
    current_date = datetime.today().strftime('%Y-%m-%d-%H:%M')
    filename = 'employee_schedule_{}.csv'.format(
        current_date
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


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--num_days_wfh',
        help='Number of days working from home',
        default=2,
        type=int)

    parser.add_argument(
        '--min_employees_in_office',
        help='Minimum number of employees in office',
        default=35)

    parser.add_argument(
        '--max_employees_in_office', 
        help='Maximum number of employees in office',
        default=46)

    parser.add_argument(
        '-p',
        '--print', 
        help='Print output to terminal',
        action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
