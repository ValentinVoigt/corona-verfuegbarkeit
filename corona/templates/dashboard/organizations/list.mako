<%inherit file="../base.mako"/>

<%def name="show_tree(base, level)">
    <li class="list-group-item d-flex justify-content-between">
        <div>
            % for i in range(level):
                <span class="mx-2"></span>
            % endfor
            <a href="${request.route_path('dashboard/organizations/show', id=base.id)}" class="font-weight-bold">
                ${base.name}
            </a>
            <span class="mx-2"></span>
            ${len(base.has_users)} ${"Mitglied" if len(base.has_users) == 1 else "Mitglieder"}
        </div>
        <div class="text-right">
            <span class="mx-2"></span>
            <a href="${request.route_path('dashboard/organizations/new', id=base.id)}">Unterorganisation anlegen</a>
        </span>
    </li>
    % for sub in base.children:
        ${show_tree(sub, level+1)}
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
