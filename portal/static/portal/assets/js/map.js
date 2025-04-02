var map; 
var region, district;

$(document).ready(function() {
    initializeMap();
    loadGeoJSONData();

// Function to initialize the map
function initializeMap() {
    if (!map) { // Only initialize if map is not already created
        map = L.map('mapdive').setView([7.099, -1.000], 7);
        
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 22,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);
    }
}
var region
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
































































































































































































































});
