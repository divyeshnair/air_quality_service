from typing import Optional

from fastapi import APIRouter, Depends

from src.resource.carbon_monoxide.core.fetch_carbon_monoxide import \
    get_h3_details
from src.resource.carbon_monoxide.core.fetch_carbon_monoxide_by_h3 import \
    get_carbon_monoxide_details_by_h3
from src.resource.carbon_monoxide.schema import GetH3IndexRequest, GetCarbonMonoxideRequest

router = APIRouter()

@router.get("/")
def h3_indexes(req: GetH3IndexRequest=Depends()):
    return get_h3_details(req)


@router.get('/api/carbon-monoxide/details')
def carbon_monoxide_details_by_h3(req: GetCarbonMonoxideRequest=Depends()):
    return get_carbon_monoxide_details_by_h3(req)
