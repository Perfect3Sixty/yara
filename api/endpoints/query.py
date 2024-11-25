# # api/endpoints/query.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.responses import StreamingResponse, JSONResponse
# from sqlalchemy.orm import Session
# from typing import Optional, List, Any, Dict
# from pydantic import BaseModel
# from services.postgres import get_db
# from processors.sql_processor import SQLQueryProcessor
# from processors.txt2sql_processor import Txt2sqlProcessor
# from services.crawler import RealTimeCrawler
# import pandas as pd
# import json
# import asyncio
# import traceback

# router = APIRouter()
# sql_processor = SQLQueryProcessor()
# txt2sql_processor = Txt2sqlProcessor()
# crawler = RealTimeCrawler()

# class QueryRequest(BaseModel):
#     query: str
#     platform: Optional[str] = None

# class ProductSearchResponse(BaseModel):
#     query: str
#     platform: str
#     products: List[Dict[str, Any]]
#     error: Optional[str] = None

# class QueryResponse(BaseModel):
#     query: str
#     results: Optional[List[Dict[str, Any]]] = None
#     error: Optional[str] = None

# async def clean_product(product: Dict) -> Dict:
#     """Clean product data for JSON serialization"""
#     cleaned_product = {}
#     for key, value in product.items():
#         if pd.isna(value):
#             cleaned_product[key] = None
#         elif isinstance(value, pd.Timestamp):
#             cleaned_product[key] = value.isoformat()
#         else:
#             cleaned_product[key] = value
#     return cleaned_product

# async def send_message(message_type: str, data: Any, platform: str = None) -> str:
#     """Helper function to format SSE messages"""
#     message = {
#         "type": message_type,
#         "data": data
#     }
#     if platform:
#         message["platform"] = platform
#     return f"data: {json.dumps(message)}\n\n"

# async def product_search_generator(query: str, platform: Optional[str] = None):
#     """Generator function for streaming product search results"""
#     platforms = ['nykaa', 'amazon']
#     total_products = 0
    
#     try:
#         if platform:
#             if platform.lower() not in platforms:
#                 yield await send_message("error", f"Unsupported platform: {platform}")
#                 return
#             platforms = [platform.lower()]
#             items_per_platform = 6
#         else:
#             items_per_platform = 3

#         # Send initial message
#         yield await send_message(
#             "info", 
#             f"Starting search for '{query}' across {', '.join(platforms)}"
#         )
        
#         for platform_name in platforms:
#             try:
#                 # Send platform start message
#                 yield await send_message(
#                     "platform_start",
#                     f"Searching {platform_name}...",
#                     platform_name
#                 )

#                 # Start the search
#                 await crawler.search_products(
#                     query=query,
#                     platform=platform_name,
#                     limit=items_per_platform
#                 )

#                 # Stream each product as it's found
#                 platform_products = 0
#                 for product in crawler.products:
#                     cleaned_product = await clean_product(product)
#                     yield await send_message("product", cleaned_product, platform_name)
#                     platform_products += 1
#                     total_products += 1
#                     await asyncio.sleep(0.1)

#                 # Platform completion message
#                 yield await send_message(
#                     "platform_complete",
#                     f"Found {platform_products} products on {platform_name}",
#                     platform_name
#                 )

#                 # Clear products for next platform
#                 crawler.products = []
#                 await asyncio.sleep(0.5)  # Brief pause between platforms

#             except Exception as e:
#                 error_details = traceback.format_exc()
#                 print(f"Error processing {platform_name}: {error_details}")
#                 yield await send_message(
#                     "error",
#                     f"Error searching {platform_name}: {str(e)}",
#                     platform_name
#                 )

#         # Ensure we send a completion message
#         if total_products > 0:
#             yield await send_message(
#                 "complete",
#                 f"Search completed. Found {total_products} products total."
#             )
#         else:
#             yield await send_message(
#                 "complete",
#                 "Search completed. No products found."
#             )

#     except Exception as e:
#         error_details = traceback.format_exc()
#         print(f"Generator error: {error_details}")
#         yield await send_message("error", f"Search failed: {str(e)}")
#         yield await send_message("complete", "Search terminated due to error.")
        
        
# @router.get("/products/stream")
# async def stream_products(
#     query: str,
#     platform: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     """Stream product search results using server-sent events."""
#     return StreamingResponse(
#         product_search_generator(query, platform),
#         media_type="text/event-stream"
#     )
    
    
# @router.post("/query", response_model=QueryResponse)
# async def process_query(
#     request: QueryRequest,
#     db: Session = Depends(get_db)
# ):
#     """Process natural language query and return results."""
#     result = await sql_processor.process_query(request.query)
#     if result.get("error"):
#         print(f"Error occurred: {result['error']}")
#         return result

# @router.post("/v1/query", response_model=QueryResponse)
# async def process_natural_query(
#     request: QueryRequest,
#     db: Session = Depends(get_db)
# ):
#     """Process natural language query using PremSQL agent and return results."""
#     try:
#         agent_response = txt2sql_processor.agent(request.query)
        
#         if agent_response is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="No results found for the given query"
#             )
        
#         df = agent_response.show_output_dataframe()
        
#         if df is None or df.empty:
#             return QueryResponse(
#                 query=request.query,
#                 results=[],
#                 error=None
#             )
        
#         results = df.to_dict(orient='records')
        
#         cleaned_results = []
#         for item in results:
#             cleaned_item = {}
#             for key, value in item.items():
#                 if pd.isna(value):
#                     cleaned_item[key] = None
#                 elif isinstance(value, pd.Timestamp):
#                     cleaned_item[key] = value.isoformat()
#                 else:
#                     cleaned_item[key] = value
#             cleaned_results.append(cleaned_item)
        
#         return QueryResponse(
#             query=request.query,
#             results=cleaned_results,
#             error=None
#         )
        
#     except Exception as e:
#         print(f"Error processing query: {str(e)}")
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=QueryResponse(
#                 query=request.query,
#                 results=None,
#                 error=f"Error processing query: {str(e)}"
#             ).dict()
#         )