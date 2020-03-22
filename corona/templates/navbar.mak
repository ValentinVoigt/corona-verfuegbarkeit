<nav class="navbar navbar-expand-lg navbar-light bg-light mb-3">
    <a class="navbar-brand" href="${request.route_path('home')}">
	Corona-Verfügkarbeit
    </a>
    <button
	class="navbar-toggler"
	type="button"
	data-toggle="collapse"
	data-target="#navbarSupportedContent"
	aria-controls="navbarSupportedContent"
	aria-expanded="false"
	aria-label="Toggle navigation"
	>
	<span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
	<ul class="navbar-nav mr-auto">
	    <li class="nav-item active">
		<a class="nav-link" href="${request.route_path('home')}">
		    Startseite
		</a>
	    </li>
	    <li class="nav-item">
		<a class="nav-link" href="${request.route_path('imprint')}">Impressum</a>
	    </li>
	</ul>
	<ul class="navbar-nav">
	    <li class="navbar-item">
		<a class="btn btn-outline-primary" href="${request.route_path('register')}">
		    Neue Organisation gründen
		</a>
	    </li>
	    <li class="navbar-item ml-0 ml-md-3 mt-2 mt-md-0">
		<a class="btn btn-primary" href="${request.route_path('login')}">Einloggen</a>
	    </li>
	</ul>
    </div>
</nav>
