var map; 
var region, district;

$(document).ready(function() {
    initializeMap();
    loadGeoJSONData();
});

// Function to initialize the map
function initializeMap() {
    if (!map) { // Only initialize if map is not already created
        map = L.map('mapdive').setView([7.099, -1.000], 7);
        
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    }
}

// Function to load GeoJSON data
function loadGeoJSONData() {
    // Load region GeoJSON data
    $.get("/map/region", function (data) {
        region = L.geoJSON(data, {
            style: transparentStyle,
            onEachFeature: onEachFeatureRegion,
        }).addTo(map);
        region.bringToBack();
    });

    // Load district GeoJSON data
    $.get("/map/district", function (data) {
        district = L.geoJSON(data, {
            style: regionStyle,
            onEachFeature: onEachFeatureRegion,
        });
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
    labelToShow += "<thead><tr style='background-color:#4aa;color:white;'><th colspan='2'><b><center>" + feature.properties.farm_reference + "</center></b></th></tr></thead>";
    labelToShow += "<tbody><tr><td><b>Farmer Name</b></td><td>" + feature.properties.farmername + "</td></tr>";
    labelToShow += "<tr><td><b>Location</b></td><td>" + feature.properties.location + "</td></tr>";
    labelToShow += "<tr><td><b>Farm Size</b></td><td>" + feature.properties.farm_size + "</td></tr>";
    labelToShow += "</tbody></table>";

    layer.bindPopup(labelToShow);
    layer.on({
        click: regionzoomToFeaturer
    });
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

// Event listener for region checkbox
$('body').on('change', '#region_check', function() {
    alert("ff")
  
    $(this).is(':checked') ? map.addLayer(region) : map.removeLayer(region);
});

// Event listener for district checkbox
$('body').on('change', '#district_check', function() {
    if (!district) return; // Exit if layer not loaded
    $(this).is(':checked') ? map.addLayer(district) : map.removeLayer(district);
});


