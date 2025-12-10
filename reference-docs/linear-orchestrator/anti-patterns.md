# Anti-Patterns Guide

Common mistakes in Linear orchestration workflows and how to avoid them.

## Critical Anti-Patterns

These are mistakes that fundamentally break the workflow and must never occur.

### 1. Subagents Writing Directly to Linear

**The mistake:**
Allowing engineers or reviewers to update Linear issues themselves.

**Why it's wrong:**
- Breaks single source of truth (orchestrator doesn't know about changes)
- Creates audit trail gaps
- Enables scope creep
- Loses central coordination
- Makes metrics unreliable

**How to avoid:**
- ✅ Only Linear PM writes to Linear
- ✅ Agents return structured outputs
- ✅ Orchestrator validates then updates
- ✅ Maintain clear responsibility boundary

**Detection:**
- Issue updates appear without orchestrator action
- Working state diverges from Linear
- Unexpected status changes

**Recovery:**
- Review all issue changes
- Sync working state with Linear
- Reinforce protocol with agents
- Document gap for learning

---

### 2. Memory MCP Queries During Execution Mode

**The mistake:**
Querying Memory MCP for learnings during active coordination.

**Why it's wrong:**
- Adds latency to every assignment
- Breaks efficient coordination flow
- Context already loaded in Planning
- Wastes tokens and time
- Degrades throughput

**How to avoid:**
- ✅ Load learnings in Planning Mode once
- ✅ Store in working_state.loaded_learnings
- ✅ Reference loaded learnings during Execution
- ✅ Only query in Recovery Mode for specific patterns

**Detection:**
- Slow assignment turnaround
- Memory MCP calls in working state logs
- Token usage spikes during coordination

**Recovery:**
- Stop querying immediately
- Reference already-loaded learnings
- If truly needed → Switch to Recovery Mode

---

### 3. Assignments Without Acceptance Criteria

**The mistake:**
Assigning work to engineers without clear "done" definition.

**Why it's wrong:**
- Engineer doesn't know when task is complete
- Leads to scope creep or incomplete work
- Review has no objective standard
- Iteration cycles increase
- Learning is lost (can't assess against criteria)

**How to avoid:**
- ✅ Every sub-issue has acceptance criteria
- ✅ Criteria are testable and specific
- ✅ Include in every engineer assignment
- ✅ Validate during Planning Mode

**Detection:**
- Multiple clarification rounds
- Review iterations >2
- Engineers asking "is this enough?"
- Scope ambiguity

**Recovery:**
- Define acceptance criteria immediately
- Communicate clearly to engineer
- Update Linear sub-issue
- Document for pattern recognition

---

### 4. Engineers Reading Unrelated Issues

**The mistake:**
Allowing engineers access to issues beyond their assigned task.

**Why it's wrong:**
- Context pollution
- Distracts from focused work
- Can lead to unauthorized scope expansion
- Makes context overhead metrics meaningless
- Creates coordination confusion

**How to avoid:**
- ✅ Provide single issue ID per assignment
- ✅ Engineers use get_issue for their task only
- ✅ Include all needed context in assignment
- ✅ Dependencies referenced by ID only

**Detection:**
- Engineers mention information not in assignment
- Work includes features from other issues
- Questions about unrelated tasks

**Recovery:**
- Refocus engineer on assigned issue
- Provide missing context if legitimate
- Reinforce single-task focus
- Review context scoping

---

### 5. Scope Expansion Without Architecture Review

**The mistake:**
Allowing work scope to expand beyond planned sub-issues without architect consultation.

**Why it's wrong:**
- Breaks planned architecture
- Introduces unreviewed dependencies
- Timeline estimates become meaningless
- May violate constraints
- Creates technical debt

**How to avoid:**
- ✅ Reviewers only assess stated criteria
- ✅ Scope changes require Recovery Mode
- ✅ Architect evaluates significant divergences
- ✅ New features = new sub-issues

**Detection:**
- Features not in acceptance criteria
- "While I was at it..." in engineer notes
- Reviewer suggests additions
- Timeline slippage

**Recovery:**
- Assess divergence significance
- If minor → Document and proceed
- If major → Invoke architect for review
- Create new sub-issues for additions

---

### 6. Losing Coordination State

**The mistake:**
Not maintaining working state or letting it diverge from reality.

**Why it's wrong:**
- Lose track of assignments
- Blockers go unnoticed
- Next actions unclear
- Metrics become unreliable
- Cannot recover from interruptions

**How to avoid:**
- ✅ Update working state after every action
- ✅ Track all assignments and statuses
- ✅ Monitor blockers continuously
- ✅ Maintain next_actions queue

**Detection:**
- Uncertainty about current assignments
- Duplicate work
- Forgotten blockers
- State doesn't match Linear

**Recovery:**
- Rebuild state from Linear issues
- Verify all current assignments
- Check for missed blockers
- Resume coordination

---

### 7. Missing Divergence Documentation

**The mistake:**
Allowing plan changes without documenting rationale.

**Why it's wrong:**
- Learning opportunity lost
- Future projects repeat same issues
- Stakeholders unaware of changes
- Audit trail incomplete
- Pattern recognition impossible

**How to avoid:**
- ✅ Document ALL plan changes, even minor
- ✅ Require rationale for every divergence
- ✅ Include impact assessment
- ✅ Validate divergence documentation before approval

**Detection:**
- Changes appear without explanation
- Engineer notes lack rationale
- Reviewer approves without divergence check
- Linear comments missing divergence info

**Recovery:**
- Request rationale from engineer
- Document retroactively
- Update Linear immediately
- Flag pattern for learning

---

### 8. Manual Learning Extraction

**The mistake:**
Orchestrator trying to extract and store learnings instead of delegating to Knowledge Synthesizer.

**Why it's wrong:**
- Distracts from coordination
- Lower quality pattern extraction
- Inconsistent categorization
- Adds cognitive load
- Slows completion

**How to avoid:**
- ✅ Only Knowledge Synthesizer writes learnings
- ✅ Orchestrator focuses on coordination
- ✅ Hand off complete project state
- ✅ Trust specialized agent

**Detection:**
- Orchestrator writing to Memory MCP
- Completion Mode taking excessive time
- Inconsistent learning formats
- Missing pattern synthesis

**Recovery:**
- Stop manual extraction immediately
- Invoke Knowledge Synthesizer properly
- Provide complete project context
- Let specialist do its job

---

## Common Anti-Patterns

These are mistakes that degrade quality but don't break the workflow.

### 9. Context Overload

**The mistake:**
Providing too much information in agent assignments.

**Why it's problematic:**
- Reduces focus on actual task
- Wastes token budget
- Increases cognitive load
- Slows comprehension
- Lower throughput

**How to avoid:**
- ✅ Target <2000 tokens per assignment
- ✅ Include only task-relevant information
- ✅ Reference dependencies by ID
- ✅ Limit learnings to 2-3 most applicable

**Signs:**
- Assignment context >2500 tokens
- Engineers ignore most of context
- Lots of boilerplate in assignments
- Slow assignment processing

**Improvement:**
- Trim to essentials only
- Use issue IDs for references
- Be selective with learnings
- Measure context overhead

---

### 10. Reviewers Expanding Scope

**The mistake:**
Code reviewers suggesting features or improvements beyond acceptance criteria.

**Why it's problematic:**
- Scope creep
- Extends iteration cycles
- Confuses "done" definition
- Defers completion unnecessarily
- Misaligns with plan

**How to avoid:**
- ✅ Reviewers assess only stated criteria
- ✅ Suggestions flagged as "future improvement"
- ✅ New features require new issues
- ✅ Specify review scope clearly

**Signs:**
- Review feedback includes "would be nice to add..."
- Suggestions unrelated to acceptance criteria
- Iteration cycles for feature additions
- Engineers confused about requirements

**Correction:**
- Clarify review scope with reviewer
- Separate "must fix" from "nice to have"
- Create new issues for legitimate additions
- Stay focused on original criteria

---

### 11. Architect Making Implementation Decisions

**The mistake:**
Architect specifying implementation details beyond structural design.

**Why it's problematic:**
- Removes engineer autonomy
- May not be optimal for context
- Slows down implementation
- Reduces learning opportunities
- Can miss better approaches

**How to avoid:**
- ✅ Architect defines structure and interfaces
- ✅ Engineers choose implementation details
- ✅ Trust technical judgment
- ✅ Divergences document better approaches

**Signs:**
- Plan specifies exact libraries/functions
- No room for engineer decision-making
- Frequent conflicts with implementation reality
- Engineers ask permission for obvious choices

**Adjustment:**
- Architect focuses on "what" and "why"
- Engineers decide "how"
- Divergences capture improvements
- Trust and document

---

### 12. Skipping Checkpoints

**The mistake:**
Not performing sanity checks at major milestones.

**Why it's problematic:**
- Issues compound unnoticed
- Late discovery of drift
- Harder to correct course
- Metrics miss patterns
- Quality erosion

**How to avoid:**
- ✅ Checkpoint after Planning
- ✅ Mid-project checkpoint (50%)
- ✅ Pre-completion checkpoint
- ✅ Use standard checklist

**Signs:**
- Surprise issues at completion
- Systematic problems discovered late
- Unclear progress status
- Stakeholder misalignment

**Implementation:**
- Schedule checkpoints explicitly
- Use checklist consistently
- Document findings
- Adjust course as needed

---

### 13. Forgetting GitHub Integration

**The mistake:**
Not linking code artifacts to Linear issues via GitHub.

**Why it's problematic:**
- Artifacts hard to find
- Code review harder
- Audit trail incomplete
- Learning synthesis limited
- Future reference difficult

**How to avoid:**
- ✅ Link PRs to sub-issues
- ✅ Reference commits in updates
- ✅ Store artifact paths in state
- ✅ Validate links at completion

**Signs:**
- "Where's the code for this issue?"
- Reviewers can't find artifacts
- Broken links in Linear
- Missing in completion summary

**Fix:**
- Link artifacts retroactively
- Update Linear with links
- Include in working state
- Verify at checkpoints

---

### 14. Excessive Review Iterations

**The mistake:**
Allowing issues to cycle through review >2 times without intervention.

**Why it's problematic:**
- Indicates unclear criteria
- Wastes time and resources
- Demoralizes engineers
- Suggests systematic issue
- Blocks other work

**How to avoid:**
- ✅ Switch to Recovery Mode after 2 iterations
- ✅ Diagnose root cause
- ✅ Clarify criteria or escalate
- ✅ May indicate need for architect

**Signs:**
- Same issue reviewed 3+ times
- Similar feedback repeated
- Engineer frustration
- Timeline slippage

**Intervention:**
- Stop iteration cycle
- Diagnose: Criteria? Quality? Communication?
- Address root cause
- May need architect consultation
- Resume with clarity

---

### 15. Ignoring Blocker Patterns

**The mistake:**
Treating each blocker as isolated incident without pattern recognition.

**Why it's problematic:**
- Miss systematic issues
- Repeated failures
- No process improvement
- Learning opportunity lost
- Inefficient resolutions

**How to avoid:**
- ✅ Track blocker types
- ✅ Recognize recurring themes
- ✅ Query Memory MCP for patterns
- ✅ Adjust process for common issues

**Signs:**
- Same type of blocker repeatedly
- "We've seen this before"
- Inefficient resolutions
- No improvement over time

**Improvement:**
- Document blocker patterns
- Query for similar cases
- Adjust planning to prevent
- Capture in learnings

---

## Detection and Prevention

### Early Warning Signs

Watch for these indicators of anti-patterns:

**Communication breakdown:**
- Multiple clarification rounds
- Misunderstandings
- Format violations
- Slow responses

**Quality issues:**
- High review iteration rates
- Acceptance criteria disputes
- Scope ambiguity
- Missing divergence docs

**Coordination problems:**
- Unclear assignments
- Duplicate work
- Lost blockers
- State divergence

**Efficiency degradation:**
- Slow turnaround
- Excessive context
- Unnecessary queries
- Process overhead

### Prevention Strategies

**1. Protocol Discipline**
- Follow communication formats strictly
- Validate inputs and outputs
- Use checklists
- Maintain standards

**2. Regular Checkpoints**
- Scheduled sanity checks
- Pattern recognition
- Course correction
- Quality validation

**3. Clear Boundaries**
- Explicit tool access rules
- Single responsibility per agent
- Defined escalation paths
- Scope control

**4. Metric Tracking**
- Monitor key indicators
- Trend analysis
- Early intervention
- Continuous improvement

**5. Learning Application**
- Load relevant patterns
- Reference during work
- Document resolutions
- Enable improvement

---

## Recovery Procedures

When anti-pattern detected:

**1. Immediate Actions**
- Stop the problematic behavior
- Assess impact and extent
- Document the occurrence
- Determine root cause

**2. Correction**
- Apply appropriate fix
- Update affected artifacts
- Sync state if needed
- Communicate changes

**3. Prevention**
- Identify why it occurred
- Adjust process if needed
- Update protocols
- Document learning

**4. Monitoring**
- Watch for recurrence
- Track effectiveness of fix
- Adjust if needed
- Share learning

---

## Anti-Pattern Checklist

Use this checklist to audit your workflow:

**State Management:**
- [ ] Only orchestrator writes to Linear
- [ ] Working state synchronized
- [ ] Blockers tracked
- [ ] Next actions clear

**Memory Usage:**
- [ ] Load once in Planning
- [ ] Reference in Execution
- [ ] Query only in Recovery
- [ ] Delegate to Synthesizer

**Communication:**
- [ ] Structured formats used
- [ ] Acceptance criteria present
- [ ] Context <2000 tokens
- [ ] Divergences documented

**Agent Boundaries:**
- [ ] Single issue per assignment
- [ ] Reviewers stay in scope
- [ ] Architect plans, engineers implement
- [ ] Clear responsibilities

**Quality Control:**
- [ ] Criteria validated
- [ ] Artifacts linked
- [ ] Checkpoints performed
- [ ] Iterations tracked

**Learning:**
- [ ] Patterns recognized
- [ ] Resolutions documented
- [ ] Synthesizer invoked
- [ ] Improvements captured

Regular use of this checklist helps maintain workflow health and catch anti-patterns early.
