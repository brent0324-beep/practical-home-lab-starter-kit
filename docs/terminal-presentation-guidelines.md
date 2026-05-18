# Terminal Presentation Guidelines

Use these guidelines when recording terminal-heavy walkthroughs or capturing
screenshots for documentation.

## Font Recommendations

- Use a clear monospace font such as JetBrains Mono, Fira Code, DejaVu Sans
  Mono, Ubuntu Mono, or IBM Plex Mono.
- At 1920x1080, start around 16 to 20 pt.
- Avoid thin font weights and low-contrast color themes.
- Keep line spacing comfortable enough that commands and output do not blend
  together.

## Terminal Sizing

- Keep terminals wide enough for commands but not so wide that text becomes
  small.
- Aim for 100 to 120 columns for most recorded command sequences.
- Use full-screen terminal capture only when the output needs the space.
- Avoid resizing the terminal during a take unless the resize itself is part of
  the demonstration.

## Prompt Cleanliness

- Use sanitized prompts such as `labuser@lab-host:~/repo$`.
- Hide private usernames, hostnames, absolute home paths, and shell plugin
  status segments.
- Avoid prompts that show cloud account names, branch metadata from unrelated
  work, VPN names, or local network details.
- Keep command examples reproducible from the repository root.

## Avoiding Clutter

- Clear the terminal before each scene.
- Collapse or close unrelated panes, tabs, and split views.
- Keep command output focused on the teaching point.
- Avoid recording package-manager noise unless it is necessary to the lesson.
- Prefer short, readable command sequences over long pasted blocks.

## Screenshot and Video Readability

- Review screenshots at thumbnail size and at full size.
- Confirm commands are legible on a laptop screen and a phone screen.
- Use browser or editor zoom when showing README sections or code.
- Crop only after confirming the crop does not remove useful context.
- Re-record clips with unreadable text instead of relying on narration to
  explain invisible details.
