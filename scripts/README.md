# Profile assets

Python 3.11+ standard library only. Run from the repository root:

```sh
python3 scripts/generate_avatar.py
python3 scripts/generate_info.py
python3 scripts/generate_sections.py
python3 scripts/generate_mobile.py
python3 scripts/generate_intro.py
python3 scripts/generate_languages.py
python3 scripts/test_languages.py
```

Edit personal information in generate_info.py; building/toolbox copy in
generate_sections.py and generate_mobile.py; pixel art in generate_avatar.py.
Regenerate intro after changing avatar or info. No external fonts or CDN assets.
Animations play once and support prefers-reduced-motion.

Language assets reuse real name/percentage pairs from metrics.svg, with a
blue palette and the same typography as the rest of the profile. Percentages
represent repository code composition, not proficiency or time spent coding.
The lowlighter languages plugin and its existing METRICS_TOKEN supply the
source data. Invalid or missing language data stops rendering and publication.

The Metrics workflow runs daily at 00:00 UTC / 09:00 Asia/Seoul or manually.
It generates metrics.svg without committing, renders both profile language
assets, and commits only those three files if they changed. The former custom
contribution calendar and its workflow are removed; GitHub's native calendar
remains visible. GitHub rules may prohibit bot pushes.

Sources:
https://github.com/lowlighter/metrics/blob/master/source/plugins/languages/README.md
https://github.com/lowlighter/metrics/blob/master/source/plugins/core/README.md
