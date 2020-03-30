<%inherit file="../base.mako"/>

<%! from datetime import date %>

<%def name="show_tree(base, level)">
    <li class="list-group-item d-flex justify-content-between">
        <div>
            % for i in range(level):
                <span class="mx-2"></span>
            % endfor
            % if request.has_permission("details", base):
                <a href="${request.route_path('dashboard/organizations/show', id=base.id)}" class="font-weight-bold">
            % else:
                <strong>
            % endif
            ${base.name}
            % if request.has_permission("details", base):
                </a>
            % else:
                </strong>
            % endif
            % if request.has_permission("details", base):
                <span class="mx-2"></span>
                ${len(base.has_users)} ${"Mitglied" if len(base.has_users) == 1 else "Mitglieder"}
                <span class="mx-2"></span>
                <a href="${request.route_path('dashboard/organizations/availability', id=base.id)}">
                    Verfügbarkeit
                </a> heute:
                ${base.num_available(date.today(), 'day')} tagsüber,
                ${base.num_available(date.today(), 'night')} nachts
            % elif request.user in [h.user for h in base.has_users]:
                <span class="mx-2"></span>
                Du bist hier Mitglied!
            % endif
        </div>
        % if request.has_permission("edit", base):
            <div class="text-right">
                <span class="mx-2"></span>
                <a href="${request.route_path('dashboard/organizations/new', id=base.id)}">Unterorganisation anlegen</a>
            </span>
        % endif
    </li>
    % for sub in base.children:
        % if request.has_permission("view", sub):
            ${show_tree(sub, level+1)}
        % endif
    % endfor
</%def>

<div class="container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item active">Organisationen</li>
        </ol>
    </nav>

    <h1>Meine Organisationen</h1>

    <ul class="list-group">
        % for organization in organizations:
            ${show_tree(organization, 0)}
        % endfor
    </ul>
</div>
