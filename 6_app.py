import asyncio
from pydantic import BaseModel
from agents import Agent, Runner


class Invoice(BaseModel):
    invoice_number: str
    vendor: str
    invoice_date: str
    due_date: str
    total_amount: float
    currency: str

# invoice agent
invoice_agent = Agent(
    name="Invoice Extractor",
    instructions="""
    Extract invoice information from the text.
    Return the invoice number, vendor, invoice date,
    due date, total amount, and currency.
    """,
    output_type=Invoice,
    model="gpt-4o-mini",
)


async def main() -> None:
        invoice_text = """
        Invoice #INV-2026-1458

        Vendor: Amazon Web Services
        Invoice Date: July 10, 2026
        Due Date: August 9, 2026

        Total Due: USD 2,458.72
        """

        result = await Runner.run(starting_agent=invoice_agent, input=invoice_text)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())