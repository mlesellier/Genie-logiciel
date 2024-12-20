class Employee:
    def __init__(self, employee_id, name):
        self.employee_id = employee_id
        self.name = name
        self.leave_balance = {
            "vacances": 20,
            "RTT": 10,
            "conge_maladie": 0,
            "conge_droit": 5
        }
        self.leave_requests = []

    def create_leave_request(self, leave_type, start_date, end_date):
        if leave_type not in self.leave_balance:
            return f"Type de congé invalide: {leave_type}"
        
        leave_request = {
            "employee_id": self.employee_id,
            "name": self.name,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "status": "En attente"
        }
        self.leave_requests.append(leave_request)
        return f"Demande de congé créée avec succès pour {leave_type} du {start_date} au {end_date}."

class Manager:
    def __init__(self, manager_id, name):
        self.manager_id = manager_id
        self.name = name
        self.team_requests = []

    def validate_leave_request(self, leave_request, approve=True):
        if approve:
            leave_request["status"] = "Validé"
            return f"La demande de congé de {leave_request['name']} a été validée."
        else:
            leave_request["status"] = "Rejeté"
            return f"La demande de congé de {leave_request['name']} a été rejetée."

class HR:
    def __init__(self):
        self.all_requests = []

    def generate_report(self):
        report = {}
        for request in self.all_requests:
            leave_type = request["leave_type"]
            report[leave_type] = report.get(leave_type, 0) + 1
        return report

# Exemple d'utilisation
employee = Employee(1, "Alice")
manager = Manager(101, "Bob")
hr = HR()

# Création d'une demande de congé
request_result = employee.create_leave_request("vacances", "2024-12-25", "2024-12-30")
print(request_result)

# Validation par le manager
leave_request = employee.leave_requests[0]
validation_result = manager.validate_leave_request(leave_request, approve=True)
print(validation_result)

# Ajouter la demande à la base RH
hr.all_requests.append(leave_request)

# Génération du rapport RH
report = hr.generate_report()
print("Rapport RH :", report)