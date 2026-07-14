from pydantic import BaseModel
from agents import Agent, Runner, function_tool
import asyncio
from enum import Enum
import sqlite3
import mysql.connector

@function_tool
def get_customer_by_email_v1(email: str) -> dict:
    """
    Retrieve a customer's information using their email address.
    """

    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT customer_id,
               first_name,
               last_name,
               email,
               phone,
               membership_level,
               account_status
        FROM customers
        WHERE email = ?
        """,
        (email,),
    )

    customer = cursor.fetchone()
    conn.close()

    if customer is None:
        return {
            "found": False,
            "message": f"No customer found with email {email}"
        }

    return {
        "found": True,
        "customer": dict(customer)
    }


@function_tool
def get_customer_by_email_v2(email: str) -> dict:

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="sales"
    )

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM customers WHERE email=%s",
        (email,),
    )

    customer = cursor.fetchone()

    conn.close()

    return customer or {}



class Category(Enum):
    BILLING = "Billing"
    TECHNICAL = "Technical Support"
    ACCOUNT = "Account Management"
    SALES = "Sales"
    SHIPPING = "Shipping"
    REFUND = "Refund"
    FEATURE_REQUEST = "Feature Request"
    BUG_REPORT = "Bug Report"
    GENERAL = "General Inquiry"

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Sentiment(Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"
    FRUSTRATED = "Frustrated"
    URGENT = "Urgent"

class SupportTicket(BaseModel):
    ticket_id: str
    customer_name: str
    email: str
    categories: list[Category]
    priority: Priority
    sentiment: Sentiment
    summary: str


agent = Agent(
    name="Support Ticket Analyzer",
    instructions="""
    Classify the support ticket into a category,
    determine its priority,
    analyze customer sentiment,
    and summarize the issue.
    Whenever the user asks about their accounts, use the get_customer_by_email tool first.
    """,
    output_type=SupportTicket,
    model="gpt-4o-mini",
    tools=[get_customer_by_email_v1, get_customer_by_email_v2]
)

async def main() -> None:
        support_text = """
        Hello,
        I'm John Smith. I was charged twice for my monthly subscription after upgrading my account. 
        I've contacted support twice but haven't received a response.
        Please refund the duplicate charge as soon as possible.
        My email is john@gmail.com.
        Ticket ID: CS-10452.

        Can you check my account? my email is john@gmail.com.
        """

        result = await Runner.run(starting_agent=agent, input=support_text)
        print(f"Agent: {result.final_output}\n")
        print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())