## claude-subagents

A collection of specialized agents, skills, and slash commands for Claude Code that enable structured multi-agent workflows, implementation planning, and Linear-based project orchestration.

## Table of Contents

- [Overview](#overview)
- [Skills](#skills)
- [Slash Commands](#slash-commands)
- [Agents](#agents)
- [Configuration](#configuration)

## Overview

This repository provides a framework for coordinating complex software development workflows using Claude Code. It includes:

- **Skills**: Reusable patterns and best practices for specific domains (planning, memory, context handoff, Linear operations)
- **Slash Commands**: Pre-built workflows that coordinate multiple agents through structured phases
- **Agents**: Specialized subagents with focused expertise and clear responsibilities

Together, these components enable systematic implementation of features with proper planning, execution, review, and learning capture.

## Skills

Skills are reusable pattern libraries that provide structured approaches for specific domains. Claude Code can invoke these skills when needed for guidance on best practices.

### context-handoff

**Use when:** Managing communication between multiple agents or workflow phases.

**Purpose:** Provides structured JSON formats for passing context between agents, ensuring minimal overhead while maintaining necessary information. Prevents context bloat and communication failures in multi-agent systems.

**Key patterns:**
- Standard task assignment formats
- Result return structures
- Phase transition patterns
- Error escalation protocols

**Location:** `skills/context-handoff/SKILL.md`

---

### implementation-planning

**Use when:** Breaking down features into implementable tasks or creating detailed implementation plans.

**Purpose:** Systematic decomposition of features into atomic tasks with clear acceptance criteria, dependencies, and risk assessment. Ensures work is properly scoped and testable.

**Key patterns:**
- Task sizing guidelines (XS/S/M/L/XL)
- Acceptance criteria templates
- Dependency mapping techniques
- Risk assessment frameworks

**Location:** `skills/implementation-planning/SKILL.md`

---

### linear-operations

**Use when:** Interacting with Linear issue tracking or maintaining Linear as source of truth.

**Purpose:** Best practices for creating, updating, and managing Linear issues programmatically. Provides consistent patterns for status updates, divergence documentation, and artifact linking.

**Key patterns:**
- Parent/child issue structures
- Status update formats
- Divergence documentation
- Progress tracking patterns

**Location:** `skills/linear-operations/SKILL.md`

---

### memory-patterns

**Use when:** Storing or retrieving persistent knowledge using the memory2 MCP server.

**Purpose:** Guidelines for building long-term knowledge while avoiding transient data pollution. Defines what to store (architectural decisions, learnings, business context) and what not to store (working state, progress updates).

**Key patterns:**
- Entity schemas (branches, features, decisions, learnings)
- Query patterns for planning phases
- Required fields (date_added, date_updated)
- Relation types for knowledge graphs

**Location:** `skills/memory-patterns/SKILL.md`

## Slash Commands

Slash commands are complete workflows that coordinate multiple specialist agents through structured phases. They can be invoked with `/command-name` in Claude Code.

### /implement

**Use when:** Implementing a feature without Linear integration.

**Purpose:** Guides users through a structured implementation workflow from requirements gathering to code review, all within an isolated git worktree.

**Workflow phases:**
1. **Requirements Gathering** - Interactive Q&A to capture needs
2. **Solution Design** - Architect proposes approach for user approval
3. **Implementation Planning** - Detailed task breakdown
4. **Feasibility Review** - Engineer validates the plan
5. **Worktree Setup** - Isolated environment for changes
6. **Implementation** - Engineer executes the plan
7. **Code Review** - Reviewer validates quality
8. **Completion** - User merges changes

**Agents spawned:** `implementation-architect`, `data-infra-engineer`, `code-reviewer`

**Location:** `~/.claude/commands/implement.md`

---

### /implement-linear-issue

**Use when:** Orchestrating a multi-agent software project with Linear issue tracking.

**Purpose:** Coordinates specialist agents through planning, execution, and completion phases with Linear as the single source of truth. Enables systematic feature delivery with sub-issue tracking, divergence documentation, and learning capture.

**Workflow phases:**
1. **Planning** - Architect creates plan, sub-issues generated
2. **Execution** - Engineers implement, reviewers validate
3. **Completion** - Knowledge synthesizer extracts learnings
4. **Recovery** - Handles blockers and systematic issues

**Agents spawned:** `implementation-architect`, `data-infra-engineer`, `code-reviewer`, `knowledge-synthesizer`

**Location:** `~/.claude/commands/implement-linear-issue.md`

## Agents

Agents are specialized subagents with focused expertise. Claude Code spawns these using the Task tool when their capabilities are needed.

### Planning & Architecture

#### implementation-architect
**Use when:** Planning features, evaluating approaches, or creating implementation plans before coding begins.

**Expertise:** Requirements analysis, solution design, risk assessment, acceptance criteria definition.

**Model:** Opus (complex planning requires advanced reasoning)

**Location:** `agents/implementation-architect.md`

---

### Implementation & Engineering

#### data-infra-engineer
**Use when:** Building data infrastructure, distributed systems, or backend services.

**Expertise:** Python, cloud platforms (AWS/GCP/DNAnexus), Ray/Spark, API design, dependency management, infrastructure as code.

**Model:** Sonnet (efficient for implementation tasks)

**Location:** `agents/data-infra-engineer.md`

#### data-engineer
**Use when:** Building data pipelines, ETL processes, or data infrastructure.

**Expertise:** Big data technologies, cloud platforms, scalable data processing.

**Location:** `agents/data-engineer.md`

---

### Review & Quality

#### code-reviewer
**Use when:** Reviewing code for quality, security, performance, and maintainability.

**Expertise:** Static analysis, security vulnerabilities, design patterns, test coverage, best practices across multiple languages.

**Location:** `agents/code-reviewer.md`

---

### Coordination & Orchestration

#### linear-orchestrator
**Use when:** Coordinating multi-agent projects through Linear issue tracking (typically invoked via `/implement-linear-issue`).

**Expertise:** Multi-agent coordination, Linear integration, workflow orchestration, context management.

**Location:** `agents/linear-orchestrator.md`

#### linear-project-manager
**Use when:** Managing Linear project state or retrieving project/issue context.

**Expertise:** Linear operations, project management, issue tracking.

**Location:** `agents/linear-project-manager.md`

#### multi-agent-coordinator
**Use when:** Managing complex workflows with parallel agent execution and dependency management.

**Expertise:** Agent coordination, parallel execution, fault tolerance.

**Location:** `agents/multi-agent-coordinator.md`

#### workflow-orchestrator
**Use when:** Designing or implementing complex process workflows and state machines.

**Expertise:** Workflow patterns, state management, business process automation.

**Location:** `agents/workflow-orchestrator.md`

#### agent-organizer
**Use when:** Assembling and coordinating teams of agents for complex tasks.

**Expertise:** Task decomposition, agent selection, team optimization.

**Location:** `agents/agent-organizer.md`

---

### Knowledge & Context

#### knowledge-synthesizer
**Use when:** Extracting learnings from completed projects or multi-agent interactions.

**Expertise:** Pattern identification, knowledge extraction, persistent memory management.

**Location:** `agents/knowledge-synthesizer.md`

#### context-manager
**Use when:** Managing information storage, retrieval, and synchronization across agents.

**Expertise:** State management, version control, data lifecycle.

**Location:** `agents/context-manager.md`

---

### Monitoring & Analysis

#### performance-monitor
**Use when:** Collecting metrics, analyzing system performance, or identifying optimization opportunities.

**Expertise:** Real-time monitoring, anomaly detection, distributed systems observability.

**Location:** `agents/performance-monitor.md`

#### error-coordinator
**Use when:** Handling distributed errors, implementing recovery strategies, or preventing failure cascades.

**Expertise:** Error correlation, automated recovery, system resilience.

**Location:** `agents/error-coordinator.md`

---

### Project Management

#### project-manager
**Use when:** Planning projects, managing resources, or coordinating stakeholder communication.

**Expertise:** Project planning, risk mitigation, resource management.

**Location:** `agents/project-manager.md`

#### task-distributor
**Use when:** Allocating work across agents, managing queues, or balancing load.

**Expertise:** Work allocation, priority scheduling, capacity tracking.

**Location:** `agents/task-distributor.md`

---

### Documentation

#### api-documenter
**Use when:** Creating or maintaining API documentation.

**Expertise:** OpenAPI/Swagger specs, interactive docs, documentation automation.

**Location:** `agents/api-documenter.md`

## Configuration

### Installing Skills

Skills are automatically available if the repository files are present. To use skills in your projects:

1. Clone this repository or copy the `skills/` directory to your project
2. Claude Code will automatically detect and load skill files
3. Invoke skills with: `Skill("skill-name")`

**Example:**
```
Skill("implementation-planning")
```

### Installing Slash Commands

Slash commands must be installed to your Claude Code configuration directory.

**For user-global commands** (available in all projects):

```bash
# Create commands directory if it doesn't exist
mkdir -p ~/.claude/commands

# Copy command files
cp path/to/claude-subagents/.claude/commands/*.md ~/.claude/commands/
```

**For project-specific commands**:

```bash
# In your project directory
mkdir -p .claude/commands
cp path/to/claude-subagents/.claude/commands/*.md .claude/commands/
```

After installation, commands are available with:
- `/implement` - For non-Linear workflows
- `/implement-linear-issue` - For Linear-integrated workflows

### Installing Agents

Agents are loaded automatically when referenced by other components (skills or commands). To use agents:

1. **Option A - Copy to project** (project-specific agents):
   ```bash
   cp -r path/to/claude-subagents/agents .claude/agents
   ```

2. **Option B - Copy to home** (user-global agents):
   ```bash
   mkdir -p ~/.claude/agents
   cp path/to/claude-subagents/agents/*.md ~/.claude/agents/
   ```

3. **Option C - Reference directly**: If this repository is in a known location, Claude Code can reference agent files directly via their path.

Agents are spawned by Claude Code using the Task tool when their capabilities are needed. You typically don't invoke them directly; they're called by slash commands or by Claude Code when appropriate.

### Verifying Installation

To verify your installation:

1. **Check skills**: In a Claude Code session, try `Skill("implementation-planning")`
2. **Check commands**: Type `/` in Claude Code to see available commands
3. **Check agents**: Agents will be automatically spawned when needed by workflows

### Project-Specific Configuration

For project-specific patterns or agent configurations, create a `CLAUDE.md` file in your project root with:

```markdown
# Project-Specific Instructions

## Available agents
- implementation-architect: For planning features
- data-infra-engineer: For implementing infrastructure

## Custom patterns
[Your project-specific patterns here]
```

Claude Code will automatically load and follow project-specific instructions from `CLAUDE.md` or `.claude/CLAUDE.md`.

## Usage Examples

### Example 1: Implementing a Feature Without Linear

```
User: /implement
Claude: What would you like to implement?
User: Add user authentication with JWT tokens
Claude: [Guides through requirements → design → planning → implementation → review]
```

### Example 2: Multi-Agent Project with Linear

```
User: /implement-linear-issue
Claude: What's the parent Linear issue ID?
User: LIN-100
Claude: [Coordinates architect, engineers, reviewers through structured phases]
```

### Example 3: Manual Agent Invocation

```
User: I need to plan the architecture for a new feature
Claude: [Spawns implementation-architect agent]
Agent: [Analyzes requirements, proposes approaches, creates plan]
```

## Contributing

To add new skills, commands, or agents:

1. **Skills**: Add to `skills/[skill-name]/SKILL.md` with frontmatter metadata
2. **Commands**: Add to `.claude/commands/[command-name].md` with description frontmatter
3. **Agents**: Add to `agents/[agent-name].md` with frontmatter specifying name, description, tools, model

Follow existing patterns for consistency.

## License

[Add your license here]
