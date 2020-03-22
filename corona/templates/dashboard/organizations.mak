<%inherit file="base.mak"/>

<ul>
    % for organization in request.user.organizations:
	<li>${organization.name}</li>
    % endfor
</ul>
