# Project Descriptions

Each project uses a `YYYY-project-name` folder and the same README sections: Summary, Objective, Design Constraints, Engineering Work, Outcome and Evidence, Media, and Source Files.

- `README.md`: revised project narrative, constraints, evidence, and linked asset inventory.
- `media/`: images and videos with lowercase, hyphen-separated names. Double hyphens separate original subdirectory names for nested assets.
- `source/`: original notes, documents, CAD, analysis, and supporting directories. Native filenames and internal folder relationships are retained to avoid disrupting CAD references.
- Nested source images/videos also have presentation copies in `media/`; originals remain alongside their source files. Existing duplicate assets are preserved.
- `file-map.json`: original paths, current paths, and SHA-256 hashes for checking preservation and locating renamed files.

Project years follow the supplied folder names. Team awards and additional course constraints come from the existing portfolio. Missing test results are identified rather than inferred. The website catalog is maintained in `assets/data/projects.json`. Run `python scripts/build_projects.py` from the repository root after editing it to rebuild the project cards and case-study data in `index.html`. The HRC L2 leg is one project; both design archives are consolidated under `2025-hrc-l2-humanoid-leg/source/`, with shared presentation media in its `media/` folder.

| Year | Project | Context |
| --- | --- | --- |
| 2023 | [Clothes Hanger](2023-clothes-hanger/README.md) | Personal project |
| 2023 | [Desk Pencil Holder](2023-desk-pencil-holder/README.md) | Personal project |
| 2023 | [Pine Display Shelf](2023-pine-display-shelf/README.md) | Personal project |
| 2024 | [ASME Mini RC Car](2024-asme-mini-rc-car/README.md) | ASME Small Projects team |
| 2024 | [Bachelor Payload Capsule](2024-bachelor-payload-capsule/README.md) | PART · R&D Mechanical Systems |
| 2024 | [Ball Joint](2024-ball-joint/README.md) | HRC · Small Leg Components |
| 2024 | [Clip-On Sunglasses Holder](2024-clip-on-sunglasses-holder/README.md) | Personal project |
| 2024 | [Display Hooks](2024-display-hooks/README.md) | Personal project |
| 2024 | [Dodo Rear Motor Mount](2024-dodo-rear-motor-mount/README.md) | PART · R&D Mechanical Systems |
| 2025 | [HRC L2 Humanoid Leg](2025-hrc-l2-humanoid-leg/README.md) | HRC · L2 Team |
| 2026 | [Felon the Freestylin’ Feline](2026-skateboard-cat/README.md) | ME 444 · Interactive Toy Design |
| 2026 | [Tipping Hat Battle Bot](2026-tipping-hat-battle-bot/README.md) | ME 444 · Battle Bot Competition |
| 2026 | [Ghost Arm](2026-ghost-arm/README.md) | StarkHacks |
