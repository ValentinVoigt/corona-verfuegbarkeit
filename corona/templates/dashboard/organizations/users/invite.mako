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
                Einladungen verschicken
            </li>
        </ol>
    </nav>

    <h1>Einladungen verschicken</h1>

    <p>
        Hier kannst du Einladungen an alle Mitglieder verschicken, die noch nicht eingeladen wurden.
    </p>

    <p>
        Folgende E-Mail wird an ${num} Personen verschickt:
    </p>

    <pre style="white-space: pre-wrap;" class="my-4 border-left pl-3">${subject}</pre>
    <pre style="white-space: pre-wrap;" class="my-4 border-left pl-3">${text}</pre>

    <form method="POST" action="${request.route_path('dashboard/users/invite', id=organization.id)}">
        <input class="btn btn-primary" type="submit" value="E-Mails senden" />
    </form>
</div>
