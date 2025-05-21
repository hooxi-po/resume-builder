from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AISuggestionRequest(BaseModel):
    section_data: Dict[str, Any] = Field(..., example={"current_text": "Managed team of 5 engineers."})
    context_text: str = Field(..., example="Job description for a Senior Software Engineer role requiring leadership skills.")
    section_type: str = Field(..., example="experience_responsibility")

class AISuggestion(BaseModel):
    original_text: Optional[str] = Field(None, example="Managed team of 5 engineers.")
    suggested_text: str = Field(..., example="Led and mentored a team of 5 software engineers, fostering a collaborative environment.")
    explanation: Optional[str] = Field(None, example="Rephrased to emphasize leadership and collaboration, using stronger action verbs.")

class AISuggestionResponse(BaseModel):
    suggestions: List[AISuggestion] = Field(default_factory=list)
