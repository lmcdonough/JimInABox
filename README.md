# **DevOps Metrics Viewer**

A modular Python project that simulates an HTTP server for retrieving and displaying key deployment metrics for engineering teams. This project provides hands-on experience with Python classes, decorators, structured logging using `rich`, and API development with `Flask`. It is structured as an iterative learning exercise focused on real-world DevOps challenges.

## **Features 🚀**

* **Metrics Retrieval:** A Flask-based HTTP server (`MetricsServer`) provides key deployment metrics in JSON format.
* **Key Metrics Tracked:**
  * Deployment Frequency
  * Change Lead Time
  * Mean Time to Recovery (MTTR)
  * Change Failure Rate
  * Cycle Time
  * Automation Percentage
  * Test Coverage
  * System Uptime
  * Customer Feedback
  * Team Collaboration
* **Rich Logging:** Outputs clean, color-coded logs for requests and operations using the `rich` library.
* **Phased Development:** Built incrementally to encourage structured problem-solving and extensibility.
* **Environment Management:** Utilizes Poetry for managing dependencies and project setup.

## **Tech Stack 🛠️**

* **Python:** Core programming language.
* **Flask:** For building the HTTP server.
* **Rich:** For color-coded logging and enhanced developer experience.
* **Poetry:** For dependency management and environment setup.
* **Unit Testing:** Using `unittest` and `pytest` for robust test coverage.

---

## **Installation 🐍**

### 1. **Clone the Repository**

```bash
git clone https://github.com/lmcdonough/devops-metrics-viewer.git
cd devops-metrics-viewer
```

### 2. **Set Up the Environment with Poetry**

Install Poetry (if not already installed):

```bash
pip install poetry
```

Install project dependencies:

```bash
poetry install
```

### 3. **Activate the Poetry Environment**

Use the updated Poetry command to activate the virtual environment:

```bash
poetry env use python
poetry env info
```

(Tip: Run `poetry env list` to get the correct path.)

---

## **Mocked Metrics Data (JSON File) 📊**

Mocked metrics data are stored in a JSON file to allow easy data management. This file contains initial data for various metrics and can be modified to simulate different values without changing the source code.

---

## **Running the Application 🛡️**

Start the Flask server:

```bash
poetry run python main.py
```

By default, the server will run on:  
**`http://localhost:5005`**

---

## **API Endpoints**

Retrieve metrics via these endpoints:

### **Core Metrics**

| Metric                     | Endpoint                                  |
|----------------------------|-------------------------------------------|
| Deployment Frequency       | `GET /metrics/deployment-frequency`       |
| Change Lead Time           | `GET /metrics/change-lead-time`           |
| Mean Time to Recovery (MTTR) | `GET /metrics/mean-time-to-recovery`   |
| Change Failure Rate        | `GET /metrics/change-failure-rate`        |
| Cycle Time                 | `GET /metrics/cycle-time`                 |

### **Additional Metrics**

| Metric                  | Endpoint                                  |
|-------------------------|-------------------------------------------|
| Automation Percentage   | `GET /metrics/automation-percentage`      |
| Test Coverage          | `GET /metrics/test-coverage`             |
| System Uptime          | `GET /metrics/system-uptime`             |
| Customer Feedback      | `GET /metrics/customer-feedback`         |
| Team Collaboration     | `GET /metrics/team-collaboration`        |

Example Request:

```bash
curl "http://127.0.0.1:5005/metrics/deployment-frequency"
```

---

## **Phases of Development**

1. **Phase 1:** Simulates an HTTP server returning metrics in JSON format. ✅ *(Completed)*
2. **Phase 2:** Implements a client fetching metrics from mocked endpoints in `MetricsServer`. 🔄 *(In Progress)*
3. **Phase 3:** Adds timestamps and text-based graphing. 🚧 *(Planned)*

---

## **Testing 🧪**

Run unit tests using `pytest`:

```bash
poetry run pytest
```

---

## **Development Workflow 🧑‍💻**

1. Implement a Flask-based server (`MetricsServer`) with a modular design.
2. Store mocked metrics in a JSON file for easy data management.
3. Use Python decorators to log incoming requests with `rich`.
4. Write unit tests for API endpoints to ensure reliability.
5. Plan for extending functionality with timestamped data and visualizations.

---

## **Future Enhancements 🛠️**

* Extend functionality to include real-time CI/CD metrics via API integration.
* Add timestamped metrics and trend visualization (Phase 3).
* Implement more advanced text-based or graphical visualization libraries (e.g., `matplotlib`).

---

## **License 📜**

This project is licensed under the **MIT License**.

---
