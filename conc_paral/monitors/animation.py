import tkinter as tk
from tkinter import ttk
import threading
import time
import random
from queue import Queue
import uuid

class Thread:
    def __init__(self, thread_id):
        self.id = thread_id
        self.state = 'waiting'  # waiting, executing, blocked, finished
        self.canvas_id = None
        self.text_id = None
        self.work_time = random.uniform(1, 4)  # 1-4 seconds
        self.uuid = str(uuid.uuid4())[:8]

class Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.is_locked = False
        self.current_thread = None
        self.counter = 0
        self.waiting_queue = Queue()
        self.blocked_threads = []
    
    def try_enter(self, thread):
        with self.lock:
            if not self.is_locked:
                self.is_locked = True
                self.current_thread = thread
                return True
            else:
                if thread not in self.blocked_threads:
                    self.blocked_threads.append(thread)
                return False
    
    def exit_monitor(self):
        with self.lock:
            self.is_locked = False
            self.current_thread = None
            self.counter += 1
            
            # Wake up next thread if any
            if self.blocked_threads:
                next_thread = self.blocked_threads.pop(0)
                return next_thread
            return None

class MonitorSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Monitor de Concurrencia - Python Tkinter")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Initialize components
        self.monitor = Monitor()
        self.threads = []
        self.thread_counter = 1
        self.simulation_running = False
        self.animation_speed = 100  # milliseconds
        
        self.setup_ui()
        self.create_initial_threads()
        self.start_animation_loop()
    
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, 
                              text="🔒 Monitor de Concurrencia", 
                              font=('Arial', 24, 'bold'),
                              fg='white', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Simulación de acceso exclusivo a recursos compartidos",
                                 font=('Arial', 12),
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left side - Threads
        left_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        threads_title = tk.Label(left_frame, 
                                text="Hilos (Threads)", 
                                font=('Arial', 16, 'bold'),
                                fg='#3498db', bg='#34495e')
        threads_title.pack(pady=10)
        
        # Canvas for threads
        self.threads_canvas = tk.Canvas(left_frame, 
                                       width=400, height=400,
                                       bg='#34495e', highlightthickness=0)
        self.threads_canvas.pack(pady=10)
        
        # Right side - Monitor and Queue
        right_frame = tk.Frame(main_frame, bg='#34495e', relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Monitor section
        monitor_title = tk.Label(right_frame,
                                text="MONITOR",
                                font=('Arial', 16, 'bold'),
                                fg='#3498db', bg='#34495e')
        monitor_title.pack(pady=10)
        
        # Monitor canvas
        self.monitor_canvas = tk.Canvas(right_frame,
                                       width=300, height=200,
                                       bg='#2c3e50', highlightthickness=2,
                                       highlightbackground='#3498db')
        self.monitor_canvas.pack(pady=10)
        
        # Counter display
        self.counter_var = tk.StringVar(value="0")
        counter_label = tk.Label(right_frame,
                                text="Contador Compartido:",
                                font=('Arial', 12),
                                fg='white', bg='#34495e')
        counter_label.pack()
        
        counter_value = tk.Label(right_frame,
                                textvariable=self.counter_var,
                                font=('Arial', 32, 'bold'),
                                fg='#3498db', bg='#34495e')
        counter_value.pack()
        
        # Mutex indicator
        self.mutex_var = tk.StringVar(value="🔓 DESBLOQUEADO")
        self.mutex_label = tk.Label(right_frame,
                              textvariable=self.mutex_var,
                              font=('Arial', 14, 'bold'),
                              fg='#2ecc71', bg='#34495e')
        self.mutex_label.pack(pady=10)
        
        # Queue section
        queue_title = tk.Label(right_frame,
                              text="Cola de Espera",
                              font=('Arial', 14, 'bold'),
                              fg='#3498db', bg='#34495e')
        queue_title.pack(pady=(20, 5))
        
        self.queue_canvas = tk.Canvas(right_frame,
                                     width=300, height=80,
                                     bg='#34495e', highlightthickness=0)
        self.queue_canvas.pack()
        
        # Controls
        controls_frame = tk.Frame(self.root, bg='#2c3e50')
        controls_frame.pack(pady=20)
        
        style = ttk.Style()
        style.configure('Custom.TButton', font=('Arial', 12, 'bold'))
        
        self.start_btn = ttk.Button(controls_frame, text="▶️ Iniciar",
                                   command=self.start_simulation,
                                   style='Custom.TButton')
        self.start_btn.pack(side='left', padx=5)
        
        self.pause_btn = ttk.Button(controls_frame, text="⏸️ Pausar",
                                   command=self.pause_simulation,
                                   style='Custom.TButton')
        self.pause_btn.pack(side='left', padx=5)
        
        self.reset_btn = ttk.Button(controls_frame, text="🔄 Reiniciar",
                                   command=self.reset_simulation,
                                   style='Custom.TButton')
        self.reset_btn.pack(side='left', padx=5)
        
        self.add_btn = ttk.Button(controls_frame, text="➕ Agregar Hilo",
                                 command=self.add_thread,
                                 style='Custom.TButton')
        self.add_btn.pack(side='left', padx=5)
        
        # Status legend
        legend_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=1)
        legend_frame.pack(fill='x', padx=20, pady=10)
        
        legend_title = tk.Label(legend_frame,
                               text="Estados de los Hilos",
                               font=('Arial', 12, 'bold'),
                               fg='#3498db', bg='#34495e')
        legend_title.pack(pady=5)
        
        legend_content = tk.Frame(legend_frame, bg='#34495e')
        legend_content.pack()
        
        # Legend items
        legends = [
            ("🔴 Esperando", "Hilo listo para ejecutar"),
            ("🟢 Ejecutando", "Acceso exclusivo al monitor"),
            ("🟠 Bloqueado", "En cola esperando acceso"),
            ("🟢 Terminado", "Operación completada")
        ]
        
        for i, (status, desc) in enumerate(legends):
            frame = tk.Frame(legend_content, bg='#34495e')
            frame.pack(side='left', padx=20)
            
            tk.Label(frame, text=status, font=('Arial', 10, 'bold'),
                    fg='white', bg='#34495e').pack()
            tk.Label(frame, text=desc, font=('Arial', 8),
                    fg='#bdc3c7', bg='#34495e').pack()
    
    def create_initial_threads(self):
        for i in range(3):
            self.create_thread()
    
    def create_thread(self):
        thread = Thread(self.thread_counter)
        self.thread_counter += 1
        self.threads.append(thread)
        self.draw_thread(thread)
        return thread
    
    def draw_thread(self, thread):
        # Calculate position
        index = len([t for t in self.threads if t.canvas_id is not None])
        x = 50 + (index % 4) * 90
        y = 50 + (index // 4) * 90
        
        # Color based on state
        colors = {
            'waiting': '#e74c3c',
            'executing': '#2ecc71',
            'blocked': '#f39c12',
            'finished': '#95a5a6'
        }
        
        color = colors.get(thread.state, '#e74c3c')
        
        # Draw circle
        thread.canvas_id = self.threads_canvas.create_oval(
            x-30, y-30, x+30, y+30,
            fill=color, outline='white', width=2
        )
        
        # Draw text
        thread.text_id = self.threads_canvas.create_text(
            x, y, text=f"T{thread.id}",
            fill='white', font=('Arial', 12, 'bold')
        )
    
    def update_thread_display(self, thread):
        if thread.canvas_id is None:
            return
            
        colors = {
            'waiting': '#e74c3c',
            'executing': '#2ecc71',
            'blocked': '#f39c12',
            'finished': '#95a5a6'
        }
        
        color = colors.get(thread.state, '#e74c3c')
        self.threads_canvas.itemconfig(thread.canvas_id, fill=color)
        
        # Add pulsing effect for executing thread
        if thread.state == 'executing':
            self.pulse_thread(thread)
    
    def pulse_thread(self, thread):
        if thread.state == 'executing' and thread.canvas_id:
            # Simple pulsing effect by changing outline width
            current_width = self.threads_canvas.itemcget(thread.canvas_id, 'width')
            new_width = '4' if current_width == '2' else '2'
            self.threads_canvas.itemconfig(thread.canvas_id, width=new_width)
            
            if thread.state == 'executing':
                self.root.after(500, lambda: self.pulse_thread(thread))
    
    def update_monitor_display(self):
        self.counter_var.set(str(self.monitor.counter))
        
        if self.monitor.is_locked:
            self.mutex_var.set("🔐 BLOQUEADO")
            self.mutex_label.configure(fg='#e74c3c')
        else:
            self.mutex_var.set("🔓 DESBLOQUEADO")
            self.mutex_label.configure(fg='#2ecc71')
    
    def update_queue_display(self):
        self.queue_canvas.delete("all")
        
        blocked_threads = [t for t in self.threads if t.state == 'blocked']
        
        for i, thread in enumerate(blocked_threads):
            x = 30 + i * 60
            y = 40
            
            # Draw small circle for queued thread
            self.queue_canvas.create_oval(
                x-20, y-20, x+20, y+20,
                fill='#f39c12', outline='white', width=1
            )
            
            self.queue_canvas.create_text(
                x, y, text=f"T{thread.id}",
                fill='white', font=('Arial', 10, 'bold')
            )
    
    def start_simulation(self):
        self.simulation_running = True
        self.process_threads()
    
    def pause_simulation(self):
        self.simulation_running = False
    
    def reset_simulation(self):
        self.simulation_running = False
        
        # Reset monitor
        self.monitor = Monitor()
        
        # Reset all threads
        for thread in self.threads:
            thread.state = 'waiting'
            self.update_thread_display(thread)
        
        self.update_monitor_display()
        self.update_queue_display()
    
    def add_thread(self):
        self.create_thread()
    
    def process_threads(self):
        if not self.simulation_running:
            return
        
        # Process currently executing thread
        if self.monitor.current_thread:
            executing_thread = self.monitor.current_thread
            
            def finish_execution():
                if self.monitor.current_thread == executing_thread:
                    executing_thread.state = 'finished'
                    self.update_thread_display(executing_thread)
                    
                    next_thread = self.monitor.exit_monitor()
                    self.update_monitor_display()
                    
                    if next_thread:
                        next_thread.state = 'executing'
                        self.update_thread_display(next_thread)
                        self.monitor.try_enter(next_thread)
                        self.update_monitor_display()
                    
                    self.update_queue_display()
                    
                    # Continue processing
                    self.root.after(500, self.process_threads)
            
            # Schedule thread completion
            delay = int(executing_thread.work_time * 1000)
            self.root.after(delay, finish_execution)
            return
        
        # Try to start a new thread
        waiting_threads = [t for t in self.threads if t.state == 'waiting']
        blocked_threads = [t for t in self.threads if t.state == 'blocked']
        
        if waiting_threads:
            thread = waiting_threads[0]
            if self.monitor.try_enter(thread):
                thread.state = 'executing'
                self.update_thread_display(thread)
                self.update_monitor_display()
            else:
                thread.state = 'blocked'
                self.update_thread_display(thread)
            
            # Block other waiting threads
            for t in waiting_threads[1:]:
                if t.state == 'waiting':
                    t.state = 'blocked'
                    self.update_thread_display(t)
                    self.monitor.try_enter(t)  # Add to blocked list
        
        self.update_queue_display()
        
        # Check if we should restart finished threads
        all_finished = all(t.state == 'finished' for t in self.threads)
        if all_finished and self.threads:
            def restart_threads():
                for thread in self.threads:
                    thread.state = 'waiting'
                    thread.work_time = random.uniform(1, 4)
                    self.update_thread_display(thread)
                self.monitor.blocked_threads.clear()
                self.update_queue_display()
                self.root.after(500, self.process_threads)
            
            self.root.after(2000, restart_threads)
        else:
            # Continue processing
            self.root.after(1000, self.process_threads)
    
    def start_animation_loop(self):
        def animate():
            # Continuous animation updates
            if self.simulation_running:
                # Update any ongoing animations
                pass
            
            self.root.after(self.animation_speed, animate)
        
        animate()

def main():
    root = tk.Tk()
    app = MonitorSimulation(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
    
    
    
    