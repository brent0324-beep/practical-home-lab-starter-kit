# Video Folder Workflow

This workflow keeps video assets predictable and separates source captures from
reviewed exports.

## Raw Recordings

Store original OBS recordings in `media/raw/`.

Use descriptive sanitized filenames:

```text
walkthrough-readme-topology-raw-YYYYMMDD.mkv
walkthrough-terminal-validation-raw-YYYYMMDD.mkv
```

Do not publish raw recordings without review. Raw captures are more likely to
include accidental browser chrome, notifications, shell history, or private
desktop details.

## Edited Exports

Store rendered drafts and final video exports in `media/edited/`.

Use names that make review status clear:

```text
walkthrough-v0.1-draft-01.mp4
walkthrough-v0.1-final-reviewed.mp4
```

Only final reviewed exports should be published.

## Narration Audio

Store AI voiceover files, scratch narration, and mixed narration in
`media/audio/`.

Keep the matching script in `video/ai-voiceover-script-draft.md` or a reviewed
script file. Regenerate narration after any major script edit instead of trying
to patch many small audio fragments.

## Screenshots

Store reviewed screenshots in `media/screenshots/`.

Use screenshots for thumbnails, README updates, blog posts, and video inserts
only after checking for private data and visual readability.

## Reusable Intro and Outro Assets

Store reusable video assets in the closest matching media folder:

- Intro and outro video clips go in `media/edited/`.
- Voice tags, stingers, or music beds go in `media/audio/`.
- Static title cards and end cards go in `media/thumbnails/` or
  `media/screenshots/` depending on how they are used.

Keep reusable assets generic enough for future walkthroughs and AI-narrated
demos.
