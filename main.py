from multi_agent_executor import MultiAgentExecutor


if __name__ == "__main__":
    executor = MultiAgentExecutor()
    try:
        executor.run()
    finally:
        executor.close()
