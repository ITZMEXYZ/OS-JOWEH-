import tkinter as tk
from tkinter import ttk, messagebox

# Import the standalone module sub-frames
from cpu_dispatcher import CPUModule
from memory_mvt import MemoryModule
from virtual_memory import VirtualMemoryModule
from disk_router import DiskRouterModule

class ComprehensiveOSCADApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRISIS-LINK // Unified 4-in-1 OS Capstone Dashboard")
        self.root.geometry("1350x800")
        self.root.state('zoomed')  
        self.root.configure(bg="#0f171e")

        self.base_frame = tk.Frame(self.root, bg="#0f171e")
        self.container_panel = tk.Frame(self.base_frame, bg="#0f171e")

        self.cpu_frame = CPUModule(self.container_panel)
        self.memory_frame = MemoryModule(self.container_panel)
        self.vm_frame = VirtualMemoryModule(self.container_panel)
        self.disk_frame = DiskRouterModule(self.container_panel)
        
        self.sidebar_width = 250
        self.current_x = -250
        self.animation_job = None

        self.setup_styles()
        self.build_navigation_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview", 
                        background="#16222f", 
                        foreground="#ffffff", 
                        rowheight=32, 
                        fieldbackground="#16222f",
                        font=("Courier New", 10)) 

        style.configure("Treeview.Heading",
                        background="#1c2d3d",
                        foreground="#ffffff",
                        font=("Courier New", 10, "bold"),
                        padding=6)
        
        style.map("Treeview", background=[('selected', '#1f5370')], foreground=[('selected', '#ffffff')])

    def build_navigation_layout(self):
        # Top Header Banner Strip
        top_banner = tk.Label(self.root, text="🚨 SYSTEM INTERNALS CORE DASHBOARD // 911 COMPUTER AIDED DISPATCH TERMINAL 🚨",
                              bg="#16222f", fg="#ff4a4a", font=("Courier", 12, "bold"), pady=8, relief="raised", bd=1)
        top_banner.pack(fill=tk.X, side=tk.TOP)

        self.base_frame.pack(fill=tk.BOTH, expand=True)

        self.trigger_strip = tk.Label(self.base_frame, text="▶", bg="#16222f", fg="#5dade2", 
                                      font=("Courier New", 12, "bold"), width=2, cursor="hand2")
        self.trigger_strip.pack(side=tk.LEFT, fill=tk.Y)

        self.container_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.sidebar = tk.Frame(self.base_frame, bg="#111c24", width=self.sidebar_width, relief="solid", bd=1)
        self.sidebar.pack_propagate(False)
        self.sidebar.place(x=self.current_x, y=0, relheight=1.0) 

        menu_title = tk.Label(self.sidebar, text="OS CAD ENGINE DIRECTORY", bg="#111c24", fg="#5dade2", font=("Courier", 10, "bold"), pady=15)
        menu_title.pack()

        modules = [
            ("1. CPU Dispatcher", self.show_cpu_module),
            ("2. Active Memory (MVT/MFT)", self.show_memory_module),
            ("3. Virtual Memory Unit", self.show_vm_module),
            ("4. Multi-Disk Router", self.show_storage_module)
        ]
        
        for name, callback in modules:
            btn = tk.Button(self.sidebar, text=name, bg="#1c2d3d", fg="#ffffff", activebackground="#293f54",
                            activeforeground="#ffffff", font=("Courier", 10), anchor="w", padx=15, pady=10,
                            relief="flat", bd=0, command=callback)
            btn.pack(fill=tk.X, pady=2, padx=5)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#293f54"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#1c2d3d"))

        for f in [self.cpu_frame, self.memory_frame, self.vm_frame, self.disk_frame]:
            f.master = self.container_panel

        self.trigger_strip.bind("<Enter>", lambda e: self.animate_sidebar(open_direction=True))
        self.sidebar.bind("<Leave>", lambda e: self.animate_sidebar(open_direction=False))

        self.show_cpu_module()

    def animate_sidebar(self, open_direction):
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

        if open_direction:
            if self.current_x < 0:
                self.current_x += 25  
                self.sidebar.place(x=self.current_x)
                self.animation_job = self.root.after(10, lambda: self.animate_sidebar(True))
        else:
            self.animation_job = self.root.after(300, self._execute_slide_shut)

    def _execute_slide_shut(self):
        self.animation_job = None
        mouse_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        mouse_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        
        try:
            strip_x = self.trigger_strip.winfo_x()
            strip_y = self.trigger_strip.winfo_y()
            strip_w = self.trigger_strip.winfo_width()
            strip_h = self.trigger_strip.winfo_height()
            over_trigger = (strip_x <= mouse_x <= strip_x + strip_w) and (strip_y <= mouse_y <= strip_y + strip_h)
        except:
            over_trigger = False

        # 🌟 FIXED INDENTATION WINDOW BOUNDS:
        # Only abort closing if the mouse is safely inside the menu grid column box bounds.
        # This catches top/bottom/left exits and slides the drawer away instantly!
        if (0 <= mouse_x <= self.sidebar_width) or over_trigger:
            return

        if self.current_x > -self.sidebar_width:
            self.current_x -= 25
            self.sidebar.place(x=self.current_x)
            self.animation_job = self.root.after(10, self._execute_slide_shut)

    # =========================================================================
    # 📑 SIDEBAR NAVIGATION TAB SWITCHERS
    # =========================================================================
    def show_cpu_module(self):
        self.memory_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.cpu_frame.pack(fill=tk.BOTH, expand=True)

    def show_memory_module(self):
        self.cpu_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.memory_frame.pack(fill=tk.BOTH, expand=True)

    def show_vm_module(self):
        self.cpu_frame.pack_forget()
        self.memory_frame.pack_forget()
        self.disk_frame.pack_forget()
        self.vm_frame.pack(fill=tk.BOTH, expand=True)

    def show_storage_module(self):
        self.cpu_frame.pack_forget()
        self.memory_frame.pack_forget()
        self.vm_frame.pack_forget()
        self.disk_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ComprehensiveOSCADApp(root)
    root.mainloop()