## Additional skills

### project-specific dev tools / workflows 
This would be a skill such as `unit-testing` which triggers `just test` when activated, or `uv run pytest <args>` if needing to filter tests. This could be done for all just commands. These would be project-level skills, so each project could specify its own toolchain.
project-specific useful skills:
- testing
- deployment
- build image
- retrieve project context
    - this could be a good way to make a single source of truth for accessing context, and could be customized to where the project docs are stored.
- reflection
    - use when completing a task or ses

### sending / receiving a slack message
This could be super useful for when claude has questions - it's really easy to lose track of the terminal and have claude waiting on you. Maybe you could even have a skill for retrieving messages so it could poll and you could just respond to its message in slack

### break up context-handoff into multiple skills