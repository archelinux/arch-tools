# archelinux tools for Arch

These three commands can run on a plain Arch Linux system. Their original implementations ship with [archelinux](https://github.com/archelinux/archelinux). The source is licensed under GPL-3.0-only.

| Command | Purpose |
| --- | --- |
| `arche-waybar-github` | Show unread GitHub pull requests and issues in Waybar using the current user's GitHub CLI session. |
| `arche-waybar-status disk\|vpn\|gpu` | Show low disk space, active VPNs or GPU readings as Waybar JSON. Each indicator hides when it has nothing to report. |
| `arche-rollback PACKAGE` | Select the newest cached version older than the installed package and reinstall it with pacman. Reads the cache directories from pacman.conf. |

## Waybar

Sign in with `gh auth login --hostname github.com`. Your token needs read access to notifications. Put `custom/github` in the appropriate `modules-left`, `modules-center` or `modules-right` array, then add this object to your Waybar configuration:

```json
"custom/github": {
  "exec": "arche-waybar-github",
  "return-type": "json",
  "interval": 120,
  "hide-empty-text": true,
  "on-click": "xdg-open https://github.com/notifications"
}
```

Restart Waybar. An empty inbox hides the widget. `GH login` asks you to sign in. `GH ?` means the check failed; hover for details. The optional click action uses xdg-utils. For the other indicators use the same module format, a separate module name, and one of `arche-waybar-status disk`, `arche-waybar-status vpn` or `arche-waybar-status gpu` as the command.

## Cached rollback

Use `sudo arche-rollback PACKAGE` for a specific package with a known-good older archive in your pacman cache. The tool runs the pacman transaction immediately. Related libraries may need to be downgraded together. On archelinux, the maintenance package already provides the rollback command.

## Install on plain Arch

Install `base-devel` and Git, then clone this repository. In the corresponding directory under `aur/`, inspect the PKGBUILD and run `makepkg -si` as your regular user. Runtime dependencies come from Arch repositories. On archelinux, use the signed distro repository for the packages shipped by the distro.
