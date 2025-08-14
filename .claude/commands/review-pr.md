---
description: Review pull request for completeness and quality
argument-hint: "pr-number (e.g., 2 or #2)"
---

Review pull request $ARGUMENTS for quality and completeness:

## Step 1: Fetch PR Details
Use `gh pr view $ARGUMENTS --json number,title,body,state,files,additions,deletions,commits,reviews,checks` to get comprehensive PR information.

## Step 2: Review Related Documentation
Based on the PR changes, review relevant documentation to ensure alignment:
1. **Verify against project guidelines**:
   - CLAUDE.md for development standards and workflows
   - Check if PR follows the defined branch strategy and commit conventions
2. **Architecture alignment** - Review applicable docs in `/docs`:
   - `architecture.md` - Ensure changes align with system design
   - `database-design.md` - Verify database changes follow schema conventions
   - `infrastructure.md` - Check infrastructure changes are compatible
   - `data-pipelines.md` - Validate ETL modifications maintain data flow
3. **Feature documentation**:
   - Check if feature docs in `/[feature-name]/README.md` need updates
   - Verify API documentation is updated if endpoints changed
   - Ensure README is updated for user-facing changes
4. **External compliance**:
   - Verify external API usage follows documented patterns
   - Check security considerations from documentation

## Step 3: Review Code Changes
Examine the diff using `gh pr diff $ARGUMENTS` and evaluate:

### Code Quality
- Follows project coding standards and conventions per CLAUDE.md
- Clean, readable, and maintainable code
- No code smells or anti-patterns
- Proper error handling
- Consistent with existing codebase patterns

### Testing
- Adequate test coverage for new functionality
- Tests are meaningful and cover edge cases
- All tests pass
- Testing approach aligns with project's TDD principles

### Documentation
- Code is self-documenting with clear naming
- Complex logic has appropriate comments
- Project documentation updated if needed
- Feature documentation created/updated in `/[feature-name]/README.md` if applicable
- Commit messages follow project conventions

### Functionality
- Meets all acceptance criteria from the linked issue
- No regressions introduced
- Performance considerations addressed
- Changes align with documented architecture

## Step 4: Check CI/CD Status
Review any automated checks, tests, or linting results.

## Step 5: Cross-Reference with Project Standards
Verify the PR adheres to:
- Development workflow from CLAUDE.md
- Database design principles if DB changes included
- API design principles for endpoint changes
- Security considerations documented in the project

## Step 6: Provide Feedback
Summarize findings:
- ✅ What looks good
- ⚠️ Suggestions for improvement
- ❌ Required changes before merge
- Overall recommendation (approve/request changes)

Note any security concerns, potential bugs, or architectural issues.