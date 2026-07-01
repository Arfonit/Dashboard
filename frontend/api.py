import requests
from uuid import UUID
from backend.config import settings


base_url = settings.API_URL

class APIClient:

    def __init__(self, base_url: str):
        self.base = base_url
        
    def get_all_companies(self):
        return requests.get(f"{self.base}/get_all_companies").json()
        
    def get_unpaid_projects(self):
        return requests.get( f"{self.base}/get_unpaid_projects").json()

    def get_project(self, project_id):
        resp = requests.get(f"{self.base}/project/{project_id}")
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            return data[0]

        return data
    
    def get_all_project_types(self):
        return requests.get(f"{self.base}/get_all_project_types").json()
        
    def get_project_types(self):
        return requests.get(f"{self.base}/project_types").json()
        
    def get_dashboard_main(self):
        return requests.get(f"{self.base}/dashboard_main").json()

    def get_income_by_year(self): 
        resp = requests.get(f"{self.base}/get_income_by_year")
        print (resp.status_code)
        print(resp.text)
        resp.raise_for_status()
        
        return resp.json()

    def get_income_by_month(self, year):
        resp = requests.get(f"{self.base}/get_income_by_month/{year}")
        print (resp.status_code)
        print(resp.text)
        resp.raise_for_status()
        
        return resp.json()

    def update_start_project_date(self, project_id: UUID, project_date):            
        requests.post(f"{self.base}/post_start_project_date/{project_id}", json={"unique_project_key": project_id,"project_date": project_date.isoformat()})
            
    def update_company_name(self, project_id: UUID, company):
        requests.post(f"{self.base}/post_company_name/{project_id}", json={"unique_project_key": project_id,"company_name": company})
                    
    def update_project_type(self, project_id: UUID, ptype):
        requests.post(f"{self.base}/post_project_type/{project_id}", json={"unique_project_key": project_id,"project_type": ptype})
            
    def update_comment(self, project_id: UUID, comment):
        requests.post(f"{self.base}/post_comment/{project_id}", json={"unique_project_key": project_id, "comment": comment})       

    def update_fact_payment(self, project_id: UUID, payment):
        requests.post(f"{self.base}/post_fact_payment/{project_id}", json={"unique_project_key": project_id, "fact_payment": payment})
            
    def update_project_budget(self, project_id: UUID, budget):
        requests.post(f"{self.base}/post_payment_fixed/{project_id}", json={"unique_project_key": project_id, "project_budjet": budget})
            
    def update_extra_work(self, project_id: UUID, hour_price,hours):
        requests.post(f"{self.base}/post_payment_hourly/{project_id}", json={"unique_project_key": project_id, "extra_work_price": hour_price, "extra_work_hours": hours})
        
    def update_all_project(self, project_id: UUID, form, change_type: str):
        requests.post(f"{self.base}/post_project_update/{project_id}",params={"change_type": change_type}, 
                                                                    json = {"project_date": form["project_date"].isoformat(),
                                                                            "company_name": form["company_name"],
                                                                            "project_type": form["project_type"],
                                                                            "comment": form["comment"],
                                                                            "project_budjet": form["project_budjet"],
                                                                            "extra_work_price": form["extra_work_price"],
                                                                            "extra_work_hours": form["extra_work_hours"],
                                                                            "fact_payment": form["fact_payment"]})

        
    
    
api = APIClient(base_url)