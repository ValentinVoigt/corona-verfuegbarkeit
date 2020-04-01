<%inherit file="../base.mako"/>
<%namespace file="../../functions/field.mako" import="field"/>
<%! from datetime import date, timedelta %>
<%! ONE_DAY = timedelta(days=1) %>

<%def name="day_link(mydate, pre=None, post=None)">
    <a class="page-link" href="${request.route_path('dashboard/organizations/availability', id=request.context.id, date=mydate)}">
        ${pre + " " if pre else ""}${mydate.strftime('%d.%m.%Y')}${" " + post if post else ""}
    </a>
</%def>

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

    <nav>
        <ul class="pagination justify-content-center">
            <li class="page-item">
                ${day_link(mydate-ONE_DAY, pre="«")}
            </li>
            <li class="page-item active" aria-current="page">
                ${day_link(mydate)}
            </li>
            <li class="page-item">
                ${day_link(mydate+ONE_DAY, post="»")}
            </li>
        </ul>
    </nav>


    <canvas id="myChart" width="400" height="200"></canvas>
    <%block name="script">
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, ${data|n});
    </%block>
</div>
