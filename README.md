# CPU Scheduling Simulator

## Operating Systems Project

A complete CPU Scheduling Simulator developed using Python to simulate and compare different CPU scheduling algorithms used in operating systems.

---

# Project Overview

This project demonstrates how operating systems manage CPU allocation between processes using different scheduling algorithms.

The simulator calculates important performance metrics and compares algorithm efficiency under multiple workload scenarios.

Implemented scheduling algorithms:

- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR)
- Priority Scheduling

---

# Features

- Multiple scheduling algorithms
- Waiting Time calculation
- Turnaround Time calculation
- Completion Time calculation
- CPU Utilization analysis
- Throughput analysis
- Gantt Chart generation
- Performance comparison graphs
- Multiple workload scenarios
- CSV result export
- Process priority support
- Time Quantum support

---

# Implemented Algorithms

## 1. First Come First Serve (FCFS)

Processes are executed according to their arrival order in the ready queue.

### Advantages
- Simple implementation
- Low overhead
- Fair based on arrival order

### Disadvantages
- High waiting time
- Convoy effect
- Poor responsiveness

---

## 2. Shortest Job First (SJF)

The process with the shortest burst time executes first.

### Advantages
- Best average waiting time
- Efficient CPU usage
- Better throughput

### Disadvantages
- Possible starvation
- Requires burst time estimation

---

## 3. Round Robin (RR)

Processes execute using fixed time slices called quantum.

### Advantages
- High fairness
- Good responsiveness
- Suitable for time-sharing systems

### Disadvantages
- Context switching overhead
- Performance depends on quantum size

---

## 4. Priority Scheduling

Processes execute according to assigned priority values.

### Advantages
- Fast execution for important processes
- Flexible scheduling

### Disadvantages
- Starvation risk for low-priority processes

---

# Performance Metrics

| Metric | Description |
|---|---|
| WT | Waiting Time |
| TAT | Turnaround Time |
| CT | Completion Time |
| CPU Utilization | CPU busy percentage |
| Throughput | Completed processes per unit time |

---

# Experimental Scenarios

## Stress Test Scenario
Heavy workload with many processes and large burst times.

## Balanced Workload Scenario
Balanced process distribution with moderate workload.

## Starvation Scenario
Designed to test fairness and starvation behavior.

---

# Results Summary

The results showed major behavioral differences between scheduling algorithms.

- SJF achieved the lowest average waiting and turnaround times.
- Round Robin provided better fairness and responsiveness.
- FCFS was simple but suffered from high waiting times.
- Priority Scheduling performed well for important tasks.

---

# Technologies Used

- Python 3
- Pandas
- Matplotlib

---

# How to Run

Install required libraries:

```bash
pip install pandas matplotlib
```bash
pip install pandas matplotlib
