# Transformer

The transformer module is currently aimed at importing, exporting and publishing content managed via the SSDLC module, which in turn builds on doorstop. Therefore, the three currently implemented functions, i.e., import, export and publish, act as a front-end to doorstop.

## Import SSDLC data

The import function can be used not only to import new content into a project repository managed by C5-DEC CAD, but it can also be used to temporarily move content out of the doorstop data store, modify it and have it imported back into the data store, thereby overwriting the content, e.g., exporting requirements to xlsx so they can be edited in MS Excel and then migrated back to the project repository. This is a front-end for invoking the [doorstop import](https://doorstop.readthedocs.io/en/latest/cli/interchange/) function.

![SSDLC transformer import function](./_figures/ssdlc-transformer-import.png)

## Export SSDLC data

The export function follows the same logic as above, just in reverse.

![SSDLC transformer export function](./_figures/ssdlc-transformer-export.png)

## Publish SSDLC data

The publish function can be used for viewing purposes and end-user analysis, navigation, etc. it can export to HTML, plain text (.txt), Markdown and LaTeX; it acts as a front-end to [doorstop publishing](https://doorstop.readthedocs.io/en/latest/cli/publishing/).

![SSDLC transformer publish function](./_figures/ssdlc-transformer-publish.png)

## Convert data

The convert data function is currently not implemented, but it is on the roadmap and part of the backlog candidates. The TUI component is however implemented, showcasing the currently planned feature. In the meantime, a similar functionality can be achieved by using Zettlr or pandoc directly. Users can also use the C5-DEC documentation engine (DocEngine), which is still under development; further details can be found in the corresponding entry on the Abstractions Lab GitHub page.

![SSDLC transformer convert data function](./_figures/ssdlc-transformer-convert-data.png)