# Paper 60 VLA Highlight Hardening Plan

Objective: make Paper 60's boxed PDF highlights match the VLA-v4 role-model PDF while preserving the final full-scale embodied model disagreement benchmark and bounded scientific claims.

## Role-Model Target

- Citation links use green rectangular borders with no fill.
- Internal references use red rectangular borders with no fill.
- URL links use the same green border family as citations.
- Border width is `pdfborder={0 0 1}`, matching the VLA-v4 annotation metadata.
- Boxes stay tight to linked text and must not affect typography, spacing, figure captions, tables, or scientific content.

## Current Paper 60 Mismatch

- `Downloads/60.pdf` has link annotations on pages 2, 5, 8, 9, 10, 12, 13, 14, 15, and 26.
- Annotation colors are already red/green, but every link has border width `0`.
- `paper/main.tex` uses `\hypersetup{hidelinks}`, so the link boxes are invisible and do not match the VLA-v4 role model.
- `child_status.md` still describes an older v2/workshop-only state, so it needs metadata refresh after the build.

## Execution Plan

1. Keep RAM use low by rendering only affected pages before and after the edit: pages 2, 5, 8, 9, 10, 12, 13, 14, 15, and 26.
2. Replace `\hypersetup{hidelinks}` in `paper/main.tex` with explicit VLA-style link annotation settings:
   - `colorlinks=false`
   - `pdfborder={0 0 1}`
   - `citebordercolor={0 1 0}`
   - `linkbordercolor={1 0 0}`
   - `urlbordercolor={0 1 0}`
3. Rebuild with `build_pdf.ps1`, which exports the canonical final PDF to `C:\Users\wangz\Downloads\60.pdf`, writes build metadata, and removes local `paper/main.pdf`.
4. Validate the rebuilt PDF annotation metadata with `pypdf`.
5. Render pages 2, 5, 8, 9, 10, 12, 13, 14, 15, and 26 again and visually compare with the VLA-v4 role model.
6. Update README/status/build metadata and SHA text if present.
7. Remove Paper 60 temporary render folders, then commit and push the clean repo.

## Non-Goals

- Do not rerun the full-scale benchmark.
- Do not change tables, figures, result claims, page count target, or bounded safety language.
- Do not pad the paper or alter manuscript content beyond link-box styling and stale metadata.
