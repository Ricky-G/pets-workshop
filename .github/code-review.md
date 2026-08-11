# Code Review Guidelines

Focus reviews on changes that could affect users, data, security, or
maintainability. Report only actionable findings, ordered by severity.

## Review checklist

- Verify the change solves the stated requirement without unrelated scope.
- Check correctness, including error paths, empty data, invalid input, and
  boundary cases.
- Identify security concerns such as missing authorization, exposed secrets,
  unsafe input handling, and insecure dependencies.
- Confirm API changes preserve documented response shapes and status codes.
- Ensure database changes preserve model relationships and data integrity.
- Check frontend changes handle loading and failure states and remain
  accessible.
- Verify relevant tests cover changed behavior and that the appropriate test
  commands pass.
- Flag missing documentation only when the change affects user-facing behavior,
  APIs, configuration, or operational procedures.

## Findings

For each finding, include:

1. A severity: `critical`, `high`, `medium`, or `low`.
2. The affected file and line or a precise code location.
3. A concise explanation of the impact and the condition that triggers it.
4. A specific recommendation for resolving it.

Do not report style preferences, formatting, or speculative issues. If there
are no actionable findings, state that explicitly and summarize any remaining
test or review limitations.