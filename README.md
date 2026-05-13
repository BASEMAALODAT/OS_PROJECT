<h1 align="center">CPU Scheduling Simulator</h1>

<p align="center">
  <b>Operating Systems Project | CPU Scheduling Algorithms Simulation and Performance Analysis</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Matplotlib-Visualization-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/OS-CPU%20Scheduling-purple?style=for-the-badge">
</p>

---

## Project Overview

This project is a complete **CPU Scheduling Simulator** developed using Python.  
It simulates and compares different CPU scheduling algorithms used in operating systems.

The simulator calculates important performance metrics, generates professional Gantt charts, compares algorithm performance, and exports results for analysis.

---

## Implemented Algorithms

- First Come First Serve **FCFS**
- Shortest Job First **SJF**
- Round Robin **RR**
- Priority Scheduling

---

## Features

- Multiple workload scenarios
- Arrival Time and Burst Time support
- Priority support
- Time Quantum support for Round Robin
- Waiting Time calculation
- Turnaround Time calculation
- Average Waiting Time
- Average Turnaround Time
- CPU Utilization
- Throughput
- Gantt Chart visualization
- Performance comparison charts
- CSV result export

---

## Project Scenarios

| Scenario | Description |
|---|---|
| Stress Test | Heavy workload with long and short CPU bursts |
| Balanced Workload | Moderate workload with balanced process distribution |
| Starvation Case | Scenario designed to test starvation and fairness issues |

---

## Performance Metrics

| Metric | Meaning |
|---|---|
| WT | Waiting Time |
| TAT | Turnaround Time |
| CT | Completion Time |
| CPU Utilization | Percentage of time CPU is busy |
| Throughput | Number of completed processes per unit time |

---

## Stress Test Results

### FCFS Gantt Chart

<img src="cpu_scheduling_output/Stress_Test_FCFS_gantt.png" width="900">

### SJF Gantt Chart

<img src="cpu_scheduling_output/Stress_Test_SJF_gantt.png" width="900">

### Round Robin Gantt Chart

<img src="cpu_scheduling_output/Stress_Test_Round_Robin_gantt.png" width="900">

### Priority Scheduling Gantt Chart

<img src="cpu_scheduling_output/Stress_Test_Priority_Scheduling_gantt.png" width="900">

### Stress Test Comparison

<img src="cpu_scheduling_output/Stress_Test_comparison.png" width="900">

---

## Balanced Workload Results

### FCFS Gantt Chart

<img src="cpu_scheduling_output/Balanced_Workload_FCFS_gantt.png" width="900">

### SJF Gantt Chart

<img src="cpu_scheduling_output/Balanced_Workload_SJF_gantt.png" width="900">

### Round Robin Gantt Chart

<img src="cpu_scheduling_output/Balanced_Workload_Round_Robin_gantt.png" width="900">

### Priority Scheduling Gantt Chart

<img src="cpu_scheduling_output/Balanced_Workload_Priority_Scheduling_gantt.png" width="900">

### Balanced Workload Comparison

<img src="cpu_scheduling_output/Balanced_Workload_comparison.png" width="900">

---

## Starvation Case Results

### FCFS Gantt Chart

<img src="cpu_scheduling_output/Starvation_Case_FCFS_gantt.png" width="900">

### SJF Gantt Chart

<img src="cpu_scheduling_output/Starvation_Case_SJF_gantt.png" width="900">

### Round Robin Gantt Chart

<img src="cpu_scheduling_output/Starvation_Case_Round_Robin_gantt.png" width="900">

### Priority Scheduling Gantt Chart

<img src="cpu_scheduling_output/Starvation_Case_Priority_Scheduling_gantt.png" width="900">

### Starvation Case Comparison

<img src="cpu_scheduling_output/Starvation_Case_comparison.png" width="900">

---

## How to Run

Install the required libraries:

```bash
pip install pandas matplotlib
