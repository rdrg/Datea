	
window.olwidget.DateaEditablePointLayer = OpenLayers.Class(olwidget.BaseVectorLayer, {
    //undoStack: null,
    //undoStackPos: null,
    //undoStackLength: 1000,

    initialize: function(mapModel, mapModelField, options, centerData, boundaryData) {
        olwidget.BaseVectorLayer.prototype.initialize.apply(this, [options]);
        //this.undoStack = [];
		this.mapModel = mapModel;
        this.mapModelField = mapModelField;
        
        if (typeof(boundaryData) != "undefined") {
        	this.boundaryData = boundaryData;
        }
        if (typeof(centerData) != "undefined") {
        	this.mapCenter = new OpenLayers.LonLat( centerData.coordinates[0], centerData.coordinates[1]);
        }
    },
    
    setMap: function(map) {
        this.defaultOpts = {
            editable: true,
            geometry: 'point',
            isCollection: false
        };
        olwidget.BaseVectorLayer.prototype.setMap.apply(this, arguments);
        // force non-clustering, it doesn't make sense for editable maps.
        this.opts.cluster = false;
        this.buildControls();
        this.readWKT();
         

    },
    _addDrawFeature: function(obj_type, obj_options, controls) {
        var drawControl = new OpenLayers.Control.DrawFeature(
            this, obj_type, obj_options);
        drawControl.activate = function() {
            OpenLayers.Control.prototype.activate.apply(this, []);
            this.map.div.style.cursor = "crosshair";
        };
        drawControl.deactivate = function() {
            OpenLayers.Control.prototype.deactivate.apply(this, []);
            this.map.div.style.cursor = "auto";
        };       
        controls.push(drawControl);   
        if (!this.defaultControl) {
            this.defaultControl = drawControl;
        }
    },

    buildControls: function() {
        var controls = [];
        var context = this;

        //
        // Custom controls:
        //

        // Clear all
        controls.push(new OpenLayers.Control.Button({
            displayClass: 'olControlClearFeatures',
            trigger: function() {
                context.clearFeatures();
            },
            title: "Clear all"
        }));

        // don't add duplicate functionality from single point maps.
        if (this.opts.geometry != 'point' || this.opts.isCollection) {
            // Delete vertex
            controls.push(new olwidget.DeleteVertex(this, {
                title: "Delete vertices"
            }));
        }


        var nav = new OpenLayers.Control.Navigation({
            "title": "Move the map"
        });
        controls.push(nav);

        // Drawing control(s)
        var geometries;
        if (this.opts.geometry.constructor == Array) {
            geometries = this.opts.geometry;
        } else {
            geometries = [this.opts.geometry];
        }
        this.defaultControl = null;

        var has_point = false;
        var has_linestring = false;
        var has_polygon = false;
        for (var i = 0; i < geometries.length; i++) {
            if (geometries[i] == 'linestring')
                has_linestring = true;
            else if (geometries[i] == 'polygon')
                has_polygon = true;
            else if (geometries[i] == 'point')
                has_point = true;
        }
        if (has_polygon) {
            this._addDrawFeature(OpenLayers.Handler.Polygon, {
                'displayClass': 'olControlDrawFeaturePolygon',
                "title": "Draw polygons",
            }, controls);
        }
        if (has_linestring) {
            this._addDrawFeature(OpenLayers.Handler.Path, {
                'displayClass': 'olControlDrawFeaturePath',
                'title': "Draw lines"
            }, controls);
        }
        if (has_point) {
            this._addDrawFeature(OpenLayers.Handler.Point, {
                'displayClass': 'olControlDrawFeaturePoint',
                "title": "Draw points"
            }, controls);
        }

        // don't add duplicate functionality from single point maps.
        if (this.opts.geometry != 'point' || this.opts.isCollection) {
            // Modify feature control
            var mod = new OpenLayers.Control.ModifyFeature(this, {
                clickout: true,
                title: "Modify features"
            });
            controls.push(mod);
        }

        this.controls = controls;
    },
    clearFeatures: function() {
        this.removeFeatures(this.features);
        this.destroyFeatures();
		this.mapModel.set(this.mapModelField, null, {silent: true});
    },

    setUndoButtonStates: function() {
    	return;
    },
    
    readWKT: function() {

        // Read WKT from the text field.  We assume that the WKT uses the
        // projection given in "displayProjection", and ignore any initial
        // SRID.
        //var wkt = this.textarea.value;
        if (this.features) {
            this.removeFeatures(this.features);
        }
        //if (wkt) {
        //    var geom = olwidget.ewktToFeature(wkt);
        if (this.mapModel.attributes[this.mapModelField]) {
        	
			var gjson = new OpenLayers.Format.GeoJSON();
        	var geom = gjson.read(
        		JSON.stringify(this.mapModel.get(this.mapModelField))
        	, 'FeatureCollection');
        	
            if (!olwidget.isCollectionEmpty(geom)) {
                geom = olwidget.transformVector(geom,
                    this.map.displayProjection,
                    this.map.projection);
                if (geom.constructor == Array ||
                        geom.geometry.CLASS_NAME ===
                                "OpenLayers.Geometry.MultiLineString" ||
                        geom.geometry.CLASS_NAME ===
                                "OpenLayers.Geometry.MultiPoint" ||
                        geom.geometry.CLASS_NAME ===
                                "OpenLayers.Geometry.MultiPolygon") {
                    // extract geometries from MULTI<geom> types into
                    // individual components (keeps the vector layer flat)
                    if (geom.geometry != undefined) {
                        var geoms = [];
                        var n = geom.geometry.components.length;
                        for (var i = 0; i < n; i++) {
                            geoms.push(
                                new OpenLayers.Feature.Vector(
                                    geom.geometry.components[i])
                            );
                        }
                        this.addFeatures(geoms, {silent: true});
                    } else {
                        this.addFeatures(geom, {silent: true});
                    }
                } else {
                    this.addFeatures([geom], {silent: true});
                }
                this.numGeom = this.features.length;
            } else {
                this.numGeom = 0;
            }
        }
        
        // CREATE BOUNDARY LAYER IF NECESARY
        if (typeof(this.boundaryData) != 'undefined' && this.boundaryData != null) {

        	var gjson = new OpenLayers.Format.GeoJSON();
        	var collection = gjson.read(
        		JSON.stringify(this.boundaryData)
        	, 'FeatureCollection');
        	
        	this.boundaryPolygon = olwidget.transformVector(collection[0],
                    this.map.displayProjection,
                    this.map.projection);
                    
            this.boundaryPolygon.style = {
            	'strokeWidth': 3,
    			'strokeOpacity': 1,
    			'strokeColor': '#ecff00',
    			'fillOpacity': 0,
            };
      
        	this.boundaryLayer = new OpenLayers.Layer.Vector("Boundary Layer");
        	this.boundaryLayer.addFeatures(this.boundaryPolygon);
			this.map.addLayer(this.boundaryLayer);
			       	
        }
         
    },
    // Callback for openlayers "featureadded"
    addWKT: function(event) {

        // This function will sync the contents of the `vector` layer with the
        // WKT in the text field.
        if (typeof(this.popup) != 'undefined') {
        	this.map.removePopup(this.popup);
        	this.popup.destroy();
        	delete this.popup;
        }
        
        // CHEQUEAR SI ESTA DENTRO
    	var point = new OpenLayers.Geometry.Point(event.feature.geometry.x, event.feature.geometry.y);
    	if (typeof(this.boundaryPolygon) != 'undefined') {
    		if (!this.boundaryPolygon.geometry.containsPoint(point)){
    			this.popup = new OpenLayers.Popup.FramedCloud("Aviso",
                        	event.feature.geometry.getBounds().getCenterLonLat(),
                            null,
                            'Fuera de la zona permitida!',
                            null, false);
				this.map.addPopup(this.popup);
				
				this.mapModel.set(this.mapModelField, null, {silent: true});
				this.destroyFeatures();
				return;
    		}
	    }
	    
        var center = new OpenLayers.LonLat( event.feature.geometry.x, event.feature.geometry.y);
        this.map.panTo(center);
        
        if (this.opts.isCollection) {
            this.featureToTextarea(this.features);
        } else {
            // Make sure to remove any previously added features.
            if (this.features.length > 1) {
                var old_feats = [this.features[0]];
                this.removeFeatures(old_feats);
                this.destroyFeatures(old_feats);
            }
            this.featureToTextarea(event.feature);
        }
    },
    // Callback for openlayers "featuremodified"
    modifyWKT: function(event) {
        if (this.opts.isCollection){
            // OpenLayers adds points around the modified feature that we want
            // to strip.  So only take the features up to "numGeom", the number
            // of features counted when we last added.
            var feat = [];
            for (var i = 0; i < Math.min(this.numGeom, this.features.length); i++) {
                feat.push(this.features[i].clone());
            }
            this.featureToTextarea(feat);
        } else {
            if (event.feature) {
                this.featureToTextarea(event.feature);
            } else {
                this.mapModel.set(this.mapModelField, null, {silent: true});
            }
        }
        //this.addUndoState();
    },
    featureToTextarea: function(feature) {
    	
        if (this.opts.isCollection) {
            this.numGeom = feature.length;
        } else {
            this.numGeom = 1;
        }
        feature = olwidget.transformVector(feature,
                this.map.projection, this.map.displayProjection);
        if (this.opts.isCollection) {
            // Convert to multi-geometry types if we are a collection.  Passing
            // arrays to the WKT formatter results in a "GEOMETRYCOLLECTION"
            // type, but if we have only one geometry, we should use a
            // "MULTI<geometry>" type.
            if (this.opts.geometry.constructor != Array) {
                var geoms = [];
                for (var i = 0; i < feature.length; i++) {
                    geoms.push(feature[i].geometry);
                }
                var GeoClass = olwidget.multiGeometryClasses[this.opts.geometry];
                feature = new OpenLayers.Feature.Vector(new GeoClass(geoms));
            }
        }
        //this.textarea.value = olwidget.featureToEWKT(
        //    feature, this.map.displayProjection);  
        var gjson = new OpenLayers.Format.GeoJSON();
    	this.mapModel.set(
    		this.mapModelField, 
    		jQuery.parseJSON(gjson.write(feature.geometry)), 
    		{silent: true}
    	);
    },
    cancel: function() {
        this.mapModel.set(this.mapModelField, null, {silent: true});
		this.destroyFeatures();
		this.map.zoomToExtent(this.boundaryBounds);
		this.map.zoomTo(Math.min(this.map.getZoom(), this.map.opts.zoomToDataExtentMin));
    },
    refresh_form: function (textareaId) {
    	this.destroyFeatures();
    	this.readWKT();
    },
    CLASS_NAME: "olwidget.DateaEditablePointLayer"
});


window.Datea.CreateEditablePointMap = function (mapDivId, model, modelField, centerData, boundaryData) {
	
	var $mapDiv = $('#'+mapDivId); 
	
	var map = new olwidget.Map(mapDivId, [
	        new olwidget.DateaEditablePointLayer(model, modelField, {"name": "Posición"}, centerData, boundaryData)
	    ], 
	    { "layers": ['google.streets', 'osm.mapnik'],
	      "mapDivStyle": {'width': $mapDiv.css('width'), 'height': $mapDiv.css('height')},
	      "overlayStyle": {
	      	"externalGraphic": "/static/openlayers-dev/img/marker.png", 
	      	"graphicHeight": 21, 
	      	"graphicWidth": 16, 
	      	"graphicOpacity": 1
	      },
	      'mapOptions': {
	      	"controls" : ['LayerSwitcher', 'Navigation', 'PanZoom', 'Attribution'],
	      	'numZoomLevels': 5,
	      }
	    }
	);
	
	for (var i = 0; i < map.controls.length; i++) {
		if (map.controls[i] && map.controls[i].CLASS_NAME =="olwidget.EditableLayerSwitcher") {
	    	map.controls[i].setEditing(map.vectorLayers[0]);
	    	break;
		}
	}
	
	var pointLayer = map.vectorLayers[0];
	
	if (pointLayer.features.length > 0) {
		map.zoomToExtent(pointLayer.features[0].geometry.getBounds());
		map.zoomTo(Math.min(map.getZoom(), map.opts.zoomToDataExtentMin));
		
	}else if (pointLayer.boundaryPolygon){
		map.zoomToExtent(pointLayer.boundaryPolygon.geometry.getBounds());
		map.zoomTo(Math.min(map.getZoom(), map.opts.zoomToDataExtentMin));
	}else{
	    map.panTo(pointLayer.mapCenter.transform(
	        		map.displayProjection,
	                map.projection
	              ));
	    map.zoomTo(12);
	}
	
	return {'map':map, 'layer': pointLayer};
}




