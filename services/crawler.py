# services/crawler.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from core.config import OPENAI_API_KEY, OPENAI_MODEL
from schemas.product import ProductInfo
import logging
from typing import Optional
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from urllib.parse import quote, urljoin, urlparse, parse_qs
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealTimeCrawler:
	def __init__(self):
		self.products = []
		self.platform_configs = {
            'nykaa': {
                'product_wrapper': 'div[class*="productWrapper"]',
                'base_url': 'https://www.nykaa.com',
                'search_url': 'https://www.nykaa.com/search/result/?q={query}&root=search&searchType=Manual&sourcepage=Search+Page',
                'product_url_pattern': 'https://www.nykaa.com/{product_path}?productId={product_id}&pps=1',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
            },
            'amazon': {
                'product_wrapper': 'div[data-component-type="s-search-result"]',
                'base_url': 'https://www.amazon.in',
                'search_url': 'https://www.amazon.in/s?k={query}',
                'product_url_pattern': 'https://www.amazon.in/dp/{asin}',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                }
            }
        }
        
		self.llm = ChatOpenAI(
            temperature=0.7,
            model=OPENAI_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
		self.parser = PydanticOutputParser(pydantic_object=ProductInfo)
		self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a product information extraction expert. 
            Extract product information from the provided HTML content for {platform}.
            For Nykaa products:
            - Look for product URLs in <a> tags with href attributes
            - Extract product IDs from URL patterns like '/product-name/p/12345'
            - Look for mrp-price class for original price and selling-price for current price
            For Amazon products:
            - Look for product URLs in <a> tags with href attributes
            - Extract ASIN from URL patterns like '/dp/B0XXXXX' or '/gp/product/B0XXXXX'
            - Look for 'a-price' class elements for prices
            Format the information exactly according to the specified schema.
            If information is not available, leave it as null."""),
            ("user", "Extract product information from this HTML:\n{html_content}\n\n{format_instructions}")
        ])
  
	async def fetch_page(self, url: str, platform: str, retries: int = 3) -> Optional[str]:
		"""Fetch page content with retries"""
		config = self.platform_configs.get(platform.lower())
		if not config:
			raise ValueError(f"Unsupported platform: {platform}")

		for attempt in range(retries):
			try:
				async with aiohttp.ClientSession(headers=config['headers']) as session:
					async with session.get(url, ssl=False, timeout=30) as response:
						if response.status == 200:
							return await response.text()
						elif response.status == 404:
							logger.error(f"Page not found: {url}")
							return None
						elif response.status == 429:
							wait_time = 2 ** attempt
							logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
							await asyncio.sleep(wait_time)
							continue
						else:
							logger.error(f"Failed to fetch page: {response.status}")
			except Exception as e:
				logger.error(f"Error fetching page (attempt {attempt + 1}): {str(e)}")
				if attempt < retries - 1:
					await asyncio.sleep(2 ** attempt)
				continue
		return None

	async def extract_product_info(self, html_content: str, platform: str) -> Optional[ProductInfo]:
		"""Extract product information using LangChain and OpenAI"""
		try:
			messages = self.prompt.format_messages(
                platform=platform,
                html_content=html_content,
                format_instructions=self.parser.get_format_instructions()
            )
			response = await self.llm.agenerate([messages])
			product_info = self.parser.parse(response.generations[0][0].text)
			if product_info.product_url:
				if platform.lower() == 'nykaa':
					product_info.product_url = self.process_nykaa_url(product_info.product_url)
				elif platform.lower() == 'amazon':
					product_info.product_url = self.process_amazon_url(product_info.product_url)
			product_info.platform = platform
			return product_info

		except Exception as e:
			logger.error(f"Error extracting product info: {str(e)}")
			return None
			
	async def search_products(self, query: str, platform: str, limit: int = 10):
		"""Search products with a query and limit results"""
		config = self.platform_configs.get(platform.lower())
		if not config:
			raise ValueError(f"Unsupported platform: {platform}")

		self.products = []
		encoded_query = quote(query)
		search_url = config['search_url'].format(query=encoded_query)
        
		logger.info(f"Searching for '{query}' on {platform}")
		content = await self.fetch_page(search_url, platform)
        
		if content:
			soup = BeautifulSoup(content, 'html.parser')
			product_elements = soup.select(config['product_wrapper'])
            
			if not product_elements:
				logger.warning(f"No products found for query: {query}")
				return
            
			product_elements = product_elements[:limit]
            
			for element in product_elements:
				product_info = await self.extract_product_info(str(element), platform)
				if product_info:
					self.products.append(product_info.dict())
					logger.info(f"Extracted product: {product_info.product_name}")
            
				await asyncio.sleep(2)  # Respect rate limits
		else:
			logger.error(f"Failed to fetch search results for query: {query}")
   
	# Platform Specific:
	#############################################################
	# Amazon
 	#############################################################
	def process_amazon_url(self, raw_url: str) -> str:
		"""Process Amazon product URL to ensure complete format"""
		try:
			if raw_url.startswith(self.platform_configs['amazon']['base_url']):
				asin = self.extract_amazon_asin(raw_url)
				if asin:
					return self.platform_configs['amazon']['product_url_pattern'].format(asin=asin)
				return raw_url

			if raw_url.startswith('/'):
				asin = self.extract_amazon_asin(raw_url)
				if asin:
					return self.platform_configs['amazon']['product_url_pattern'].format(asin=asin)
				return urljoin(self.platform_configs['amazon']['base_url'], raw_url)
			return raw_url
		except Exception as e:
			logger.error(f"Error processing Amazon URL: {str(e)}")
			return raw_url
  
	def extract_amazon_asin(self, url: str) -> Optional[str]:
		"""Extract ASIN from Amazon URL"""
		try:
			patterns = [
                r'/dp/([A-Z0-9]{10})',
                r'/product/([A-Z0-9]{10})',
                r'/gp/product/([A-Z0-9]{10})',
                r'asin=([A-Z0-9]{10})'
            ]
   
			parsed_url = urlparse(url)
			path = parsed_url.path
			query = parse_qs(parsed_url.query)
   
			for pattern in patterns:
				match = re.search(pattern, path)
				if match:
					return match.group(1)
				if 'asin' in query:
					return query['asin'][0]
				return None

		except Exception as e:
			logger.error(f"Error extracting ASIN: {str(e)}")
			return None
  
  
	#############################################################
	# Nykaa
 	#############################################################
	def process_nykaa_url(self, raw_url: str) -> str:
		"""Process Nykaa product URL to ensure complete format"""
		try:
			if raw_url.startswith(self.platform_configs['nykaa']['base_url']):
				return raw_url
			parts = raw_url.split('/')
			product_id = None

			for part in parts:
				if part.startswith('p_'):
					product_id = part[2:]
				elif part.startswith('p/'):
					product_id = part[2:]
            
			if not product_id and parts[-2] == 'p':
				product_id = parts[-1]
                
			if product_id:
				product_path = '/'.join(p for p in parts if not p.startswith('p_') and p != 'p' and p != product_id)
				product_path = product_path.strip('/')
				return self.platform_configs['nykaa']['product_url_pattern'].format(
                    product_path=product_path,
                    product_id=product_id
                )
                
			return urljoin(self.platform_configs['nykaa']['base_url'], raw_url)
        
		except Exception as e:
			logger.error(f"Error processing Nykaa URL: {str(e)}")
			return raw_url
