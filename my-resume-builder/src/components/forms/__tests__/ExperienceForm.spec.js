import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mount } from '@vue/test-utils';
import ExperienceForm from '../ExperienceForm.vue'; // Adjust path as needed
import { getAIContentSuggestions } from '../../../services/api'; // To mock

// Mock the API service
vi.mock('../../../services/api', () => ({
  getAIContentSuggestions: vi.fn(),
}));

// Helper function to create a default props structure for resumeData
const createDefaultResumeData = () => ({
  experience: [
    {
      id: 'exp1',
      company: 'TestCo',
      role: 'Tester',
      location: 'Testville',
      startDate: '2020-01',
      endDate: '2021-01',
      responsibilities: ['Tested things', 'Documented tests'],
      achievements: ['Found critical bug', 'Improved test coverage'],
    },
  ],
});

describe('ExperienceForm.vue AI Suggestions', () => {
  let wrapper;
  let resumeData;

  beforeEach(() => {
    // Reset resumeData for each test to ensure isolation
    resumeData = createDefaultResumeData();
    
    // Clear mock history and reset implementation before each test
    getAIContentSuggestions.mockClear();
    getAIContentSuggestions.mockResolvedValue({ // Default mock implementation
      suggestions: [
        {
          original_text: 'Tested things',
          suggested_text: 'Professionally tested various things',
          explanation: 'Sounds more professional',
        },
        {
          original_text: 'Tested things',
          suggested_text: 'Collaborated with team to test things',
          explanation: 'Highlights teamwork',
        },
      ],
    });

    wrapper = mount(ExperienceForm, {
      props: {
        resumeData: resumeData,
      },
      global: {
        // If there are any global provides or stubs needed, add them here
        // stubs: { Transition: false } // Example if transitions cause issues in tests
      }
    });
  });

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount();
    }
  });

  it('renders job context textarea and AI suggestion buttons', () => {
    expect(wrapper.find('label[for="job-context-text"]').exists()).toBe(true);
    expect(wrapper.find('#job-context-text').exists()).toBe(true);

    // Check for AI suggestion buttons for responsibilities and achievements
    // Assuming there's at least one experience item with responsibilities/achievements
    const experienceItem = resumeData.experience[0];
    expect(experienceItem.responsibilities.length).toBeGreaterThan(0);
    expect(experienceItem.achievements.length).toBeGreaterThan(0);
    
    // Find buttons within the scope of responsibilities/achievements
    // The exact selector might need adjustment based on final HTML structure.
    // This looks for buttons with the specific text/class.
    const responsibilityAIButtons = wrapper.findAll('.button-ai-suggestion').filter(btn => 
        btn.text().includes('获取AI建议') && btn.attributes('onclick') && btn.attributes('onclick').includes('responsibility')
    );
    const achievementAIButtons = wrapper.findAll('.button-ai-suggestion').filter(btn => 
        btn.text().includes('获取AI建议') && btn.attributes('onclick') && btn.attributes('onclick').includes('achievement')
    );
    
    // More robust: find by specific data-testid or more unique class if available
    // For now, let's assume the buttons exist if there are responsibilities/achievements
    expect(wrapper.findAll('.button-ai-suggestion').length).toBeGreaterThanOrEqual(
        experienceItem.responsibilities.length + experienceItem.achievements.length
    );
  });

  it('does not attempt to fetch AI suggestions if job context is empty', async () => {
    const jobContextTextarea = wrapper.find('#job-context-text');
    await jobContextTextarea.setValue(''); // Ensure it's empty

    // Find the first "Get AI Suggestions" button for a responsibility
    // The button is inside .ai-suggestion-controls, which is a sibling of .sub-list-item
    const firstResponsibilityButton = wrapper.find('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion');
    await firstResponsibilityButton.trigger('click');
    
    expect(getAIContentSuggestions).not.toHaveBeenCalled();
    // Check for window.alert mock if possible, or rely on no API call
    // Vitest doesn't mock window.alert by default. Can be done globally if needed.
  });
  
  it('does not attempt to fetch AI suggestions if target text (e.g. responsibility) is empty', async () => {
    const jobContextTextarea = wrapper.find('#job-context-text');
    await jobContextTextarea.setValue('Relevant job description context.');

    // Temporarily empty the first responsibility for this test
    const firstResponsibilityOriginalText = resumeData.experience[0].responsibilities[0];
    resumeData.experience[0].responsibilities[0] = '';
    await wrapper.setProps({ resumeData: { ...resumeData } }); // Force reactivity if needed, or directly modify via wrapper.vm

    const firstResponsibilityButton = wrapper.find('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion');
    await firstResponsibilityButton.trigger('click');
    
    expect(getAIContentSuggestions).not.toHaveBeenCalled();
  });


  it('calls getAIContentSuggestions with correct payload and shows modal on button click', async () => {
    const jobContextTextarea = wrapper.find('#job-context-text');
    await jobContextTextarea.setValue('Senior Software Engineer job description requiring leadership.');

    // Target the first responsibility of the first experience item
    const expItem = resumeData.experience[0];
    const respIndex = 0;
    const originalResponsibilityText = expItem.responsibilities[respIndex];

    // Find the AI suggestion button for the first responsibility
    // This selector assumes a structure. A data-testid attribute would be more robust.
    const aiButton = wrapper.findAll('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion').at(0);
    expect(aiButton.exists()).toBe(true);
    
    await aiButton.trigger('click');

    expect(getAIContentSuggestions).toHaveBeenCalledTimes(1);
    const expectedPayload = {
      section_data: {
        for_role: expItem.role,
        for_company: expItem.company,
        current_text: originalResponsibilityText,
      },
      context_text: 'Senior Software Engineer job description requiring leadership.',
      section_type: 'experience_responsibility',
    };
    expect(getAIContentSuggestions).toHaveBeenCalledWith(expectedPayload);

    // Check if modal becomes visible
    // Need to wait for Vue's next tick for DOM updates after state change
    await wrapper.vm.$nextTick(); // Or import { nextTick } from 'vue' and use await nextTick();
    
    const modal = wrapper.find('.modal-backdrop');
    expect(modal.exists()).toBe(true);
    expect(wrapper.vm.showSuggestionModal).toBe(true); // Check component state
    expect(wrapper.find('.modal-content h3').text()).toBe('AI 建议');
    expect(wrapper.findAll('.suggestion-item').length).toBe(2); // From default mock
  });

  it('applies suggestion and closes modal when "Apply this suggestion" is clicked', async () => {
    // 1. Setup: Set job context, trigger AI suggestions to open modal
    await wrapper.find('#job-context-text').setValue('Relevant context');
    const aiButton = wrapper.findAll('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion').at(0);
    await aiButton.trigger('click');
    await wrapper.vm.$nextTick(); // Ensure modal is open and suggestions loaded

    // Verify modal is open
    expect(wrapper.vm.showSuggestionModal).toBe(true);
    const modalApplyButtons = wrapper.findAll('.suggestion-item .button-primary');
    expect(modalApplyButtons.length).toBeGreaterThan(0);

    // 2. Action: Click the first "Apply this suggestion" button
    const firstSuggestionText = getAIContentSuggestions.mock.results[0].value.suggestions[0].suggested_text;
    await modalApplyButtons.at(0).trigger('click');

    // 3. Assertions:
    // Check that the responsibility text was updated
    expect(resumeData.experience[0].responsibilities[0]).toBe(firstSuggestionText);
    
    // Check that the modal is closed
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.showSuggestionModal).toBe(false);
    expect(wrapper.find('.modal-backdrop').exists()).toBe(false);
  });

  it('closes modal when "Close" button is clicked', async () => {
    // 1. Setup: Open modal
    await wrapper.find('#job-context-text').setValue('Relevant context');
    const aiButton = wrapper.findAll('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion').at(0);
    await aiButton.trigger('click');
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.showSuggestionModal).toBe(true); // Modal is open

    // 2. Action: Click close button
    const closeButton = wrapper.find('.modal-content .button-secondary'); // Adjust selector if needed
    expect(closeButton.exists()).toBe(true);
    await closeButton.trigger('click');

    // 3. Assertions: Modal is closed
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.showSuggestionModal).toBe(false);
    expect(wrapper.find('.modal-backdrop').exists()).toBe(false);
  });
  
  it('displays original text in the modal', async () => {
    await wrapper.find('#job-context-text').setValue('Context for testing original text display.');
    const originalText = resumeData.experience[0].responsibilities[0];

    const aiButton = wrapper.findAll('.list-item .form-group .ai-suggestion-controls .button-ai-suggestion').at(0);
    await aiButton.trigger('click');
    await wrapper.vm.$nextTick();

    expect(wrapper.vm.showSuggestionModal).toBe(true);
    const modalOriginalText = wrapper.find('.modal-content p strong'); // Assuming first <p><strong> contains "原内容:"
    expect(modalOriginalText.exists()).toBe(true);
    expect(modalOriginalText.text()).toContain('原内容:');
    // The actual text is a sibling or part of the parent, need to check structure from ExperienceForm.vue
    // Example: <p><strong>原内容:</strong> {{ suggestionTarget.originalText }}</p>
    // So, the text content of the <p> element should include originalText
    expect(wrapper.find('.modal-content p').text()).toContain(originalText);
  });

});
