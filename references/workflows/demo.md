# Approved media only

Route only with actual media or an approved recording scenario. Record its source, consent/scope, allowed commands and sanitized environment. Absent media means skip.

For simple approved-footage transcoding, use project-local ffmpeg and ffprobe, inspect results and link the final asset. A full recording/editing request may resolve the pinned external extension in `references/extensions.json`, then execute its complete original workflow. Recording, editing and renderer failure are different responsibilities.
