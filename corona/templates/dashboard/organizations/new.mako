<%inherit file="../base.mako"/>
<%namespace file="../../functions/field.mako" import="field"/>

<div class="container">
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <a href="${request.route_path('dashboard/organizations')}">
                    Organisationen
                </a>
            </li>
            <li class="breadcrumb-item active" aria-current="page">
                <a href="${request.route_path('dashboard/organizations/show', id=organization.id)}">
                    ${organization.name}
                </a>
            </li>
            <li class="breadcrumb-item active" aria-current="page">
                Neue Organisation
            </li>
        </ol>
    </nav>

    <h2>Organisation anlegen</h2>

    <form method="POST" action="${request.route_path('dashboard/organizations/new', id=organization.id)}">
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
        <input type="submit" value="Speichern" class="btn btn-primary" />
    </form>
</div>
