# Known Issues Table Generator

`gen_known_issues.py` builds the **Known Issues** grid table in the Astra release
notes from the `JIRA` sheet of the TestRail `.xlsx` test reports.

## Requirements

```console
pip install openpyxl
```

## Usage

Run from the `doc/` directory:

```console
python3 ./scripts/known_issues/gen_known_issues.py "reports/*.xlsx" \
    -p release_notes/scarthgap_6.12_v2.* \
    -r scripts/known_issues/component_renames.json \
    -t scripts/known_issues/tag_config.json \
    -u release_notes/scarthgap_6.12_v2.6.0.rst
```

With no `-u` / `-o` the table is printed to stdout, which is useful for
previewing the result before rewriting a release notes file. The review report
(new entries, renames, unrecognised tags, warnings) is always written to stderr.

## How it works

1. **Reports** - one `.xlsx` per SoC. The SoC is taken from the filename
   (`SL1620`, `SL1640`, ...) unless `--soc` is given. Reports are processed in
   SoC column order (SL1620, SL1640, SL1680, SL2611, SL2615, SL2619), and the
   issues within a report keep the order of the `JIRA` sheet. This is the order
   the rows appear in the generated table.
2. **Previous release notes** (`-p`) - any issue ID that already appears in an
   older notes file reuses that entry's Module and Summary unchanged, so hand
   edits are preserved. Only new SoC flags are added. The file passed to `-u`
   is read last, so edits to the current release notes win.
3. **New IDs** - get a generated entry. The Module comes from the Jira
   *Components* value (mapped through the rename file) and the Summary from the
   Jira summary with `[bracket]` tags interpreted and removed.
4. **SoC columns** - a `Y` is set for the SoC of the report the issue came from,
   plus any SoC named in a `[SLxxxx]` tag. Everything else is `N/A`.

## Options

| Option | Description |
| --- | --- |
| `reports` | Test report `.xlsx` files (globs are expanded by the script). |
| `-p`, `--previous` | Previous release notes `.rst` files or directories. |
| `-u`, `--update` | Replace the known issues table in this `.rst` in place. |
| `-o`, `--output` | Write the table to this file. |
| `--soc` | SoC to use when it isn't in the report filename. |
| `--socs` | Comma-separated SoC columns, in order. Rows with no SoC in this list are dropped. |
| `-r`, `--renames` | JSON file of Jira component to Module renames. |
| `-t`, `--tags` | JSON tag config (`soc_aliases` / `profiles` / `boards` / `ignore`). |
| `--match-cutoff` | Similarity (0-1) used for automatic close matches of component names. `0` disables. |
| `--no-tag-socs` | Don't set SoC flags from `[SLxxxx]` tags in Jira summaries. |
| `--fresh-socs` | Set SoC flags only from the current reports, ignoring previous notes. |
| `--sort` | `report` (default, SoC order then report row order), `previous` (keep the previous notes' order), or `id`. |
| `--width` | Summary column width. Default 83. |

## Configuration files

### `component_renames.json`

Maps a Jira *Components* value to the Module text in the table. Matching ignores
case, spaces and punctuation. These entries override the built-in renames in the
script.

```json
{
  "Gstream Pipeline": "Gstreamer Pipeline",
  "HDMI TX": "HDMI-TX"
}
```

A component with no mapping is used as-is, and is listed as `unmapped` in the
review report so it can be added here if needed.

### `tag_config.json`

Controls how `[bracket]` tags in Jira summaries are handled. Entries are merged
with the defaults in the script.

| Key | Meaning |
| --- | --- |
| `soc_aliases` | Tag SoC to the SoC columns it covers, e.g. `SL2610` to `SL2611`/`SL2615`/`SL2619`. Wildcards like `SL16x0` work without an alias. |
| `profiles` | Profile tag to a note appended to new summaries. `""` means recognised but no note. |
| `boards` | Board tag to a note appended to new summaries. `""` means standard hardware, no note. |
| `ignore` | Tags dropped silently. |
| `yocto_releases` | Yocto release names, also dropped silently. |

Unrecognised tags are reported on stderr so they can be added to `profiles`,
`boards` or `ignore`.

## Reviewing the output

The generated table is a starting point. Always review:

* **New entries** - the Module and Summary are derived automatically and usually
  need wording fixes. Once edited in the release notes, later runs reuse them.
* **`close match - check` renames** - a component was fuzzy-matched to an
  existing Module name.
* **SoC mismatch** - an issue appears in a report for a SoC that isn't in its
  tags.
