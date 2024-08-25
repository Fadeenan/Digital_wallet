import asyncio
import pathlib
import datetime
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from digimon import models, config, main, security
from pydantic_settings import SettingsConfigDict


# Set up testing-specific settings
SettingsTesting = config.Settings
SettingsTesting.model_config = SettingsConfigDict(
    env_file=".testing.env", validate_assignment=True, extra="allow"
)


@pytest.fixture(name="app", scope="session")
def app_fixture():
    settings = SettingsTesting()
    settings.SQLDB_URL = "sqlite+aiosqlite:///./test-data/test-sqlalchemy.db"

    path = pathlib.Path("test-data")
    if not path.exists():
        path.mkdir()

    app = main.create_app(settings)

    # Ensure the tables are created
    asyncio.run(models.recreate_table())

    yield app


@pytest.fixture(name="client", scope="session")
def client_fixture(app: FastAPI) -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


@pytest_asyncio.fixture(name="session", scope="session")
async def get_session() -> models.AsyncIterator[models.AsyncSession]:
    settings = SettingsTesting()
    settings.SQLDB_URL = "sqlite+aiosqlite:///./test-data/test-sqlalchemy.db"
    models.init_db(settings)

    async_session = models.sessionmaker(
        models.engine, class_=models.AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="user1")
async def example_user1(session: models.AsyncSession) -> models.DBUser:
    password = "123456"
    username = "user1"

    query = await session.exec(
        models.select(models.DBUser).where(models.DBUser.username == username).limit(1)
    )
    user = query.one_or_none()
    if user:
        return user

    user = models.DBUser(
        username=username,
        password=password,
        email="test@test.com",
        first_name="Firstname",
        last_name="lastname",
        last_login_date=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    await user.set_password(password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture(name="token_user1")
async def oauth_token_user1(user1: models.DBUser) -> dict:
    settings = SettingsTesting()
    access_token_expires = datetime.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    user = user1
    return models.Token(
        access_token=security.create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires,
        ),
        refresh_token=security.create_refresh_token(
            data={"sub": user.id},
            expires_delta=access_token_expires,
        ),
        token_type="Bearer",
        scope="",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_at=datetime.datetime.now() + access_token_expires,
        issued_at=user.last_login_date,
        user_id=user.id,
    )


@pytest_asyncio.fixture(name="merchant_user1")
async def example_merchant_user1(
    session: models.AsyncSession, user1: models.DBUser
) -> models.DBMerchant:
    name = "merchant1"

    query = await session.exec(
        models.select(models.DBMerchant)
        .where(models.DBMerchant.name == name, models.DBMerchant.user_id == user1.id)
        .limit(1)
    )
    merchant = query.one_or_none()
    if merchant:
        return merchant

    merchant = models.DBMerchant(
        name=name, user=user1, description="Merchant Description", tax_id="0000000000000"
    )

    session.add(merchant)
    await session.commit()
    await session.refresh(merchant)
    return merchant
