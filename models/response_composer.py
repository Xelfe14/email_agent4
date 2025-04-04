from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class ResponseComposer:
    """
    Composes a final email response by combining style drafts with web research.
    """

    def __init__(self, api_key: str):
        """
        Initialize the response composer.

        Args:
            api_key: OpenAI API key
        """
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )

        self.template = """
        <Context>
        You are a professional and experienced investment fund representative. Your task is to compose a complete, personalized email response to a potential investment opportunity.
        </Context>

        <Input>
        EXTRACTED INFORMATION FROM THE ORIGINAL EMAIL:
        {extracted_info}

        STYLE-BASED DRAFT (based on past similar responses):
        {style_draft}

        RESEARCH FINDINGS ABOUT THE COMPANY:
        {research_data}
        </Input>

        <Task>
        1. Create a polished, complete email response that maintains the style and tone from the draft.
        2. Incorporate relevant details from the research findings to demonstrate knowledge about the company and industry.
        3. Address the specific request or ask mentioned in the original email.
        4. Be specific and personalized, referencing the company name, founder names, and industry details where appropriate.
        5. Include a clear next step or call to action if appropriate.
        6. Keep the response professional but warm.
        </Task>
        <Rules>
        SIGNATURE INSTRUCTIONS (VERY IMPORTANT):
        - End the email with ONLY a simple sign-off like "Best regards," or "Kind regards," or "Best,"
        - DO NOT add any signature block
        - DO NOT include placeholders like [Your Name], [Your Title], [Your Contact Information]
        - DO NOT include any name, title, or company information
        </Rules>
        <Examples>
        Example of correct ending:
        "I look forward to our discussion.

        Best regards,"

        Example of INCORRECT ending (DO NOT USE):
        "I look forward to our discussion.

        Best regards,
        [Your Name]
        [Your Title]
        [Your Contact Information]"
        </Examples>

        <Output>
        COMPLETE EMAIL RESPONSE:
        </Output>
        """

        self.prompt = ChatPromptTemplate.from_template(self.template)

    def compose_response(self,
                        extracted_info: Dict[str, Any],
                        style_draft: str,
                        research_data: str) -> str:
        """
        Compose a final email response by merging style and research data.

        Args:
            extracted_info: Dictionary of extracted entities from the original email
            style_draft: Draft response generated based on similar historical emails
            research_data: Research findings about the company/sender

        Returns:
            Final composed email response
        """
        # Format extracted info as text
        if isinstance(extracted_info, dict):
            extracted_info_text = "\n".join([f"{k}: {v}" for k, v in extracted_info.items()])
        else:
            extracted_info_text = str(extracted_info)

        # Generate final response
        chain = self.prompt | self.llm
        response = chain.invoke({
            "extracted_info": extracted_info_text,
            "style_draft": style_draft,
            "research_data": research_data
        })

        return response.content
