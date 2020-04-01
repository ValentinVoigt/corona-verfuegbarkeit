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
                Verfügbarkeit
            </li>
        </ol>
    </nav>

    <h1>${organization.display_name}: Verfügbarkeit</h1>

    <canvas id="myChart" width="400" height="200"></canvas>
    <%block name="script">
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, ${data|n});
    </%block>
</div>
