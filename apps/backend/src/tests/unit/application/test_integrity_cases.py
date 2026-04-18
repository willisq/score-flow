import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from src.features.tournament.data.repository import CategoryRepository
from src.features.tournament.domain.entities import (
    Category,
    CategoryModality,
    PhysicalRequirement,
    Modality,
    RankGroup,
)
from src.features.tournament.data.models import PhysicalRequirementModel, CategoryModalityModel


def test_repository_deduplicates_by_rounding():
    # Setup
    session = AsyncMock()
    # Mocking identity_map and new collections
    session.new = []
    session.identity_map = {}
    repo = CategoryRepository(session)
    
    # Existing model in session (represented as already added)
    pr_id = uuid4()
    pr_model = PhysicalRequirementModel(
        id=pr_id,
        initial_weight=10.0,
        final_weight=20.0,
        initial_height=0,
        final_height=100
    )
    session.new.append(pr_model)
    
    # 1. Call with slightly different float values (should match due to rounding)
    result = asyncio.run(repo.get_or_create_physical_requirement(
        initial_weight=10.00001,
        final_weight=19.99999,
        initial_height=0.0000001,
        final_height=100.0000002,
        preferred_id=pr_id
    ))
    
    # Verification
    assert result == pr_model
    session.add.assert_not_called()


def test_create_category_internal_caching():
    # Setup
    session = AsyncMock()
    session.new = []
    session.identity_map = {}
    repo = CategoryRepository(session)
    
    pr_id = uuid4()
    pr_domain = PhysicalRequirement(
        id=pr_id,
        initial_weight=10.0,
        final_weight=20.0,
        initial_height=0,
        final_height=200
    )
    
    # Mock session.get to return None first, then the model
    def mock_get(cls, id):
        if cls == PhysicalRequirementModel:
            for obj in session.new:
                if isinstance(obj, PhysicalRequirementModel) and obj.id == id:
                    return obj
        return None
        
    session.get.side_effect = mock_get
    
    # Mock execute for DB query
    session.execute.return_value = MagicMock(scalars=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None))))
    
    category = Category(id=uuid4(), ages=[10, 12], special_condition=False)
    modality = Modality(id=uuid4(), name="Test")
    rg = RankGroup(id=uuid4(), name="RG", ranks=[])
    
    # Multiple modalities with SAME PR domain object
    category.modalities = [
        CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[], rank_group=rg, physical_requirement=pr_domain),
        CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[], rank_group=rg, physical_requirement=pr_domain)
    ]
    
    asyncio.run(repo.create(category))
    
    # Verification
    # physical_requirement check should only hit DB/Session logic once due to repo-level cache
    # But wait, CategoryRepository.create now has its own cache too.
    # So get_or_create_physical_requirement should only be called ONCE.
    
    # Check how many times session.add was called for PR models
    pr_add_calls = [call for call in session.add.call_args_list if isinstance(call.args[0], PhysicalRequirementModel)]
    assert len(pr_add_calls) == 1
    
    # Verify that modalities used the correct PR ID
    cat_mod_adds = [call.args[0] for call in session.add.call_args_list if isinstance(call.args[0], CategoryModalityModel)]
    for mod in cat_mod_adds:
        assert mod.physical_requirement_id == pr_id


def test_deduplicates_different_ids_same_data_in_session():
    # Setup
    session = AsyncMock()
    session.new = []
    session.identity_map = {}
    session.get.return_value = None # Fix: prevent mock from returning a truthy mock object by default
    repo = CategoryRepository(session)
    
    # Object already in session with ID 1
    pr_id1 = uuid4()
    pr_model1 = PhysicalRequirementModel(
        id=pr_id1,
        initial_weight=10.0,
        final_weight=20.0,
        initial_height=0,
        final_height=100
    )
    session.new.append(pr_model1)
    
    # Call with a DIFFERENT ID but SAME data
    pr_id2 = uuid4()
    result = asyncio.run(repo.get_or_create_physical_requirement(
        initial_weight=10.0,
        final_weight=20.0,
        initial_height=0,
        final_height=100,
        preferred_id=pr_id2
    ))
    
    # Verification
    # Should return the existing object with ID 1, ignoring ID 2 to avoid data duplication
    assert result == pr_model1
    assert result.id == pr_id1
    session.add.assert_not_called()
