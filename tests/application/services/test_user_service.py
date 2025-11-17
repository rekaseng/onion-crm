import pytest
from unittest.mock import AsyncMock
from application.use_cases.user_service import UserService
from application.dto.user_dto import UserRegistrationDTO


@pytest.mark.asyncio
async def test_register_user_use_case_success():
    # Mocking the UserRepository dependency
    user_repository_mock = AsyncMock()
    user_repository_mock.add = AsyncMock()

    # Creating a test instance of the use case
    user_service = UserService(user_repository=user_repository_mock)

    # Creating a test DTO
    user_dto = UserRegistrationDTO(username="testuser", email="test@example.com", password="password123")

    # Executing the use case
    user = await user_service.register(user_dto)

    # Assertions to verify the use case behavior
    assert user.username == user_dto.username
    assert user.email == user_dto.email
    user_repository_mock.add.assert_called_once()  # Verify the repository's add method was called once