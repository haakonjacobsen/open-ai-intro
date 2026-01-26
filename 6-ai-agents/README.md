# AI Agents Workshop

## How to Run

1. **Install dependencies**:

   ```bash
   uv sync
   ```

2. **Create a `.env` file with your OpenAI API key**:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the agent**:

   ```bash
   uv run main.py
   ```

## Task 1: Add Tools

[Docs: Core concepts - Agents](https://ai.pydantic.dev/agents/)

Add two tools using `@agent.tool` that use the `database` dictionary:

1. **`read_data(id)`** - returns `database[id]` or "not found"
2. **`write_data(id, content)`** - saves to `database[id]` with a 2s delay

Example run, add a celbrity with key 0 to the database and then confirm its added to the in memory database.

```zsh
Type 'quit' to stop

You: Add a celebrity to the database on key "0", just pick someone
Writing '{"name": "Taylor Swift", "profession": "Singer-Songwriter", "birth_date": "1989-12-13", "nationality": "American"}' to id: 0
Agent: I have successfully added Taylor Swift, a singer-songwriter, to the database under key "0".

You: Find a celebrity with key 0
Reading data with id: 0
Agent: The celebrity with key 0 is Taylor Swift. She is an American singer-songwriter, born on December 13, 1989.
```

## Task 2: Add Dependencies

[Docs: Core Condepts -Dependencies](https://ai.pydantic.dev/dependencies/)

We have a celebrity database that persists to `database/celebrity.json`. Use dependency injection to connect the agent to this database.

1. Create an `AgentDependencies` dataclass with `celebrity_db: CelebrityDatabase`
2. Set `deps_type=AgentDependencies` on the agent
3. Add tools that use `ctx.deps.celebrity_db.read()`, `.write()`, and `.search()`
4. Pass `deps=AgentDependencies(celebrity_db=CelebrityDatabase())` when calling `agent.run_sync()`

Test with: "Who is celebrity 0?" or "Search for Taylor"

## Task 3: Structured Output

[Docs: Core Concepts - Output](https://ai.pydantic.dev/output/)

Add a structured response type so the agent returns a Pydantic model instead of plain text.

1. Create `AgentCelebrityResponse` with:
   - `celebrity: str | None` - the celebrity name if found
   - `message: str` - a message from the AI
2. Use `Field(description="...")` to describe each field to the model
3. Set `output_type=AgentCelebrityResponse` on the agent

Test with: "Find celebrity 0" - the response should include `celebrity: "Taylor Swift"`

## Task 4: Verify Data with External Source

Add a tool that looks up celebrity data from SNL (Store norske leksikon).

API docs: https://snl.no/api/v1/search?query=Taylor%20Swift

1. Create a `lookup_celebrity(name)` tool that fetches data from SNL, or use the functions in `snl.py`.
2. Update the system prompt to instruct the agent to **only** write verified data
3. The agent should refuse to write user-provided data without verification

Try to vibe code this! Explore the SNL API and see what data you can extract.

Test with:

- "Add Taylor Swift to the database" - should lookup and verify first
- "Make Taylor Swift 50 years old" - should refuse (can't verify fake data)

## Task 5: Streaming Output

[Docs: Streaming](https://ai.pydantic.dev/agents/#streaming-events-and-final-output)

Stream the agent's response to the terminal as it's generated.

1. Change `main()` to `async def main()` and use `asyncio.run(main())`
2. Use `agent.run_stream()` instead of `agent.run_sync()`
3. Stream text with `async for text in response.stream_text()`

```python
async with agent.run_stream(user_input, deps=deps) as response:
    async for text in response.stream_text():
        print(text, end="", flush=True)
```
