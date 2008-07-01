function gmaps_isIE()
{
	return /msie/i.test(navigator.userAgent) && !/opera/i.test(navigator.userAgent);
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

function gmaps_showAddress(el, address, text)
{
	if (text == '')
		text = address;
	
	var map = new GMap2(el);
	map.addControl(new GMapTypeControl());
	map.addControl(new GLargeMapControl());
	
	var geocoder = new GClientGeocoder();
	geocoder.getLatLng(
		address,
		function(point) {
			if (!point) {
				gmaps_failed(el, address, text);
			} else {
				map.setCenter(point, 13);
				var marker = new GMarker(point, { title: text } );
				map.addOverlay(marker);
				marker.openInfoWindowHtml(text);
			}
		}
	);
}

function gmaps_showGPS(el, gps, text)
{
	var map = new GMap2(el);
	map.addControl(new GMapTypeControl());
	map.addControl(new GLargeMapControl());
	
	gps = gps.split(',');
	var la, lo, z;
	if (gps.length >= 1)
		la = gps[0].replace(/^\s+|\s+$/g, '');
	if (gps.length >= 2)
		lo = gps[1].replace(/^\s+|\s+$/g, '');
	if (gps.length >= 3)
		z = gps[2].replace(/^\s+|\s+$/g, '');
	else
		z = 13;
	
	if (!la || !lo)
	{
		gmaps_failed(el, address, text);
	}
	else
	{
		var point = new GLatLng(la, lo);
		map.setCenter(point, parseInt(z));
		if (text != '')
		{
			var marker = new GMarker(point, { title: text } );
			map.addOverlay(marker);
			marker.openInfoWindowHtml(text);
		}
	}
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
