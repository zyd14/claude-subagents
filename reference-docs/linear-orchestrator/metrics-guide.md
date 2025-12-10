# Metrics Guide

Comprehensive guide for tracking and analyzing Linear orchestration metrics.

## Overview

Metrics serve three purposes:
1. **Real-time monitoring:** Detect issues during execution
2. **Project assessment:** Evaluate completion quality
3. **Continuous improvement:** Identify patterns for learning

## Priority Metrics

Track these from day 1 of any project.

---

### 1. Sub-Issue Completion Rate

**Definition:** Percentage of sub-issues that complete on first assignment without requiring significant rework.

**Formula:**
```
Completion Rate = (First-Pass Completions / Total Sub-Issues) × 100
```

**Target:** >95%

**Tracking:**
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "first_pass_complete": true,
      "review_iterations": 1
    },
    {
      "id": "LIN-102",
      "first_pass_complete": false,
      "review_iterations": 3,
      "failure_reason": "Acceptance criteria misunderstood"
    }
  ]
}
```

**Red flags:**
- <85%: Indicates unclear acceptance criteria or poor planning
- <70%: Critical issue with communication or skill match

**What it measures:**
- Quality of acceptance criteria
- Engineer understanding of requirements
- Alignment between plan and implementation
- Effectiveness of loaded learnings

**Improvement actions:**
If low:
- Review acceptance criteria clarity
- Check if engineers have needed context
- Verify loaded learnings are relevant
- Consider more detailed sub-issue descriptions

---

### 2. Review Iteration Count

**Definition:** Average number of review cycles per sub-issue before approval.

**Formula:**
```
Avg Review Iterations = Sum(Review Cycles per Issue) / Total Sub-Issues
```

**Target:** <1.5

**Tracking:**
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "review_iterations": 1,
      "review_cycle_reasons": []
    },
    {
      "id": "LIN-102",
      "review_iterations": 3,
      "review_cycle_reasons": [
        "Security policy violation",
        "Missing error handling",
        "Test coverage gap"
      ]
    }
  ]
}
```

**Red flags:**
- >2.0: Quality issues, unclear criteria, or communication problems
- >3.0 for any single issue: Trigger Recovery Mode

**What it measures:**
- Quality of initial implementation
- Clarity of acceptance criteria
- Effectiveness of review feedback
- Engineer skill alignment

**Improvement actions:**
If high:
- Analyze common review feedback themes
- Improve acceptance criteria specificity
- Load relevant quality learnings
- Consider engineer skill match

---

### 3. Divergence Documentation Rate

**Definition:** Percentage of plan divergences that are documented with rationale.

**Formula:**
```
Documentation Rate = (Documented Divergences / Total Divergences) × 100
```

**Target:** 100%

**Tracking:**
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "divergences": [
        {
          "description": "Added Redis connection pooling",
          "rationale": "Prevent connection exhaustion under load",
          "impact": "Minor performance improvement",
          "documented": true
        }
      ]
    },
    {
      "id": "LIN-102",
      "divergences": [
        {
          "description": "Changed API endpoint path",
          "documented": false
        }
      ]
    }
  ]
}
```

**Red flags:**
- <100%: Learning opportunities being lost
- <90%: Critical gap in audit trail

**What it measures:**
- Discipline in capturing changes
- Quality of engineer outputs
- Effectiveness of validation
- Learning corpus quality

**Improvement actions:**
If low:
- Validate engineer outputs more rigorously
- Request rationale before approval
- Update communication protocol
- Flag pattern for process improvement

---

### 4. Context Overhead

**Definition:** Token count of context provided in agent assignments.

**Targets:**
- Assignment context: <2000 tokens
- Relevance ratio: >80%

**Tracking:**
```json
{
  "assignments": [
    {
      "issue_id": "LIN-101",
      "context_tokens": 1847,
      "relevant_tokens_used": 1612,
      "relevance_ratio": 87.3,
      "overhead_within_target": true
    },
    {
      "issue_id": "LIN-102",
      "context_tokens": 2534,
      "relevant_tokens_used": 1456,
      "relevance_ratio": 57.5,
      "overhead_within_target": false,
      "issues": ["Too many learnings included", "Full dependency context provided"]
    }
  ]
}
```

**Red flags:**
- >2500 tokens: Context bloat
- <60% relevance: Providing too much unrelated info
- Growing over time: Scope creep

**What it measures:**
- Context scoping effectiveness
- Information relevance
- Communication efficiency
- Cognitive load on agents

**Improvement actions:**
If high:
- Trim to essentials only
- Reference dependencies by ID
- Limit learnings to 2-3 max
- Remove boilerplate

---

### 5. Communication Rounds

**Definition:** Number of back-and-forth exchanges per sub-issue assignment.

**Formula:**
```
Communication Rounds = Messages Between Assignment and Completion
```

**Target:** 1-2 rounds (assign → return, possibly one clarification)

**Tracking:**
```json
{
  "sub_issues": [
    {
      "id": "LIN-101",
      "communication_rounds": 2,
      "messages": [
        "Assignment sent",
        "Clarification requested: Which Redis instance?",
        "Clarification provided: Use prod-redis-01",
        "Completion returned"
      ]
    },
    {
      "id": "LIN-102",
      "communication_rounds": 5,
      "issues": ["Multiple clarification loops", "Acceptance criteria unclear"]
    }
  ]
}
```

**Red flags:**
- >3 rounds: Unclear assignments or missing context
- >5 rounds: Critical communication breakdown

**What it measures:**
- Assignment clarity
- Context completeness
- Communication protocol effectiveness
- Understanding between agents

**Improvement actions:**
If high:
- Review what clarifications were needed
- Include that context upfront next time
- Update communication protocol
- Consider checkpoint before assignment

---

## Context Overhead Deep Dive

This metric requires special attention as it directly impacts efficiency.

### Measurement Points

Track at each agent handoff:

**1. Context Size**
```python
def measure_context_size(assignment):
    return len(json.dumps(assignment).encode('utf-8'))
```

**2. Relevant Context Ratio**
After completion, assess which parts of context were actually used:
```python
relevance = (tokens_referenced_in_work / total_tokens_provided) * 100
```

**3. Retrieval Time**
```python
retrieval_start = time.time()
# Fetch learnings, issue data, etc.
retrieval_time_ms = (time.time() - retrieval_start) * 1000
```

**4. Communication Rounds**
Count messages between assignment and completion.

### Target Metrics

**Optimal:**
- Context size: 1200-1800 tokens
- Relevance ratio: 80-95%
- Retrieval time: <300ms
- Communication rounds: 1 (assign → return)

**Acceptable:**
- Context size: 1800-2000 tokens
- Relevance ratio: 70-80%
- Retrieval time: 300-500ms
- Communication rounds: 2 (one clarification)

**Problematic:**
- Context size: >2000 tokens
- Relevance ratio: <70%
- Retrieval time: >500ms
- Communication rounds: >2

### Red Flag Analysis

**Context size growing over time:**
- Indicates: Scope creep or poor scoping
- Action: Review what's being added
- Fix: Return to essentials only

**Low relevance ratio (<60%):**
- Indicates: Providing too much unrelated information
- Action: Analyze what wasn't used
- Fix: Trim to task-relevant only

**High communication rounds (>3):**
- Indicates: Unclear assignments or missing context
- Action: Review clarification requests
- Fix: Include that context upfront

**Retrieval time increasing:**
- Indicates: Inefficient learning queries
- Action: Review query patterns
- Fix: Load once, reference during execution

### Optimization Strategies

**For context size:**
- Reference by ID, not full text
- Limit learnings to 2-3 most applicable
- Summarize dependencies
- Remove boilerplate

**For relevance ratio:**
- Only include what's needed for task
- Ask: "Would engineer be stuck without this?"
- Remove nice-to-know information
- Focus on must-know

**For communication rounds:**
- Include likely questions preemptively
- Clear acceptance criteria
- Explicit constraints
- Complete dependency info

**For retrieval time:**
- Load learnings once in Planning
- Cache issue data
- Batch queries
- Avoid redundant lookups

---

## Project-Level Metrics

Calculate these at project completion.

### Overall Project Health

```json
{
  "project_metrics": {
    "sub_issues_total": 12,
    "sub_issues_complete": 12,
    "sub_issues_first_pass": 8,
    "sub_issues_iterations": 4,
    
    "completion_rate": 66.7,
    "avg_review_iterations": 1.33,
    "divergences_total": 6,
    "divergences_documented": 6,
    "divergence_documentation_rate": 100,
    
    "blockers_encountered": 2,
    "blockers_resolved": 2,
    "avg_blocker_resolution_time_hours": 4.5,
    
    "avg_context_overhead_tokens": 1847,
    "avg_communication_rounds": 1.8,
    
    "timeline_planned_days": 10,
    "timeline_actual_days": 11,
    "timeline_variance_pct": 10
  }
}
```

### Quality Indicators

**High Quality Project:**
- Completion rate >90%
- Avg review iterations <1.3
- Divergence documentation 100%
- Context overhead <1800 tokens
- Communication rounds <2
- Timeline variance <20%

**Acceptable Quality:**
- Completion rate 80-90%
- Avg review iterations 1.3-1.7
- Divergence documentation >95%
- Context overhead 1800-2200 tokens
- Communication rounds 2-2.5
- Timeline variance 20-40%

**Needs Improvement:**
- Completion rate <80%
- Avg review iterations >1.7
- Divergence documentation <95%
- Context overhead >2200 tokens
- Communication rounds >2.5
- Timeline variance >40%

---

## Future Metrics

Add these once system matures and baseline data exists.

### Agent Utilization

**Definition:** Percentage of time agents spend on active work vs waiting.

**Calculation:**
```python
utilization = (active_work_time / total_project_time) * 100
```

**Target:** >70%

**Use case:** Identify bottlenecks in coordination

### Learning Application Rate

**Definition:** Percentage of loaded learnings actually referenced during execution.

**Calculation:**
```python
application_rate = (learnings_referenced / learnings_loaded) * 100
```

**Target:** >60%

**Use case:** Optimize learning selection in Planning Mode

### Blocker Escalation Time

**Definition:** Hours from blocker identification to resolution initiation.

**Target:** <4 hours

**Use case:** Improve Recovery Mode responsiveness

### Stakeholder Satisfaction

**Definition:** Qualitative feedback on delivery.

**Measurement:** Post-project survey

**Use case:** Validate that metrics align with value

---

## Metric Tracking Implementation

### During Execution

Update working state with metrics:

```json
{
  "metrics": {
    "sub_issues_complete": 7,
    "sub_issues_total": 12,
    "completion_rate_current": 85.7,
    "review_iterations_total": 9,
    "avg_review_iterations": 1.29,
    "divergences_tracked": 4,
    "context_overhead_avg": 1823
  }
}
```

### At Completion

Generate final metrics report:

```json
{
  "final_metrics": {
    "completion_rate": 91.7,
    "avg_review_iterations": 1.25,
    "divergence_documentation_rate": 100,
    "avg_context_overhead": 1847,
    "avg_communication_rounds": 1.8,
    "timeline_variance": 10,
    "quality_grade": "high"
  }
}
```

### For Learning

Include metrics in Knowledge Synthesizer input:

```json
{
  "metrics": {
    /* All tracked metrics */
  },
  "metric_insights": {
    "strengths": [
      "Excellent divergence documentation",
      "Low review iteration count"
    ],
    "improvements": [
      "Context overhead could be reduced",
      "Communication rounds higher than target"
    ]
  }
}
```

---

## Metric Analysis

### Trend Analysis

Track metrics across projects:

```python
projects = [
  {"id": "LIN-100", "completion_rate": 91.7, "review_iterations": 1.25},
  {"id": "LIN-200", "completion_rate": 88.3, "review_iterations": 1.42},
  {"id": "LIN-300", "completion_rate": 93.8, "review_iterations": 1.18}
]

# Identify trends
improving = completion_rate_trending_up()
patterns = common_issues_across_projects()
```

### Correlation Analysis

Identify relationships:
- High review iterations ↔ Low completion rate?
- High context overhead ↔ More communication rounds?
- Divergence rate ↔ Planning quality?

### Pattern Recognition

Flag recurring issues:
- Same sub-issue types always iterate?
- Specific engineers struggle with certain tasks?
- Certain learnings never applied?
- Review feedback themes?

---

## Reporting

### Real-Time Dashboard

Show during execution:
- Current completion rate
- Review iterations (running average)
- Context overhead trend
- Communication efficiency

### Project Summary

Include in completion report:
```
Project LIN-100: User Authentication System
Status: Delivered

Quality Metrics:
- Completion Rate: 91.7% (target >95%, near target)
- Avg Review Iterations: 1.25 (target <1.5, excellent)
- Divergence Documentation: 100% (target 100%, perfect)
- Context Overhead: 1847 tokens (target <2000, good)
- Communication Rounds: 1.8 (target 1-2, excellent)

Timeline:
- Planned: 10 days
- Actual: 11 days
- Variance: 10% (acceptable)

Grade: High Quality
```

### Trend Report

Monthly or quarterly:
```
Projects: 5 completed
Avg Completion Rate: 90.2% (trend: improving)
Avg Review Iterations: 1.31 (trend: stable)
Common Issues: Context overhead, clarification loops
Improvements Made: Better learning selection, clearer criteria
```

---

## Using Metrics for Improvement

### When Completion Rate Low

1. Analyze which sub-issues failed
2. Review acceptance criteria clarity
3. Check engineer skill match
4. Verify loaded learnings relevant
5. Adjust Planning Mode process

### When Review Iterations High

1. Identify common review feedback
2. Add to loaded learnings
3. Improve acceptance criteria
4. Consider code quality checklist
5. Update engineer assignments

### When Context Overhead High

1. Audit what's included
2. Identify unused information
3. Trim to essentials
4. Update scoping guidelines
5. Monitor next assignments

### When Communication Rounds High

1. Review clarification requests
2. Identify missing context
3. Include proactively next time
4. Update communication protocol
5. Consider checkpoint before assignment

---

## Metrics Best Practices

**Do:**
- ✅ Track consistently across projects
- ✅ Analyze trends, not just point values
- ✅ Use for learning, not punishment
- ✅ Focus on improvement opportunities
- ✅ Correlate with quality outcomes

**Don't:**
- ❌ Optimize metrics at expense of quality
- ❌ Track more than you can act on
- ❌ Use for engineer evaluation
- ❌ Ignore context when comparing
- ❌ Let tracking slow coordination

**Remember:**
- Metrics inform decisions, don't make them
- Context matters for interpretation
- Trends matter more than single values
- Purpose is continuous improvement
- Quality over metric perfection
