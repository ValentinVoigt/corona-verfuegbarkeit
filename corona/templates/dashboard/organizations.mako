<%inherit file="base.mako"/>

<div class="container">
    <ul>
	% for organization in request.user.organizations:
	    <li>${organization.name}</li>
	% endfor
    </ul>
</div>
