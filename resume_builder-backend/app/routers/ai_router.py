# resume_builder-backend/app/routers/ai_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import ai_models, user_models
from app.services import ai_service
from app.core import security

router = APIRouter()

@router.post("/suggest-content", response_model=ai_models.AISuggestionResponse)
async def suggest_content_endpoint(
    request: ai_models.AISuggestionRequest,
    current_user: user_models.User = Depends(security.get_current_active_user) # Protect endpoint
):
    '''
    Provides AI-powered content suggestions for a given resume section and context.
    Requires authentication.
    '''
    if not request.section_data or not request.context_text or not request.section_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing section_data, context_text, or section_type in request."
        )

    try:
        suggestions = await ai_service.get_ai_content_suggestions(request)
        return suggestions
    except Exception as e:
        # Log the exception details here if you have a logger configured
        print(f"Error in suggest_content_endpoint: {e}") # Basic logging
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating content suggestions."
        )
