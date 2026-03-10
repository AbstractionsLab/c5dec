# Beamer PDF Output - Known Issues and Workarounds

## Current Status

The presentation template currently has compatibility issues with Beamer PDF output due to advanced Reveal.js-specific features used in the content slides. **Reveal.js (HTML) and PowerPoint (PPTX) formats work perfectly.**

## Known Issues

1. **`.r-stack` fragments**: The Reveal.js stacking animations don't translate to Beamer
2. **Complex column layouts**: Some advanced column syntax may not render in Beamer
3. **Custom callouts**: Quarto callouts may have rendering issues in Beamer

## Workarounds

### Option 1: Create Beamer-Specific Content (Recommended for Production)

Create separate slide files for Beamer format:

1. **Create** `slides/intro-beamer.qmd`, `slides/content-beamer.qmd`, etc.
2. **Simplify** content (remove .r-stack, complex animations)
3. **Update** `index.qmd` to conditionally include:
   ```markdown
   ::::: {.content-visible when-format="beamer"}
   {{< include slides/intro-beamer.qmd >}}
   :::::
   
   ::::: {.content-visible unless-format="beamer"}
   {{< include slides/intro.qmd >}}
   :::::
   ```

### Option 2: Simplify Existing Content

Edit `slides/content.qmd` and remove:
- Line ~151-157: `.r-stack` demo section
- Complex conditional blocks
- Fancy Reveal.js features

### Option 3: Use Reveal.js PDF Export

Instead of Beamer, use Reveal.js PDF export:

1. **Render to HTML**: `quarto render index.qmd --to revealjs`
2. **Open in browser**: `_output/index.html`
3. **Add ?print-pdf** to URL: `index.html?print-pdf`
4. **Print to PDF** using browser's print function

This preserves animations and layout better than Beamer.

### Option 4: Skip Beamer  

For most use cases, Reveal.js (HTML) for presentations and PowerPoint for editing is sufficient. Beamer PDF is primarily useful for:
- Print handouts
- Archival purposes  
- Venues requiring PDF-only submissions

## Future Improvements

To enable Beamer support:
1. Remove Reveal.js-specific features from shared content
2. Use more conditional blocks for format-specific features
3. Create minimal Beamer template without advanced features
4. Test LaTeX compatibility thoroughly

## Quick Test

To test if Beamer issues are resolved:

```bash
cd /home/alab/c5dec/c5dec/assets/presentation
quarto render index.qmd --to beamer
```

Check `index.log` for specific LaTeX errors.

## Getting Help

If you need Beamer PDF output:
- **Email**: info@abstractionslab.lu
- **Issue**: Report with `index.log` contents
- **Workaround**: Use Option 3 (Reveal.js PDF export) in the meantime

---

**Status**: Beamer support is a known limitation in v1.0. Reveal.js and PowerPoint work perfectly.
