import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime
import random

class SemaphoreSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 Simulador de Semáforos - Programación Concurrente")
        self.root.geometry("1000x800")
        self.root.configure(bg='#2c3e50')
        
        # Variables del semáforo
        self.semaphore_value = 3
        self.waiting_queue = []
        self.active_processes = []
        self.process_states = {1: 'waiting', 2: 'waiting', 3: 'waiting', 4: 'waiting', 5: 'waiting'}
        self.auto_running = False
        self.auto_thread = None
        
        # Colores
        self.colors = {
            'bg': '#2c3e50',
            'panel': '#34495e',
            'waiting': '#95a5a6',
            'active': '#27ae60',
            'blocked': '#e74c3c',
            'queue': '#f39c12',
            'text': '#ecf0f1',
            'button': '#3498db'
        }
        
        self.setup_ui()
        self.update_display()
        self.add_log("Simulación inicializada. Semáforo con valor 3")
    
    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="🚦 Semáforos en Programación Concurrente", 
                              font=('Arial', 18, 'bold'), fg=self.colors['text'], bg=self.colors['bg'])
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Mecanismo de sincronización para controlar el acceso a recursos compartidos",
                                 font=('Arial', 10), fg=self.colors['text'], bg=self.colors['bg'])
        subtitle_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Panel superior (Semáforo y recursos)
        top_panel = tk.Frame(main_frame, bg=self.colors['panel'], relief=tk.RAISED, bd=2)
        top_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Semáforo
        semaphore_frame = tk.Frame(top_panel, bg=self.colors['panel'])
        semaphore_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(semaphore_frame, text="Semáforo", font=('Arial', 14, 'bold'), 
                fg=self.colors['text'], bg=self.colors['panel']).pack()
        
        self.semaphore_label = tk.Label(semaphore_frame, text="3", font=('Arial', 36, 'bold'),
                                       fg=self.colors['active'], bg=self.colors['panel'])
        self.semaphore_label.pack()
        
        tk.Label(semaphore_frame, text="Valor actual", font=('Arial', 10),
                fg=self.colors['text'], bg=self.colors['panel']).pack()
        
        # Recursos
        resources_frame = tk.Frame(top_panel, bg=self.colors['panel'])
        resources_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        tk.Label(resources_frame, text="Recursos Compartidos (Máximo 3)", font=('Arial', 12, 'bold'),
                fg=self.colors['text'], bg=self.colors['panel']).pack()
        
        self.resources_frame_inner = tk.Frame(resources_frame, bg=self.colors['panel'])
        self.resources_frame_inner.pack(pady=10)
        
        self.resource_labels = []
        for i in range(3):
            resource_label = tk.Label(self.resources_frame_inner, text=f"R{i+1}", 
                                    font=('Arial', 12, 'bold'), width=4, height=2,
                                    bg=self.colors['active'], fg='white', relief=tk.RAISED, bd=2)
            resource_label.grid(row=0, column=i, padx=5)
            self.resource_labels.append(resource_label)
        
        # Panel de procesos
        processes_frame = tk.LabelFrame(main_frame, text="Procesos", font=('Arial', 12, 'bold'),
                                       fg=self.colors['text'], bg=self.colors['panel'])
        processes_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.process_frames = {}
        for i in range(1, 6):
            process_frame = tk.Frame(processes_frame, bg=self.colors['waiting'], 
                                   relief=tk.RAISED, bd=2, width=120, height=80)
            process_frame.pack(side=tk.LEFT, padx=10, pady=10)
            process_frame.pack_propagate(False)
            
            tk.Label(process_frame, text=f"Proceso {i}", font=('Arial', 10, 'bold'),
                    bg=self.colors['waiting']).pack(pady=5)
            
            status_label = tk.Label(process_frame, text="Esperando", font=('Arial', 9),
                                   bg=self.colors['waiting'])
            status_label.pack()
            
            self.process_frames[i] = {'frame': process_frame, 'status': status_label}
        
        # Cola de espera
        queue_frame = tk.LabelFrame(main_frame, text="Cola de Espera", font=('Arial', 12, 'bold'),
                                   fg=self.colors['text'], bg=self.colors['panel'])
        queue_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.queue_frame_inner = tk.Frame(queue_frame, bg=self.colors['panel'], height=60)
        self.queue_frame_inner.pack(fill=tk.X, padx=10, pady=10)
        
        self.queue_label = tk.Label(self.queue_frame_inner, text="Los procesos bloqueados aparecerán aquí",
                                   font=('Arial', 10), fg=self.colors['text'], bg=self.colors['panel'])
        self.queue_label.pack(pady=20)
        
        # Controles
        controls_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones Wait
        wait_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        wait_frame.pack(pady=5)
        
        for i in range(1, 6):
            btn = tk.Button(wait_frame, text=f"Proceso {i} - Wait()", 
                           command=lambda p=i: self.simulate_wait(p),
                           bg=self.colors['button'], fg='white', font=('Arial', 10),
                           padx=10, pady=5, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Botones de control
        control_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        control_frame.pack(pady=5)
        
        self.signal_btn = tk.Button(control_frame, text="Signal()", command=self.simulate_signal,
                                   bg=self.colors['blocked'], fg='white', font=('Arial', 10, 'bold'),
                                   padx=15, pady=5, cursor='hand2', state=tk.DISABLED)
        self.signal_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(control_frame, text="Reset", command=self.reset_simulation,
                             bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'),
                             padx=15, pady=5, cursor='hand2')
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.auto_btn = tk.Button(control_frame, text="Auto Simulación", command=self.toggle_auto_simulation,
                                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                                 padx=15, pady=5, cursor='hand2')
        self.auto_btn.pack(side=tk.LEFT, padx=5)
        
        # Panel inferior con información y log
        bottom_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información
        info_frame = tk.LabelFrame(bottom_frame, text="Información del Semáforo", 
                                  font=('Arial', 12, 'bold'), fg=self.colors['text'], bg=self.colors['panel'])
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = ("Wait(): Decrementa el contador. Si es ≤ 0, el proceso se bloquea.\n"
                    "Signal(): Incrementa el contador y desbloquea un proceso en espera.")
        tk.Label(info_frame, text=info_text, font=('Arial', 10), justify=tk.LEFT,
                fg=self.colors['text'], bg=self.colors['panel']).pack(padx=10, pady=5)
        
        stats_frame = tk.Frame(info_frame, bg=self.colors['panel'])
        stats_frame.pack(padx=10, pady=5)
        
        self.stats_labels = {}
        stats_text = ["Valor actual: 3", "Procesos activos: 0", "Procesos bloqueados: 0"]
        for i, text in enumerate(stats_text):
            label = tk.Label(stats_frame, text=text, font=('Arial', 10, 'bold'),
                           fg=self.colors['text'], bg=self.colors['panel'])
            label.grid(row=0, column=i, padx=20, sticky='w')
            self.stats_labels[i] = label
        
        # Log
        log_frame = tk.LabelFrame(bottom_frame, text="Log de Eventos", font=('Arial', 12, 'bold'),
                                 fg=self.colors['text'], bg=self.colors['panel'])
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=('Courier', 9),
                                                 bg='#1a1a1a', fg='#00ff00', insertbackground='white')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_display(self):
        # Actualizar valor del semáforo
        self.semaphore_label.config(text=str(self.semaphore_value))
        if self.semaphore_value > 0:
            self.semaphore_label.config(fg=self.colors['active'])
        else:
            self.semaphore_label.config(fg=self.colors['blocked'])
        
        # Actualizar procesos
        for i in range(1, 6):
            state = self.process_states[i]
            frame = self.process_frames[i]['frame']
            status = self.process_frames[i]['status']
            
            if state == 'waiting':
                frame.config(bg=self.colors['waiting'])
                status.config(text="Esperando", bg=self.colors['waiting'])
            elif state == 'active':
                frame.config(bg=self.colors['active'])
                status.config(text="Usando recurso", bg=self.colors['active'])
            elif state == 'blocked':
                frame.config(bg=self.colors['blocked'])
                status.config(text="Bloqueado", bg=self.colors['blocked'])
        
        # Actualizar recursos
        for i, label in enumerate(self.resource_labels):
            if i < len(self.active_processes):
                label.config(bg=self.colors['blocked'])
            else:
                label.config(bg=self.colors['active'])
        
        # Actualizar cola de espera
        for widget in self.queue_frame_inner.winfo_children():
            widget.destroy()
        
        if not self.waiting_queue:
            self.queue_label = tk.Label(self.queue_frame_inner, text="Los procesos bloqueados aparecerán aquí",
                                       font=('Arial', 10), fg=self.colors['text'], bg=self.colors['panel'])
            self.queue_label.pack(pady=20)
        else:
            queue_inner = tk.Frame(self.queue_frame_inner, bg=self.colors['panel'])
            queue_inner.pack(pady=10)
            
            for i, process_id in enumerate(self.waiting_queue):
                queue_item = tk.Label(queue_inner, text=f"Proceso {process_id}",
                                     font=('Arial', 10, 'bold'), bg=self.colors['queue'],
                                     fg='white', padx=10, pady=5, relief=tk.RAISED, bd=2)
                queue_item.pack(side=tk.LEFT, padx=5)
        
        # Actualizar estadísticas
        self.stats_labels[0].config(text=f"Valor actual: {self.semaphore_value}")
        self.stats_labels[1].config(text=f"Procesos activos: {len(self.active_processes)}")
        self.stats_labels[2].config(text=f"Procesos bloqueados: {len(self.waiting_queue)}")
        
        # Actualizar botón Signal
        if self.active_processes:
            self.signal_btn.config(state=tk.NORMAL)
        else:
            self.signal_btn.config(state=tk.DISABLED)
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"{timestamp}: {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def simulate_wait(self, process_id):
        if self.process_states[process_id] != 'waiting':
            self.add_log(f"Proceso {process_id} ya está en uso o bloqueado")
            return
        
        self.add_log(f"Proceso {process_id} ejecuta Wait()")
        
        if self.semaphore_value > 0:
            self.semaphore_value -= 1
            self.process_states[process_id] = 'active'
            self.active_processes.append(process_id)
            self.add_log(f"Proceso {process_id} obtiene recurso. Semáforo: {self.semaphore_value}")
        else:
            self.process_states[process_id] = 'blocked'
            self.waiting_queue.append(process_id)
            self.add_log(f"Proceso {process_id} bloqueado. Agregado a cola de espera")
        
        self.update_display()
    
    def simulate_signal(self):
        if not self.active_processes:
            self.add_log("No hay procesos activos para liberar recursos")
            return
        
        process_id = self.active_processes.pop(0)
        self.process_states[process_id] = 'waiting'
        self.semaphore_value += 1
        
        self.add_log(f"Proceso {process_id} ejecuta Signal(). Recurso liberado. Semáforo: {self.semaphore_value}")
        
        # Verificar si hay procesos esperando
        if self.waiting_queue:
            next_process = self.waiting_queue.pop(0)
            self.semaphore_value -= 1
            self.process_states[next_process] = 'active'
            self.active_processes.append(next_process)
            self.add_log(f"Proceso {next_process} despertado de la cola y obtiene recurso. Semáforo: {self.semaphore_value}")
        
        self.update_display()
    
    def reset_simulation(self):
        self.auto_running = False
        if self.auto_thread and self.auto_thread.is_alive():
            self.auto_thread.join(timeout=1)
        
        self.semaphore_value = 3
        self.waiting_queue = []
        self.active_processes = []
        self.process_states = {1: 'waiting', 2: 'waiting', 3: 'waiting', 4: 'waiting', 5: 'waiting'}
        
        self.log_text.delete(1.0, tk.END)
        self.add_log("Simulación reiniciada")
        self.auto_btn.config(text="Auto Simulación")
        self.update_display()
    
    def toggle_auto_simulation(self):
        if self.auto_running:
            self.auto_running = False
            self.auto_btn.config(text="Auto Simulación")
        else:
            self.auto_running = True
            self.auto_btn.config(text="Detener Auto")
            self.auto_thread = threading.Thread(target=self.run_auto_simulation, daemon=True)
            self.auto_thread.start()
    
    def run_auto_simulation(self):
        while self.auto_running:
            try:
                waiting_processes = [p for p, state in self.process_states.items() if state == 'waiting']
                has_active_processes = len(self.active_processes) > 0
                
                if random.random() < 0.6 and waiting_processes:
                    # 60% probabilidad de hacer Wait() con un proceso en espera
                    random_process = random.choice(waiting_processes)
                    self.root.after(0, lambda: self.simulate_wait(random_process))
                elif has_active_processes:
                    # 40% probabilidad de hacer Signal() si hay procesos activos
                    self.root.after(0, self.simulate_signal)
                
                time.sleep(2)
            except Exception as e:
                print(f"Error en simulación automática: {e}")
                break

def main():
    root = tk.Tk()
    app = SemaphoreSimulator(root)
    
    # Configurar el cierre de la aplicación
    def on_closing():
        app.auto_running = False
        if app.auto_thread and app.auto_thread.is_alive():
            app.auto_thread.join(timeout=1)
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()