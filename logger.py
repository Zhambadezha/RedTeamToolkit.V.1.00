import json
from datetime import datetime

class Logger:
    def save(self, results, output_file):
        results_with_timestamp = {
            "results": results,
            "timestamp": str(datetime.now())
        }
        with open(output_file, 'w') as f:
            json.dump(results_with_timestamp, f, indent=2)
