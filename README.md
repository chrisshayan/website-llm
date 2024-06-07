# website-llm
Using OpenAI, LangChain, BeautifulSoup and Gradio to build a tool to talk to your website.

In my example, I built a Spring Framework Q&A interface by scraping documentation (depth 10). This approach allows users to have a natural conversation and find answers directly within your website. You can scrape the website data using BeautifulSoup, embed it into Chroma and use OpenAIEmbeddings then use ChatOpenAI LLM to build the chat and quickly launch it with beautiful UI of Gradio.

# How to use it
python Scrape.py --site https://spring.io/projects/spring-framework --depth 10
python Embed.py
python main.py
