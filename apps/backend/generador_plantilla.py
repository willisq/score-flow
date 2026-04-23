import pandas as pd
import random

# 1. Definición de catálogos basados en tu plantilla
sexos = ["Masculino", "Femenino"]
rangos = ["Blanco", "R. Amarilla"]
academias = [
    "Chois Kwan Do",
    "Moo Sul Kwang",
    "Cemar",
    "Chundungkwan",
    "Choi's II",
    "Choi's Msk",
    "Il Do Kwan",
    "Kwontae",
    "Cemar II",
    "Moosulkwan II",
    "Choi's",
    "Legado Choi's-do",
    "Kwontae Msk",
    "Choi's Do",
]

nombres_m = [
    "Juan",
    "Carlos",
    "Luis",
    "Diego",
    "Miguel",
    "Jorge",
    "Andrés",
    "Roberto",
    "Mateo",
    "Santiago",
]
nombres_f = [
    "María",
    "Sofía",
    "Elena",
    "Ana",
    "Laura",
    "Lucía",
    "Valentina",
    "Paula",
    "Isabella",
    "Camila",
]
apellidos = [
    "Pérez",
    "García",
    "Rodríguez",
    "Martínez",
    "Sánchez",
    "López",
    "Gómez",
    "Torres",
    "Díaz",
    "Castro",
]

# 2. Generación de 50 registros ficticios
data = []
for _ in range(50):
    sexo = random.choice(sexos)
    nombre = random.choice(nombres_m if sexo == "Masculino" else nombres_f)
    apellido = random.choice(apellidos)
    edad = random.randint(6, 45)
    rango = random.choice(rangos)
    # Peso y altura proporcionales a la edad (aproximación)
    altura = round(
        random.uniform(1.10, 1.90) if edad > 15 else random.uniform(1.10, 1.60), 2
    )
    peso = round(random.uniform(50, 95) if edad > 15 else random.uniform(20, 55), 1)
    condicion = random.choice(["SI", "NO"])
    academia = random.choice(academias)

    data.append(
        [nombre, apellido, edad, rango, peso, altura, sexo, condicion, academia]
    )

# 3. Creación de DataFrames
df_competidores = pd.DataFrame(
    data,
    columns=[
        "Nombre",
        "Apellido",
        "Edad",
        "Rango",
        "Peso",
        "Altura",
        "Sexo",
        "Condición Especial",
        "Academia",
    ],
)

df_validaciones = pd.DataFrame(
    {
        "Sexos": pd.Series(sexos),
        "Rangos": pd.Series(rangos),
        "Academias": pd.Series(academias),
    }
)

# 4. Exportación a Excel
nombre_archivo = "plantilla_pruebas_torneo.xlsx"
with pd.ExcelWriter(nombre_archivo, engine="openpyxl") as writer:
    df_competidores.to_excel(writer, sheet_name="Sheet1", index=False)
    df_validaciones.to_excel(writer, sheet_name="_Validaciones", index=False)

print(f"¡Listo! Se ha creado '{nombre_archivo}' con 50 competidores de prueba.")
