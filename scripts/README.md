# Profile assets

Python 3.11+; no third-party packages or external fonts.

From the repository root:

```sh
python3 scripts/generate_avatar.py
python3 scripts/generate_info.py
python3 scripts/generate_intro.py
python3 scripts/generate_sections.py
python3 scripts/generate_mobile.py
python3 scripts/fetch_contributions.py --username chiyo-an
python3 scripts/generate_contribution.py
python3 scripts/test_profile.py
```

Edit personal information in `generate_info.py`, building/toolbox copy in
`generate_sections.py` and `generate_mobile.py`, and the original pixel grid
in `generate_avatar.py`. Regenerate the affected SVGs after editing.

Activity is public GitHub calendar data, not a count of all private work.
The public HTML endpoint is undocumented and can change. The parser requires
365–371 consecutive recent dates, valid levels, and matching tooltip counts.
Network requests use a timeout and bounded retries. Unexpected HTML fails
without replacing the last successful JSON; the workflow then stops before
rendering or committing. Empty data renders an explicit unavailable state.
No fetch timestamp is stored, so unchanged data produces no daily commit.

The 53 × 7 grid reserves future cells as unavailable. Counts are real data;
tech lists imply focus, not proficiency scores. All animation plays once and
CSS reduced-motion disables it. SVGs contain no scripts, foreignObject,
external resources, or embedded fonts. README uses GitHub-supported image
and picture markup; narrow screens select mobile assets and stack the intro.

The workflow uses only checkout and setup-python. Contribution fetching needs
no personal token; committing uses GitHub's built-in GITHUB_TOKEN with
contents: write. It runs at 04:23 UTC (13:23 Asia/Seoul) daily or manually on
the default branch. Only the activity JSON and SVG are staged. Repository
rules can still prohibit bot pushes. Scheduled workflows can be delayed or
disabled by GitHub for prolonged public-repository inactivity.

Local checks cover XML, asset paths, real-data grid size, empty state, malformed
HTML, and preservation on failure. GitHub's Markdown API retained picture
sources. Desktop and narrow-container layouts were reviewed in a browser.
Live GitHub image proxy behavior, actual mobile-device rendering, and hosted
Actions execution remain to be verified after publication.

Implementation approach: https://www.avivashishta.com/blog/build-animated-github-profile-readme
Actions: https://github.com/actions/checkout and https://github.com/actions/setup-python
