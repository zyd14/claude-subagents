# Workflow Details

Comprehensive guidance for each operating mode in the Linear orchestration workflow.

## Overview

The Linear PM orchestrator operates in four modes:
1. **Planning Mode:** Project initialization and architecture
2. **Execution Mode:** Active implementation coordination
3. **Recovery Mode:** Exception and blocker handling
4. **Completion Mode:** Project finalization and learning handoff

Each mode has specific entry/exit criteria, responsibilities, and workflows.

---

## Planning Mode

**Entry criteria:**
- New parent issue received or created
- Project requires decomposition into sub-tasks
- Ready to begin implementation planning

**Exit criteria:**
- All sub-issues created in Linear
- Acceptance criteria defined for each
- Dependencies mapped and documented
- Relevant learnings loaded into working state
- Ready to assign first sub-issue

### Workflow Steps

**1. Issue Intake**
- Receive or create parent Linear issue
- Validate requirements are clear
- Identify any immediate constraints
- Assess project scope and complexity

**2. Learning Retrieval**
```
Query Memory MCP for:
- Similar project types ("authentication", "API development")
- Relevant technology stack ("Python", "Redis", "JWT")
- Architectural patterns ("microservices", "REST API")
- Recent learnings (last 6 months prioritized)

Limit to top 10-15 most relevant learnings
Store in working_state.loaded_learnings
```

**3. Architect Invocation**
- Prepare architect input using communication protocol
- Include parent issue ID, requirements, constraints
- Provide context about related systems
- Set clear expectations for output format

**4. Plan Review and Validation**
Check architect output for:
- ✅ All requirements addressed
- ✅ Sub-tasks are atomic and testable
- ✅ Dependencies clearly identified
- ✅ Risks have mitigation strategies
- ✅ Acceptance criteria defined per task
- ✅ Timeline estimate reasonable

If inadequate, provide specific feedback and re-invoke.

**5. Sub-Issue Creation**
For each sub-task from architect plan:
```
Create Linear sub-issue with:
- Title: Clear, action-oriented (e.g., "Implement JWT middleware")
- Description: Detailed task description from plan
- Acceptance Criteria: Copy from plan, ensure testable
- Parent Link: Link to parent issue
- Dependencies: Reference other sub-issue IDs
- Labels: Technology tags, phase tags
- Priority: Based on dependency order
```

**6. Working State Initialization**
```json
{
  "parent_issue": "LIN-100",
  "project_name": "User Authentication System",
  "status": "planning",
  "current_mode": "planning",
  "sub_issues": [
    /* Array of sub-issue objects */
  ],
  "blockers": [],
  "next_actions": ["Assign LIN-101 (no dependencies)"],
  "loaded_learnings": [
    /* Learnings from Memory MCP query */
  ]
}
```

**7. Dependency Graph Validation**
- Verify no circular dependencies
- Identify independent tasks (can start immediately)
- Order tasks by dependency chain
- Plan parallel work where possible

**8. Mode Transition**
- Update working_state.current_mode = "execution"
- Identify first sub-issue(s) to assign
- Prepare for high-throughput coordination

### Key Practices

**Learning Selection:**
- Prioritize recent learnings (recency bias for technology)
- Include 1-2 global best practices
- Focus on applicable architectural patterns
- Avoid overloading (max 10-15 learnings)

**Sub-Issue Quality:**
- Single responsibility per issue
- Testable acceptance criteria
- Clear definition of "done"
- Appropriate scope (2-5 days work)

**Architect Collaboration:**
- Provide comprehensive context upfront
- Request structured output
- Validate completeness before proceeding
- Don't micromanage implementation details

---

## Execution Mode

**Entry criteria:**
- Sub-issues created and ready
- Learnings loaded in working state
- At least one sub-issue has no blocking dependencies

**Exit criteria:**
- All sub-issues complete and reviewed
- No active assignments
- Ready for project completion

**Critical constraint:** NO Memory MCP queries during this mode (use loaded learnings only)

### Workflow Steps

**1. Work Assignment**
Select next sub-issue:
```
Criteria for assignment:
- Status = "pending" (not assigned)
- All dependencies complete
- No current blockers
- Highest priority in dependency chain
```

Prepare engineer input:
```json
{
  "issue_id": "LIN-101",
  "context_summary": "Brief task description",
  "acceptance_criteria": [/* From Linear issue */],
  "dependencies": [/* Completed issues this depends on */],
  "constraints": [/* Technical limitations */],
  "relevant_learnings": [/* 2-3 from loaded_learnings */]
}
```

Invoke Data Infrastructure Engineer.

**2. Progress Tracking**
Update working state:
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "status": "in_progress",
      "assigned_to": "data-infra-engineer",
      "assigned_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

**3. Output Validation**
When engineer returns output:

Validate completeness:
- ✅ Required fields present
- ✅ Status is valid value
- ✅ Artifacts list provided
- ✅ Divergences documented with rationale

Validate quality:
- ✅ Acceptance criteria addressed
- ✅ Summary is clear and accurate
- ✅ Divergences have rationale
- ✅ No blockers or blockers are actionable

If validation fails → Request clarification or reassign

**4. Linear Update**
Update sub-issue in Linear:
```
Status: "in_review"
Comment: 
  Engineer summary
  Artifacts: [list]
  Divergences: [if any, with rationale]
  
Link GitHub artifacts if available
```

Update working state:
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "status": "in_review",
      "assigned_to": "data-infra-engineer",
      "artifacts": ["src/auth/jwt.py", "tests/test_jwt.py"],
      "divergences": [/* If any */]
    }
  ]
}
```

**5. Review Assignment**
Prepare reviewer input:
```json
{
  "issue_id": "LIN-101",
  "context_summary": "Review JWT middleware implementation",
  "acceptance_criteria": [/* Same as engineer received */],
  "artifacts": [/* From engineer output */],
  "review_scope": "Code quality, security, criteria match, test coverage",
  "engineer_notes": [/* Notable divergences or concerns */]
}
```

Invoke Code Reviewer.

Update working state:
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "status": "in_review",
      "reviewer": "code-reviewer",
      "review_started_at": "2024-01-15T14:00:00Z"
    }
  ]
}
```

**6. Review Processing**
When reviewer returns output:

**If approved:**
- Update Linear issue status to "complete"
- Add reviewer feedback as comment
- Link to working state
- Mark sub-issue complete in working state
- Identify next sub-issues now unblocked

**If changes required:**
- Determine if minor (same engineer) or major (reassign)
- Prepare engineer input with review feedback
- Increment iteration count
- If >2 iterations → Consider Recovery Mode

**If rejected:**
- Switch to Recovery Mode
- Escalate to architect if architectural issue
- Reassess acceptance criteria
- May need to revise plan

**7. Iteration Management**
Track review cycles per issue:
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "review_iterations": 2,
      "review_feedback_summary": "Security concerns addressed, minor style updates"
    }
  ]
}
```

If issue requires >2 iterations:
- Flag as pattern for learning
- Consider if acceptance criteria were unclear
- May indicate need for architect consultation

**8. Continuous Assignment**
After each completion:
- Check for newly unblocked sub-issues
- Assign next task if engineer available
- Update next_actions in working state
- Maintain assignment queue

**9. Checkpoint Execution**
Mid-project checkpoint (50% complete):
- Verify progress on track
- Check for systematic issues
- Identify any emerging patterns
- Validate quality standards maintained
- Assess if Recovery Mode needed

### Key Practices

**Context Management:**
- Keep assignment context <2000 tokens
- Include only task-relevant learnings (2-3 max)
- Reference dependencies by ID, not full context
- Focus engineer on single issue

**Validation Rigor:**
- Always validate before updating Linear
- Check divergences have rationale
- Ensure artifacts are linked
- Verify acceptance criteria addressed

**Throughput Optimization:**
- Minimize time between completion and next assignment
- Batch Linear updates where possible
- Avoid unnecessary queries or tool calls
- Stay focused on coordination

**Quality Gates:**
- No sub-issue marked complete without review
- All divergences documented before moving on
- Track iteration counts for learning
- Maintain audit trail in Linear

---

## Recovery Mode

**Entry criteria:**
- Blocker encountered during execution
- Multiple sub-issues failing review
- Significant divergence from plan
- New requirements emerge
- >2 review iterations on single issue

**Exit criteria:**
- Blocker resolved or escalated
- Plan adjusted if needed
- Ready to return to Execution Mode
- Resolution documented for learning

### Workflow Steps

**1. Blocker Diagnosis**
Categorize the issue:
- **Technical blocker:** Missing dependency, API limitation, performance issue
- **Architectural issue:** Plan doesn't account for requirement, design flaw
- **Process issue:** Unclear acceptance criteria, communication breakdown
- **External blocker:** Dependency on another team, policy decision needed
- **Resource constraint:** Timeline, skill, or capacity limitation

**2. Pattern Recognition**
Query Memory MCP for relevant patterns:
```
Query for:
- Similar blockers ("Redis connection issues", "JWT validation")
- Error resolution patterns
- Past escalation outcomes
- Known workarounds

Use specific, focused queries
Limit to top 5 most relevant learnings
```

**3. Resolution Strategy**

**For technical blockers:**
- Provide additional context to engineer
- Reference relevant learnings from query
- May need to adjust acceptance criteria
- Document workaround if applicable

**For architectural issues:**
- Invoke Implementation Architect with:
  - Original plan
  - Blocker description
  - Failed attempts
  - Current state
- Request revised plan or approach
- May need to create new sub-issues

**For process issues:**
- Clarify acceptance criteria
- Adjust communication format
- Provide additional examples
- May indicate need for protocol update

**For external blockers:**
- Document dependency clearly
- Update Linear with blocker status
- Set reminder to check status
- Plan work around blocker if possible

**4. Plan Adjustment**
If plan needs modification:
- Create new sub-issues if needed
- Update dependencies in Linear
- Revise timeline estimate
- Update parent issue with changes
- Document rationale in Linear

**5. Working State Update**
```json
{
  "blockers": [
    {
      "issue_id": "LIN-105",
      "type": "technical",
      "description": "Redis connection pooling required",
      "resolution": "Added connection pooling, updated all Redis usage",
      "resolved_at": "2024-01-15T16:00:00Z"
    }
  ]
}
```

**6. Learning Capture**
Note resolution for Knowledge Synthesizer:
- What was the blocker?
- How was it resolved?
- Is this a pattern?
- Should acceptance criteria be adjusted?
- Applicable to future projects?

**7. Mode Transition**
Once resolved:
- Update working_state.current_mode = "execution"
- Reassign work with updated context
- Resume normal coordination

### Key Practices

**Escalation Timing:**
- Don't spend >2 hours diagnosing alone
- Architect should be invoked for architectural issues
- Memory MCP queries should be specific and targeted

**Documentation:**
- Always document blocker and resolution
- Include resolution time for metric tracking
- Capture pattern for learning
- Update Linear with clear status

**Communication:**
- Be explicit about what changed and why
- Provide adjusted context to engineers
- Don't hide blockers from stakeholders

---

## Completion Mode

**Entry criteria:**
- All sub-issues complete
- All reviews approved
- Parent issue acceptance criteria met
- Ready to finalize project

**Exit criteria:**
- Parent issue updated with summary
- All artifacts linked via GitHub
- Knowledge Synthesizer invoked
- Parent issue closed
- Working state archived

### Workflow Steps

**1. Completeness Verification**
Final checkpoint:
- ✅ All sub-issues status = "complete"
- ✅ All reviews approved
- ✅ All divergences documented
- ✅ All artifacts linked
- ✅ Parent acceptance criteria met
- ✅ No outstanding blockers

If any item fails → Return to Execution/Recovery Mode

**2. Summary Generation**
Create project summary:
```
High-level overview:
- What was delivered
- Key features/capabilities
- Timeline (planned vs actual)

Implementation notes:
- Significant divergences from plan
- Rationale for changes
- Lessons learned

Statistics:
- Total sub-issues: X
- First-pass completions: Y
- Review iterations average: Z
- Divergences tracked: N
- Blockers resolved: M
```

**3. Linear Parent Issue Update**
Update parent issue:
```
Status: "complete"
Comment: [Project summary]

Linked sub-issues: [All sub-issue IDs]
Artifacts: [Key deliverables]
GitHub: [Main PR if applicable]

Metrics:
- Completion rate: X%
- Avg review iterations: Y
- Timeline: Z days
```

**4. Knowledge Synthesizer Invocation**
Prepare handoff:
```json
{
  "parent_issue_id": "LIN-100",
  "project_summary": "Brief description",
  "completion_status": "delivered",
  "working_state": {/* Complete final state */},
  "metrics": {
    "sub_issues_total": 12,
    "sub_issues_first_pass": 7,
    "sub_issues_iterations": 5,
    "avg_review_iterations": 1.4,
    "divergences_tracked": 6,
    "blockers_encountered": 2
  },
  "notes": "Notable observations for learning extraction"
}
```

Invoke Knowledge Synthesizer agent.

**5. GitHub Integration**
- Ensure all PRs linked to sub-issues
- Main project PR linked to parent issue
- Artifact paths documented
- Code accessible for future reference

**6. Issue Closure**
Close parent issue in Linear:
- Status: "complete"
- Resolution: "delivered" or "cancelled"
- Final comment with summary
- All links verified

**7. Working State Archive**
```json
{
  "parent_issue": "LIN-100",
  "status": "complete",
  "current_mode": "completion",
  "completion_date": "2024-01-20",
  "final_metrics": {/* All tracked metrics */},
  "archived": true
}
```

**8. Cleanup**
- Clear working state for next project
- Reset current_mode
- Loaded learnings discarded (new project will reload)

### Key Practices

**Thoroughness:**
- Don't rush completion verification
- Validate every acceptance criterion
- Check all artifacts accessible
- Ensure nothing missing

**Learning Handoff:**
- Provide complete context to synthesizer
- Include all divergence records
- Share blocker resolutions
- Note communication issues

**Documentation Quality:**
- Summary should be readable by non-technical stakeholders
- Divergences explained with rationale
- Metrics provide real insight
- Artifacts are discoverable

---

## Mode Transition Guidelines

### Planning → Execution
Trigger: All sub-issues created, learnings loaded
Actions:
- Identify first assignable sub-issues
- Prepare engineer assignments
- Update mode in working state

### Execution → Recovery
Triggers:
- Engineer reports significant blocker
- Multiple issues failing review
- Divergence requires architect input
- >2 review iterations on one issue

Actions:
- Document current state
- Categorize the issue
- Determine resolution approach
- Update mode in working state

### Recovery → Execution
Trigger: Blocker resolved or plan adjusted
Actions:
- Update working state with resolution
- Prepare adjusted assignments
- Resume coordination
- Update mode in working state

### Execution → Completion
Triggers:
- All sub-issues complete
- All reviews approved
- No blockers

Actions:
- Perform final verification
- Update mode in working state
- Begin completion workflow

### Emergency: Any Mode → Recovery
Triggers:
- Critical blocker discovered
- Project scope change
- Resource constraint
- Stakeholder escalation

Actions:
- Pause current work
- Switch to Recovery Mode immediately
- Assess situation
- Determine resolution path

---

## Best Practices Across All Modes

**Working State Discipline:**
- Update after every significant action
- Keep synchronized with Linear
- Use as coordination memory
- Don't let it get stale

**Communication Consistency:**
- Always use structured formats
- Validate inputs and outputs
- Track communication rounds
- Maintain audit trail

**Context Management:**
- Load once in Planning
- Reference during Execution
- Query specifically in Recovery
- Never during Completion

**Quality Standards:**
- Never compromise on acceptance criteria
- Always document divergences
- Maintain review rigor
- Track for learning

**Efficiency Focus:**
- Minimize unnecessary tool calls
- Batch updates where possible
- Stay in appropriate mode
- Optimize for throughput in Execution

**Learning Orientation:**
- Capture patterns continuously
- Document resolutions
- Note communication issues
- Enable future improvement
