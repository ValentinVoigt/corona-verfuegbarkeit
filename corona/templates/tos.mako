<%inherit file="layout.mako"/>

<div class="container py-5">
    <h1 class="text-center">Willkommen bei Corona-Verfuegbarkeit.de</h1>

    <div style="max-width:600px; margin:auto;">
        <p>
            Für die Nutzung von Corona-Verfuegbarkeit.de ist deine Einwilligung in die Nutzung
            deiner personenbezogenen Daten erforderlich. Weitere Informationen findest du in
            unserer <a href="${request.route_path('imprint')}">Datenschutzerklärung</a>.
        </p>

        <form action="${request.route_path('dashboard/tos')}" method="POST">
            <p class="text-right">
                <input type="hidden" name="agrees" value="yes" />
                <input
                    type="submit"
                    value="Ich willige ein (fortfahren) »"
                    class="btn btn-primary btn-lg"
                />
            </p>
        </form>
    </div>
</div>
