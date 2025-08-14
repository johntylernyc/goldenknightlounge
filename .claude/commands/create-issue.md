---
description: Create a GitHub issue draft from requirements
argument-hint: "description of the feature or bug"
---

Based on the following requirements: $ARGUMENTS

Create a GitHub issue draft following the project's issue template format. The draft should be saved as a temporary markdown file (GITHUB_ISSUE_DRAFT.md) that can be easily copied to GitHub.

The issue should include:
1. **Feature/Bug Description**: Clear, concise description of what needs to be done
2. **User Story**: As a [type of user], I want [goal] so that [benefit]
3. **Acceptance Criteria**: Specific, testable requirements (as checkboxes)
4. **Dependencies**: Any issues that must be completed first
5. **Priority**: High/Medium/Low
6. **Labels**: Appropriate labels (feature, bug, enhancement, etc.)

Technical requirements will be determined during the review phase.

Generate a filename based on the issue type and a brief kebab-case description (e.g., `feature_yahoo-oauth.md` or `bug_data-pipeline-error.md`). Save the draft to this dynamically named file in ..\.github\issues.