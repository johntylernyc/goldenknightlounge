---
description: Review GitHub issue and implement solution with full PR workflow
argument-hint: "issue-number (e.g., 1 or #1)"
allowed-tools: Task, Bash, Read, Edit, MultiEdit, Write, Grep, Glob, LS, TodoWrite, WebFetch
---

Review and implement GitHub issue $ARGUMENTS following the complete development workflow:

## Step 1: Fetch and Analyze Issue
Use `gh issue view $ARGUMENTS --json number,title,body,state,labels,assignees,createdAt,updatedAt` to retrieve issue details.

## Step 2: Review Relevant Documentation
Based on the issue content, review applicable documentation:
1. **Project documentation**:
   - Check CLAUDE.md for development guidelines and conventions
   - Review README.md for project overview
2. **Technical documentation** in `/docs`:
   - `architecture.md` - If issue involves system design changes
   - `database-design.md` - For database-related features
   - `infrastructure.md` - For deployment or environment changes
   - `data-pipelines.md` - For ETL or data processing features
   - `deployment.md` - For deployment-related issues
3. **Feature documentation**:
   - Check `/[feature-name]/README.md` for existing feature docs
   - Review related code comments and docstrings
4. **External documentation**:
   - Yahoo Fantasy API docs if working with fantasy data
   - Framework/library documentation as needed

## Step 3: Plan Implementation
1. Create a todo list to track all implementation steps
2. Analyze the acceptance criteria
3. Identify files that need to be modified based on documentation review
4. Plan the technical approach aligned with existing architecture

## Step 4: Create Feature Branch
Create branch with pattern: `feature/$ARGUMENTS-[brief-description]`

## Step 5: Implement Solution
1. Follow Test-Driven Development (TDD) principles when applicable
2. Write clean, maintainable code following project conventions
3. Update relevant documentation if needed
4. Follow patterns established in existing codebase

## Step 6: Verify Implementation
1. Run lint and typecheck commands if available
2. Ensure all acceptance criteria are met
3. Test the implementation thoroughly
4. Verify changes align with documented architecture

## Step 7: Create Pull Request
1. Commit changes with descriptive message
2. Push branch to remote
3. Create PR using `gh pr create` with:
   - Clear title and description
   - Link to closes issue
   - Test plan
   - Summary of changes

Follow all guidelines in CLAUDE.md for the development workflow.