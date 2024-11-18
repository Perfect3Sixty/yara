# processors/sql_processor.py
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, text
from core.config import POSTGRES_URL, OPENAI_API_KEY

class SQLQueryProcessor:
    def __init__(self):
        self.db = SQLDatabase.from_uri(POSTGRES_URL)
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)
        self.chain = create_sql_query_chain(llm=self.llm, db=self.db)
        
        # Define the table schema for context
        self.table_context = """
        The 'products' table contains beauty products with the following columns:
        - id: Integer (primary key)
        - product_name: String (name of the product)
        - price: String (price with currency symbol)
        - price_value: Float (numerical price value)
        - rating: Float (product rating)
        - description: Text (product description)
        - link: String (product URL)
        
        Return only the raw SQL query without any markdown formatting, prefixes, or explanations.
        """
    
    def clean_sql_query(self, sql_query: str) -> str:
        """Clean the SQL query by removing markdown formatting, prefixes, and extra whitespace."""
        sql_query = sql_query.replace('```sql', '').replace('```', '')
        prefixes_to_remove = [
            "SQLQuery:", 
            "SQL:", 
            "Query:", 
            "postgresql:"
        ]
        for prefix in prefixes_to_remove:
            if sql_query.startswith(prefix):
                sql_query = sql_query[len(prefix):]
        
        # Clean up whitespace and newlines
        sql_query = ' '.join(sql_query.split())
        
        return sql_query.strip()
    
    async def process_query(self, query_text: str) -> dict:
        """Process natural language query and return SQL results."""
        try:
            # Generate SQL query using the chain
            sql_query = await self.chain.ainvoke({
                "question": query_text,
                "schema": self.table_context
            })
            
            # Clean the SQL query
            sql_query = self.clean_sql_query(sql_query)
            
            # TODO will be removed
            print(f"Cleaned SQL: {sql_query}")  # Debug logging
            
            # Execute query and get results
            engine = create_engine(POSTGRES_URL)
            with engine.connect() as connection:
                result = connection.execute(text(sql_query))
                rows = result.fetchall()
                
            # Convert results to list of dicts
            columns = result.keys()
            results = [dict(zip(columns, row)) for row in rows]
            
            return {
                "query": sql_query,
                "results": results,
                "error": None
            }
        except Exception as e:
            print(f"Error processing query: {str(e)}")  # Debug logging
            return {
                "error": str(e),
                "query": None,
                "results": None
            }