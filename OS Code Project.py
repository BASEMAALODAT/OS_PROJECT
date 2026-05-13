import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


os.system("cls" if os.name == "nt" else "clear")

OUTPUT_DIR = Path("cpu_scheduling_output")
OUTPUT_DIR.mkdir(exist_ok=True)

SHOW_PLOTS = True
SAVE_RESULTS = True


scenarios = {
    "Stress Test": {
        "processes": [
            {"pid": "P1",  "at": 0,  "bt": 20, "priority": 5},
            {"pid": "P2",  "at": 1,  "bt": 2,  "priority": 1},
            {"pid": "P3",  "at": 2,  "bt": 1,  "priority": 1},
            {"pid": "P4",  "at": 3,  "bt": 8,  "priority": 3},
            {"pid": "P5",  "at": 4,  "bt": 16, "priority": 4},
            {"pid": "P6",  "at": 6,  "bt": 3,  "priority": 2},
            {"pid": "P7",  "at": 7,  "bt": 25, "priority": 5},
            {"pid": "P8",  "at": 9,  "bt": 2,  "priority": 1},
            {"pid": "P9",  "at": 10, "bt": 14, "priority": 4},
            {"pid": "P10", "at": 11, "bt": 1,  "priority": 1},
            {"pid": "P11", "at": 13, "bt": 7,  "priority": 3},
            {"pid": "P12", "at": 15, "bt": 30, "priority": 5}
        ],
        "quantum": 3
    },

    "Balanced Workload": {
        "processes": [
            {"pid": "P1", "at": 0,  "bt": 6, "priority": 3},
            {"pid": "P2", "at": 1,  "bt": 4, "priority": 2},
            {"pid": "P3", "at": 2,  "bt": 9, "priority": 4},
            {"pid": "P4", "at": 4,  "bt": 5, "priority": 1},
            {"pid": "P5", "at": 5,  "bt": 3, "priority": 2},
            {"pid": "P6", "at": 7,  "bt": 8, "priority": 5},
            {"pid": "P7", "at": 8,  "bt": 2, "priority": 1},
            {"pid": "P8", "at": 10, "bt": 7, "priority": 3}
        ],
        "quantum": 4
    },

    "Starvation Case": {
        "processes": [
            {"pid": "P1", "at": 0,  "bt": 18, "priority": 5},
            {"pid": "P2", "at": 1,  "bt": 2,  "priority": 1},
            {"pid": "P3", "at": 2,  "bt": 2,  "priority": 1},
            {"pid": "P4", "at": 3,  "bt": 3,  "priority": 2},
            {"pid": "P5", "at": 4,  "bt": 1,  "priority": 1},
            {"pid": "P6", "at": 6,  "bt": 20, "priority": 5},
            {"pid": "P7", "at": 8,  "bt": 2,  "priority": 1},
            {"pid": "P8", "at": 10, "bt": 1,  "priority": 1}
        ],
        "quantum": 3
    }
}


def pid_number(pid):
    if pid == "Idle":
        return 10**9
    return int(pid.replace("P", ""))


def copy_processes(processes):
    return [p.copy() for p in processes]


def calculate_metrics(process, current_time):
    process["ct"] = current_time
    process["tat"] = process["ct"] - process["at"]
    process["wt"] = process["tat"] - process["bt"]


def add_gantt(gantt_chart, pid, start, end):
    if start == end:
        return

    if gantt_chart and gantt_chart[-1][0] == pid and gantt_chart[-1][2] == start:
        old_pid, old_start, _ = gantt_chart[-1]
        gantt_chart[-1] = (old_pid, old_start, end)
    else:
        gantt_chart.append((pid, start, end))


def next_arrival_time(processes, current_time, completed):
    future = [
        p["at"] for p in processes
        if p not in completed and p["at"] > current_time
    ]
    return min(future) if future else current_time


def fcfs(processes):
    processes_copy = copy_processes(processes)
    processes_copy.sort(key=lambda p: (p["at"], pid_number(p["pid"])))

    current_time = 0
    gantt_chart = []

    for p in processes_copy:
        if current_time < p["at"]:
            add_gantt(gantt_chart, "Idle", current_time, p["at"])
            current_time = p["at"]

        start_time = current_time
        current_time += p["bt"]
        add_gantt(gantt_chart, p["pid"], start_time, current_time)
        calculate_metrics(p, current_time)

    return processes_copy, gantt_chart


def sjf(processes):
    processes_copy = copy_processes(processes)

    current_time = 0
    completed = []
    gantt_chart = []

    while len(completed) < len(processes_copy):
        available = [
            p for p in processes_copy
            if p["at"] <= current_time and p not in completed
        ]

        if not available:
            next_time = next_arrival_time(processes_copy, current_time, completed)
            add_gantt(gantt_chart, "Idle", current_time, next_time)
            current_time = next_time
            continue

        selected = min(
            available,
            key=lambda p: (p["bt"], p["at"], pid_number(p["pid"]))
        )

        start_time = current_time
        current_time += selected["bt"]
        add_gantt(gantt_chart, selected["pid"], start_time, current_time)
        calculate_metrics(selected, current_time)

        completed.append(selected)

    return completed, gantt_chart


def priority_scheduling(processes):
    processes_copy = copy_processes(processes)

    current_time = 0
    completed = []
    gantt_chart = []

    while len(completed) < len(processes_copy):
        available = [
            p for p in processes_copy
            if p["at"] <= current_time and p not in completed
        ]

        if not available:
            next_time = next_arrival_time(processes_copy, current_time, completed)
            add_gantt(gantt_chart, "Idle", current_time, next_time)
            current_time = next_time
            continue

        selected = min(
            available,
            key=lambda p: (p["priority"], p["at"], pid_number(p["pid"]))
        )

        start_time = current_time
        current_time += selected["bt"]
        add_gantt(gantt_chart, selected["pid"], start_time, current_time)
        calculate_metrics(selected, current_time)

        completed.append(selected)

    return completed, gantt_chart


def round_robin(processes, quantum):
    processes_copy = copy_processes(processes)

    for p in processes_copy:
        p["remaining"] = p["bt"]

    processes_copy.sort(key=lambda p: (p["at"], pid_number(p["pid"])))

    current_time = 0
    completed = []
    ready_queue = []
    gantt_chart = []

    while len(completed) < len(processes_copy):

        for p in processes_copy:
            if (
                p["at"] <= current_time
                and p not in ready_queue
                and p not in completed
                and p["remaining"] > 0
            ):
                ready_queue.append(p)

        if not ready_queue:
            future = [
                p["at"] for p in processes_copy
                if p not in completed and p["remaining"] > 0 and p["at"] > current_time
            ]

            if future:
                next_time = min(future)
                add_gantt(gantt_chart, "Idle", current_time, next_time)
                current_time = next_time
                continue

        current_process = ready_queue.pop(0)

        start_time = current_time
        execution_time = min(quantum, current_process["remaining"])

        current_time += execution_time
        current_process["remaining"] -= execution_time

        add_gantt(gantt_chart, current_process["pid"], start_time, current_time)

        for p in processes_copy:
            if (
                p["at"] <= current_time
                and p not in ready_queue
                and p not in completed
                and p != current_process
                and p["remaining"] > 0
            ):
                ready_queue.append(p)

        if current_process["remaining"] > 0:
            ready_queue.append(current_process)
        else:
            calculate_metrics(current_process, current_time)
            completed.append(current_process)

    for p in completed:
        p.pop("remaining", None)

    return completed, gantt_chart


def calculate_extra_metrics(results, gantt_chart):
    total_time = gantt_chart[-1][2] - gantt_chart[0][1]
    busy_time = sum(end - start for pid, start, end in gantt_chart if pid != "Idle")
    process_count = len(results)

    cpu_utilization = (busy_time / total_time) * 100 if total_time else 0
    throughput = process_count / total_time if total_time else 0

    return round(cpu_utilization, 2), round(throughput, 4)


def make_results_df(results):
    df = pd.DataFrame(results)
    columns = ["pid", "at", "bt", "priority", "ct", "tat", "wt"]
    df = df[columns].copy()
    df["pid_num"] = df["pid"].apply(pid_number)
    df = df.sort_values("pid_num").drop(columns=["pid_num"])
    return df


def display_results(results, gantt_chart, algorithm_name):
    df = make_results_df(results)

    print("\n" + "═" * 86)
    print(f"{algorithm_name} Scheduling Results")
    print("═" * 86)
    print(df.to_string(index=False))

    avg_wt = df["wt"].mean()
    avg_tat = df["tat"].mean()
    cpu_utilization, throughput = calculate_extra_metrics(results, gantt_chart)

    print("\nPerformance Summary")
    print("-" * 40)
    print(f"Average Waiting Time      : {avg_wt:.2f}")
    print(f"Average Turnaround Time   : {avg_tat:.2f}")
    print(f"CPU Utilization           : {cpu_utilization:.2f}%")
    print(f"Throughput                : {throughput:.4f} process/unit time")

    return {
        "algorithm": algorithm_name,
        "avg_wt": round(avg_wt, 2),
        "avg_tat": round(avg_tat, 2),
        "cpu_utilization": cpu_utilization,
        "throughput": throughput
    }


def get_process_colors(processes):
    palette = [
        "#4E79A7", "#F28E2B", "#E15759", "#76B7B2",
        "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7",
        "#9C755F", "#BAB0AC", "#2A9D8F", "#6A4C93"
    ]

    colors = {"Idle": "#D9D9D9"}
    sorted_processes = sorted(processes, key=lambda p: pid_number(p["pid"]))

    for i, p in enumerate(sorted_processes):
        colors[p["pid"]] = palette[i % len(palette)]

    return colors


def display_gantt_chart(gantt_chart, title, process_colors, file_name):
    total_time = gantt_chart[-1][2]
    chart_width = max(14, min(32, total_time / 3.7))
    chart_height = 5.8 if "Round Robin" in title else 4.8

    fig, ax = plt.subplots(figsize=(chart_width, chart_height))

    for pid, start, end in gantt_chart:
        duration = end - start

        ax.barh(
            y=0,
            width=duration,
            left=start,
            height=0.55,
            color=process_colors.get(pid, "#999999"),
            edgecolor="black",
            linewidth=1.1
        )

        if duration >= 2:
            text_color = "black" if pid == "Idle" else "white"
            ax.text(
                start + duration / 2,
                0,
                pid,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color=text_color
            )

    ax.set_title(title, fontsize=17, fontweight="bold", pad=15)
    ax.set_xlabel("Time", fontsize=12, fontweight="bold")
    ax.set_yticks([])
    ax.set_xlim(0, total_time)

    time_points = sorted(set([0] + [start for _, start, _ in gantt_chart] + [end for _, _, end in gantt_chart]))

    if len(time_points) > 28:
        step = max(1, len(time_points) // 28)
        time_points = time_points[::step] + [total_time]

    ax.set_xticks(sorted(set(time_points)))
    ax.tick_params(axis="x", labelrotation=45)
    ax.grid(axis="x", linestyle="--", alpha=0.35)

    used_pids = sorted(set(pid for pid, _, _ in gantt_chart), key=pid_number)
    legend_items = [
        Patch(facecolor=process_colors[pid], edgecolor="black", label=pid)
        for pid in used_pids
    ]

    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.25),
        ncol=min(7, len(legend_items)),
        fontsize=9
    )

    plt.tight_layout()

    save_path = OUTPUT_DIR / file_name
    plt.savefig(save_path, dpi=180, bbox_inches="tight")

    if SHOW_PLOTS:
        plt.show()

    plt.close(fig)


def display_comparison(summary_results, scenario_name):
    df = pd.DataFrame(summary_results)

    print("\n" + "═" * 86)
    print("Algorithms Performance Comparison")
    print("═" * 86)
    print(df.to_string(index=False))

    fig, ax = plt.subplots(figsize=(11, 6))

    x = range(len(df))
    width = 0.35

    bars1 = ax.bar(
        [i - width / 2 for i in x],
        df["avg_wt"],
        width,
        label="Average Waiting Time",
        edgecolor="black"
    )

    bars2 = ax.bar(
        [i + width / 2 for i in x],
        df["avg_tat"],
        width,
        label="Average Turnaround Time",
        edgecolor="black"
    )

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold"
            )

    ax.set_title("Scheduling Algorithms Comparison", fontsize=16, fontweight="bold")
    ax.set_xlabel("Algorithm", fontsize=11, fontweight="bold")
    ax.set_ylabel("Average Time", fontsize=11, fontweight="bold")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["algorithm"])
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    plt.tight_layout()

    comparison_file = OUTPUT_DIR / f"{scenario_name}comparison.png".replace(" ", "")
    plt.savefig(comparison_file, dpi=180, bbox_inches="tight")

    if SHOW_PLOTS:
        plt.show()

    plt.close(fig)

    best_wt = df.loc[df["avg_wt"].idxmin()]
    best_tat = df.loc[df["avg_tat"].idxmin()]

    print("\nBest Analysis")
    print("-" * 40)
    print(f"Best Average Waiting Time    : {best_wt['algorithm']} ({best_wt['avg_wt']:.2f})")
    print(f"Best Average Turnaround Time : {best_tat['algorithm']} ({best_tat['avg_tat']:.2f})")

    if SAVE_RESULTS:
        csv_path = OUTPUT_DIR / f"{scenario_name}summary.csv".replace(" ", "")
        df.to_csv(csv_path, index=False)


def save_algorithm_results(results, scenario_name, algorithm_name):
    if not SAVE_RESULTS:
        return

    df = make_results_df(results)
    file_path = OUTPUT_DIR / f"{scenario_name}{algorithm_name}_results.csv".replace(" ", "")
    df.to_csv(file_path, index=False)


def run_algorithm(algorithm_name, algorithm_function, processes, quantum, scenario_name, process_colors):
    if algorithm_name == "Round Robin":
        results, gantt_chart = algorithm_function(processes, quantum)
    else:
        results, gantt_chart = algorithm_function(processes)

    safe_name = algorithm_name.replace(" ", "_")
    safe_scenario = scenario_name.replace(" ", "_")

    display_gantt_chart(
        gantt_chart,
        f"{algorithm_name} Gantt Chart",
        process_colors,
        f"{safe_scenario}_{safe_name}_gantt.png"
    )

    summary = display_results(results, gantt_chart, algorithm_name)
    save_algorithm_results(results, scenario_name, algorithm_name)

    return summary


def run_scenario(scenario_name):
    processes = scenarios[scenario_name]["processes"]
    quantum = scenarios[scenario_name]["quantum"]
    process_colors = get_process_colors(processes)

    print("\n" + "█" * 86)
    print("CPU Scheduling Simulator")
    print("█" * 86)
    print(f"Selected Scenario       : {scenario_name}")
    print(f"Time Quantum            : {quantum}")
    print(f"Number of Processes     : {len(processes)}")
    print(f"Output Folder           : {OUTPUT_DIR.resolve()}")

    algorithms = [
        ("FCFS", fcfs),
        ("SJF", sjf),
        ("Round Robin", round_robin),
        ("Priority Scheduling", priority_scheduling)
    ]

    summary_results = []

    for algorithm_name, algorithm_function in algorithms:
        summary = run_algorithm(
            algorithm_name,
            algorithm_function,
            processes,
            quantum,
            scenario_name,
            process_colors
        )
        summary_results.append(summary)

    display_comparison(summary_results, scenario_name)


# =========================
# Run Project
# =========================
all_Scenarios = [
    "Stress Test",
    "Balanced Workload",
    "Starvation Case"
]
for scenario in all_Scenarios:
    run_scenario(scenario)