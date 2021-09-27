from typing import List, Dict
import csv

class Employee:
    def __init__(self, full_name: str, department: str, division: str, position: str, score, salary):
        self.full_name = full_name
        self.position = position
        self.department = department
        self.division = division
        self.score = float(score)
        self.salary = int(salary)
        
        
class Report:
    def __init__(self, report_file: str):
        self.employees = []
        with open(report_file, 'r', encoding="utf-8") as f:
            f.readline()
            for line in f:
                employee = self._split(line)
                self.employees.append(employee)


    def _split(self, line: str, delimiter: str=";") -> Employee:
        """
            Split line with employee info
        """
        return Employee(*line.split(delimiter))


class SummaryReport:
    def __init__(self, report: Report):
        departments_employees = self._group_by_department(report)
        self.departments = [{"name": name, **self._compute_department_info(employees)}
                                 for name, employees in departments_employees.items()]


    def console_print(self):
        """
            Summary report console print
        """
        print("{: >30}Deportment {: >7}Size {: >10}Fork {: >15}Avg salary".format(*[""]*4))
        for department in self.departments:
            print("{name: >40} {size: >10} {min_salary: >10} - {max_salary} {avg_salary: >20}".format(**department))
    

    def to_csv(self):
        """
            Save to csv file
        """
        with open("summary_report.csv", 'w', newline="") as f:
            writer = csv.writer(f, delimiter =';')
            writer.writerow("Deportment Size Fork Avg salary".split())
            for department in self.departments:
                writer.writerow("{name} {size} {min_salary}-{max_salary} {avg_salary}".format(**department).split())


    def _group_by_department(self, report: Report) -> Dict:
        """ 
            Division into groups by department
        """
        departments = {}
        for employee in report.employees:
            if employee.department in departments.keys():
                departments[employee.department].append(employee)
            else:
                departments[employee.department] = [employee]
        return departments
    

    def _compute_department_info(self, department_employees: List):
        """
            Computation deportment info
        """
        department_salaries = [employee.salary for employee in department_employees]
        min_salary =  min(department_salaries)
        max_salary =  max(department_salaries)
        avg_salary = sum(department_salaries)/len(department_salaries) if department_salaries != [] else 0
        department_size = len(department_employees)
        return {"size": department_size, "min_salary": min_salary, "max_salary": max_salary, "avg_salary": round(avg_salary, 3)}


def main():
    report = Report("Corp_Summary.csv")
    summary_report = SummaryReport(report=report)
    while True:
        action = input("Choose action:\n1 - print deportment\n2 - summary report console print\n3 - save summary report\n")
        
        if action == '1':
            for deportment in summary_report.departments:
                print(deportment.get("name"))
                      
        elif action == '2':
            summary_report.console_print()
            
        elif action == '3':
            summary_report.to_csv()

        else:
            break
        
        
if __name__ == "__main__":
    main()




        
