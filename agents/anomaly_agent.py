from tools.anomaly_detection import AnomalyDetectionTool

class AnomalyAgent:
    def __init__(self):
        self.tool = AnomalyDetectionTool()

    def detect(self, recon_data):
        print("\nRunning anomaly detection...")

        financials = recon_data["financials"]
        anomalies = self.tool.detect_anomalies(financials)

        print("Anomalies Detected:")
        for anomaly in anomalies:
            print(f"- {anomaly['anomaly_id']}: {anomaly['title']} [{anomaly['severity']}]")

        recon_data["anomalies"] = anomalies
        return recon_data