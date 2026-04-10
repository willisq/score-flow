import pandas as pd
from fastapi import UploadFile
from src.features.registration.application.schemas import CompetitorCreate
from src.features.registration.application.use_cases import RegistrationUseCases


class ExcelCompetitorProcessor:
    @staticmethod
    async def process_excel(
        file: UploadFile, use_cases: RegistrationUseCases
    ) -> list[CompetitorCreate]:
        """
        Lee un archivo Excel y mapea sus columnas a objetos CompetitorCreate.
        Resuelve nombres de academia, rango y sexo a sus respectivos IDs.
        """
        try:
            # 1. Leer el archivo Excel
            df = pd.read_excel(file.file)
        except Exception as e:
            raise ValueError(f"No se pudo leer el archivo Excel: {str(e)}")

        # 2. Cargar mapas de búsqueda (Nombre -> ID)
        ranks = {r.name.lower().strip(): r.id for r in await use_cases.list_ranks()}
        sexes = {s.name.lower().strip(): s.id for s in await use_cases.list_sexes()}
        academies = {
            a.name.lower().strip(): a.id for a in await use_cases.list_academies()
        }

        # 3. Definir mapeo de columnas
        column_map = {
            "Nombre": "first_name",
            "Apellido": "last_name",
            "Edad": "age",
            "Rango": "rank_name",
            "Peso": "weight",
            "Altura": "height",
            "Sexo": "sex_name",
            "Condición Especial": "special_condition",
            "Academia": "academy_name",
        }

        # Validar que existan las columnas mínimas requeridas
        missing_columns = [col for col in column_map.keys() if col not in df.columns]
        if missing_columns:
            raise ValueError(
                f"Faltan columnas requeridas en el Excel: {', '.join(missing_columns)}"
            )

        # Renombrar columnas para uso interno
        df = df.rename(columns=column_map)

        competitors = []
        errors = []

        # 4. Procesar cada fila
        for index, row in df.iterrows():
            row_num = index + 2  # Excel es 1-indexed y tiene cabecera
            try:
                # Limpiar y normalizar nombres para búsqueda
                rank_name = str(row["rank_name"]).lower().strip()
                sex_name = str(row["sex_name"]).lower().strip()
                academy_name = str(row["academy_name"]).lower().strip()

                # Resolución de IDs
                if rank_name not in ranks:
                    errors.append(f"Fila {row_num}: El rango '{row['rank_name']}' no existe.")
                    continue
                if sex_name not in sexes:
                    errors.append(f"Fila {row_num}: El sexo '{row['sex_name']}' no existe.")
                    continue
                if academy_name not in academies:
                    errors.append(f"Fila {row_num}: La academia '{row['academy_name']}' no existe.")
                    continue

                # Mapeo de condición especial (Sí/No a Booleano)
                sc_val = str(row["special_condition"]).lower().strip()
                special_condition = sc_val in ["sí", "si", "true", "1", "yes"]

                # Construir esquema de creación
                competitor = CompetitorCreate(
                    first_name=str(row["first_name"]).strip(),
                    last_name=str(row["last_name"]).strip(),
                    academy_id=academies[academy_name],
                    rank_id=ranks[rank_name],
                    sex_id=sexes[sex_name],
                    weight=float(row["weight"])
                    if pd.notna(row["weight"])
                    else None,
                    height=float(row["height"])
                    if pd.notna(row["height"])
                    else None,
                    age=int(row["age"]) if pd.notna(row["age"]) else None,
                    special_condition=special_condition,
                )
                competitors.append(competitor)

            except Exception as e:
                errors.append(f"Fila {row_num}: Error procesando datos. {str(e)}")

        if errors:
            raise ValueError("\n".join(errors))

        return competitors
