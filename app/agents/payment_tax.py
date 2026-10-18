from typing import Dict, Any

def get_payment_and_tax_guidance(country: str, amount_usd: float = 5000.0) -> Dict[str, Any]:
    """
    Computes payment fee comparison (Payoneer vs Wise) and provides FBR 0.25% export tax compliance report.
    """
    c_lower = country.lower()

    # Fee structures
    # Payoneer: ~1.5% - 2% on receiving / fx
    payoneer_fee = round(amount_usd * 0.018, 2)
    # Wise: ~0.5% - 0.9% for direct bank transfers in UK/EU, slightly higher for US ACH
    wise_fee = round(amount_usd * 0.008 if ("uk" in c_lower or "german" in c_lower or "euro" in c_lower) else amount_usd * 0.012, 2)

    if "uk" in c_lower or "germany" in c_lower or "europe" in c_lower:
        preferred = "Wise Business"
        savings = round(payoneer_fee - wise_fee, 2)
        rationale = "Europe aur UK ke buyers se IBAN / SEPA ya Faster Payments ke zariye direct transfer par Wise ki FX conversion aur transfer fees sab se sasti parti hain."
    else:
        preferred = "Payoneer"
        savings = round(abs(payoneer_fee - wise_fee), 2)
        rationale = "USA aur Alibaba / Amazon marketplace payout integrations ke liye Payoneer sab se zyada reliable aur directly integrated hai (PRC/FBR compliant e-PRC certificate milta hai)."

    # FBR Tax Guidance (0.25% regime)
    fbr_tax_rate = 0.0025  # 0.25% final tax regime for export of IT & goods under PSEB/Export regime
    fbr_tax_amount = round(amount_usd * fbr_tax_rate, 2)

    return {
        "invoice_amount_usd": amount_usd,
        "buyer_country": country,
        "recommended_channel": preferred,
        "fee_breakdown": {
            "payoneer_estimated_fee_usd": payoneer_fee,
            "wise_estimated_fee_usd": wise_fee,
            "estimated_savings_usd": savings
        },
        "fbr_compliance": {
            "applicable_tax_regime": "0.25% Final Tax Regime (Export Proceeds)",
            "fbr_withholding_tax_usd": fbr_tax_amount,
            "fbr_withholding_tax_pkr": round(fbr_tax_amount * 278.0, 2),
            "eprc_requirement": "Apne Pakistani bank se Electronic Proceeds Realization Certificate (e-PRC) lazmi lein taake 0.25% tax slab maintain rahe."
        },
        "urdu_advice": (
            f"{country} ke buyer ke liye humara mashwara hai ke aap **{preferred}** istemal karein. "
            f"Payoneer fee lag bhag ${payoneer_fee} hogi jabkay Wise fee lag bhag ${wise_fee} hogi. "
            f"FBR ke export regime ke tehat aap ko sirf 0.25% tax (${fbr_tax_amount}) dena hoga. "
            f"{rationale}"
        )
    }
