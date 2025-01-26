# DevOps Metrics Viewer

A modular Python project to simulate an HTTP server that retrieves and displays key deployment metrics for engineering teams. This project provides hands-on practice with Python classes, decorators, and structured logging using `rich`. It is structured as an iterative learning exercise focused on real-world DevOps challenges.

### Features 🚀
*   Metrics Retrieval: Simulates an HTTP server (MetricsServer) providing key deployment metrics in JSON format.
*   Key Metrics Tracked:
*   Deployment Frequency
*   Change Lead Time
*   Mean Time to Recovery (MTTR)
*   Change Failure Rate
*   Cycle Time
*   Automation Percentage
*   Test Coverage
*   System Uptime & Availability
*   Customer Feedback
*   Team Collaboration & Satisfaction
*   Rich Logging: Outputs clean, color-coded logs for requests and operations using the `rich` library.
*   Phased Development: Built incrementally to encourage structured problem-solving and extensibility.
*   Environment Management: Utilizes Poetry for managing dependencies and project setup.

### Tech Stack 🛠️
*    Python: Core programming language.
*    Flask: For building the HTTP server.
*    Rich: For color-coded logging and better developer experience.
*    Poetry: For dependency management and environment setup.
*    Unit Testing: Using unittest for robust test coverage.

### Installation 🐍

1. Clone the Repository:
    
```bash 
git clone https://github.com/lmcdonough/devops-metrics-viewer.git
cd devops-metrics-viewer
```


2. Set Up the Environment with Poetry:
    
```bash 
# Install Poetry
pip install poetry
    
# Install dependencies
poetry install
```
    

3. Run the Application:

```bash
# Start the Flask server
poetry run python main.py
```


### Usage 🛡️

API Endpoints:

* `GET /metrics`: Retrieve metrics based on the provided endpoint parameter.

Example Request:

```bash
curl "http://127.0.0.1:5000/metrics?endpoint=http://acme.com/ms/deployment-frequency"
```

### Phases of Development:
   1. Phase 1: Emulates an HTTP server to return metrics in JSON format. (Complete)
   2. Phase 2: Implement client for Fetching metrics from Mocked endpoints in `MetricsServer`. (In Progress)
   3. Phase 3: Add timestamps and text-based graphing. 

### Development Workflow 🧑‍💻
   1. Implement a Flask-based server (`MetricsServer`) with modular design.
   2. Add mocked metrics in a JSON file for easy data management.
   3. Use Python decorators to log incoming requests with rich.
   4. Write unit tests for API endpoints to ensure reliability.
   5. Plan for extending functionality with timestamped data and visualizations.

### Future Enhancements 🛠️
*    Extend functionality to include real-time CI/CD metrics via API integration.
*    Add timestamped metrics and trend visualization (Phase 3).
*    Implement more advanced text-based or graphical visualization libraries like matplotlib.

### License 📜

This project is licensed under the MIT License.
