# processors/sql_processor.py
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from core.config import POSTGRES_URL, OPENAI_API_KEY

class SQLQueryProcessor:
    def __init__(self):
        self.db = SQLDatabase.from_uri(POSTGRES_URL)
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613", api_key=OPENAI_API_KEY)
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
        """
    
    async def process_query(self, query_text: str) -> dict:
        """Process natural language query and return SQL results."""
        try:
            # Combine user query with table context
            full_query = f"{self.table_context}\n\nUser question: {query_text}"
            
            # Generate SQL query
            sql_query = await self.chain.ainvoke(full_query)
            
            # Execute query and get results
            engine = create_engine(POSTGRES_URL)
            with engine.connect() as connection:
                result = connection.execute(sql_query)
                rows = result.fetchall()
                
            # Convert results to list of dicts
            columns = result.keys()
            results = [dict(zip(columns, row)) for row in rows]
            
            return {
                "query": sql_query,
                "results": results
            }
        except Exception as e:
            return {
                "error": str(e),
                "query": None,
                "results": None
            }