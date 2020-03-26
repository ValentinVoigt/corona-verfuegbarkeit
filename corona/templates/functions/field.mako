<%def name="add_class(kwargs, class_)">
    % if 'class_' in kwargs:
        <% kwargs['class_'] = kwargs['class_'] + " " + class_ %>
    % else:
        <% kwargs['class_'] = class_ %>
    % endif
</%def>

<%def name="field(field, **kwargs)">
    <%
        add_class(kwargs, "form-control")

        if not 'placeholder' in kwargs:
            kwargs['placeholder'] = field.label.text

            if field.errors:
                add_class(kwargs, "is-invalid")
    %>

    ${field.label(class_="required" if field.flags.required else None)}
    ${field(**kwargs)}

    % if field.errors:
        <div class="invalid-feedback">
            <ul class="list-inline">
                % for error in field.errors:
                    <li>${error}</li>
                % endfor
            </ul>
        </div>
    % endif
</%def>
