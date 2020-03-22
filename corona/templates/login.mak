<%inherit file="layout.mak"/>

<form class="form-signin">
    <h1 class="h3 mb-3 font-weight-normal">Einloggen</h1>
    <label for="inputEmail" class="sr-only">E-Mail-Adresse</label>
    <input type="email" id="inputEmail" class="form-control" placeholder="E-Mail-Adresse" required autofocus>

    <label for="inputPassword" class="sr-only">Passwort</label>
    <input type="password" id="inputPassword" class="form-control" placeholder="Passwort" required>

    <div class="checkbox mb-3">
	<label>
	    <input type="checkbox" value="remember-me"> Eingeloggt bleiben
	</label>
    </div>
    <button class="btn btn-lg btn-primary btn-block" type="submit">
	Einloggen
    </button>
    <p class="mt-3 mb-0">
	<a href="#">
	    Passwort vergessen?
	</a>
    </p>
</form>
