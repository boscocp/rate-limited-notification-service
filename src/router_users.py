from fastapi import APIRouter
from fastapi import HTTPException

from src.domain import Item, TimeRuleDomain, TimeRuleModel, UsersDomain, UsersModel


class UsersRouter:
    def __init__(self, users_domain: UsersDomain) -> None:
        self.__users_domain = users_domain

    @property
    def router(self):
        api_router = APIRouter(prefix="/users", tags=["users"])

        @api_router.get("/")
        def index_route():
            return "Hello! Welcome to users index route"

        @api_router.get("/all")
        def get_all():
            return self.__users_domain.get_all()

        @api_router.post("/create")
        def create_user(users_model: UsersModel):
            return self.__users_domain.create_user_registry(users_model)

        @api_router.post("/notify")
        def notify(item: Item):
            return self.__users_domain.notify_user(item.email, item.type, item.message)

        @api_router.get("/get/{email}/{type}")
        def get_user(email: str, type: str):
            try:
                return self.__users_domain.get_user_registry(email, type)
            except KeyError:
                raise HTTPException(status_code=400, detail="No user found")

        return api_router


class TimeRuleRouter:
    def __init__(self, time_rule_domain: TimeRuleDomain) -> None:
        self.__time_rule_domain = time_rule_domain

    @property
    def router(self):
        api_router = APIRouter(prefix="/time-rule", tags=["time_rule"])

        @api_router.get("/")
        def index_route():
            return "Hello! Welcome to time rule index route"

        @api_router.get("/all")
        def get_all():
            return self.__time_rule_domain.get_all()

        @api_router.post("/create")
        def create_time_rule(time_rule_model: TimeRuleModel):
            return self.__time_rule_domain.create_time_rule(time_rule_model)

        @api_router.get("/get/{type}")
        def get_time_rule(type: str):
            try:
                return self.__time_rule_domain.get_time_rule(type)
            except KeyError:
                raise HTTPException(status_code=400, detail="No time rule found")

        @api_router.put("/update")
        def update_time_rule(time_rule_model: TimeRuleModel):
            return self.__time_rule_domain.update_time_rule(time_rule_model)

        @api_router.delete("/delete/{type}")
        def delete_time_rule(type: str):
            return self.__time_rule_domain.delete_time_rule(type)

        return api_router
