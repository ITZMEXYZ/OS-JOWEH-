import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CPUModule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0f171e")
        self.cpu_incidents = []  
        self.setup_ui()

    def setup_ui(self):
        form_frame = tk.LabelFrame(self, text=" LOG NEW 911 INCIDENT ", bg="#0f171e", fg="#ffcc00", font=("Courier", 10, "bold"))
        form_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(form_frame, text="Desc:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=15)
        self.cpu_desc_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_desc_ent.insert(0, "Assault")

        tk.Label(form_frame, text="Arrival:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_arr_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_arr_ent.insert(0, "0")

        tk.Label(form_frame, text="Burst:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_burst_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_burst_ent.insert(0, "10")

        tk.Label(form_frame, text="Priority (1=High):", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent = tk.Entry(form_frame, bg="#16222f", fg="white", insertbackground="white", width=6)
        self.cpu_prio_ent.pack(side=tk.LEFT, padx=5)
        self.cpu_prio_ent.insert(0, "1")

        tk.Label(form_frame, text="Algorithm:", bg="#111c24", fg="#ffffff", font=("Courier New", 9, "bold")).pack(side=tk.LEFT, padx=(10, 2))

        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_menu = ttk.Combobox(form_frame, textvariable=self.algo_var, 
                                      values=["FCFS", 
                                          "SJF (Non Pre-emptive)", 
                                          "SJF (Pre-emptive)", 
                                          "Priority (Non Pre-emptive)", 
                                          "Priority (Pre-emptive)",
                                          "Round Robin (RR)"
                                      ], 
                                      state="readonly", width=25, font=("Courier New", 9))
        self.algo_menu.pack(side=tk.LEFT, padx=5)
        self.algo_menu.bind("<<ComboboxSelected>>", self.toggle_quantum_visibility)

        self.quantum_frame = tk.Frame(form_frame, bg="#111c24")
        tk.Label(self.quantum_frame, text="Q:", bg="#111c24", fg="#ffcc00", font=("Courier New", 9, "bold")).pack(side=tk.LEFT, padx=2)
        self.quantum_ent = tk.Entry(self.quantum_frame, bg="#16222f", fg="#ffffff", insertbackground="white", width=3, relief="solid", bd=1, font=("Courier New", 9))
        self.quantum_ent.insert(0, "4")
        self.quantum_ent.pack(side=tk.LEFT)
        
        add_btn = tk.Button(form_frame, text="Add Incident", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), relief="flat", bd=0, command=self.add_incident_to_table, width=12)
        add_btn.pack(side=tk.LEFT, padx=12)

        rand_btn = tk.Button(form_frame, text="🎲 Randomize 4", bg="#1c2d3d", fg="white", font=("Courier", 9, "bold"), relief="flat", bd=0, command=self.randomize_cpu_incidents)
        rand_btn.pack(side=tk.LEFT, padx=2)

        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#293f54"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#1c2d3d"))
        
        rand_btn.bind("<Enter>", lambda e: rand_btn.config(bg="#293f54"))
        rand_btn.bind("<Leave>", lambda e: rand_btn.config(bg="#1c2d3d"))

        table_frame = tk.Frame(self, bg="#0f171e")
        table_frame.pack(fill=tk.X, pady=5)
        
        self.cpu_tree = ttk.Treeview(table_frame, columns=("ID", "Description", "Arrival Time", "Burst Time", "Priority"), show='headings', height=10)
        self.cpu_tree.heading("ID", text="ID")
        self.cpu_tree.heading("Description", text="Description")
        self.cpu_tree.heading("Arrival Time", text="Arrival Time")
        self.cpu_tree.heading("Burst Time", text="Burst Time")
        self.cpu_tree.heading("Priority", text="Priority")
        self.cpu_tree.pack(fill=tk.X, expand=True)

        bottom_workspace = tk.Frame(self, bg="#0f171e")
        bottom_workspace.pack(fill=tk.BOTH, expand=True, pady=5)
        
        left_ctrls = tk.Frame(bottom_workspace, bg="#0f171e")
        left_ctrls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        algo_row = tk.Frame(left_ctrls, bg="#0f171e")
        algo_row.pack(fill=tk.X, anchor="w", pady=2)
        
        tk.Label(algo_row, text="Algorithm:", bg="#0f171e", fg="white", font=("Courier", 9)).pack(side=tk.LEFT, padx=2)
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_box = ttk.Combobox(algo_row, textvariable=self.algo_var, values=["FCFS", "SJF (Non-Preemptive)", "SRTF (SJF Preemptive)", "Priority (Non-Preemptive)", "Priority (Preemptive)"], width=22)
        self.algo_box.pack(side=tk.LEFT, padx=5)

        run_btn = tk.Button(algo_row, text="Run Dispatch", bg="#229954", fg="white", font=("Courier", 9, "bold"), relief="flat", bd=0, command=self.execute_cpu_dispatcher)
        run_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(algo_row, text="Clear Queue", bg="#d35400", fg="white", font=("Courier", 9, "bold"), relief="flat", bd=0, command=self.clear_cpu_queue)
        clear_btn.pack(side=tk.LEFT, padx=2)

        run_btn.bind("<Enter>", lambda e: run_btn.config(bg="#2cc771"))
        run_btn.bind("<Leave>", lambda e: run_btn.config(bg="#229954"))
        
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#e67e22"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#d35400"))

        tk.Label(left_ctrls, text="System Execution Log", bg="#0f171e", fg="#52be80", font=("Courier", 10, "bold")).pack(anchor="w", pady=(8,2))
        self.cpu_log_txt = tk.Text(left_ctrls, bg="#111111", fg="#ffffff", font=("Courier", 10), height=15, width=45)
        self.cpu_log_txt.pack(fill=tk.BOTH, expand=True)

        right_graph = tk.Frame(bottom_workspace, bg="#16222f", relief="solid", bd=1)
        right_graph.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.cpu_fig = Figure(figsize=(6, 4), dpi=95, facecolor='#16222f')
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=right_graph)
        self.cpu_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.sync_cpu_table_ui()
        self.render_empty_gantt()

    def toggle_quantum_visibility(self, event=None):
        if self.algo_var.get() == "Round Robin (RR)":
            self.quantum_frame.pack(side=tk.LEFT, padx=5)
        else:
            self.quantum_frame.pack_forget()

    def add_incident_to_table(self):
        try:
            desc = self.cpu_desc_ent.get().strip()
            arr = int(self.cpu_arr_ent.get())
            burst = int(self.cpu_burst_ent.get())
            prio = int(self.cpu_prio_ent.get())
            if arr < 0 or burst <= 0 or prio <= 0 or not desc: raise ValueError
            
            nid = len(self.cpu_incidents) + 1
            self.cpu_incidents.append({"id": nid, "desc": desc, "arrival": arr, "burst": burst, "priority": prio})
            self.sync_cpu_table_ui()
        except ValueError:
            messagebox.showerror("Error", "Verify item metrics are valid positive numbers.")

    def randomize_cpu_incidents(self):
        sample_pool = ["Traffic Stop", "Assault", "Heart Attack", "Structure Fire", "Robbery", "MVA Accident", "Noise Complaint", "Burglary"]
        self.cpu_incidents.clear()
        for i in range(1, 5):
            desc = random.choice(sample_pool)
            arr = random.randint(0, 15)
            burst = random.randint(3, 20)
            prio = random.randint(1, 4)
            self.cpu_incidents.append({"id": i, "desc": f"{desc} (p{i})", "arrival": arr, "burst": burst, "priority": prio})
        self.sync_cpu_table_ui()

    def clear_cpu_queue(self):
        self.cpu_incidents.clear()
        self.sync_cpu_table_ui()
        self.cpu_log_txt.delete("1.0", tk.END)
        self.render_empty_gantt()

    def sync_cpu_table_ui(self):
        for item in self.cpu_tree.get_children(): self.cpu_tree.delete(item)
        for i in self.cpu_incidents:
            self.cpu_tree.insert("", tk.END, values=(i["id"], i["desc"], i["arrival"], i["burst"], i["priority"]))

    def render_empty_gantt(self):
        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor('#0f171e')
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=11, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.set_xlabel("Time Units", fontsize=10, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.tick_params(colors='white')
        self.cpu_canvas.draw()

    def execute_cpu_dispatcher(self):
        if not self.cpu_incidents:
            messagebox.showwarning("Warning", "Add some dispatch vectors into the simulation registry first.")
            return
        
        algo = self.algo_var.get()
        self.log_to_terminal(f"📡 INITIALIZING DISPATCHER CORE // ENGINE ALGORITHM: {algo}")
        
        # FCFS
        if algo == "FCFS":
            queue = sorted([list(item) for item in self.incident_queue], key=lambda x: x[2])
            current_time = 0
            gantt_data = []
            
            for job in queue:
                if current_time < job[2]:
                    current_time = job[2]
                gantt_data.append((job[1], current_time, job[3]))
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching '{job[1]}' (Burst: {job[3]})")
                current_time += job[3]
            self.draw_gantt_chart(gantt_data)

        # SJF (NON-PRE)    
        if algo == "SJF (Non-Preemptive)":
            queue = [list(item) for item in self.incident_queue]
            current_time = 0
            gantt_data = []
            
            while queue:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs:
                    current_time = min(job[2] for job in queue)
                    continue
                
                next_job = min(available_jobs, key=lambda x: x[3]) # Smallest burst
                queue.remove(next_job)
                
                gantt_data.append((next_job[1], current_time, next_job[3]))
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching '{next_job[1]}' (Burst: {next_job[3]})")
                current_time += next_job[3]
            self.draw_gantt_chart(gantt_data)

        # SJF (PRE)
        elif algo == "SJF (Preemptive/SRTF)":
            queue = [list(item) for item in self.incident_queue]
            current_time = 0
            gantt_data = []
            
            current_job = None
            job_start_time = 0
            
            while queue or current_job:
                available_jobs = [job for job in queue if job[2] <= current_time]
                
                if not available_jobs and not current_job:
                    current_time = min(job[2] for job in queue)
                    continue
                
                if available_jobs:
                    best_arrival_job = min(available_jobs, key=lambda x: x[3])
                    if current_job is None or best_arrival_job[3] < current_job[3]:
                        if current_job:
                            duration = current_time - job_start_time
                            if duration > 0:
                                gantt_data.append((current_job[1], job_start_time, duration))
                            queue.append(current_job)
                        
                        current_job = best_arrival_job
                        queue.remove(best_arrival_job)
                        job_start_time = current_time
                        self.log_to_terminal(f"[TIME {current_time}]: ⚠️ PREEMPTING context to shorter unit '{current_job[1]}'")

                current_time += 1
                current_job[3] -= 1

                if current_job[3] == 0:
                    gantt_data.append((current_job[1], job_start_time, current_time - job_start_time))
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for '{current_job[1]}'.")
                    current_job = None
                    
            self.draw_gantt_chart(gantt_data)

        # PRIORITY (NON-PRE)
        elif algo == "Priority (Non-Preemptive)":
            queue = [list(item) for item in self.incident_queue]
            current_time = 0
            gantt_data = []
            
            while queue:
                available_jobs = [job for job in queue if job[2] <= current_time]
                if not available_jobs:
                    current_time = min(job[2] for job in queue)
                    continue
                
                next_job = min(available_jobs, key=lambda x: x[4])
                queue.remove(next_job)
                
                gantt_data.append((next_job[1], current_time, next_job[3]))
                self.log_to_terminal(f"[TIME {current_time}]: Dispatching High Priority '{next_job[1]}' (Rank: {next_job[4]})")
                current_time += next_job[3]
            self.draw_gantt_chart(gantt_data)

        # PRIORITY (PRE-EMP)
        elif algo == "Priority (Preemptive)":
            queue = [list(item) for item in self.incident_queue]
            current_time = 0
            gantt_data = []
            
            current_job = None
            job_start_time = 0
            
            while queue or current_job:
                available_jobs = [job for job in queue if job[2] <= current_time]
                
                if not available_jobs and not current_job:
                    current_time = min(job[2] for job in queue)
                    continue
                
                if available_jobs:
                    best_arrival_job = min(available_jobs, key=lambda x: x[4])
                    if current_job is None or best_arrival_job[4] < current_job[4]:
                        if current_job:
                            duration = current_time - job_start_time
                            if duration > 0:
                                gantt_data.append((current_job[1], job_start_time, duration))
                            queue.append(current_job)
                        
                        current_job = best_arrival_job
                        queue.remove(best_arrival_job)
                        job_start_time = current_time
                        self.log_to_terminal(f"[TIME {current_time}]: ⚠️ PREEMPTING context to critical priority task '{current_job[1]}'")

                current_time += 1
                current_job[3] -= 1
                
                if current_job[3] == 0:
                    gantt_data.append((current_job[1], job_start_time, current_time - job_start_time))
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for critical task '{current_job[1]}'.")
                    current_job = None
                    
            self.draw_gantt_chart(gantt_data)

        # ROUND ROBIN
        elif algo == "Round Robin (RR)":
            try:
                quantum = int(self.quantum_ent.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for Time Quantum.")
                return

            queue = [list(item) for item in self.incident_queue]
            queue.sort(key=lambda x: x[2])

            current_time = 0
            gantt_data = []
            ready_queue = []

            while queue or ready_queue:
                while queue and queue[0][2] <= current_time:
                    ready_queue.append(queue.pop(0))

                if not ready_queue:
                    current_time = queue[0][2]
                    continue

                current_job = ready_queue.pop(0)
                inc_id, desc, arr, remaining_burst, priority = current_job

                execute_time = min(remaining_burst, quantum)
                gantt_data.append((desc, current_time, execute_time))
                
                current_time += execute_time
                remaining_burst -= execute_time

                while queue and queue[0][2] <= current_time:
                    ready_queue.append(queue.pop(0))

                if remaining_burst > 0:
                    current_job[3] = remaining_burst
                    ready_queue.append(current_job)
                else:
                    self.log_to_terminal(f"💥 [TIME {current_time}]: Completed tracking for '{desc}'.")

            self.draw_gantt_chart(gantt_data)
            
        self.cpu_ax.clear()
        self.cpu_ax.set_facecolor('#0f171e')
        self.cpu_ax.set_title("Dispatch Timeline (Gantt Chart)", fontsize=11, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.set_xlabel("Time Units", fontsize=10, fontweight="bold", color="white", fontname="Courier")
        self.cpu_ax.tick_params(colors='white')
        
        all_unique_descriptions = list(dict.fromkeys([p["desc"] for p in sorted(self.cpu_incidents, key=lambda x: x["arrival"])]))
        self.cpu_ax.set_yticks(range(len(all_unique_descriptions)))
        self.cpu_ax.set_yticklabels(all_unique_descriptions, fontname="Courier", color="white", fontsize=8)
        
        x_ticks_positions = [0]
        for block in gantt_chart:
            y_position_index = all_unique_descriptions.index(block["desc"])
            self.cpu_ax.barh(y=y_position_index, width=block["duration"], left=block["start"], height=0.6, color="#4aa3df", edgecolor="#ffffff", align="center")
            self.cpu_ax.text(block["start"] + block["duration"]/2, y_position_index, f"ID:{block['id']}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
            end_time = block["start"] + block["duration"]
            if end_time not in x_ticks_positions: x_ticks_positions.append(end_time)
                
        x_ticks_positions.sort()
        self.cpu_ax.set_xticks(x_ticks_positions)
        self.cpu_ax.xaxis.grid(True, linestyle="--", alpha=0.3, color="#ffffff")
        self.cpu_ax.set_axisbelow(True)
        self.cpu_fig.tight_layout()
        self.cpu_canvas.draw()