# GradeLightGroupGizmo

This is the development version of the tool based up on the lighting render template create by Aaron.

The gizmo is activated by hitting the `Get Light Groups` button which checks for lightgroups named "lgt##_pass_name" and creates a dropdown "lightgroup" with all the availiable lightgroups.

In the dev version this also sets up the "knob changed" callback on the dropdown

Internally the sliders connect to the grade and exposure knobs meaning that they can be controlled at an overall level or split between `direct` and `indirect` components

Access is only given to the `Exposure` and `Multiply` values so that any changes made can be replicated in the renderer if need be.


Assumptions:

- and `Unpremult/all`precedes the gizmo in the script
- pass names used are `diffuse_direct`, `diffuse_indirect`, `reflect_direct`, `reflect_indirect`, `refract_direct`, `refract_indirect`, `sss_direct`,`sss_indirect`
- lightgroups all contain the flag `lgt` followed by a number followed by the _pass_name

Limitations:

- Emission is currently not handled by the tool and should be handled externally.
- unpremult/premult is done externally to the gizmo (this is part of our larger lighting/lookdev setup)

Roadmap:

- Currently using a Group/Toolset rather than a gizmo as easier to turnaround changes. Intention to lock down into a gizmo for wider release
- The current Toolset reloads the associated `.py` when `Get Light Groups` is run for faster development. When released the python functions and callbacks will be setup directly in the `init.py` with `knob_changed` activated by a `on_create` callback.
- There will be a larger autocomp setup for lighters to use, plan is for it to create an A over B automatically from lighting and then bea starting point for lighting lookdev and comp.
