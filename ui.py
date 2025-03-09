import tkinter as tk
from tkinter import filedialog, messagebox
from csv_processor import analyze_csv_column, analyze_all_columns

class CsvAnalyzerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis CSV para Oracle")
        self.root.geometry("600x200")
        
        self.file_entry_var = tk.StringVar()
        
        self._create_widgets()
        self._center_window(self.root)
        
    def _create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill="x")
        
        select_button = tk.Button(frame, text="Seleccionar archivo CSV", command=self._select_file)
        select_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Se asigna un ancho fijo al label para la ruta del archivo
        file_label = tk.Label(frame, textvariable=self.file_entry_var, width=60, anchor="w")
        file_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        column_label = tk.Label(frame, text="Nombre de columna (opcional):")
        column_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.column_entry = tk.Entry(frame, width=30)
        self.column_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        analyze_button = tk.Button(frame, text="Analizar", command=self._analyze_file)
        analyze_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
    
    def _select_file(self):
        file = filedialog.askopenfilename(
            title="Selecciona un archivo CSV",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if file:
            self.file_entry_var.set(file)
    
    def _center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _analyze_file(self):
        file_path = self.file_entry_var.get()
        if not file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo CSV primero.")
            return

        col_name = self.column_entry.get().strip()
        try:
            result_text = ""
            if col_name:
                result = analyze_csv_column(file_path, col_name)

                result_text += f"Columna: {result['column_name']}\n"
                result_text += f"  Longitud máxima: {result['max_length']}\n"
                result_text += f"  Tipo de datos (mayoría): {result['final_type']}\n"
                result_text += f"  Sugerencia de tipo Oracle: {result['oracle_type']}\n"
                result_text += f"  Total de registros: {result['total_values']}\n"
                result_text += f"  Registros no vacíos: {result['non_empty_values']}\n"
                result_text += f"  % de registros no vacíos: {result['non_empty_ratio']}%\n"
                result_text += f"  % de registros vacíos: {result['empty_ratio']}%\n"
                result_text += f"  ¿Sugerir NOT NULL?: {'Sí' if result['sugerir_not_null'] else 'No'}\n"
            else:
                results = analyze_all_columns(file_path)

                for col, result in results.items():
                    result_text += f"Columna: {result['column_name']}\n"
                    result_text += f"  Longitud máxima: {result['max_length']}\n"
                    result_text += f"  Tipo de datos (mayoría): {result['final_type']}\n"
                    result_text += f"  Sugerencia de tipo Oracle: {result['oracle_type']}\n"
                    result_text += f"  Total de registros: {result['total_values']}\n"
                    result_text += f"  Registros no vacíos: {result['non_empty_values']}\n"
                    result_text += f"  % de registros no vacíos: {result['non_empty_ratio']}%\n"
                    result_text += f"  % de registros vacíos: {result['empty_ratio']}%\n"
                    result_text += f"  ¿Sugerir NOT NULL?: {'Sí' if result['sugerir_not_null'] else 'No'}\n\n"

            # Mostrar resultados en una ventana secundaria
            result_window = tk.Toplevel(self.root)
            result_window.title("Resultados del análisis")
            text_widget = tk.Text(result_window, wrap="word", width=100, height=30)
            text_widget.pack(expand=True, fill="both")
            text_widget.insert("1.0", result_text)
            text_widget.config(state="disabled")
            self._center_window(result_window)

        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar el archivo:\n{str(e)}")

