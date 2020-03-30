<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@4.4.1/dist/css/bootstrap.min.css"
            integrity="sha256-L/W5Wfqfa0sdBNIKN9cG6QA5F2qx4qICmU2VgLruv9Y="
            crossorigin="anonymous"
        >
        <link
            rel="stylesheet"
            href="${request.static_url('corona:static/theme.css')}"
        />

        <title>Corona-Verfügkarbeit</title>
    </head>
    <body>
        <%include file="includes/navbar.mako" />
        % if request.session.peek_flash():
            <div class="container">
                % for message in request.session.pop_flash():
                    <div class="alert alert-success">
                        ${message}
                    </div>
                % endfor
            </div>
        % endif
        ${next.body()}
        <%include file="includes/footer.mako" />

        ## Dependencies
        <script
            src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"
            integrity="sha256-R4pqcOYV8lt7snxMQO/HSbVCFRPMdrhAFMH+vr9giYI="
            crossorigin="anonymous">
        </script>
    </body>
</html>
