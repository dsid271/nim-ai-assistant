from prometheus_client import start_http_server, Summary, Counter, Gauge
import time

# Create metrics
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUESTS_TOTAL = Counter('requests_total', 'Total number of requests processed')
MODEL_LATENCY = Gauge('model_latency_seconds', 'Latency of model inference')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')

class MonitoringSystem:
    def __init__(self, port=8000):
        self.port = port

    def start(self):
        start_http_server(self.port)
        print(f"Prometheus metrics server started on port {self.port}")

    @REQUEST_TIME.time()
    def process_request(self, request):
        REQUESTS_TOTAL.inc()
        # Process the request here
        time.sleep(0.1)  # Simulate processing time
        return "Response"

    def update_model_latency(self, latency):
        MODEL_LATENCY.set(latency)

    def update_active_users(self, count):
        ACTIVE_USERS.set(count)

# Usage
monitoring = MonitoringSystem()
monitoring.start()
