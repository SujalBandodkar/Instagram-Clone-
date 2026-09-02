from locust import HttpUser, task, between

class FlaskUser(HttpUser):
    host = "http://localhost:30007"


    @task
    def health(self):
        self.client.get("/health")
