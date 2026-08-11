# Zen Browser Inactive Opacity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep Zen Browser opaque when unfocused while retaining the existing inactive opacity for every other application.

**Architecture:** Add one declarative Hyprland window rule to the existing rules module. The rule matches Zen Browser's initial class and overrides both opacity values; the global decoration configuration remains unchanged.

**Tech Stack:** Hyprland 0.56+, Lua configuration, `Hyprland --verify-config`.

---

### Task 1: Add and validate the Zen Browser opacity rule

**Files:**
- Modify: `hyprland/.config/hypr/modules/rules.lua`
- Test: Hyprland configuration verification through `hyprland/.config/hypr/hyprland.lua`

- [x] **Step 1: Establish the pre-change check**

Run: `Hyprland --verify-config -c "$PWD/hyprland/.config/hypr/hyprland.lua"`

Expected: configuration verification succeeds before the Firefox-specific rule is added.

- [x] **Step 2: Add the smallest Zen Browser-only rule**

Add this declaration after the existing application window rules:

```lua
hl.window_rule({
    name = "zen-browser-opaque-when-inactive",
    match = { initial_class = "app.zen_browser.zen" },
    opacity = "1.0 1.0",
})
```

- [x] **Step 3: Verify the changed configuration**

Run: `Hyprland --verify-config -c "$PWD/hyprland/.config/hypr/hyprland.lua"`

Expected: configuration verification succeeds with no parsing or Lua errors.

- [x] **Step 4: Inspect the exact diff**

Run: `git diff --check && git diff -- hyprland/.config/hypr/modules/rules.lua`

Expected: no whitespace errors and exactly one Zen Browser-specific window rule; no change to `decoration.inactive_opacity`.

- [x] **Step 5: Commit the implementation**

```bash
git add hyprland/.config/hypr/modules/rules.lua docs/superpowers/plans/2026-08-11-firefox-inactive-opacity.md
git commit -m "fix: keep Zen Browser opaque when unfocused"
```
