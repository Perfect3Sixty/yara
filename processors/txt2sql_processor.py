# # processors/txt2sql_processor.py
# from premsql.agents import BaseLineAgent
# from premsql.generators import Text2SQLGeneratorOpenAI
# from premsql.executors import ExecutorUsingLangChain
# from premsql.agents.tools import SimpleMatplotlibTool
# from core.config import OPENAI_MODEL, OPENAI_API_KEY, POSTGRES_URL


# class Txt2sqlProcessor:
#   def __init__(self):
#     self.premsql_client = Text2SQLGeneratorOpenAI(
#         model_name=OPENAI_MODEL,
#         experiment_name="yara_agent",
#         type="test",
#         openai_api_key=OPENAI_API_KEY
#     )
    
#     self.agent = BaseLineAgent(
# 		session_name="local_db_rag",
# 		db_connection_uri=POSTGRES_URL,
# 		specialized_model1=self.premsql_client,
# 		specialized_model2=self.premsql_client,
# 		executor=ExecutorUsingLangChain(),
# 		auto_filter_tables=False,
# 		plot_tool=SimpleMatplotlibTool()
# 	)
  