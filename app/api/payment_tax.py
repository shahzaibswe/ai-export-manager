from fastapi import APIRouter, Query
from app.agents.payment_tax import get_payment_and_tax_guidance

router = APIRouter(prefix="/api/v1/payment-tax", tags=["Payment & Tax Optimizer"])

@router.get("/optimize")
def optimize_payment_and_tax(
    country: str = Query("USA", description="Buyer country"),
    amount_usd: float = Query(5000.0, description="Order value in USD")
):
    """
    Recommends optimal payment provider (Payoneer vs Wise) and computes FBR 0.25% export tax liabilities.
    """
    return get_payment_and_tax_guidance(country=country, amount_usd=amount_usd)
