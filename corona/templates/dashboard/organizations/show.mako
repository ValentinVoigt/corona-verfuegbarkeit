<%inherit file="../base.mako"/>
<%namespace file="../../functions/field.mako" import="field"/>

<%! from datetime import datetime, timedelta %>

<div class="container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <a href="${request.route_path('dashboard/organizations')}">
                    Organisationen
                </a>
            </li>
            <li class="breadcrumb-item active" aria-current="page">
                ${organization.name}
            </li>
        </ol>
    </nav>

    <h1>${organization.name}</h1>

    <h2>Mitglieder</h2>

    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Rollen</th>
                <th scope="col">E-Mail-Adresse</th>
                <th scope="col">Status</th>
                <th scope="col">&nbsp;</th>
            </tr>
        </thead>
        <tbody>
            <% has_noninvited = False %>
            % for has_user in organization.has_users:
                <tr>
                    <th scope="row">${loop.index+1}</th>
                    <td>${has_user.user.display_name}</td>
                    <td>
                        % for role in has_user.roles:
                            <span class="badge badge-secondary">${role.name}</span>
                        % endfor
                        % if len(has_user.roles) == 0:
                            &mdash;
                        % endif
                    </td>
                    <td>${has_user.user.email}</td>
                    <td>
                        % if has_user.user.last_login:
                            % if datetime.now() - has_user.user.last_login > timedelta(days=180):
                                <span class="text-danger">inaktiv</span>, letzter Login ${has_user.user.last_login}
                            % else:
                                <span class="text-success">aktiv</span>, letzter Login ${has_user.user.last_login}
                            % endif
                        % else:
                            % if has_user.user.last_invite is None:
                                <span class="text-danger">noch nicht eingeladen</span>
                                <% has_noninvited = True %>
                            % else:
                                <span class="text-warning">eingeladen</span>, am ${has_user.user.last_invite}
                            % endif
                        % endif
                    </td>
                    <td class="text-right">
                        % if request.has_permission("edit"):
                            <a class="btn btn-sm btn-secondary" href="${request.route_path('dashboard/users/show', id=has_user.id)}">
                                Bearbeiten
                            </a>
                        % endif
                    </td>
                </tr>
            % endfor
        </tbody>
        % if request.has_permission('edit'):
            <tfoot>
                <tr>
                    <th colspan="6" class="text-right">
                        % if has_noninvited:
                            <p>
                                <a href="${request.route_path('dashboard/users/invite', id=organization.id)}" class="btn btn-primary">
                                    Einladungen verschicken
                                </a>
                            </p>
                        % endif
                        <p>
                            <a href="${request.route_path('dashboard/users/new-batch', id=organization.id)}" class="btn btn-primary">
                                Mehrere Mitglieder hinzufügen
                            </a>
                            <a href="${request.route_path('dashboard/users/new', id=organization.id)}" class="btn btn-primary">
                                Neues Mitglied hinzufügen
                            </a>
                        </p>
                    </th>
                </tr>
            </tfoot>
        % endif
    </table>

    <h2>Rollen</h2>

    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Warnschwelle</th>
                <th scope="col">&nbsp;</th>
            </tr>
        </thead>
        <tbody>
            % for (role_org, role) in organization.recursive_roles:
                <tr>
                    <th scope="row">${loop.index+1}</th>
                    <td>
                        <span class="color-box" style="background-color: ${role.color}"></span>
                        ${role.name}
                    </td>
                    <td>
                        % if role.minimum_required is None:
                            &mdash;
                        % else:
                            ${role.minimum_required}
                        % endif
                    </td>
                    <td class="text-right">
                        % if role_org == organization and request.has_permission("edit"):
                            <a class="btn btn-sm btn-secondary" href="${request.route_path('dashboard/roles/show', id=role.id)}">
                                Bearbeiten
                            </a>
                        % else:
                            % if request.has_permission("edit", role_org):
                                (aus <a href="${request.route_path('dashboard/organizations/show', id=role_org.id)}">${role_org.name}</a>)
                            % else:
                                (aus <i>${role_org.name}</i>)
                            % endif
                        % endif
                    </td>
                </tr>
            % endfor
        </tbody>
        % if request.has_permission("edit") and request.has_permission("edit"):
            <tfoot>
                <tr>
                    <th colspan="4" class="text-right">
                        <a href="${request.route_path('dashboard/roles/new', id=organization.id)}" class="btn btn-primary">
                            Rolle hinzufügen
                        </a>
                    </th>
                </tr>
            </tfoot>
        % endif
    </table>

    <h2>Status</h2>

    <table class="table">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">&nbsp;</th>
            </tr>
        </thead>
        <tbody>
            % for (status_org, status) in organization.recursive_statuses:
                <tr>
                    <th scope="row">${loop.index+1}</th>
                    <td>
                        <span class="color-box" style="background-color: ${status.color}"></span>
                        ${status.name}
                    </td>
                    <td class="text-right">
                        % if status_org == organization and request.has_permission("edit"):
                            <a class="btn btn-sm btn-secondary" href="${request.route_path('dashboard/status/show', id=status.id)}">
                                Bearbeiten
                            </a>
                        % else:
                            % if request.has_permission("edit", status_org):
                                (aus <a href="${request.route_path('dashboard/organizations/show', id=status_org.id)}">${status_org.name}</a>)
                            % else:
                                (aus <i>${status_org.name}</i>)
                            % endif
                        % endif
                    </td>
                </tr>
            % endfor
        </tbody>
        % if request.has_permission("edit"):
            <tfoot>
                <tr>
                    <th colspan="4" class="text-right">
                        <a href="${request.route_path('dashboard/status/new', id=organization.id)}" class="btn btn-primary">
                            Status hinzufügen
                        </a>
                    </th>
                </tr>
            </tfoot>
        % endif
    </table>

    % if request.has_permission('edit'):
        <h2>Organisation bearbeiten</h2>

        <form method="POST" action="${request.route_path('dashboard/organizations/show', id=organization.id)}">
            <div class="form-group">
                ${field(form.name)}
            </div>
            <div class="form-row">
                <div class="form-group col-md-6">
                    ${field(form.postal_code)}
                </div>
                <div class="form-group col-md-6">
                    ${field(form.city)}
                </div>
            </div>
            <p class="text-right">
                <input type="submit" value="Speichern" class="btn btn-primary" />
            </p>
        </form>
    % endif
</div>
