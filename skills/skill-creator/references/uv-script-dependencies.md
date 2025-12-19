# UV Script Dependencies

This guide shows how to create standalone Python scripts with inline dependency declarations that can be executed directly using `uv run --script`.

## Overview

UV supports PEP 723 inline script metadata, allowing scripts to declare their own dependencies without requiring a separate `pyproject.toml` or virtual environment setup. This makes scripts truly portable and self-contained.

## Basic Pattern

Add this header to any Python script:

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "pydantic>=2.0",
# ]
# ///
```

## Header Components

1. **Shebang line**: `#!/usr/bin/env -S uv run --script`
   - Makes the script executable
   - The `-S` flag allows passing multiple arguments through env

2. **Script metadata block**: Enclosed by `# /// script` and `# ///`
   - Must use exactly this format (three slashes, lowercase "script")
   - `requires-python`: Specify minimum Python version
   - `dependencies`: List of package requirements (supports version specifiers)

## Complete Example

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx",
#     "pydantic>=2.0",
#     "rich",
# ]
# ///

import httpx
from pydantic import BaseModel
from rich import print

class Response(BaseModel):
    status: int
    data: dict

def main():
    response = httpx.get("https://api.example.com/data")
    result = Response(status=response.status_code, data=response.json())
    print(result)

if __name__ == "__main__":
    main()
```

## Execution

Once the script has the proper header:

```bash
# Make executable (one time)
chmod +x script.py

# Run directly
./script.py

# Or run explicitly with uv
uv run --script script.py
```

UV automatically:
- Creates an isolated temporary environment
- Installs the declared dependencies
- Executes the script
- Caches the environment for subsequent runs

## Benefits for Skills

This pattern is ideal for skill scripts because:

1. **Self-contained**: Dependencies are declared inline, no separate requirements file needed
2. **Portable**: Script works anywhere UV is installed
3. **Fast**: UV caches environments, so repeated runs are quick
4. **Version-specific**: Each script can specify its own Python version and dependency versions
5. **No pollution**: Doesn't affect system Python or project virtual environments

## Best Practices

1. **Pin Python version**: Use `>=3.X` to ensure compatibility
2. **Specify dependency versions**: Use version constraints (`>=`, `<`, `==`) to ensure reproducibility
3. **Keep dependencies minimal**: Only include what the script actually needs
4. **Test the script**: Always run the script to verify it works with declared dependencies

