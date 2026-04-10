import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pandas as pd
import pytest
from fastapi import UploadFile

from src.features.registration.application.excel_processor import ExcelCompetitorProcessor
from src.features.registration.domain.entities import Academy, Person, Rank, Sex


@pytest.fixture
def mock_use_cases():
    use_cases = MagicMock()
    # Mock data
    rank = Rank(id=uuid4(), name="Blanco", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Masculino")
    academy = Academy(
        id=uuid4(),
        name="Cobra Kai",
        instructor=Person(id=uuid4(), first_name="Johnny", last_name="Lawrence"),
    )

    use_cases.list_ranks = AsyncMock(return_value=[rank])
    use_cases.list_sexes = AsyncMock(return_value=[sex])
    use_cases.list_academies = AsyncMock(return_value=[academy])
    return use_cases


def test_process_excel_success(mock_use_cases):
    # Prepare Excel data
    data = {
        "Nombre": ["Daniel"],
        "Apellido": ["LaRusso"],
        "Edad": [17],
        "Rango": ["Blanco"],
        "Peso": [65.5],
        "Altura": [175.0],
        "Sexo": ["Masculino"],
        "Condición Especial": ["No"],
        "Academia": ["Cobra Kai"],
    }
    df = pd.DataFrame(data)
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False)
    excel_io.seek(0)

    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = excel_io

    # Execute
    result = asyncio.run(
        ExcelCompetitorProcessor.process_excel(mock_file, mock_use_cases)
    )

    # Verify
    assert len(result) == 1
    competitor = result[0]
    assert competitor.first_name == "Daniel"
    assert competitor.last_name == "LaRusso"
    assert competitor.age == 17
    assert competitor.special_condition is False
    assert competitor.weight == 65.5


def test_process_excel_missing_columns(mock_use_cases):
    # Missing required columns
    data = {"Nombre": ["Daniel"], "Apellido": ["LaRusso"]}
    df = pd.DataFrame(data)
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False)
    excel_io.seek(0)

    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = excel_io

    with pytest.raises(ValueError) as exc:
        asyncio.run(ExcelCompetitorProcessor.process_excel(mock_file, mock_use_cases))

    assert "Faltan columnas requeridas" in str(exc.value)


def test_process_excel_invalid_rank(mock_use_cases):
    data = {
        "Nombre": ["Daniel"],
        "Apellido": ["LaRusso"],
        "Edad": [17],
        "Rango": ["Desconocido"],  # Not in mock_use_cases
        "Peso": [65.5],
        "Altura": [175.0],
        "Sexo": ["Masculino"],
        "Condición Especial": ["No"],
        "Academia": ["Cobra Kai"],
    }
    df = pd.DataFrame(data)
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False)
    excel_io.seek(0)

    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = excel_io

    with pytest.raises(ValueError) as exc:
        asyncio.run(ExcelCompetitorProcessor.process_excel(mock_file, mock_use_cases))

    assert "El rango 'Desconocido' no existe" in str(exc.value)


def test_process_excel_various_boolean_values(mock_use_cases):
    data = {
        "Nombre": ["A", "B", "C"],
        "Apellido": ["X", "Y", "Z"],
        "Edad": [20, 20, 20],
        "Rango": ["Blanco", "Blanco", "Blanco"],
        "Peso": [70, 70, 70],
        "Altura": [180, 180, 180],
        "Sexo": ["Masculino", "Masculino", "Masculino"],
        "Condición Especial": ["Sí", "True", "No"],
        "Academia": ["Cobra Kai", "Cobra Kai", "Cobra Kai"],
    }
    df = pd.DataFrame(data)
    excel_io = BytesIO()
    df.to_excel(excel_io, index=False)
    excel_io.seek(0)

    mock_file = MagicMock(spec=UploadFile)
    mock_file.file = excel_io

    result = asyncio.run(
        ExcelCompetitorProcessor.process_excel(mock_file, mock_use_cases)
    )

    assert result[0].special_condition is True
    assert result[1].special_condition is True
    assert result[2].special_condition is False
