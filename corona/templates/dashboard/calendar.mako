<%inherit file="base.mako"/>
<%namespace file="../functions/field.mako" import="field"/>
<%! from datetime import date %>

<div class="container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item active">Kalender</li>
        </ol>
    </nav>

    % if len(request.user.has_organizations) > 1:
        <ul class="nav nav-tabs">
            % for has_organization in request.user.has_organizations:
                <li class="nav-item">
                    <a
                        class="nav-link${' active' if has_organization.id==request.context.id else ''}"
                        href="${request.route_path('dashboard/calendar', id=has_organization.id)}">
                        ${has_organization.organization.display_name}
                    </a>
                </li>
            % endfor
        </ul>
    % endif

    % if not has_name:
        <h1>Meine Daten</h1>

        <p>
            Bitte gib zuerst deinen Namen für die Organisation ${organization.display_name} ein.
        </p>

        <form method="POST" action="${request.route_path('dashboard/calendar', id=request.context.id)}">
            <div class="form-row">
                <div class="form-group col-md-6">
                    ${field(name_form.first_name)}
                </div>
                <div class="form-group col-md-6">
                    ${field(name_form.last_name)}
                </div>
            </div>
            <p class="text-right">
                <input type="submit" value="Speichern und fortfahren »" class="btn btn-primary" />
            </p>
        </form>
    % else:
        <h1>Meine Verfügbarkeit</h1>
        <h2 class="h5">Neuen Status eintragen</h2>
        <form method="POST" action="${request.route_path('dashboard/calendar', id=request.context.id)}">
            <div class="form-group">
                ${field(calendar_form.start, type="date")}
            </div>
            <div class="form-group">
                ${field(calendar_form.end, type="date")}
            </div>
            <div class="form-group">
                ${field(calendar_form.status)}
            </div>
            <p class="text-right">
                <input type="submit" value="Speichern" class="btn btn-primary" />
            </p>
        </form>

        <h2 class="h5">Aktuell eingetragen</h2>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Von</th>
                    <th scope="col">Bis</th>
                    <th scope="col">Status</th>
                    <th scope="col">&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <% last_entry = None %>
                % for entry in has_user.calendar:
                    % if entry.end < date.today():
                        <% continue %>
                    % endif
                    % if last_entry and last_entry.end < entry.start:
                        <tr>
                            <td colspan="5" class="text-center text-danger">
                                Eintrag fehlt vom ${last_entry.end.strftime('%d.%m.%y')}
                                bis zum ${entry.start.strftime('%d.%m.%y')}
                            </td>
                        </tr>
                    % endif
                    <tr>
                        <th scope="row">${loop.index+1}</th>
                        <td>${entry.start.strftime('%d.%m.%Y')}</td>
                        <td>${entry.end.strftime('%d.%m.%Y')}</td>
                        <td>
                            <span class="color-box" style="background-color: ${entry.status.color}"></span>
                            ${entry.status.name}
                        </td>
                        <td class="text-right">
                            <form action="${request.route_path('dashboard/calendar/delete', id=entry.id)}">
                                <input
                                    type="submit"
                                    value="Löschen"
                                    class="btn btn-danger btn-sm"
                                    onclick="return confirm('Eintrag wirklich löschen?');"
                                />
                            </form>
                        </td>
                    </tr>
                    <% last_entry = entry %>
                % endfor
                % if len(has_user.calendar) == 0:
                    <tr>
                        <td colspan="5" class="text-center">
                            Noch keine Verfügbarkeiten eingetragen.
                        </td>
                    </tr>
                % endif
            </tbody>

        </table>
    % endif
</div>

