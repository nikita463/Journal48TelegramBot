import aiohttp

from .consts import *
from .parser import parse_diary, parse_vendors
from .typings import *

aiohttp_session: aiohttp.ClientSession | None = None

async def get_aiohttp_session() -> aiohttp.ClientSession:
    global aiohttp_session
    if aiohttp_session is None:
        aiohttp_session = aiohttp.ClientSession(headers=HEADERS)
    return aiohttp_session

async def get_diary(start: date, end: date, vendor: Vendor) -> List[Student]:
    await get_aiohttp_session()

    days = f"{start:%Y%m%d}-{end:%Y%m%d}"
    params = {
        **PARAMS,
        "auth_token": vendor.token,
        "student": "1728", # TODO,
        "vendor": vendor.vendor,
        "days": days
    }

    async with aiohttp_session.get(API_GET_DIARY, params=params) as response:
        response.raise_for_status()
        js = await response.json()

    return parse_diary(js)

async def get_vendors(v_token: str):
    await get_aiohttp_session()

    params = {"v_token": v_token}

    async with aiohttp_session.get(API_GET_VENDORS, params=params) as response:
        response.raise_for_status()
        js = await response.json()

    return parse_vendors(js)
