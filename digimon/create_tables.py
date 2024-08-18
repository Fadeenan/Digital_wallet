import asyncio
from digimon.config import get_settings
from digimon.models import init_db, recreate_table

async def main():
    settings = get_settings()
    init_db(settings)
    await recreate_table()

asyncio.run(main())
