<%inherit file="layout.mak"/>

<h1>Neue Organisation erstellen</h1>

<p>
    Hier kannst du dich registrieren, um deine erste Organisation anzulegen.
    Von dort aus kannst du dann Mitarbeiter hinzufügen.
</p>

<p>
    Wir fragen nur nach Daten, von denen wir glauben, dass sie dir helfen. Wir
    geben grundsätzlich keine Daten an andere weiter.
</p>

<form>
    <h2>Persönliche Angaben</h2>
    <div class="form-row">
	<div class="form-group col-md-6">
	    <label for="inputFirstName">Vorname</label>
	    <input type="firstName" class="form-control" id="inputFirstName" placeholder="Vorname">
	</div>
	<div class="form-group col-md-6">
	    <label for="inputLastName">Nachname</label>
	    <input type="lastName" class="form-control" id="inputLastName" placeholder="Nachname">
	</div>
    </div>
    <div class="form-group">
	<label for="inputEmail4">E-Mail-Adresse</label>
	<input type="email" class="form-control" id="inputEmail4" placeholder="E-Mail-Adresse">
    </div>
    <div class="form-group">
	<label for="inputPassword4">Passwort</label>
	<input type="password" class="form-control" id="inputPassword4" placeholder="Passwort">
    </div>

    <h2>Angaben zur Organisation</h2>
    <div class="form-group">
	<label for="inputAddress">Address</label>
	<input type="text" class="form-control" id="inputAddress" placeholder="1234 Main St">
    </div>
    <div class="form-group">
	<label for="inputAddress2">Address 2</label>
	<input type="text" class="form-control" id="inputAddress2" placeholder="Apartment, studio, or floor">
    </div>
    <div class="form-row">
	<div class="form-group col-md-6">
	    <label for="inputCity">City</label>
	    <input type="text" class="form-control" id="inputCity">
	</div>
	<div class="form-group col-md-4">
	    <label for="inputState">State</label>
	    <select id="inputState" class="form-control">
		<option selected>Choose...</option>
		<option>...</option>
	    </select>
	</div>
	<div class="form-group col-md-2">
	    <label for="inputZip">Zip</label>
	    <input type="text" class="form-control" id="inputZip">
	</div>
    </div>
    <div class="form-group">
	<div class="form-check">
	    <input class="form-check-input" type="checkbox" id="gridCheck">
	    <label class="form-check-label" for="gridCheck">
		Check me out
	    </label>
	</div>
    </div>
    <button type="submit" class="btn btn-primary">Sign in</button>
</form>
