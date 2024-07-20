from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from twitter.tools.search import SearchTools
from crewai_tools import SerperDevTool

@CrewBase
class TwitterCrew:
    """Twitter crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            tools=[
              SearchTools.search_twitter,
              SearchTools.open_page,
              SerperDevTool(),  # Using SerperDevTool for enhanced internet searches
            ],
            verbose=True,
        )

    @agent
    def content_strategist(self) -> Agent:
        return Agent(config=self.agents_config["content_strategist"], verbose=True)

    @agent
    def visual_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["visual_creator"],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(config=self.agents_config["copywriter"], verbose=True)

    @task
    def market_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_research"],
            agent=self.market_researcher(),
            output_file="twitter_market_research.md",
        )

    @task
    def content_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["content_strategy"],
            agent=self.content_strategist(),
        )

    @task
    def visual_content_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["visual_content_creation"],
            agent=self.visual_creator(),
            output_file="twitter_visual_content.md",
        )

    @task
    def copywriting_task(self) -> Task:
        return Task(
            config=self.tasks_config["copywriting"],
            agent=self.copywriter(),
        )

    @task
    def report_final_content_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["report_final_content_strategy"],
            agent=self.content_strategist(),
            output_file="final_twitter_content_strategy.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Twitter crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )