from fastapi import APIRouter, HTTPException
from app.models.schemas import UserLogin, TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(creds: UserLogin):
    # Support mock login for hackathon demo
    if not creds.username:
        raise HTTPException(status_code=400, detail="Username is required")

    return TokenResponse(
        access_token=f"jwt_token_coretech_{creds.username}_secret_mock",
        token_type="bearer",
        user={
            "username": creds.username,
            "role": "exporter",
            "cluster": "Sialkot / Faisalabad Export Hub",
            "team": "CoreTech Innovation"
        }
    )
