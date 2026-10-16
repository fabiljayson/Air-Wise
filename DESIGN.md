---
name: "Air-Wise Design System"
description: "Framework-agnostic design rules for web and mobile app implementation."

# ─── Colors ───────────────────────────────────────────────
colors:
  # Brand
  primary:       "#475569"
  primaryStrong: "#0f172a"
  primarySoft:   "#cbd5e1"
  accent:        "#475569"

  # Surfaces
  surface:       "#f8fafc"
  surfaceMuted:  "#e2e8f0"

  # Text & Border
  text:          "#020617"
  border:        "#1e293b"

  # Feedback
  success:       "#16A34A"
  warning:       "#D97706"
  danger:        "#DC2626"

# ─── Typography ───────────────────────────────────────────
typography:
  family:        "Nunito Sans, system-ui, sans-serif"
  displayFamily: "Nunito Sans, system-ui, sans-serif"
  monoFamily:    "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
  source:        "Optional Google Font: https://fonts.google.com/specimen/Nunito+Sans"
  weights:       "300, 400, 600, 700"
  defaultWeight: 600
  tone:          "sans"

# Spacing
spacing:
  xs:      4px
  sm:      8px
  md:      12px
  lg:      16px
  xl:      24px
  xxl:     32px
  section: 48px

# Radius
radius:
  sm: 4px
  md: 8px
  lg: 12px

# Motion
motion:
  fast:   120ms
  normal: 180ms
  slow:   260ms
---

# Design System Rules

## Purpose
Air-Wise Design System defines portable, framework-agnostic design rules for web and mobile product interfaces. Use it as the source of truth before changing layouts, components, color, typography, motion, or interaction states.

This file is a portable design skill. Any AI or engineer should be able to read it and improve a web or mobile interface without needing React, Vue, Svelte, Tailwind, native mobile, or any other specific technology.

## Operating Modes

### New Project Mode
- Use these rules to create a coherent first implementation when no existing UI exists.
- Build the information architecture, component system, and responsive behavior from the tokens and rules below.

### Existing Project Refactor Mode
- Treat the existing product as the source of truth for content, routes, behavior, data, and information architecture.
- Improve the visual system by patching styles, tokens, spacing, typography, hierarchy, responsive behavior, and component states.
- Do not regenerate whole pages from scratch when a targeted patch can preserve the current experience.
- Do not replace real content with placeholder, demo, lorem ipsum, or simplified content.
- If a section looks inconsistent with this design system, restyle it first. Do not remove it.
- If removing content, routes, features, media, or data logic seems necessary, stop and ask for approval.

## Preservation Rules For Existing Products
- Preserve all existing headings, paragraphs, labels, buttons, links, images, icons, forms, navigation items, sections, routes, and data-fetching logic unless the user explicitly requests removal.
- Preserve semantic meaning and section order unless the user asks for an information-architecture change.
- Preserve working interactions: forms, menus, language toggles, theme toggles, dialogs, tabs, carousels, and scroll behavior.
- Preserve real brand/product names and domain-specific copy. Design changes must not make the page generic.
- Keep every original section represented after the refactor. A redesigned section is acceptable; a missing section is not.
- Never leave the first viewport empty unless the existing product intentionally has an empty state.

## Safe Refactor Workflow
1. Read the existing UI code before editing. Identify sections, routes, state, data dependencies, and user actions.
2. Inventory current colors, typography, spacing, radius, shadows, and component states.
3. Map old visual values to the tokens in this file one-to-one where possible.
4. Patch section by section. Avoid full-file rewrites when the current structure works.
5. After each section, verify the original content is still present, visible, and reachable.
6. After changing colors, check every affected text/background pair for contrast.
7. Verify desktop and mobile before finishing.

## Visual Direction
- Color direction: Slate - Calm technical base.
- Typography direction: Rounded Sans - Friendly controls.
- Style direction: Perspective - Spatial UI compositions with floating panels, angled mockups, depth planes, and immersive product staging
- References: VR gallery interfaces, 3D UI perspective course covers, Spatial product mockups, Layered translucent interface panels.
- Visual style: Slate color direction, Rounded Sans typography, Perspective style.

## Style System: Perspective
Use Perspective to create interfaces that feel staged in space: floating glass-like panels, angled product mockups, VR/gallery environments, layered UI cards, soft depth shadows, and controlled 3D planes. It works best for art galleries, portfolio showcases, design courses, product launches, app mockup presentations, immersive marketing pages, and visual storytelling. Depth should make the product feel dimensional and premium while the content remains readable, clickable, and calm.

### Layout Rules
- use a clear spatial stage: background environment or gradient field, midground floating panel/mockup, and foreground controls or headline.
- hero sections can use a large tilted UI mockup, VR/gallery panel, or device stack as the main visual anchor.
- use perspective transforms on visual containers, screenshots, cards, and image galleries; keep long text on a stable readable plane.
- combine depth with soft shadows, ambient blur, translucent panels, and controlled overlap to imply distance.
- use wave grids, gallery walls, device shadows, or soft spatial backdrops as atmosphere, not as competing content.
- limit each composition to three to five depth planes so the scene feels designed instead of scattered.
- place navigation and primary CTAs on the topmost stable layer so they never feel buried behind mockups.
- mobile layout should simplify into stacked panels and reduce extreme rotations, parallax, and overlap.

### Component Patterns
- visual cards can use perspective tilt between 4deg and 12deg when they are screenshots, thumbnails, course modules, or gallery artworks.
- text cards should use little or no tilt; if rotated, keep the angle subtle enough for comfortable reading.
- gallery panels may use translucent frosted surfaces, side rails, thumbnails, artist metadata, and a large artwork preview.
- course/product mockups may use stacked app screens, floating lesson cards, annotations, and soft colored depth shadows.
- buttons should remain stable and clearly interactive; primary CTAs should not rotate away from the pointer target.
- navigation, toolbars, and side controls can float as small vertical or horizontal rails with translucent or elevated treatment.
- modals and dialogs should appear as closer spatial planes with stronger shadow, blur, or dimmed background environment.
- forms, tables, and dense controls should stay mostly flat inside a perspective shell.

### Existing Project Refactor Rules
- inventory the existing interface first: navigation, hero, content sections, CTAs, media, and footer.
- preserve all content and add depth effects as an enhancement layer.
- do not remove real content to make room for decorative parallax elements.
- patch backgrounds, transforms, shadows, media framing, and layer order section by section.
- if a section has heavy text, keep it flat and let a nearby image, screenshot, or decorative plane carry the perspective.
- when adding parallax or 3D movement, test performance on mobile and disable or reduce if it causes jank.
- if the product has complex interactions, limit perspective effects to static composition, screenshot cards, or hover states only.
- if real product screenshots exist, use them as angled mockups instead of replacing them with abstract 3D art.
- keep every transformed element inside predictable bounds so it does not overlap navigation, CTAs, or subsequent sections.
- preserve semantic structure and keyboard accessibility even with layered visuals.

### Spacing Rules
- use generous spacing to let layered elements breathe: 64px to 120px between depth sections.
- section padding should be 56px to 96px on desktop, 32px to 56px on mobile.
- card padding should be 24px to 32px with consistent alignment.
- keep gutters consistent at 20px to 32px in grid layouts, with larger visual gaps around tilted mockups.
- avoid tight stacking that makes layered elements overlap awkwardly or hide edges.
- use stable dimensions, max-widths, perspective-origin, transform-origin, and z-index consistently to manage layer order.
- keep content containers within 1100px to 1320px; allow full-bleed stages only when the hero is intentionally immersive.

### Visual Hierarchy Rules
- use depth to separate hierarchy: foreground for actions and essential labels, midground for product/artwork, background for environment.
- primary CTAs should be on the topmost interactive layer and visually simpler than the 3D scene.
- headings can be large and flat, paired with a dramatic tilted mockup rather than transformed themselves.
- images, screenshots, and panels should cast soft shadows or ambient glows that match the chosen palette.
- keep body text on a flat, high-contrast plane; never force paragraphs into steep perspective.
- use blur, opacity, and scale to push background layers back while keeping the main plane dominant.
- let scroll or hover reveal depth transitions naturally without forced constant motion.
- use perspective to clarify product structure, gallery selection, or course/module relationships, not just for spectacle.

### Style Anti-patterns
- apply perspective transforms to body text or form inputs.
- use excessive parallax layers that cause motion sickness or performance issues.
- let depth effects obscure or replace actual content.
- add 3D transforms to every element — reserve depth for key moments.
- use perspective effects on accessibility-critical content.
- sacrifice load time or performance for visual depth.
- let tilted panels overflow into unrelated sections or block navigation and CTAs.
- use 3D depth as a substitute for real product images, artwork, screenshots, or useful content.

### Style Checklist
- the page feels layered and spatial through floating panels, angled mockups, or immersive gallery/product staging.
- primary content is readable on a stable plane.
- parallax and tilt effects are subtle and performant.
- depth is used to guide the user through content flow.
- interactive elements remain accessible and clearly interactive.
- mobile layout disables or reduces heavy depth effects.
- transformed panels stay within predictable bounds and do not overlap critical UI.
- the result feels cinematic, dimensional, and useful without sacrificing usability.

## Design Tokens
Use semantic tokens first. Raw values from frontmatter are source values, not permission to scatter hex codes or one-off sizes through implementation.

### Color
- Primary action color: #475569.
- Strong primary: #0f172a. Use for high-emphasis text, selected state, or strong borders.
- Soft primary: #cbd5e1. Use for subtle surfaces, selected backgrounds, or calm highlights.
- Surface: #f8fafc.
- Muted surface: #e2e8f0.
- Text: #020617.
- Border: #1e293b.
- Success, warning, and danger are semantic states. Pair them with labels, icons, or position; never rely on color alone.
- When moving from a dark theme to a light or warm theme, update inherited light text classes such as white, muted-white, or low-opacity foregrounds.
- Do not apply one warm/cream/brown palette across the entire page without contrast, hierarchy, and content anchors.

### Text Selection
- Use this style-specific `::selection` treatment for Perspective. It should follow the selected color tokens and stay readable.
```css
/* Perspective selection: lifted spatial glow. */
::selection {
  background-color: #cbd5e1;
  color: #020617;
  text-shadow: 0 2px 14px #475569;
}
```
- If the selected color changes, keep the same style behavior but re-check text/background contrast.

### Contrast And Visibility Gate
- Every visible text node must remain readable after color changes.
- Check hero text, navigation, buttons, card titles, form labels, helper text, icons, borders, and disabled states against their actual backgrounds.
- If legacy classes or CSS keep text white on a light surface, replace them with semantic foreground tokens.
- If content appears missing after a restyle, inspect contrast and visibility before deleting or rebuilding the section.
- Do not finish with invisible text, hidden CTAs, empty hero areas, or decorative backgrounds replacing product content.

### Typography
- Primary family: Nunito Sans, system-ui, sans-serif.
- Display family: Nunito Sans, system-ui, sans-serif.
- Monospace family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace.
- Allowed weights: 300, 400, 600, 700.
- Default UI weight: 600.
- Keep heading levels semantic. Visual size must follow layout importance, not HTML heading number.
- Keep letter spacing at 0 by default. Use uppercase labels sparingly and only for short metadata.

### Spacing And Radius
- Spacing scale: 4/8/12/16/24/32/48.
- Prefer spacing and grouping over extra borders.
- Use 4px radius for compact controls, 8px for standard cards/inputs, and 12px only for larger feature surfaces.
- Do not invent new spacing values unless the layout cannot be solved with the scale.

## Layout Rules
- Start mobile-first. The smallest useful viewport defines the base layout.
- Use content-driven breakpoints. Do not scale type directly with viewport width.
- Keep navigation, primary actions, and form completion paths easy to reach on touch devices.
- Prefer a clear grid, predictable alignment, and stable dimensions for controls, cards, tabs, and repeated items.
- Empty, loading, and error states must preserve layout stability and explain the next action.

## Component Rules
- Every interactive component must define default, hover, active, focus-visible, disabled, loading, success, and error behavior when those states apply.
- Buttons must communicate hierarchy through role: primary, secondary, tertiary, destructive, or icon-only.
- Forms must keep labels visible, helper text close to the field, and errors specific enough to fix.
- Cards must represent repeated items or contained tools. Do not nest cards inside other cards.
- Modals and popovers must include focus management, escape behavior, and clear dismissal affordances.

## Interaction And Motion
- Motion must clarify state change, not decorate the screen.
- Transitions should usually stay between 120ms and 260ms.
- Provide reduced-motion behavior for animations, parallax, shimmer, and auto-moving content.
- Pointer hover cannot be the only way to reveal important controls because touch devices do not have hover.

## Accessibility Requirements
WCAG 2.2 AA, keyboard-first interactions, visible focus states, semantic HTML before ARIA, reduced-motion support, accessible target sizes.

- Text and meaningful non-text UI must meet WCAG 2.2 AA contrast.
- Keyboard users must be able to reach, understand, and operate every interactive control.
- Focus indicators must be visible, high-contrast, and not hidden by overflow or animation.
- Semantic HTML or native platform semantics come before ARIA patches.
- Touch targets should be at least 24px by WCAG 2.2 AA and should reach 44px when layout allows.

## Content Tone
Clear, concise, implementation-focused, low-jargon, and helpful without being decorative.

- Use direct labels for actions.
- Avoid vague UI copy like "Submit" when the action can be named.
- Keep empty states useful: state what happened, why it matters, and what the user can do next.

## Rules: Do
- use semantic tokens before raw values in components.
- preserve existing content, copy, media, routes, and behavior when applying this system to an existing project.
- preserve hierarchy with spacing, contrast, typography, and component state.
- define default, hover, active, focus-visible, disabled, loading, success, and error states.
- design mobile-first, then enhance for tablet and desktop density.
- keep implementation guidance portable across React, Vue, Svelte, plain HTML/CSS, and mobile UI stacks.
- use layered planes, tilted screenshots, floating panels, and soft shadows to create a spatial product stage.
- keep primary copy, CTAs, and form controls on stable readable layers.
- apply parallax and tilt effects to visual media, previews, and decorative planes before applying them to text.
- test performance on mobile and disable heavy effects, scroll-linked transforms, or constant animation if needed.
- use depth to guide the user through a gallery, product demo, course preview, or narrative sequence.
- keep interactive elements on the topmost layer with visible focus states and predictable hit targets.

## Rules: Don't
- use low-contrast text, hidden focus indicators, or color-only state communication.
- delete or replace existing product content unless the user explicitly asks for content removal.
- introduce one-off spacing, typography, or radius values outside the token system.
- mix unrelated visual metaphors in the same screen.
- depend on framework-specific component names in design rules.
- add decorative motion without reduced-motion fallbacks.
- apply perspective transforms to body text or form inputs.
- use excessive parallax layers that cause motion sickness or performance issues.
- let depth effects obscure or replace actual content.
- add 3D transforms to every element — reserve depth for key moments.
- use perspective effects on accessibility-critical content.
- sacrifice load time or performance for visual depth.
- let tilted panels overflow into unrelated sections or block navigation and CTAs.
- use 3D depth as a substitute for real product images, artwork, screenshots, or useful content.

## AI Implementation Checklist
- Read this file before changing UI, layout, component styling, or interaction behavior.
- Identify the target surface: mobile app, mobile web, desktop web, dashboard, landing page, form flow, or content-heavy view.
- Map the design tokens to the project technology without changing the design intent.
- Reuse existing project components when they can satisfy these rules.
- If the current UI conflicts with this file, explain the conflict and choose the more accessible, consistent option.
- Confirm all original navigation items, hero content, CTAs, media, sections, and forms still exist unless removal was requested.
- Confirm no text became invisible from background, opacity, blend-mode, or inherited color changes.
- Confirm the first viewport contains meaningful product content, not just a background treatment.
- Verify keyboard navigation, focus-visible styling, responsive behavior, text overflow, loading state, and error state before finishing.
