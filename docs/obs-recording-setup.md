# OBS Recording Setup

Use this as the baseline for walkthrough recordings and AI-narrated demos. Keep
all examples sanitized and avoid recording private terminals, browser sessions,
tokens, account pages, public IP addresses, private keys, or real environment
details.

## Recommended OBS Settings

- Recording format: `mkv` during capture, then remux to `mp4` after recording.
- Encoder: hardware encoder if stable on the host, otherwise x264 with a
  conservative CPU preset.
- Rate control: use a quality-focused mode such as CQP or CRF when available.
- Frame rate: 30 FPS for documentation walkthroughs; 60 FPS is usually
  unnecessary for terminal-heavy videos.
- Audio sample rate: 48 kHz.
- Capture source: prefer a specific window or display dedicated to the demo.

## Resolution Guidance

- Record at 1920x1080 when possible.
- Use 1280x720 only for quick internal drafts or low-resource hosts.
- Keep the output canvas and scaled resolution the same unless there is a clear
  reason to downscale.
- Avoid ultra-wide recordings for YouTube walkthroughs because code, diagrams,
  and terminal text become harder to read on small screens.

## Terminal Readability

- Use a large monospace font, typically 16 to 20 pt at 1080p.
- Keep terminal width moderate, around 100 to 120 columns.
- Use a high-contrast theme with a plain background.
- Clear the terminal before recording each command sequence.
- Use sanitized prompts such as `labuser@lab-host:~/practical-home-lab$`.
- Avoid showing shell history, private paths, cloud account names, or local-only
  host details.

## Linux and XFCE Notes

- Disable screen locking and notification popups before recording.
- Use a clean XFCE workspace with only the demo windows open.
- Set panel clocks, tray items, and desktop widgets so they do not expose
  private details.
- Test window capture before recording; if window capture is unreliable, use a
  dedicated display capture with all unrelated windows closed.
- Keep the browser and terminal on predictable workspaces to avoid accidental
  context switching.

## Microphone Optional

Live microphone audio is optional. For repeatable demos, record silent screen
capture first and add AI narration later. If using a microphone, record a short
test clip and check keyboard noise, room noise, and audio levels before starting
the full take.

## AI Voiceover Workflow

1. Record the walkthrough silently using the approved outline.
2. Export a rough cut with timing notes.
3. Generate narration from `video/ai-voiceover-script-draft.md`.
4. Review the narration for accuracy, tone, and pronunciation.
5. Align narration to the edited video timeline.
6. Export a draft, review for sanitization, then export the final version.

## Recommended Scene Layout

- Primary scene: full-screen browser or editor plus terminal when commands are
  being shown.
- Diagram scene: browser or image viewer focused on the topology diagram.
- Terminal scene: large terminal with no unrelated panels or tabs.
- Split reference scene: README or docs on one side and terminal on the other
  only when both are needed at the same time.
- Ending scene: README, release checklist, or repository homepage with no
  private browser state visible.
