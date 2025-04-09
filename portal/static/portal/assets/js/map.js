var map; 
var region, district;

$(document).ready(function() {
    initializeMap();
    loadGeoJSONData();

// Function to initialize the map
function initializeMap() {
    if (!map) { // Only initialize if map is not already created
        map = L.map('mapdive').setView([7.099, -1.000], 7);
        
        initialbasemap = L.tileLayer(
            "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", {
            maxZoom: 20,
            subdomains: ["mt0", "mt1", "mt2", "mt3"],
        }
        ).addTo(map);
    }
}



$(".tileDiv").click(function (e) {

    map.removeLayer(initialbasemap);
    $(".tileDiv").removeClass("tactive")
    $(this).addClass("tactive");
    var toolname = $(this).attr("id");

    if (toolname == "no_basemap") {
        initialbasemap = L.tileLayer("").addTo(map);
    } else if (toolname == "osm") {

        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>',
        }
        ).addTo(map);
    } else if (toolname == "sate") {
        initialbasemap = L.tileLayer(
            "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}", {
            maxZoom: 20,
            subdomains: ["mt0", "mt1", "mt2", "mt3"],
        }
        ).addTo(map);
    } else if (toolname == "topo") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", {
            maxZoom: 17,
            attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        }
        ).addTo(map);
    } else if (toolname == "basemap3") {
        initialbasemap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean_Basemap/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
            maxZoom: 13
        }).addTo(map);
    } else if (toolname == "basemap8") {
        initialbasemap = L.tileLayer(
            "https://{s}.tile.openstreetmap.se/hydda/roads_and_labels/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }
        ).addTo(map);
    } else if (toolname == "basemap6") {

        initialbasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(map);
    } else if (toolname == "basemap9") {

        initialbasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(map);
    } else if (toolname == "basemap10") {

        initialbasemap = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);
    } else if (toolname == "basemap11") {

        initialbasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
        }).addTo(map);
    } else if (toolname == "basemap12") {

        initialbasemap = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
        }).addTo(map);
    }
    initialbasemap.bringToBack();
});














var region,hf
function loadGeoJSONData() {
   // Declare your region variable globally
    const minZoom = 7; // Show labels only at zoom 12+

    const mindsitrictZoom = 10; 
    
    // Load region GeoJSON data
    $.get("/map/region", function (data) {
        region = L.geoJSON(data, {
            style: transparentStyle,
            onEachFeature: onEachFeatureRegion,
        }).addTo(map);
        
        
        // Initial label update
        updateLabels(); // Call the label update function immediately
    
        map.on('zoomend', updateLabels); // Listen for zoom changes
    });
    
    // Function to update labels based on zoom level
    function updateLabels() {
        const shouldShow = map.getZoom() >= minZoom;
        console.log(shouldShow)
        region.eachLayer(layer => {
            layer.unbindTooltip(); // Clear existing tooltip
    
            if (shouldShow) {
                // Replace 'yourAttribute' with the actual attribute name you want to display
                layer.bindTooltip(layer.feature.properties.reg_name, {
                    permanent: true,
                    direction: 'center',
                    className: 'polygon-label'
                });
            }
        });
    }

    // Load district GeoJSON data
    $.get("/map/district", function (data) {
        district = L.geoJSON(data, {
            style: regionStyle,
            onEachFeature: onEachFeatureRegion,
        });


        disstrictupdateLabels()
        map.on('zoomend', disstrictupdateLabels); // Listen for zoom changes
    });




// Function to update labels based on zoom level
function disstrictupdateLabels() {
    const shouldShow = map.getZoom() >= mindsitrictZoom;
    console.log(shouldShow)
    district.eachLayer(layer => {
        layer.unbindTooltip(); // Clear existing tooltip

        if (shouldShow) {
            // Replace 'yourAttribute' with the actual attribute name you want to display
            layer.bindTooltip(layer.feature.properties.district_2, {
                permanent: true,
                direction: 'center',
                className: 'polygon-label'
            });
        }
    });
}





// Style function based on facility_type
function getStyle(feature) {
    switch (feature.properties.facility_type) {
        case 'Health Centre':
            return { color: 'blue', radius: 8 };
        case 'CHPS Compound':
            return { color: 'green', radius: 8 };
        case 'Maternity Home':
            return { color: 'red', radius: 8 };
        case 'Polyclinic':
            return { color: 'brown', radius: 8 };
        case 'Hospital':
                return { color: 'pink', radius: 8 };
        default:
            return { color: 'gray', radius: 8 };
    }
}




  // Function to bind popups
  function hf_onEachFeature(feature, layer) {


    let labelToShow = '<table class="table table-bordered">';
    labelToShow += "<thead><tr style='background-color:#4aa;color:white;'><th colspan='2'><b><center>" + feature.properties.facility_name + "</center></b></th></tr></thead>";
    labelToShow += "<tbody><tr><td><b>Facility Type</b></td><td>" + feature.properties.facility_type + "</td></tr>";
    labelToShow += "<tr><td><b>Ownership</b></td><td>" + feature.properties.ownership + "</td></tr>";
    labelToShow += "<tr><td><b>No. of Community</b></td><td>" + feature.properties.no_of_commuities + "</td></tr>";
    labelToShow += "<tr><td><b>Name of Incharge</b></td><td>" + feature.properties.name_of_incharge + "</td></tr>";
    labelToShow += `<tr><td><b>Coordinates</b></td><td> ${feature.properties.longitude } , ${feature.properties.latitude}</td></tr>`;

    labelToShow += "</tbody></table>";

    layer.bindPopup(labelToShow);

    layer.on('click', function() {
        const coords = layer.getLatLng();
        map.flyTo(coords, 20, {
            animate: true,
            duration: 1.5
        });
    });
}

  // Load region GeoJSON data
  $.get("/map/healthfacilities", function (data) {
   // Add GeoJSON layer with style
   hf = L.geoJSON(data, {
    pointToLayer: function (feature, latlng) {
        const style = getStyle(feature);
        return L.circleMarker(latlng, {
            radius: style.radius,
            fillColor: style.color,
            color: style.color,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
    },
    onEachFeature: hf_onEachFeature // Bind popups here
})
    
 

});

































    


}






// Function to determine color based on a property
function getColor(d) {
    return d ? '#00acc9' : '#a2a2a2'; // Adjusted color based on property
}

// Function for transparent style
function transparentStyle(feature) {
    return {
        fillColor: getColor(feature.properties.pilot),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

// Function to bind popups for region features
function onEachFeatureRegion(feature, layer) {
    let labelToShow = '<table class="table table-bordered">';
    labelToShow += "<thead><tr style='background-color:#4aa;color:white;'><th colspan='2'><b><center>" + feature.properties.region + "</center></b></th></tr></thead>";
    labelToShow += "<tbody><tr><td><b>Farmer Name</b></td><td>" + feature.properties.reg_code + "</td></tr>";
    labelToShow += "<tr><td><b>Location</b></td><td>" + feature.properties.pilot + "</td></tr>";
    labelToShow += "<tr><td><b>Farm Size</b></td><td>" + feature.properties.farm_size + "</td></tr>";
    labelToShow += "</tbody></table>";

    layer.bindPopup(labelToShow);
    layer.on({
        click: regionzoomToFeaturer
    });

    layer.labelText = feature.properties.region; 
}

// Function to zoom to the feature on click
function regionzoomToFeaturer(e) {
    map.fitBounds(e.target.getBounds());
}

// Function for region style
function regionStyle(feature) {
    return {
        fillColor: getColor(feature.properties.pilot),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}


$('body').on('change', '#region_check', function() {
    
    if (!region) return; // Exit if layer not loaded
    const isChecked = $(this).is(':checked');
    
    if (isChecked) {
        map.addLayer(region);
    } else {
        map.removeLayer(region);
    }
    
    // Avoid returning true unless it's necessary for async messaging
});



$('body').on('change', '#district_check', function() {
    if (!district) return; // Exit if layer not loaded
    const isChecked = $(this).is(':checked');
    
    if (isChecked) {
        map.addLayer(district);
    } else {
        map.removeLayer(district);
    }
    
    // Avoid returning true unless it's necessary for async messaging
});






$('body').on('change', '#health-facilities', function() {
    
    if (!hf) return; // Exit if layer not loaded
    const isChecked = $(this).is(':checked');
    
    if (isChecked) {
        map.addLayer(hf);
    } else {
        map.removeLayer(hf);
    }
    
    // Avoid returning true unless it's necessary for async messaging
});



























































































































































































































});
