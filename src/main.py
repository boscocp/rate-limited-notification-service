from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware

from src.db.generate_table import generate_table
from src.db.db import initialize_db
from src.domain import HeathCheck, TimeRuleDomain, UsersDomain
from src.repositories import TimeRuleRepository, UserRepository
from src.router_users import TimeRuleRouter, UsersRouter

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = initialize_db()
users_repository = UserRepository(db)
users_domain = UsersDomain(users_repository)
users_router = UsersRouter(users_domain)

time_rule_repository = TimeRuleRepository(db)
time_rule_domain = TimeRuleDomain(time_rule_repository)
time_rule_router = TimeRuleRouter(time_rule_domain)

app.include_router(users_router.router)
app.include_router(time_rule_router.router)

generate_table()


@app.get("/")
def index():
    return "Hello World!"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Heath Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HeathCheck,
)
async def get_health() -> HeathCheck:
    """## Perform a Health Check

    Returns:
    --------
        HeathCheck: Returns a JSON response with the health status
    """
    return HeathCheck(status="OK")
