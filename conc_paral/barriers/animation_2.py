import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class BarrierAnimation:
  def __init__(self, root):
    self.root = root
    self.root.title("Barriers - Sincronización de Hilos")
    self.root.geometry("900x700")
    self.root.configure(bg='#2c3e50')
    
    # Variables de estado
    self.threads_data = []
    self.animation_running = False
    self.threads_at_barrier = 0
    self.animation_lock = threading.Lock()
    self.num_threads = 3  # Número inicial de hilos
    self.canvas_initialized = False
    
    # Colores para los hilos
    self.thread_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', 
                          '#e67e22', '#1abc9c', '#8e44ad', '#34495e', '#c0392b']
    
    self.setup_ui()
    
    # Bind para redimensionar
    self.root.bind('<Configure>', self.on_window_resize)
    
    # Inicializar hilos después de que el canvas esté listo
    self.root.after(100, self.initialize_threads)
      
  def setup_ui(self):
    # Título
    title_frame = tk.Frame(self.root, bg='#2c3e50')
    title_frame.pack(pady=10)
    
    title_label = tk.Label( title_frame, text="Barriers en Concurrencia", 
                            font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
    title_label.pack()
    
    subtitle_label = tk.Label(title_frame, text="Simulación de sincronización de hilos en Python",
                              font=('Arial', 12), fg='#bdc3c7', bg='#2c3e50')
    subtitle_label.pack()
    
    # Frame de controles de hilo (añadir/eliminar)
    thread_controls_frame = tk.Frame(self.root, bg='#2c3e50')
    thread_controls_frame.pack(pady=10)
    
    self.add_thread_btn = tk.Button(thread_controls_frame, text="➕ Añadir Hilo", 
                                    command=self.add_thread,
                                    bg='#2ecc71', fg='white', font=('Arial', 11, 'bold'),
                                    padx=15, pady=5, cursor='hand2')
    self.add_thread_btn.pack(side='left', padx=5)
    
    self.remove_thread_btn = tk.Button(thread_controls_frame, text="➖ Eliminar Hilo", 
                                      command=self.remove_thread,
                                      bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                      padx=15, pady=5, cursor='hand2')
    self.remove_thread_btn.pack(side='left', padx=5)
    
    # Label para mostrar número de hilos
    self.thread_count_label = tk.Label(thread_controls_frame, text=f"Hilos: {self.num_threads}", 
                                      font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#2c3e50')
    self.thread_count_label.pack(side='left', padx=20)
    
    # Frame principal para la animación
    self.canvas_frame = tk.Frame(self.root, bg='#34495e', relief='ridge', bd=2)
    self.canvas_frame.pack(padx=20, pady=10, fill='both', expand=True)
    
    # Canvas para la animación
    self.canvas = tk.Canvas(self.canvas_frame, bg='#34495e', highlightthickness=0)
    self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Frame de información
    info_frame = tk.Frame(self.root, bg='#2c3e50')
    info_frame.pack(pady=10)
    
    # Indicador de fase
    self.phase_label = tk.Label(info_frame, text="Fase: Inicial", 
                                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#2c3e50')
    self.phase_label.pack()
    
    # Status
    self.status_label = tk.Label(info_frame, 
                                text="Los hilos están listos. Presiona 'Iniciar Animación'",
                                font=('Arial', 12), fg='#bdc3c7', bg='#2c3e50', 
                                wraplength=700, justify='center')
    self.status_label.pack(pady=5)
    
    # Frame de controles principales
    controls_frame = tk.Frame(self.root, bg='#2c3e50')
    controls_frame.pack(pady=10)
    
    # Botones principales
    self.start_btn = tk.Button(controls_frame, text="🚀 Iniciar Animación", 
                              command=self.start_animation,
                              bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                              padx=20, pady=10, cursor='hand2')
    self.start_btn.pack(side='left', padx=10)
    
    self.reset_btn = tk.Button(controls_frame, text="🔄 Reiniciar", 
                              command=self.reset_animation,
                              bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                              padx=20, pady=10, cursor='hand2')
    self.reset_btn.pack(side='left', padx=10)
    
  def on_window_resize(self, event):
      """Manejar redimensionamiento de la ventana"""
      if event.widget == self.root and self.canvas_initialized:
          self.root.after(100, self.redraw_canvas)
  
  def redraw_canvas(self):
    """Redibujar el canvas después del redimensionamiento"""
    if not self.canvas_initialized:
      return
        
    # Obtener dimensiones actuales del canvas
    self.canvas.update_idletasks()
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    
    if canvas_width <= 1 or canvas_height <= 1:
      return
        
    # Limpiar canvas
    self.canvas.delete("all")
    
    # Calcular nueva posición del barrier
    self.barrier_y = canvas_height // 2
    
    # Dibujar el barrier
    barrier_margin = 50
    self.canvas.create_rectangle(barrier_margin, self.barrier_y-5, 
      canvas_width-barrier_margin, self.barrier_y+5, 
      fill='#e67e22', outline='#d35400', width=2
    )
    self.canvas.create_text(canvas_width//2, self.barrier_y-20, text="BARRIER", 
      fill='white', font=('Arial', 12, 'bold')
    )
    
    # Redistribuir hilos
    self.redistribute_threads()
      
  def redistribute_threads(self):
    """Redistribuir hilos en el canvas"""
    if not self.threads_data or not self.canvas_initialized:
      return
        
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    
    if canvas_width <= 1 or canvas_height <= 1:
      return
    
    # Calcular posiciones para distribuir hilos uniformemente
    margin = 80
    available_width = canvas_width - 2 * margin
    
    if len(self.threads_data) > 1:
      spacing = available_width / (len(self.threads_data) - 1)
    else:
      spacing = 0
        
    for i, thread in enumerate(self.threads_data):
      if len(self.threads_data) == 1:
        new_x = canvas_width // 2
      else:
        new_x = margin + i * spacing
          
      # Determinar Y basado en el estado del hilo
      if thread['state'] == 'inicial':
        new_y = 60
      elif thread['state'] == 'esperando':
        new_y = self.barrier_y - 30
      elif thread['state'] == 'completado':
        new_y = canvas_height - 60
      else:
        new_y = thread['y']  # Mantener posición actual si está en movimiento
      
      thread['x'] = new_x
      thread['initial_x'] = new_x
      
      if thread['state'] == 'inicial':
        thread['y'] = new_y
        thread['initial_y'] = new_y
      
      # Recrear los elementos del canvas
      self.canvas.delete(thread['canvas_id'])
      self.canvas.delete(thread['text_id'])
      
      thread['canvas_id'] = self.canvas.create_oval(new_x-20, new_y-20, new_x+20, new_y+20,
        fill=thread['color'], outline='white', width=2)
      thread['text_id'] = self.canvas.create_text(new_x, new_y, text=f"H{thread['id']+1}",
        fill='white', font=('Arial', 10, 'bold'))
      
  def initialize_threads(self):
    """Inicializar los hilos en el canvas"""
    # Asegurar que el canvas esté listo
    self.canvas.update_idletasks()
    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()
    
    if canvas_width <= 1 or canvas_height <= 1:
      # Reintentar después de un breve delay
      self.root.after(100, self.initialize_threads)
      return
    
    self.canvas_initialized = True
    self.barrier_y = canvas_height // 2
    
    # Dibujar el barrier inicial
    barrier_margin = 50
    self.canvas.create_rectangle(barrier_margin, self.barrier_y-5, 
      canvas_width-barrier_margin, self.barrier_y+5, 
      fill='#e67e22', outline='#d35400', width=2
    )
    self.canvas.create_text(canvas_width//2, self.barrier_y-20, text="BARRIER", 
      fill='white', font=('Arial', 12, 'bold')
    )
    
    self.threads_data = []
    
    for i in range(self.num_threads):
      self.create_thread(i)
        
    self.redistribute_threads()
  
  def create_thread(self, thread_id):
    """Crear un nuevo hilo"""
    if not self.canvas_initialized:
      return
        
    x = 100  # Posición temporal, se ajustará en redistribute_threads
    y = 60
    
    # Crear círculo en el canvas
    canvas_thread_id = self.canvas.create_oval(x-20, y-20, x+20, y+20,
      fill=self.thread_colors[thread_id % len(self.thread_colors)],
      outline='white', width=2
    )
    
    # Texto del hilo
    text_id = self.canvas.create_text(x, y, text=f"H{thread_id+1}",
      fill='white', font=('Arial', 10, 'bold')
    )
    
    # Información del hilo
    thread_info = {
      'id': thread_id,
      'canvas_id': canvas_thread_id,
      'text_id': text_id,
      'x': x,
      'y': y,
      'initial_x': x,
      'initial_y': y,
      'state': 'inicial',
      'color': self.thread_colors[thread_id % len(self.thread_colors)]
    }
    
    self.threads_data.append(thread_info)
      
  def add_thread(self):
    """Añadir un nuevo hilo"""
    if self.animation_running or not self.canvas_initialized:
      return
        
    if len(self.threads_data) >= 10:  # Límite máximo
      return
        
    self.num_threads += 1
    new_thread_id = len(self.threads_data)
    self.create_thread(new_thread_id)
    self.thread_count_label.config(text=f"Hilos: {self.num_threads}")
    self.redistribute_threads()
    
  def remove_thread(self):
    """Eliminar un hilo"""
    if self.animation_running or not self.canvas_initialized:
      return
        
    if len(self.threads_data) <= 1:  # Mínimo un hilo
      return
        
    # Eliminar el último hilo
    thread_to_remove = self.threads_data.pop()
    self.canvas.delete(thread_to_remove['canvas_id'])
    self.canvas.delete(thread_to_remove['text_id'])
    
    self.num_threads -= 1
    self.thread_count_label.config(text=f"Hilos: {self.num_threads}")
    self.redistribute_threads()
  
  def update_status(self, message):
    """Actualizar el mensaje de estado"""
    self.status_label.config(text=message)
    self.root.update()
  
  def update_phase(self, phase):
    """Actualizar la fase actual"""
    self.phase_label.config(text=f"Fase: {phase}")
    self.root.update()
  
  def animate_thread_to_barrier(self, thread_index, delay=0):
    """Animar un hilo hacia el barrier"""
    if delay > 0:
      time.sleep(delay)
        
    thread = self.threads_data[thread_index]
    thread['state'] = 'moviendo'
    
    # Calcular movimiento
    start_y = thread['y']
    end_y = self.barrier_y - 30
    steps = 30
    
    for step in range(steps):
      if not self.animation_running:
        return
          
      new_y = start_y + (end_y - start_y) * (step / steps)
      
      # Actualizar posición en canvas
      self.root.after(0, lambda: self.canvas.coords(
        thread['canvas_id'], 
        thread['x']-20, new_y-20, 
        thread['x']+20, new_y+20)
      )
      self.root.after(0, lambda: self.canvas.coords(
        thread['text_id'], 
        thread['x'], new_y)
      )
      
      thread['y'] = new_y
      time.sleep(0.05)
    
    # Hilo llegó al barrier
    with self.animation_lock:
      self.threads_at_barrier += 1
      thread['state'] = 'esperando'
      
      self.root.after(0, lambda: self.update_status(
        f"Hilo {thread_index+1} llegó al barrier. Esperando... ({self.threads_at_barrier}/{len(self.threads_data)})"))
      
      # Animación de espera (pulsación)
      threading.Thread(target=self.pulse_thread, args=(thread_index,), daemon=True).start()
      
      # Si todos los hilos llegaron, liberar
      if self.threads_at_barrier == len(self.threads_data):
        threading.Thread(target=self.release_all_threads, daemon=True).start()
  
  def pulse_thread(self, thread_index):
    """Animación de pulsación mientras espera"""
    thread = self.threads_data[thread_index]
    
    while thread['state'] == 'esperando' and self.animation_running:
      # Expandir
      for scale in [1.0, 1.1, 1.2, 1.1, 1.0]:
        if thread['state'] != 'esperando' or not self.animation_running:
          break
            
        size = 20 * scale
        self.root.after(0, lambda s=size: self.canvas.coords(
          thread['canvas_id'],
          thread['x']-s, thread['y']-s,
          thread['x']+s, thread['y']+s)
        )
        time.sleep(0.1)
      
      time.sleep(0.5)
  
  def release_all_threads(self):
    """Liberar todos los hilos del barrier"""
    time.sleep(1)  # Pausa antes de liberar
    
    self.root.after(0, lambda: self.update_phase("Sincronización Completada"))
    self.root.after(0, lambda: self.update_status("¡Todos los hilos llegaron! Continuando ejecución..."))
    
    # Animar hilos continuando
    for i, thread in enumerate(self.threads_data):
      thread['state'] = 'continuando'
      threading.Thread(target=self.animate_thread_continue, args=(i,), daemon=True).start()
  
  def animate_thread_continue(self, thread_index):
    """Animar hilo continuando después del barrier"""
    thread = self.threads_data[thread_index]
    
    start_y = thread['y']
    canvas_height = self.canvas.winfo_height()
    end_y = canvas_height - 60
    steps = 30
    
    for step in range(steps):
      if not self.animation_running:
        return
          
      new_y = start_y + (end_y - start_y) * (step / steps)
      
      # Restaurar tamaño normal
      self.root.after(0, lambda: self.canvas.coords(
        thread['canvas_id'],
        thread['x']-20, new_y-20,
        thread['x']+20, new_y+20)
      )
      self.root.after(0, lambda: self.canvas.coords(
        thread['text_id'],
        thread['x'], new_y)
      )
      
      thread['y'] = new_y
      time.sleep(0.05)
    
    thread['state'] = 'completado'
    
    # Verificar si todos terminaron
    completed = sum(1 for t in self.threads_data if t['state'] == 'completado')
    if completed == len(self.threads_data):
        self.root.after(0, lambda: self.update_status("¡Sincronización completada! Todos los hilos pasaron el barrier."))
        self.root.after(0, lambda: self.update_phase("Finalizada"))
  
  def start_animation(self):
    """Iniciar la animación completa"""
    if self.animation_running: return
        
    self.reset_animation()
    time.sleep(0.1)
    
    self.animation_running = True
    
    self.update_phase("Movimiento hacia el Barrier")
    self.update_status("Los hilos se mueven hacia el barrier...")
    
    # Generar delays aleatorios para cada hilo
    delays = [random.uniform(0, 2) for _ in range(len(self.threads_data))]
    
    for i in range(len(self.threads_data)):
      threading.Thread(target=self.animate_thread_to_barrier, args=(i, delays[i]), daemon=True).start()
  
  def reset_animation(self):
    """Reiniciar la animación"""
    self.animation_running = False
    self.threads_at_barrier = 0
    
    # Restaurar posiciones iniciales
    for thread in self.threads_data:
      thread['x'] = thread['initial_x']
      thread['y'] = thread['initial_y']
      thread['state'] = 'inicial'
        
      self.canvas.coords(
        thread['canvas_id'],
        thread['x']-20, thread['y']-20,
        thread['x']+20, thread['y']+20)
      self.canvas.coords(thread['text_id'], thread['x'], thread['y'])
    
    self.update_status("Los hilos están listos. Presiona 'Iniciar Animación'")
    self.update_phase("Inicial")

def main():
  root = tk.Tk()
  app = BarrierAnimation(root)
  
  # Centrar ventana
  root.update_idletasks()
  x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
  y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
  root.geometry(f"+{x}+{y}")
  
  root.mainloop()

if __name__ == "__main__":
  main()