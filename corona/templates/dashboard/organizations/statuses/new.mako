<%inherit file="../../base.mako"/>
<%namespace file="../../../functions/field.mako" import="field"/>

<div class="container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <a href="${request.route_path('dashboard/organizations')}">Organisationen</a>
            </li>
            <li class="breadcrumb-item">
                <a href="${request.route_path('dashboard/organizations/show', id=organization.id)}">
                    ${organization.name}
                </a>
            </li>
            <li class="breadcrumb-item active" aria-current="page">
                Neuer Status
            </li>
        </ol>
    </nav>

    <h1>Neuer Status</h1>

    <form method="POST" action="${request.route_path('dashboard/status/new', id=organization.id)}">
        <div class="form-group">
            ${field(form.name)}
        </div>
        <div class="form-group">
            ${field(form.color, type="color")}
        </div>
        <div class="form-group">
            <p>Gilt als verfügbar?</p>
            <div class="form-check">
                ${form.is_available_on_workdays_day(class_="form-check-input")}
                ${form.is_available_on_workdays_day.label(class_="form-check-label")}
            </div>
            <div class="form-check">
                ${form.is_available_on_weekend_day (class_="form-check-input")}
                ${form.is_available_on_weekend_day .label(class_="form-check-label")}
            </div>
            <div class="form-check">
                ${form.is_available_on_workdays_night (class_="form-check-input")}
                ${form.is_available_on_workdays_night .label(class_="form-check-label")}
            </div>
            <div class="form-check">
                ${form.is_available_on_weekend_night (class_="form-check-input")}
                ${form.is_available_on_weekend_night .label(class_="form-check-label")}
            </div>
        </div>
        <input type="submit" value="Speichern" class="btn btn-primary" />
    </form>
</div>
