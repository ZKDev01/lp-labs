import time
import threading
from typing import Dict

import tkinter as tk
from tkinter import ttk


class Countdown:
  def __init__(self, root, counter:int=3):
    self.root = root
    self.root.title("Mecanismo de Sincronización: Countdown")
    self.root.geometry("900x700")
    self.root.configure(bg='#2c3e50')
    
    # Variables del estado
    self.counter = counter
    self.is_running = False
    self.operations = [
      {'name': 'Cargar Base de Datos', 'duration': 2.0, 'status': 'waiting', 'progress': 0},
      {'name': 'Inicializar Cache', 'duration': 1.5, 'status': 'waiting', 'progress': 0},
      {'name': 'Configurar Red', 'duration': 2.5, 'status': 'waiting', 'progress': 0}
    ]
    self.threads = [
      {'name': 'Hilo Principal', 'status': 'waiting'},
      {'name': 'Hilo Worker 1', 'status': 'waiting'},
      {'name': 'Hilo Worker 2', 'status': 'waiting'},
      {'name': 'Hilo UI', 'status': 'waiting'},
      {'name': 'Hilo Logger', 'status': 'waiting'}
    ]
    
    # Crear el latch real para demostración
    self.latch = threading.Event()
    self.operation_locks = [threading.Lock() for _ in self.operations]
    
    self.setup_ui()
    self.update_display()

  def setup_ui(self):
    # Título principal
    title_frame = tk.Frame(self.root, bg='#2c3e50')
    title_frame.pack(pady=10)
    
    title_label = tk.Label(
      title_frame, 
      text="🔄 Countdown Latches", 
      font=('Arial', 24, 'bold'),
      fg='#ecf0f1',
      bg='#2c3e50'
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
      title_frame,
      text="Mecanismo de sincronización para hilos concurrentes",
      font=('Arial', 12),
      fg='#bdc3c7',
      bg='#2c3e50'
    )
    subtitle_label.pack()
    
    # Sección del contador
    self.counter_frame = tk.LabelFrame(
      self.root,
      text="Contador del Latch",
      font=('Arial', 12, 'bold'),
      fg='#f39c12',
      bg='#34495e',
      padx=10,
      pady=10
    )
    self.counter_frame.pack(fill='x', padx=20, pady=10)
    
    self.counter_label = tk.Label(
      self.counter_frame,
      text="3",
      font=('Arial', 48, 'bold'),
      fg='#f1c40f',
      bg='#34495e'
    )
    self.counter_label.pack()
    
    counter_desc = tk.Label(
      self.counter_frame,
      text="Operaciones pendientes",
      font=('Arial', 12),
      fg='#ecf0f1',
      bg='#34495e'
    )
    counter_desc.pack()
    
    # Sección de operaciones
    self.operations_frame = tk.LabelFrame(
      self.root,
      text="📊 Operaciones en Ejecución",
      font=('Arial', 12, 'bold'),
      fg='#f39c12',
      bg='#34495e',
      padx=10,
      pady=10
    )
    self.operations_frame.pack(fill='both', expand=True, padx=20, pady=5)
    
    self.operation_widgets = []
    for i, op in enumerate(self.operations):
      op_frame = tk.Frame(self.operations_frame, bg='#34495e', relief='raised', bd=2)
      op_frame.pack(fill='x', pady=5)
      
      # Nombre de la operación
      name_label = tk.Label(
        op_frame,
        text=op['name'],
        font=('Arial', 12, 'bold'),
        fg='#ecf0f1',
        bg='#34495e'
      )
      name_label.pack(anchor='w', padx=10, pady=5)
      
      # Estado
      status_label = tk.Label(
        op_frame,
        text="En espera",
        font=('Arial', 10),
        fg='#95a5a6',
        bg='#34495e'
      )
      status_label.pack(anchor='w', padx=10)
      
      # Barra de progreso
      progress_bar = ttk.Progressbar(
        op_frame,
        length=300,
        mode='determinate',
        maximum=100
      )
      progress_bar.pack(anchor='w', padx=10, pady=5)
      
      self.operation_widgets.append({
        'frame': op_frame,
        'status_label': status_label,
        'progress_bar': progress_bar
      })
    
    # Sección de hilos
    self.threads_frame = tk.LabelFrame(
      self.root,
      text="🧵 Hilos Esperando",
      font=('Arial', 12, 'bold'),
      fg='#f39c12',
      bg='#34495e',
      padx=10,
      pady=10
    )
    self.threads_frame.pack(fill='x', padx=20, pady=5)
    
    # Frame para los hilos en grid
    threads_grid = tk.Frame(self.threads_frame, bg='#34495e')
    threads_grid.pack()
    
    self.thread_widgets = []
    for i, thread in enumerate(self.threads):
      row = i // 3
      col = i % 3
      
      thread_frame = tk.Frame(
        threads_grid, 
        bg='#2c3e50', 
        relief='raised', 
        bd=2,
        width=120,
        height=80
      )
      thread_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
      thread_frame.pack_propagate(False)
      
      name_label = tk.Label(
        thread_frame,
        text=thread['name'],
        font=('Arial', 9, 'bold'),
        fg='#ecf0f1',
        bg='#2c3e50',
        wraplength=100
      )
      name_label.pack(pady=5)
      
      status_label = tk.Label(
        thread_frame,
        text="⏳ Esperando",
        font=('Arial', 8),
        fg='#f39c12',
        bg='#2c3e50'
      )
      status_label.pack()
      
      self.thread_widgets.append({
        'frame': thread_frame,
        'status_label': status_label
      })
    
    # Botones de control
    control_frame = tk.Frame(self.root, bg='#2c3e50')
    control_frame.pack(pady=20)
    
    self.start_button = tk.Button(
      control_frame,
      text="Iniciar Demostración",
      font=('Arial', 12, 'bold'),
      bg='#e74c3c',
      fg='white',
      padx=20,
      pady=10,
      command=self.start_demo,
      cursor='hand2'
    )
    self.start_button.pack(side='left', padx=10)
    
    self.reset_button = tk.Button(
      control_frame,
      text="Reiniciar",
      font=('Arial', 12, 'bold'),
      bg='#3498db',
      fg='white',
      padx=20,
      pady=10,
      command=self.reset_demo,
      cursor='hand2'
    )
    self.reset_button.pack(side='left', padx=10)
    
    # Explicación
    explanation_frame = tk.LabelFrame(
      self.root,
      text="¿Cómo funciona?",
      font=('Arial', 12, 'bold'),
      fg='#f39c12',
      bg='#34495e',
      padx=10,
      pady=10
    )
    explanation_frame.pack(fill='x', padx=20, pady=10)
    
    explanation_text = tk.Label(
      explanation_frame,
      text="Un Countdown Latch permite que múltiples hilos esperen hasta que se complete\n"
            "un conjunto específico de operaciones. Cada operación completada decrementa\n"
            "el contador, y cuando llega a cero, todos los hilos son liberados simultáneamente.",
      font=('Arial', 10),
      fg='#ecf0f1',
      bg='#34495e',
      justify='left'
    )
    explanation_text.pack()
    
  def update_display(self):
    # Actualizar contador
    self.counter_label.config(text=str(self.counter))
    if self.counter == 0:
      self.counter_label.config(fg='#27ae60')
    else:
      self.counter_label.config(fg='#f1c40f')
    
    # Actualizar operaciones
    for i, (op, widget) in enumerate(zip(self.operations, self.operation_widgets)):
      if op['status'] == 'waiting':
        widget['status_label'].config(text="En espera", fg='#95a5a6')
        widget['frame'].config(bg='#34495e')
      elif op['status'] == 'running':
        widget['status_label'].config(text="Ejecutando...", fg='#e74c3c')
        widget['frame'].config(bg='#c0392b')
      else:  # completed
        widget['status_label'].config(text="Completado", fg='#27ae60')
        widget['frame'].config(bg='#27ae60')
      
      widget['progress_bar']['value'] = op['progress']
        
    # Actualizar hilos
    for i, (thread, widget) in enumerate(zip(self.threads, self.thread_widgets)):
      if thread['status'] == 'waiting':
        widget['status_label'].config(text="⏳ Esperando", fg='#f39c12')
        widget['frame'].config(bg='#2c3e50')
      else:  # released
        widget['status_label'].config(text="✅ Liberado", fg='#27ae60')
        widget['frame'].config(bg='#27ae60')
    
  def simulate_operation(self, operation_index):
    """Simula la ejecución de una operación en un hilo separado"""
    operation = self.operations[operation_index]
    operation['status'] = 'running'
    operation['progress'] = 0
        
    # Actualizar UI desde el hilo principal
    self.root.after(0, self.update_display)
        
    # Simular progreso
    duration = operation['duration']
    steps = 20
    step_time = duration / steps
        
    for step in range(steps + 1):
      if not self.is_running:  # Si se reinicia, salir
        return
                
      operation['progress'] = (step / steps) * 100
      self.root.after(0, self.update_display)
      time.sleep(step_time)
        
    # Marcar como completado
    operation['status'] = 'completed'
    operation['progress'] = 100
        
    # Decrementar contador (thread-safe)
    with self.operation_locks[operation_index]:
      self.counter -= 1
            
      # Actualizar UI
      self.root.after(0, self.update_display)
            
      # Si todas las operaciones terminaron, liberar hilos
      if self.counter == 0:
        self.root.after(0, self.release_all_threads)
    
  def release_all_threads(self):
    """Libera todos los hilos cuando el contador llega a 0"""
    time.sleep(0.3)  # Pequeña pausa para efecto visual
    
    for thread in self.threads:
      thread['status'] = 'released'
    
    self.update_display()
    
    # Habilitar botón de reset
    self.start_button.config(state='disabled')
    self.reset_button.config(state='normal')
    self.is_running = False
    
    # Establecer el evento del latch
    self.latch.set()
    
  def start_demo(self):
    """Inicia la demostración"""
    if self.is_running: return

    self.is_running = True
    self.start_button.config(state='disabled')
    self.reset_button.config(state='disabled')
    
    # Limpiar el latch
    self.latch.clear()
    
    # Iniciar todas las operaciones en hilos separados
    for i in range(len(self.operations)):
      thread = threading.Thread(
        target=self.simulate_operation,
        args=(i,),
        daemon=True
      )
      thread.start()
    
  def reset_demo(self):
    """Reinicia la demostración"""
    self.is_running = False
    self.counter = 3
    
    # Resetear operaciones
    for op in self.operations:
      op['status'] = 'waiting'
      op['progress'] = 0
    
    # Resetear hilos
    for thread in self.threads:
      thread['status'] = 'waiting'
    
    # Habilitar botones
    self.start_button.config(state='normal')
    self.reset_button.config(state='normal')
    
    # Limpiar el latch
    self.latch.clear()
    
    # Actualizar display
    self.update_display()

def main():
  root = tk.Tk()
  app = Countdown(root)
  
  # Configurar el cierre de la aplicación
  def on_closing():
    app.is_running = False
    root.quit()
    root.destroy()
  
  root.protocol("WM_DELETE_WINDOW", on_closing)
  root.mainloop()

if __name__ == "__main__":
  main()