from premsql.agents import BaseLineAgent
from premsql.generators import Text2SQLGeneratorOpenAI
from premsql.executors import ExecutorUsingLangChain
from premsql.agents.tools import SimpleMatplotlibTool

client = Text2SQLGeneratorOpenAI(
    model_name="gpt-4o-mini",
    experiment_name="testing_openai",
    type="test",
    openai_api_key="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"
)


# You can also use Postgres, MySQL database as well.
db_connection_uri = "postgresql://postgres:yara123@localhost:5432/p3s_agent_db"

agent = BaseLineAgent(
    session_name="local_db_rag",
    db_connection_uri=db_connection_uri,
    specialized_model1=client,
    specialized_model2=client,
    executor=ExecutorUsingLangChain(),
    auto_filter_tables=False,
    plot_tool=SimpleMatplotlibTool()
)



output = agent(question="/query show me some Parfum, and my budget is in between 3 to 4k")
# If you want to see the pandas dataframe
print(output.show_output_dataframe())

# if you want to show the full output show this
# print(output)
# print(output)

