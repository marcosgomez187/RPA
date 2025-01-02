import os
import pandas as pd
from typing import List, Dict, Optional, Union


class ExcelReader:

    def __init__(self, base_path: Optional[str] = None):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
        self.base_path = base_path if base_path else os.path.join(project_root, 'app/data/excels/')
        
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
            print(f"Se creó el directorio: {self.base_path}")

    def read_excel_to_json(self, file_name: str, columns: Dict[str, type], sheet_name: Union[str, int] = 0) -> List[Dict]:
        try:

            # Armo la ruta
            file_path = os.path.join(self.base_path, file_name)
            print(f"\nLeyendo archivo: {file_path}")

            column_names = list(columns.keys())
            
            # Leo el excel con filtros para ser mas especifico y no traer información necesaria
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                usecols=column_names,  # Lee solo las columnas necesarias
                dtype=columns,  # Asocia cada columna con su tipo
                na_values=["", "NA", "n/a"],  # Identificar valores nulos
                nrows=5  # Las primeras 5 filas
            )

            
            # Muestro lo capturado
            print("\nColumnas disponibles en el archivo:")
            for col in df.columns:
                print(f"- {col}")
                # Mostrar primeros valores para ayudar en la identificación
                sample_values = df[col].dropna().head(2).tolist()
                print(f"  Primeros valores: {sample_values}\n")

            # Mapear columnas requeridas a columnas existentes
            column_mapping = {}
            for required_col in columns:
                # Normalizar nombres para comparación
                req_col_normal = required_col.lower().strip()
                
                # Buscar coincidencia en las columnas existentes
                found = False
                for excel_col in df.columns:
                    excel_col_normal = str(excel_col).lower().strip()
                    
                    # Verificar coincidencia exacta o parcial
                    if (req_col_normal in excel_col_normal or 
                        excel_col_normal in req_col_normal):
                        column_mapping[required_col] = excel_col
                        print(f"✓ Columna '{required_col}' encontrada como '{excel_col}'")
                        found = True
                        break
                
                if not found:
                    raise KeyError(f"No se encontró la columna '{required_col}'")

            # Seleccionar y renombrar columnas
            df_selected = df[list(column_mapping.values())]
            df_selected.columns = list(column_mapping.keys())

            # Convertir a lista de diccionarios
            result = df_selected.to_dict(orient='records')
            print(f"\nSe procesaron {len(result)} registros exitosamente")
            
            return result

        except Exception as e:
            print(f"Error al procesar el archivo: {str(e)}")
            raise
