# Creating a Custom PowerPoint Template

The presentation template supports custom PowerPoint templates for branded output. Here's how to create one:

## Option 1: Generate from Default (Recommended)

1. **Generate a basic PowerPoint** first:
   ```bash
   cd /home/alab/c5dec/c5dec/assets/presentation
   quarto render index.qmd --to pptx
   ```

2. **Customize the master slides**:
   - Open `_output/index.pptx` in Microsoft PowerPoint or LibreOffice Impress
   - Go to View → Master → Slide Master
   - Customize:
     - Title slide layout (add logos from `figs/`)
     - Content slide layouts
     - Color scheme (ALab Red: #E30613, ALab Light Blue: #00A8E1)
     - Fonts (Ubuntu or your preferred font)
     - Footer and headers

3. **Save as template**:
   - Save As → `custom-pptx-template.pptx` in the presentation directory
   - Close PowerPoint

4. **Enable in configuration**:
   - Edit `_quarto.yml`
   - Uncomment the line: `reference-doc: custom-pptx-template.pptx`

5. **Test**:
   ```bash
   quarto render index.qmd --to pptx
   ```

## Option 2: Start from Scratch

1. Open PowerPoint and create a new blank presentation
2. Go to View → Master → Slide Master
3. Design your master slides with ALab branding
4. Save as `custom-pptx-template.pptx` in this directory
5. Follow steps 4-5 from Option 1

## Option 3: Copy from Report Template

If you already have a PowerPoint template for C5-DEC reports:

```bash
cp /path/to/your/existing/template.pptx custom-pptx-template.pptx
```

Then enable it in `_quarto.yml`.

## Tips for PowerPoint Templates

- **Keep it simple**: Complex master slides may not render perfectly
- **Test thoroughly**: Generate a full presentation to verify all slide types
- **Use web-safe fonts**: Or ensure fonts are embedded
- **Image placement**: Position logos consistently across master slides
- **Color consistency**: Use ALab brand colors throughout

## Without a Custom Template

The presentation works fine without a custom template! Quarto will use PowerPoint's default template. Your content will still be properly formatted, just without custom branding on the master slides.

---

For more information, see: https://quarto.org/docs/presentations/powerpoint.html
