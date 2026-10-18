# Browser-review evidence

The final publication review used the live URL at desktop 1440 × 900 and mobile
390 × 844. The browser session verified the rendered layouts, console output,
keyboard skip link, catalogue filtering and horizontal-overflow checks.

The live capture images are included in the publication handoff. The browser
automation sandbox could capture them but could not export its image bytes to
this repository directory.

## New evidence produced for the portfolio review (2026-10-18)

This is a separate review from the original publication handoff described above.
The work is contained in `feature/real-demo-og-validation`; public `main` is unchanged until approval.

- `projectpilot-demo.txt` is a transcript derived from a genuine CLI run of ProjectPilot in an isolated Ubuntu GitHub Actions environment (Python 3.12), not a simulation.
- Verified run: https://github.com/migmcc/migmcc.github.io/actions/runs/39114405547
- Commands: `pp init`, `pp status`, `pp next`, `pp dashboard`. Test project name: `Review Assistant`.
- The run creates local state and recommends `pp validate` but does not execute an AI agent.
- Browser screenshots are generated anew in GitHub Actions for 1440 × 900 and 390 × 844, and archived as the workflow's `migmcc-review-evidence` artifact.
- Screenshots cover home, Quality Docs Validator and ProjectPilot; browser tests traverse eight routes, verify no horizontal overflow or script errors, and exercise catalog search.
- `assets/og-card.svg` is the original editable Open Graph design; `assets/og-card.png` is the generated 1200 × 630 raster intended for social previews. The illustration does not depict an actual CLI screenshot or traffic figures.

Evidence artifacts are stored with the Actions run rather than permanently committed as binary screenshots. See https://github.com/migmcc/migmcc.github.io/actions for the latest successful workflow. Verify actual social previews after publishing because platforms may cache previous metadata.
