
# csv-oracle-data-type-analyzer

Una herramienta sencilla en Python para analizar archivos CSV y sugerir el tipo de dato de Oracle más adecuado para cada columna. La aplicación detecta si los valores son números, fechas, textos o booleanos, y utiliza el nombre de la columna para ayudar a decidir entre tipos como `NUMBER`, `VARCHAR2`, `DATE` o `TIMESTAMP`.

## Funcionalidades

- **Inferencia de tipos:**
  Determina si los valores de una columna son enteros, flotantes, fechas (o timestamps) o cadenas de texto. Se asegura de que solo se intente interpretar fechas si el valor contiene separadores comunes como `-`, `/` o `:`.

- **Heurísticas por nombre de columna:**
  - Columnas que contienen palabras como "document", "passport", "dni", etc., se tratan como texto.
  - Identificadores (por ejemplo, "id" o columnas que terminan en "_id") se asignan a `NUMBER` si son numéricos.
  - Columnas relacionadas con fechas (por ejemplo, que contienen "created", "updated" o "at") se evalúan para sugerir `DATE` o `TIMESTAMP`.

- **Soporte para booleanos:**
  Si todos los valores son booleanos (como `true`, `false`, `1` o `0`), se sugiere un tipo compacto como `CHAR(1)`.

- **Interfaz gráfica (GUI):**
  Con Tkinter se puede:
  - Seleccionar un archivo CSV.
  - Ingresar opcionalmente el nombre de una columna específica (o analizar todas si se deja vacío).
  - Visualizar los resultados en una ventana separada.

## Uso

1. **Clona el repositorio:**

   ```bash
   git clone <https://github.com/tu-usuario/csv-oracle-data-type-analyzer.git>
   cd csv-oracle-data-type-analyzer
    ```

2. **(Opcional) Activa un entorno virtual:**

    ```bash
    Copiar
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
    ```

3. **Ejecuta la aplicación:**

    ```bash
    python main.py
    ```

4.**En la interfaz:**
    - Haz clic en **"Seleccionar archivo CSV"** y elige tu archivo.
    - (Opcional) Ingresa el nombre de una columna en el campo **"Nombre de columna (opcional)"**. Si se deja en blanco, se analizarán todas las columnas.
    - Presiona **"Analizar"** para ver los resultados.

## Estructura del Proyecto

- **csv_processor.py:**

    Procesa el archivo CSV y calcula estadísticas (longitud máxima, frecuencia de tipos, etc.) para cada columna.

- **data_types.py:**

    Funciones para detectar el tipo de dato de cada valor y determinar el tipo predominante en una columna.

- **oracle_mapper.py:**

    Sugiere el tipo de dato de Oracle basándose en el análisis y en heurísticas relacionadas con el nombre de la columna.

- **ui.py:**

    Implementa la interfaz gráfica con Tkinter.

- **main.py:**

    Punto de entrada que inicia la aplicación.
