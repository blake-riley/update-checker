# Update-checker

Checks for outdated packages.
My intention is to hook this up to a cronscript and a macOS alerter.
This will alert me every day if something is out of date --- so I can update a formula on homebrew, for instance.

## Limitations

Currently, this package only has the ability to track releases via Github.

## Install

- git clone
- `pipx install -e .`

## Config

Requires that `config_filename` (default: `tracked_packages.yml`) exists in one of:
    - ./{config_filename}
    - ~/.config/update-checker/{config_filename}
    - env["UPDATE_CHECKER_CONFIG_FILE"]

## Example config file

```yaml
packages:
- source: github
  owner: project-gemmi
  repo: gemmi
  current_tag: 0.5.0
```
