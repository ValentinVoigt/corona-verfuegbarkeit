<%inherit file="../base.mako"/>

<%def name="show_tree(base, level)">
    <li class="list-group-item">
	% for i in range(level):
	    <span class="mx-2"></span>
	% endfor
	<a href="${request.route_path('dashboard/organizations/show', id=base.id)}">
	    ${base.name}
	</a>
    </li>
    % for sub in base.children:
	${show_tree(sub, level+1)}
    % endfor
</%def>

<div class="container">
    <nav aria-label="breadcrumb">
	<ol class="breadcrumb">
	    <li class="breadcrumb-item active">Organisationen</li>
	</ol>
    </nav>

    <h1>Meine Organisationen</h1>

    <ul class="list-group">
	% for organization in organizations:
	    ${show_tree(organization, 0)}
	% endfor
    </ul>
</div>
