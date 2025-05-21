import pytest
from app.models.ai_models import AISuggestionRequest, AISuggestionResponse, AISuggestion
from app.services import ai_service
from app.core.config import settings # Required for the service to load settings

# Mark all tests in this module as asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
def summary_request_fixture():
    return AISuggestionRequest(
        section_data={"current_summary": "I am a professional."},
        context_text="Job description for a software engineer.",
        section_type="summary"
    )

@pytest.fixture
def experience_request_fixture():
    return AISuggestionRequest(
        section_data={"current_text": "Managed a team.", "for_role": "Manager", "for_company": "Tech Inc."},
        context_text="Looking for leadership skills.",
        section_type="experience_responsibility"
    )

@pytest.fixture
def generic_request_fixture():
    return AISuggestionRequest(
        section_data={"current_text": "Some details."},
        context_text="Generic context.",
        section_type="other_section"
    )

async def test_get_ai_content_suggestions_summary(summary_request_fixture):
    """Test AI suggestions for summary section type."""
    response = await ai_service.get_ai_content_suggestions(summary_request_fixture)
    assert isinstance(response, AISuggestionResponse)
    assert len(response.suggestions) == 1
    suggestion = response.suggestions[0]
    assert isinstance(suggestion, AISuggestion)
    assert suggestion.original_text == "I am a professional."
    assert "[AI-Suggested Summary]" in suggestion.suggested_text
    assert "placeholder suggestion for a summary" in suggestion.explanation

async def test_get_ai_content_suggestions_experience_responsibility(experience_request_fixture):
    """Test AI suggestions for experience_responsibility section type."""
    response = await ai_service.get_ai_content_suggestions(experience_request_fixture)
    assert isinstance(response, AISuggestionResponse)
    assert len(response.suggestions) == 2 # Expecting two placeholder suggestions
    
    suggestion1 = response.suggestions[0]
    assert isinstance(suggestion1, AISuggestion)
    assert suggestion1.original_text == "Managed a team."
    assert "[AI-Suggested Bullet Point] Enhanced managed a team." in suggestion1.suggested_text # Note: Placeholder logic makes it lowercase
    assert "placeholder suggestion for an experience bullet point" in suggestion1.explanation

    suggestion2 = response.suggestions[1]
    assert isinstance(suggestion2, AISuggestion)
    assert suggestion2.original_text == "Managed a team."
    assert "[AI-Suggested Bullet Point] Optimized managed a team. resulting in quantifiable improvement." in suggestion2.suggested_text
    assert "another placeholder suggestion, emphasizing quantification" in suggestion2.explanation

async def test_get_ai_content_suggestions_generic(generic_request_fixture):
    """Test AI suggestions for a generic section type."""
    response = await ai_service.get_ai_content_suggestions(generic_request_fixture)
    assert isinstance(response, AISuggestionResponse)
    assert len(response.suggestions) == 1
    suggestion = response.suggestions[0]
    assert isinstance(suggestion, AISuggestion)
    assert suggestion.original_text == str(generic_request_fixture.section_data) # Placeholder logic stringifies section_data
    assert "[AI-Suggested Generic Text] Improved content based on context." in suggestion.suggested_text
    assert "generic placeholder suggestion" in suggestion.explanation

async def test_prompt_construction_includes_input_data(mocker, experience_request_fixture):
    """Verify that the prompt construction includes parts of the input context and section data."""
    # We are not testing the LLM call itself, but the prompt fed to it (even if placeholder)
    # The current service prints the prompt, so we can capture stdout or mock 'print'
    
    mock_print = mocker.patch('builtins.print')
    
    await ai_service.get_ai_content_suggestions(experience_request_fixture)
    
    # Check that print was called with the prompt
    prompt_call_args = None
    for call in mock_print.call_args_list:
        args, _ = call
        if args and "DEBUG: AI Service Prompt:" in args[0]:
            prompt_call_args = args[0]
            break
    
    assert prompt_call_args is not None, "Prompt was not printed by the service"
    
    # Check for key parts of the request in the constructed prompt
    assert experience_request_fixture.section_type in prompt_call_args
    assert str(experience_request_fixture.section_data) in prompt_call_args # The placeholder prompt stringifies section_data
    assert experience_request_fixture.context_text in prompt_call_args
    assert settings.AI_SERVICE_API_KEY[:5] in prompt_call_args # Check if API key logging part is there

# Example of how one might test the actual LLM call if it weren't a placeholder
# This requires more advanced mocking with httpx.
# async def test_get_ai_content_suggestions_llm_call(mocker, experience_request_fixture):
#     mock_response_data = {
#         "choices": [{"text": "LLM suggested text."}]
#     }
#     mock_httpx_response = httpx.Response(200, json=mock_response_data)
    
#     # Mock the post method of an AsyncClient instance
#     mock_async_client_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_httpx_response)
    
#     # To make this test work, you'd need to uncomment the actual API call block in ai_service.py
#     # and potentially adjust the settings.AI_SERVICE_ENDPOINT to avoid a real call during tests
#     # settings.AI_SERVICE_ENDPOINT = "http://mock-ai-service.com/api" 
    
#     # response = await ai_service.get_ai_content_suggestions(experience_request_fixture)
    
#     # if settings.AI_SERVICE_ENDPOINT != "https://api.example.com/v1/completions": # i.e. if we are in "real call" mode
#     #     mock_async_client_post.assert_called_once()
#     #     args, kwargs = mock_async_client_post.call_args
#     #     assert settings.AI_SERVICE_ENDPOINT in args[0]
#     #     assert f"Bearer {settings.AI_SERVICE_API_KEY}" in kwargs["headers"]["Authorization"]
#     #     assert experience_request_fixture.context_text in kwargs["json"]["prompt"] # Example check
#     #     assert response.suggestions[0].suggested_text == "LLM suggested text."
#     pass

# Ensure that settings are loaded before running tests that might depend on them
# This is implicitly handled by importing settings in the service module,
# but can be made explicit if needed, e.g. by a fixture.
@pytest.fixture(autouse=True)
def ensure_settings():
    return settings
