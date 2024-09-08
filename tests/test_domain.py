from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timedelta

from src.domain import UsersDomain


def test_notify_user_limit_exceeded():
    repository_mock = MagicMock()
    users_domain = UsersDomain(repository_mock)
    notification_values_mock = {
        "type": "some_type",
        "email": "bosco@gmail.com",
        "last_notification": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "notification_limit": 0,
    }

    with patch.object(
        users_domain, "_get_time_rule", return_value={"time": 60, "limit": 2}
    ):
        with patch.object(
            users_domain,
            "_get_or_create_notification_values",
            return_value=notification_values_mock,
        ):
            result = users_domain.notify_user(
                email="test@example.com", type="some_type"
            )
            assert result.status_code == 429


def test_notify_user_time_exceeded():
    repository_mock = MagicMock()
    users_domain = UsersDomain(repository_mock)
    notification_values_mock = {
        "type": "some_type",
        "email": "bosco@gmail.com",
        "last_notification": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "notification_limit": 1,
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = "ok"

    with patch.object(
        users_domain, "_get_time_rule", return_value={"time": 60, "limit": 2}
    ):
        with patch.object(
            users_domain,
            "_get_or_create_notification_values",
            return_value=notification_values_mock,
        ):
            with patch.object(
                repository_mock,
                "create_or_replace_user_registry",
                return_value=mock_response,
            ):
                result = users_domain.notify_user(
                    email="test@example.com", type="some_type"
                )
                assert result.status_code == 200
                result = users_domain.notify_user(
                    email="test@example.com", type="some_type"
                )
                assert result.status_code == 429


def test_notify_user_time_and_limit_exceeded():
    repository_mock = MagicMock()
    users_domain = UsersDomain(repository_mock)
    past_seconds = datetime.now() - timedelta(seconds=130)
    notification_values_mock = {
        "type": "some_type",
        "email": "bosco@gmail.com",
        "last_notification": past_seconds.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "notification_limit": 0,
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = "ok"

    with patch.object(
        users_domain, "_get_time_rule", return_value={"time": 120, "limit": 2}
    ):
        with patch.object(
            users_domain,
            "_get_or_create_notification_values",
            return_value=notification_values_mock,
        ):
            with patch.object(
                repository_mock,
                "create_or_replace_user_registry",
                return_value=mock_response,
            ):
                result = users_domain.notify_user(
                    email="test@example.com", type="some_type"
                )
                assert result.status_code == 200
