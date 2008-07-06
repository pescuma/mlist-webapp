function gmaps_isIE()
{
	return /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent);
}

function gmaps_trim(txt)
{
	return txt.replace(/^\s+|\s+$/g, '');
}

function gmaps_failed(el, address, text)
{
	if (el.innerText)
		el.innerText = text;
	else
		el.textContent = text;
	el.style.width = '';
	el.style.height = '';
	el.style.display = 'inline';
}

function gmaps_addMarkerListener(marker, text)
{
	GEvent.addListener(marker, "click", function() {
		marker.openInfoWindowHtml(text);
	});
}

function gmaps_addMarker(map, point, text, showOnStart)
{
	text = gmaps_trim(text);
	
	var marker = new GMarker(point, { title: text } );
	map.addOverlay(marker);
	
	if (showOnStart)
		marker.openInfoWindowHtml(text);
	
	gmaps_addMarkerListener(marker, text);
}

function gmaps_addAddress(map, el, hasMoreThanOne, address, text, onError)
{
	var points = address.split(/-&gt;/i);
	if (points.length > 1)
	{
		var texts = text.split(/-&gt;/i);
		
		var directions = new GDirections(map);
		GEvent.addListener(directions, "addoverlay", function() {
			for(var i = 0; i < directions.getNumGeocodes(); i++)
			{
				var title = '';
				if (i < texts.length)
					title = gmaps_trim(texts[i]);
				if (title == '' && i < points.length)
					title = points[i];
				
				gmaps_addMarkerListener(directions.getMarker(i), title);
			}
		});
		GEvent.addListener(directions, "error", function() {
			onError();
		});
		directions.loadFromWaypoints(points);
	}
	else
	{
		if (text == '')
			text = address;
		
		var geocoder = new GClientGeocoder();
		geocoder.getLatLng(
			address,
			function(point) {
				if (!point) {
					onError();
				} else {
					map.setCenter(point, 13);
					gmaps_addMarker(map, point, text, !hasMoreThanOne);
				}
			}
		);
	}
}

function gmaps_showAddress(el, address, text)
{
	var map = new GMap2(el);
	map.addControl(new GMapTypeControl());
	map.addControl(new GLargeMapControl());
	
	var addresses = address.split('|');
	var texts = text.split('|');
	for(var i = 0; i < addresses.length; i++)
		gmaps_addAddress(map, el, addresses.length > 1, addresses[i], (i >= texts.length ? '' : gmaps_trim(texts[i])), function() {
			gmaps_failed(el, address, text);
		});
}

function gmaps_addGPS(map, el, hasMoreThanOne, gps, text, onError)
{
	gps = gps.split(',');
	var la, lo, z;
	if (gps.length >= 1)
		la = gmaps_trim(gps[0]);
	if (gps.length >= 2)
		lo = gmaps_trim(gps[1]);
	if (gps.length >= 3)
		z = gmaps_trim(gps[2]);
	else
		z = 13;
	
	if (!la || !lo)
	{
		onError();
	}
	else
	{
		var point = new GLatLng(la, lo);
		map.setCenter(point, parseInt(z));
		if (text != '')
			gmaps_addMarker(map, point, text, !hasMoreThanOne);
	}
}

function gmaps_showGPS(el, gps, text)
{
	var map = new GMap2(el);
	map.addControl(new GMapTypeControl());
	map.addControl(new GLargeMapControl());

	var gpses = gps.split('|');
	var texts = text.split('|');
	for(var i = 0; i < gpses.length; i++)
		gmaps_addGPS(map, el, gpses.length > 1, gpses[i], (i >= texts.length ? '' : gmaps_trim(texts[i])), function() {
			gmaps_failed(el, gps, text);
		});
}

function gmaps_load()
{
	if (GBrowserIsCompatible())
	{
		var maps;
		if (gmaps_isIE())
		{
			var divs = document.getElementsByTagName('div');
			maps = [];
			for(var i=0; i<divs.length; i++)
				if (divs[i].getAttribute('name') == 'gmap')
					maps.push(divs[i]);
		}
		else
		{
			maps = document.getElementsByName('gmap');
		}
		
		for(var i = 0; i < maps.length; i++)
		{
			var el = maps[i];
			var data = el.innerHTML;
			if (!data)
				continue;
			
			data = data.split(/<br *\/?>/i);
			var address = '', gps = '', text = '';
			for(var j = 0; j < data.length; j++)
			{
				var tmp = data[j].replace(/^\s+|\s+$/g, '');
				if (tmp.length <= 0)
					continue;
				
				if (tmp.length > 6 && tmp.substring(0, 5).toLowerCase() == 'text:')
					text = tmp.substring(5).replace(/^\s+|\s+$/g, '');
				else if (tmp.length > 5 && tmp.substring(0, 4).toLowerCase() == 'gps:')
					gps = tmp.substring(4).replace(/^\s+|\s+$/g, '');
				else
					address = tmp;
			}
			
			if (gps != '')
				gmaps_showGPS(el, gps, text);
			else if (address != '')
				gmaps_showAddress(el, address, text);
		}
	}
}

function gmaps_unload() {
	GUnload();
}
