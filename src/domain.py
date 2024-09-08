from datetime import datetime
from fastapi import Response
from pydantic import Field
from pydantic import BaseModel
from typing import Optional

from src.repositories import TimeRuleRepository, UserRepository
from src.db.db import initialize_db


class HeathCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class Item(BaseModel):
    type: str
    email: str
    message: str | None = None


class UsersModel(BaseModel):
    type: Optional[str] = None
    email: str = Field(..., example="bosco@gmail.com")
    last_notification: Optional[str] = Field(..., example="2024-09-07 17:43:22.095267")
    notification_limit: Optional[int] = Field(..., example=2)


class TimeRuleModel(BaseModel):
    type: Optional[str] = None
    time: int = Field(..., example=120)
    limit: int = Field(..., example=2)


class UsersDomain:
    def __init__(self, repository: UserRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_user_registry(self, email: str, type: str):
        return self.__repository.get_user_registry(email, type)

    def create_user_registry(self, user: UsersModel):
        return self.__repository.create_or_replace_user_registry(user.model_dump())

    def notify_user(self, email: str, type: str, message: str = None):
        """
        Notifies a user via email based on specified rules.

        Args:
            email (str): The recipient's email address.
            type (str): The type of notification (e.g., "reminder", "alert").
            message (str, optional): An optional message to include in the notification.

        Returns:
            Response: A FastAPI Response object with appropriate status code and content.

        Behavior:
        - Retrieves the time rule associated with the specified notification type.
        - Checks the user's notification history and remaining notification limit.
        - If the user has remaining notifications, decrements the limit and updates the registry.
        - If the limit is exhausted and enough time has passed (according to the time rule),
        resets the notification limit and updates the last notification timestamp.
        - If neither condition is met, returns a 429 (Too Many Requests) status with a message
        indicating how long the user needs to wait before sending another notification.
        - Simulates redirecting the email by printing the recipient and message (if provided).
        """
        time_rule = self._get_time_rule(type)
        notification_values = self._get_or_create_notification_values(
            email, type, time_rule["limit"]
        )
        difference = self._get_time_difference(notification_values["last_notification"])
        if notification_values["notification_limit"] > 0:
            # Simulate sending the email
            print(f"Send to {email}: {message}")
            notification_values["notification_limit"] -= 1
            return self.__repository.create_or_replace_user_registry(
                notification_values
            )
        elif difference.total_seconds() > time_rule["time"]:
            # Simulate sending the email
            print(f"Send to {email}: {message}")
            notification_values["last_notification"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f"
            )
            notification_values["notification_limit"] = time_rule["limit"]
            return self.__repository.create_or_replace_user_registry(
                notification_values
            )
        else:
            # Too soon to notify
            return Response(
                content=f"Wait more {time_rule['time'] - difference.seconds} seconds to notify",
                status_code=429,
            )

    def _get_time_difference(self, time):

        date_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.now()
        difference = now - date_time
        return difference

    def _get_time_rule(self, type) -> TimeRuleModel:
        db = initialize_db()
        time_rule_repository = TimeRuleRepository(db)
        time_rule_domain = TimeRuleDomain(time_rule_repository)
        time_rule = time_rule_domain.get_time_rule(type)
        return time_rule

    def _get_or_create_notification_values(self, email, type, limit):
        notification_values = self.get_user_registry(email, type)
        if not notification_values:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

            notification_values = {
                "type": type,
                "email": email,
                "last_notification": now,
                "notification_limit": limit,
            }
            self.__repository.create_or_replace_user_registry(notification_values)

        return notification_values


class TimeRuleDomain:
    def __init__(self, repository: TimeRuleRepository) -> None:
        self.__repository = repository

    def get_all(self):
        return self.__repository.get_all()

    def get_time_rule(self, type: str):
        return self.__repository.get_time_rule(type)

    def create_time_rule(self, time_rule: TimeRuleModel):
        return self.__repository.create_time_rule(time_rule.model_dump())

    def update_time_rule(self, time_rule: TimeRuleModel):
        return self.__repository.update_time_rule(time_rule.model_dump())

    def delete_time_rule(self, type: str):
        return self.__repository.delete_time_rule(type)
