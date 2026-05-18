# Video Production Checklist

Use this checklist before recording, editing, narrating, and exporting public
walkthrough videos.

## Pre-Recording Checklist

- Confirm the repository is on the intended branch.
- Run the validation and redaction scripts before recording.
- Open only the windows needed for the walkthrough.
- Use sanitized terminal prompts, paths, inventory values, and browser tabs.
- Confirm OBS is recording the expected window or display.
- Record a short test clip and review text readability.

## Sanitization Checks

- No real secrets, tokens, private keys, PSKs, or account data are visible.
- No public IP addresses or private environment details are visible.
- No private hostnames, real usernames, cloud accounts, or browser profiles are
  visible.
- All examples use placeholder lab names and private documentation ranges.
- Screenshots and thumbnails are reviewed separately from video exports.

## Terminal Cleanup

- Clear scrollback before each recorded command sequence.
- Use a clean shell prompt with no private path details.
- Avoid showing command history.
- Keep unrelated panes, tmux sessions, and editor buffers closed.
- Pre-stage commands in a sanitized note if needed, but do not show private
  notes on screen.

## Browser Cleanup

- Use a clean browser profile for recording.
- Hide bookmarks, extensions, synced profile names, and personal shortcuts.
- Close unrelated tabs.
- Use local files or public repository pages only.
- Confirm autocomplete and address-bar suggestions do not expose private data.

## GitHub README Validation

- Open the README at a readable zoom level.
- Confirm hero visuals, diagram links, docs links, and script names render
  correctly.
- Validate that the README still explains what the project is and what it is
  not.
- Check that public screenshots or previews do not contain private data.

## Audio Generation Checklist

- Use the latest reviewed voiceover script.
- Keep the narration educational and specific.
- Avoid sales language, exaggerated claims, and urgency.
- Listen for incorrect pronunciations of GNS3, Ansible, UFW, SSH, and Mermaid.
- Keep generated audio files in `media/audio/`.

## Export Checklist

- Export video drafts to `media/edited/`.
- Export thumbnails or social previews to `media/thumbnails/`.
- Store selected still frames in `media/screenshots/`.
- Review the final export full-screen before publishing.
- Run `./scripts/validate.sh`, `./scripts/redaction-check.sh`,
  `bash -n scripts/*.sh`, and `git diff --check` before committing.
