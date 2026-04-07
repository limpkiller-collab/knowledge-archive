# High-End Knowledge Management Design System

## 1. Overview & Creative North Star
**Creative North Star: "The Obsidian Curator"**

This design system moves away from the "SaaS-standard" dashboard. Instead, it adopts the persona of a high-end editorial gallery. It treats knowledge not as data to be managed, but as assets to be curated. The aesthetic is defined by **Low-Light Sophistication**: a deep, obsidian-like foundation where information glows with intentionality.

To break the "template" look, we employ:
*   **Intentional Asymmetry:** Avoid perfect 50/50 splits. Use a 60/40 or 70/30 layout ratio to create a rhythmic, editorial flow.
*   **Tonal Depth:** We eliminate harsh lines in favor of light-source modeling.
*   **High-Contrast Typography:** Inter and Noto Sans KR are used with dramatic scale shifts—pairing massive `display-lg` headlines with micro `label-sm` metadata to create an authoritative hierarchy.

---

## 2. Colors & Surface Logic

The palette is rooted in a "Dark Mode First" philosophy, utilizing a layered charcoal base to provide infinite depth.

### Color Tokens (Material Design Convention)
*   **Background:** `#0e0e0e` (The void)
*   **Surface:** `#0e0e0e`
*   **Surface Container (Low to Highest):** `#131313` → `#1a1919` → `#201f1f` → `#262626`
*   **Primary (Tech):** `#85adff` (Electric Blue tint)
*   **Secondary (Investment):** `#69f6b8` (Emerald tint)
*   **Tertiary (Culture):** `#ff6f7e` (Rose tint)
*   **Amber (Real Estate):** Custom token for Real Estate modules.

### The "No-Line" Rule
**Prohibit 1px solid borders for sectioning.** 
Boundaries must be defined solely through background color shifts. To separate a sidebar from a main feed, transition from `surface` to `surface-container-low`. The human eye perceives the change in luminance as a structural boundary without the "boxed-in" feel of a stroke.

### The "Glass & Gradient" Rule
Floating elements (modals, dropdowns, navigation rails) must use **Glassmorphism**.
*   **Fill:** `surface-variant` at 60% opacity.
*   **Backdrop Blur:** 20px to 32px.
*   **The Glow:** Use a linear gradient stroke (Top-Left to Bottom-Right) from `outline-variant` at 20% opacity to `transparent`. This mimics a light source hitting the "edge" of the glass.

---

## 3. Typography
The system uses a dual-font approach to ensure global readability without sacrificing the "Tech-Noir" aesthetic.

*   **Inter (Latin/Numbers):** The workhorse. Use it for data-heavy tables and functional labels.
*   **Noto Sans KR (Korean):** Optimized for high-density reading. 

**Hierarchy Strategy:**
*   **Editorial Headlines:** Use `display-md` (2.75rem) with a `-0.02em` letter-spacing for a "tight," premium look.
*   **The Metadata Micro-Scale:** Use `label-sm` (0.6875rem) in uppercase with `+0.05em` letter-spacing. This creates a technical, architectural feel when paired with larger body text.
*   **Contrast:** Always keep `on-surface` (white) for primary headings and `on-surface-variant` (muted grey) for secondary descriptions to maintain clear focus.

---

## 4. Elevation & Depth

### The Layering Principle
Depth is achieved by stacking `surface-container` tiers. 
*   **Base:** `surface` (#0e0e0e)
*   **Section:** `surface-container-low` (#131313)
*   **Card/Module:** `surface-container-high` (#201f1f)
*   **Active/Pop-over:** `surface-bright` (#2c2c2c)

### Ambient Shadows
Forget "Drop Shadows." Use **Ambient Glows**.
*   **Shadow Color:** Use the tint of the accent color (e.g., Electric Blue) at 4-8% opacity.
*   **Blur:** 40px to 60px.
*   **Spread:** -10px.
This makes components appear to be emitting light onto the surface below, rather than casting a shadow from an external sun.

### The "Ghost Border" Fallback
If a border is required for accessibility, it must be a **Ghost Border**:
*   **Token:** `outline-variant`
*   **Opacity:** 15% 
*   **Logic:** Only use this to define input fields or high-density table cells.

---

## 5. Components

### Cards & Modules
*   **Strict Rule:** No dividers. Separate content using `48px` or `64px` vertical whitespace.
*   **Corner Radius:** `xl` (0.75rem) for main containers; `md` (0.375rem) for inner nested elements.
*   **Interaction:** On hover, transition the background from `surface-container-high` to `surface-bright` and apply a subtle `primary` glow.

### Interactive Chips
*   **Tech (Primary):** `primary-container` background with `on-primary-container` text.
*   **Investment (Secondary):** `secondary-container` background with `on-secondary-container` text.
*   **Visual Style:** Pills should be `full` rounded. Use `label-md` for the font to keep them crisp.

### Data Visualization
*   **The "Vibrant Stroke":** Graphs should use a 2.5px stroke width.
*   **Area Charts:** Use a vertical gradient from the accent color (100% opacity) to `transparent` (0% opacity) to create a "liquid" data feel.

### Buttons
*   **Primary:** Fill with `primary-fixed`. Use `on-primary-fixed` (Black) for text to ensure maximum contrast.
*   **Secondary (Ghost):** No fill. Use a `Ghost Border` with `primary` text. On hover, add a 5% `primary` background tint.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical margins (e.g., 80px left, 40px right) to create editorial interest in long-form knowledge articles.
*   **Do** use "Optical Centering"—sometimes an icon looks better 1px higher than the mathematical center. Trust your eye.
*   **Do** use `primary-dim` for interactive icons to signal clickability without being distracting.

### Don't
*   **Don't** use pure black (#000) for anything other than `surface-container-lowest` or shadows. It "kills" the tonal depth.
*   **Don't** use standard 1px grey dividers between list items. Use 16px of vertical padding instead.
*   **Don't** stack more than three levels of surfaces. If you need a fourth level, use a Glassmorphism overlay.
*   **Don't** use high-saturation backgrounds for text-heavy areas. Keep accents for highlights, chips, and data points only.