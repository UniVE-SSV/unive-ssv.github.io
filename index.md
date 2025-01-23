---
layout: home
---

<center>
	<img src="{{ site.baseurl }}/images/ssv.png" alt="{{ site.title | escape }}" style="max-height: 200px; margin-bottom: 20px;"/>
</center>

The Software and System Verification group @ Ca’ Foscari University of Venice is a research team focused on static analysis and its applications.

<style>
.column {
	float: left;
	width: 49.4%;
}

/* Clear floats after the columns */
.row:after {
	content: "";
	display: table;
	clear: both;
}
</style>

<div class="row">
	<div class="column" style="margin-right: 5px">
		<h2>Latest news</h2>
	</div>
  	<div class="column" style="margin-left: 5px">
  		<h2>Latest events</h2>
		<ul class="list-page">
{% for post in site.categories.events limit: 2 %}
			<li>
				<a href="{{ post.url }}">{{ post.title }}</a><br/>
				<small>{{ post.date | date: "%-d %B %Y" }}</small>
			</li>
{% endfor %}
		</ul>
		<a href="{{ site.baseurl }}/events/">All events ({{ site.categories.events.size }}) »</a><br><br>
	</div>
</div> 

{%- include index_people.html -%}
