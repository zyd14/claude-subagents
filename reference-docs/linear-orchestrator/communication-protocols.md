# Communication Protocols

Structured formats for all agent communication in the Linear orchestration workflow.

## Core Principles

- **Always use JSON** for structured data exchange
- **Validate inputs** before invoking agents
- **Validate outputs** before updating Linear
- **Standardize field names** across all protocols
- **Include rationale** for all divergences and decisions

## Engineer Input Format

Provide when assigning implementation work to Data Infrastructure Engineer.

```json
{
  "issue_id": "LIN-123",
  "context_summary": "Implement user authentication endpoint",
  "acceptance_criteria": [
    "POST /api/auth/login accepts email/password",
    "Returns JWT token on success",
    "Returns 401 on invalid credentials",
    "Includes rate limiting (5 attempts/minute)",
    "Comprehensive error handling for DB timeouts"
  ],
  "dependencies": [
    "LIN-120: User model created and tested",
    "LIN-121: JWT library integrated"
  ],
  "constraints": [
    "Use existing auth library (auth-lib v2.1)",
    "Don't create new authentication mechanism",
    "Must be backward compatible with v1 API",
    "Rate limiting must use Redis"
  ],
  "relevant_learnings": [
    "Always include error handling for DB timeouts",
    "Previous engineers needed extra input validation",
    "Redis preferred over in-memory for rate limiting"
  ]
}
```

**Field descriptions:**
- `issue_id`: Linear issue ID (required)
- `context_summary`: One-line description of task (required)
- `acceptance_criteria`: Testable conditions for completion (required, array)
- `dependencies`: Issues that must be complete first (optional, array with descriptions)
- `constraints`: Technical or business limitations (optional, array)
- `relevant_learnings`: 2-3 applicable insights from past work (optional, array)

**Key practices:**
- Keep context_summary to one sentence
- Make acceptance_criteria specific and testable
- List dependencies with brief context
- Include only directly relevant learnings
- Target <2000 tokens total

## Engineer Output Format

Expected return format from Data Infrastructure Engineer.

```json
{
  "issue_id": "LIN-123",
  "status": "complete",
  "summary": "Implemented login endpoint with JWT token generation, rate limiting via Redis, and comprehensive error handling including DB timeout scenarios",
  "divergences": [
    {
      "description": "Added Redis connection pooling",
      "rationale": "Without pooling, rate limiting caused connection exhaustion under load testing",
      "impact": "Minor performance improvement, no API changes"
    },
    {
      "description": "Extended token expiry from 1h to 4h",
      "rationale": "Product team requested during implementation for better UX",
      "impact": "Security implication - should be reviewed"
    }
  ],
  "artifacts": [
    "src/api/auth/login.py",
    "src/api/auth/rate_limiter.py",
    "tests/test_auth_login.py",
    "tests/test_rate_limiting.py",
    "docs/api/auth.md"
  ],
  "blockers": [],
  "notes": "All acceptance criteria met. Added comprehensive logging for security audits. Token expiry change should be reviewed by security team."
}
```

**Field descriptions:**
- `issue_id`: Linear issue ID (required)
- `status`: "complete" | "blocked" | "needs_clarification" (required)
- `summary`: Brief description of work completed (required)
- `divergences`: Any changes from original plan (required, array - empty if none)
  - Each divergence must include description, rationale, and impact
- `artifacts`: All files created/modified (required, array)
- `blockers`: Any issues preventing completion (required, array - empty if none)
- `notes`: Additional context, warnings, or recommendations (optional)

**Status values:**
- `complete`: All acceptance criteria met, ready for review
- `blocked`: Cannot proceed, requires external action
- `needs_clarification`: Acceptance criteria unclear or contradictory

**Divergence guidelines:**
- Document ALL changes from plan, even minor ones
- Always include rationale (why was this necessary?)
- Assess impact (breaking changes, performance, security)
- Flag concerns that need review

## Reviewer Input Format

Provide when assigning quality review to Code Reviewer.

```json
{
  "issue_id": "LIN-123",
  "context_summary": "Review login endpoint implementation",
  "acceptance_criteria": [
    "POST /api/auth/login accepts email/password",
    "Returns JWT token on success",
    "Returns 401 on invalid credentials",
    "Includes rate limiting (5 attempts/minute)",
    "Comprehensive error handling for DB timeouts"
  ],
  "artifacts": [
    "src/api/auth/login.py",
    "src/api/auth/rate_limiter.py",
    "tests/test_auth_login.py",
    "tests/test_rate_limiting.py"
  ],
  "review_scope": "Code quality, security best practices, acceptance criteria match, test coverage",
  "engineer_notes": "Token expiry changed from 1h to 4h per product request - should be reviewed for security implications"
}
```

**Field descriptions:**
- `issue_id`: Linear issue ID (required)
- `context_summary`: One-line description of what's being reviewed (required)
- `acceptance_criteria`: Same criteria given to engineer (required, array)
- `artifacts`: Files to review (required, array)
- `review_scope`: What to assess (required)
- `engineer_notes`: Important context from implementation (optional)

**Review scope should specify:**
- Code quality and maintainability
- Security considerations
- Acceptance criteria compliance
- Test coverage and quality
- NOT: Scope expansion or new features

## Reviewer Output Format

Expected return format from Code Reviewer.

```json
{
  "issue_id": "LIN-123",
  "status": "approved_with_suggestions",
  "feedback": [
    {
      "type": "required_change",
      "description": "Token expiry of 4h violates security policy (max 2h)",
      "location": "src/api/auth/login.py:45",
      "priority": "high",
      "suggestion": "Reduce to 2h or obtain security team approval"
    },
    {
      "type": "suggestion",
      "description": "Consider adding logging for failed login attempts",
      "location": "src/api/auth/login.py:67",
      "priority": "low",
      "suggestion": "Log failed attempts for security monitoring"
    },
    {
      "type": "praise",
      "description": "Excellent error handling for DB timeouts",
      "location": "src/api/auth/login.py:89",
      "priority": "info"
    }
  ],
  "concerns": [
    "Token expiry change needs security team review before production"
  ],
  "decision": "approved_with_changes",
  "reasoning": "Implementation meets all acceptance criteria and code quality is high. However, token expiry change violates security policy and must be addressed before merge."
}
```

**Field descriptions:**
- `issue_id`: Linear issue ID (required)
- `status`: Detailed status (see values below) (required)
- `feedback`: Array of specific feedback items (required, may be empty)
- `concerns`: High-level issues needing attention (optional, array)
- `decision`: Final approval decision (required)
- `reasoning`: Brief explanation of decision (required)

**Status values:**
- `approved`: No changes needed, ready to merge
- `approved_with_suggestions`: Optional improvements identified
- `approved_with_changes`: Minor required changes
- `changes_required`: Significant issues must be fixed
- `rejected`: Does not meet acceptance criteria

**Feedback types:**
- `required_change`: Must be fixed before approval
- `suggestion`: Optional improvement
- `question`: Needs clarification
- `praise`: Positive observation (for learning)
- `concern`: Broader issue to flag

**Decision values:**
- `approved`: Ready for merge
- `approved_with_changes`: Fix required items then merge
- `changes_required`: Re-review needed after fixes
- `rejected`: Fundamental issues, reassign

## Architect Input Format

Provide when requesting implementation plan from Implementation Architect.

```json
{
  "issue_id": "LIN-100",
  "project_summary": "Build user authentication system with JWT tokens, rate limiting, and session management",
  "requirements": [
    "Support email/password authentication",
    "JWT token-based sessions",
    "Rate limiting per user and globally",
    "Session invalidation support",
    "Integration with existing user database"
  ],
  "constraints": {
    "technical": [
      "Must use Python 3.11+",
      "PostgreSQL for user data",
      "Redis available for caching",
      "Must integrate with existing API gateway"
    ],
    "timeline": "2 weeks for MVP",
    "resources": "2 engineers available",
    "security": "Must comply with OWASP guidelines"
  },
  "context": {
    "related_systems": [
      "User management API (existing)",
      "Authorization service (existing)",
      "API gateway (Kong)"
    ],
    "existing_architecture": "Microservices with REST APIs",
    "known_issues": "Current auth system has no rate limiting"
  }
}
```

**Field descriptions:**
- `issue_id`: Parent Linear issue ID (required)
- `project_summary`: High-level goal (required)
- `requirements`: Functional requirements (required, array)
- `constraints`: Technical, timeline, resource, policy limitations (required, object)
- `context`: Related systems and architectural context (optional, object)

## Architect Output Format

Expected return format from Implementation Architect.

```json
{
  "issue_id": "LIN-100",
  "implementation_plan": {
    "approach": "Build authentication microservice using existing patterns",
    "architecture": "REST API with JWT middleware, Redis for rate limiting and sessions",
    "phases": [
      "Phase 1: Core authentication (JWT generation/validation)",
      "Phase 2: Rate limiting and security",
      "Phase 3: Session management and invalidation"
    ]
  },
  "sub_task_breakdown": [
    {
      "task": "Implement JWT middleware",
      "description": "Create middleware for token generation and validation using PyJWT library",
      "dependencies": [],
      "estimated_effort": "2 days",
      "acceptance_criteria": [
        "Generates JWT tokens with user claims",
        "Validates incoming tokens",
        "Returns 401 on invalid/expired tokens",
        "Supports token refresh"
      ],
      "technical_notes": "Use RS256 algorithm, 1h token expiry, 7d refresh expiry"
    },
    {
      "task": "Add rate limiting",
      "description": "Implement rate limiting using Redis and sliding window algorithm",
      "dependencies": ["JWT middleware complete"],
      "estimated_effort": "2 days",
      "acceptance_criteria": [
        "5 attempts per minute per user",
        "100 attempts per minute globally",
        "Returns 429 when limit exceeded",
        "Headers show remaining attempts"
      ],
      "technical_notes": "Use Redis sorted sets for efficient sliding window"
    }
  ],
  "dependencies": [
    {
      "from": "Add rate limiting",
      "to": "Implement JWT middleware",
      "type": "requires",
      "reason": "Rate limiting needs user identity from JWT"
    }
  ],
  "risks": [
    {
      "description": "Token refresh complexity",
      "likelihood": "medium",
      "impact": "high",
      "mitigation": "Use proven refresh token pattern, add comprehensive tests"
    },
    {
      "description": "Redis single point of failure",
      "likelihood": "low",
      "impact": "high",
      "mitigation": "Accept graceful degradation if Redis down (no rate limiting)"
    }
  ],
  "timeline_estimate": "10-12 days for 2 engineers",
  "recommendations": [
    "Add monitoring for failed auth attempts",
    "Consider implementing 2FA in future phase"
  ]
}
```

**Field descriptions:**
- `issue_id`: Parent Linear issue ID (required)
- `implementation_plan`: High-level approach and architecture (required, object)
- `sub_task_breakdown`: Detailed tasks for sub-issues (required, array)
- `dependencies`: Task relationships (required, array)
- `risks`: Identified risks with mitigations (required, array)
- `timeline_estimate`: Rough time estimate (optional)
- `recommendations`: Suggestions for future improvements (optional, array)

**Sub-task requirements:**
Each sub-task must have:
- Clear, single-purpose task name
- Detailed description
- Explicit dependencies (or empty array)
- Testable acceptance criteria
- Technical implementation notes

## Knowledge Synthesizer Input Format

Provide when invoking post-project learning extraction.

```json
{
  "parent_issue_id": "LIN-100",
  "project_summary": "User authentication system with JWT, rate limiting, and session management",
  "completion_status": "delivered",
  "working_state": {
    /* Final working state object with all sub-issues, divergences, etc. */
  },
  "metrics": {
    "sub_issues_total": 12,
    "sub_issues_first_pass": 7,
    "sub_issues_iterations": 5,
    "avg_review_iterations": 1.4,
    "divergences_tracked": 6,
    "blockers_encountered": 2
  },
  "notes": "Project completed on time. Redis connection pooling was recurring theme. Token expiry policy unclear initially."
}
```

**Field descriptions:**
- `parent_issue_id`: Completed parent issue (required)
- `project_summary`: Brief project description (required)
- `completion_status`: "delivered" | "cancelled" | "blocked" (required)
- `working_state`: Complete final state (required)
- `metrics`: Key performance metrics (required)
- `notes`: Notable observations for learning (optional)

## Knowledge Synthesizer Output Format

Expected output after learning extraction (stored to Memory MCP).

```json
{
  "parent_issue_id": "LIN-100",
  "learnings": [
    {
      "learning_id": "learning-auth-001",
      "category": "best-practice",
      "scope": "global",
      "title": "Always include Redis connection pooling for rate limiting",
      "description": "Multiple sub-issues needed Redis connection pooling added after initial implementation to prevent connection exhaustion under load",
      "source_issues": ["LIN-102", "LIN-105"],
      "applies_to": ["rate-limiting", "redis-usage", "load-handling"],
      "confidence": "high",
      "created_at": "2024-01-15"
    },
    {
      "learning_id": "learning-auth-002",
      "category": "process-improvement",
      "scope": "global",
      "title": "Clarify security policies during planning phase",
      "description": "Token expiry policy was unclear, leading to implementation that violated security guidelines and required changes during review",
      "source_issues": ["LIN-101"],
      "applies_to": ["security", "planning"],
      "confidence": "high",
      "created_at": "2024-01-15"
    }
  ],
  "patterns": {
    "divergence_themes": [
      "Scaling concerns (Redis pooling, caching)",
      "Security policy clarifications"
    ],
    "review_feedback_themes": [
      "Security best practices",
      "Test coverage gaps"
    ],
    "success_factors": [
      "Clear acceptance criteria",
      "Comprehensive error handling"
    ]
  },
  "recommendations": [
    "Add security policy review checklist to planning phase",
    "Include scalability testing in acceptance criteria for infrastructure components"
  ]
}
```

## Validation Checklist

Before sending to any agent:
- ✅ Required fields present
- ✅ issue_id valid and exists in Linear
- ✅ acceptance_criteria are testable
- ✅ Context is focused and relevant
- ✅ Total token count <2000

After receiving from any agent:
- ✅ Required fields present
- ✅ Status value is valid
- ✅ Divergences include rationale
- ✅ Artifacts list is complete
- ✅ Output matches expected format

## Error Handling

When agent returns unexpected format:
1. Log the malformed response
2. Request clarification with specific issue
3. Provide format example
4. Track as communication round

When agent status is "blocked" or "needs_clarification":
1. Switch to Recovery Mode
2. Diagnose the blocker
3. Provide additional context or escalate
4. Track resolution for learning

## Communication Efficiency

Target metrics:
- **Context size:** <2000 tokens per handoff
- **Communication rounds:** 1-2 per issue
- **Clarification rate:** <10% of assignments

Red flags:
- >3 communication rounds for single issue
- Agents requesting information already provided
- Frequent format violations
- Context size >2500 tokens
