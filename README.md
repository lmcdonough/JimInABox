
# DevOps Metrics Viewer

A CLI application to retrieve and display key deployment metrics for engineering teams, emulating an HTTP server and enabling tracking of critical DevOps KPIs. This project is a simulation of real-world DevOps challenges and is structured as an iterative learning exercise.

## Features 🚀

- **Metrics Retrieval**: Simulate an HTTP server providing key deployment metrics.
- **Key Metrics Tracked**:
  - Deployment Frequency
  - Change Lead Time
  - Mean Time to Recovery (MTTR)
  - Change Failure Rate
  - Cycle Time
  - Automation Percentage
  - Test Coverage
  - System Uptime & Availability
  - Customer Feedback
  - Team Collaboration & Satisfaction
- **Graphical Visualization**: Display trends of metrics over 5, 10, and 30-minute windows using a text-based plotting library.
- **Phased Approach**: Built in iterative steps to promote structured problem-solving.

## Tech Stack 🛠️

- **Python**: Core programming language.
- **Flask**: For simulating the HTTP server.
- **Gunicorn/uWSGI**: WSGI server to handle requests.
- **tplot**: Library for text-based graphical visualization.
- **Docker**: For containerized deployment.

## Installation 🐍

1. **Clone the Repository**:

   git clone [https://github.com/lmcdonough/devops-metrics-viewer.git](https://github.com/lmcdonough/devops-metrics-viewer.git)
   cd devops-metrics-viewer

2. **Set Up Virtual Environment**:

   python3 -m venv venv
   source venv/bin/activate

3. **Install Dependencies**:

   pip install -r requirements.txt

4. **Run the Application**:

   python app.py

## Usage 🛡️

- **Phase 1**: Emulates an HTTP server using `MetricsServer` to return metrics in JSON format. (*Completed*)
- **Phase 2**: Fetches and displays individual metrics using mocked endpoints. (*In Progress*)
- **Phase 3**: Enhances `MetricsServer` to provide timestamps and graphing capabilities. (*TODO*)

Example Command:
```bash
python metrics_client.py --metric deployment-frequency --window 10
```

## Sample Output 📊

Metric: Deployment Frequency
Window: Last 10 minutes

```bash
Graph:
+--------------------+
|   *   **  *  *   *|
+--------------------+
```

## Development Workflow 🧑‍💻

1. Implement HTTP server (`Phase 1`). (_Completed_)
2. Mock CI metrics (`Phase 2`). (*In Progress*)
3. Add timestamped metrics and graph visualization (`Phase 3`). (*TODO*)

## Future Enhancements 🛠️

- Write comprehensive tests for `MetricsServer`.
- Add support for real CI/CD API integration.
- Improve visualization using libraries like `matplotlib`.

## License 📜

This project is licensed under the MIT License.

---

![License](https://img.shields.io/badge/license-MIT-blue)
