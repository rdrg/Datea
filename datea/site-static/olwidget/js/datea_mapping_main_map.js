
Datea.map_functions = {};
	
Datea.map_functions.getClusterSize = function (feature) {
	var n = feature.attributes.count;
    var pix;
    if (n == 1) {
        pix = 12;
    } else if (n <= 5) {
        pix = 16;
    } else if (n <= 25) {
        pix = 20;
    } else if (n <= 50) {
        pix = 24;
    } else {
        pix = 28;
    }
    return pix * 2;
}

olwidget.DateaMainMapItemLayer = OpenLayers.Class(olwidget.BaseVectorLayer, {
    
    initialize: function(mappingModel, mapItems, options) {
        olwidget.BaseVectorLayer.prototype.initialize.apply(this, [options]);
        this.mappingModel = mappingModel,
        this.mapItems = mapItems,
        this.categories = {}
        var self = this;
        _.each(this.mappingModel.get('item_categories'), function(cat){
        	self.categories[cat.id] = cat;
        });
    },
    
    setMap: function(map) {
        if (this.opts.cluster || map.opts.cluster) {
            // Use a different default style if we are clustering.
            var clusterStyle = {
                //pointRadius: "${radius}",
                //strokeWidth: "${width}",
                //fillColor: "${color}",
                //strokeColor: "${color}",
                //label: "${label}",
                externalGraphic: "${external}",
                graphicWidth: "${getClusterWidth}",
                graphicHeight: "${getClusterHeight}",
                strokeWidth: 0,
                fillOpacity: "${getOpacity}",
                
                labelSelect: true,
                fontSize: "11px",
                fontFamily: "Helvetica, sans-serif",
                fontColor: "#ffffff"
            };
            this.defaultOpts.overlayStyle = olwidget.deepJoinOptions(
                {}, clusterStyle);
            this.defaultOpts.selectOverlayStyle = olwidget.deepJoinOptions(
                {}, clusterStyle);
            this.defaultOpts.overlayStyleContext = {
                width: function(feature) {
                    return (feature.cluster) ? 2 : 1;
                },
                radius: function(feature) {
                    var n = feature.attributes.count;
                    var pix;
                    if (n == 1) {
                        pix = 6;
                    } else if (n <= 5) {
                        pix = 8;
                    } else if (n <= 25) {
                        pix = 10;
                    } else if (n <= 50) {
                        pix = 12;
                    } else {
                        pix = 14;
                    }
                    return pix;
                },
                label: function(feature) {
                    if (feature.cluster && feature.cluster.length > 1) {
                        return feature.cluster.length;
                    }
                    return '';
                },
                color: function (feature) {
                	if (feature.cluster) {
                		if(feature.cluster.length == 1) {
	                		return feature.cluster[0].category.color;
	                	}else{
	                		return '#cccccc';
	                	}
                	}else{
	                	return feature.cluster[0].category.color;
                	}
                },
                external: function (feature) {
                	
                	if (feature.cluster && feature.cluster.length == 1){
                		if (!feature.cluster[0].category.marker_image) {
                			var size = parseInt(Datea.map_functions.getClusterSize(feature) / 2);
                			var color = feature.cluster[0].category.color.replace('#','');
                			return '/png/svgcircle?radius='+size+'&color='+color;
                		}else{
                			return feature.cluster[0].category.marker_image.image;
                		}
                	
                	}else{
                		var size = parseInt(Datea.map_functions.getClusterSize(feature) / 2);
                		var count_cat = {}
                		for (i in feature.cluster) {
                			var color = feature.cluster[i].category.color;
                			if (typeof(count_cat[color]) == 'undefined') {
                				count_cat[color] = 1;
                			}else{
                				count_cat[color]++;
                			}
                		}
                		var values = [];
                		var colors = [];
                		for (var color in count_cat) {
                			values.push(count_cat[color]);
                			colors.push(color.replace('#',''));
                		}
                		var url = '/png/piecluster?values='+values.join(',')+'&colors='+colors.join(',')+'&radius='+size;
                		return url;
                	}
                },
                getSize: function (feature) {
                	return Datea.map_functions.getClusterSize(feature);
                },
                getClusterWidth: function(feature) {
                	if (feature.cluster && feature.cluster.length == 1) {
                		if (!feature.cluster[0].category.marker_image) {
                			return Datea.map_functions.getClusterSize(feature);
                		}else{
                			feature.cluster[0].category.marker_image.width;
                		}
                	}else if (feature.cluster){
                		return Datea.map_functions.getClusterSize(feature);
                	}else{
                		if (!feature.cluster[0].category.marker_image) {
                			return Datea.map_functions.getClusterSize(feature);
                		}else{
                			return feature.cluster[0].category.marker_image.width;
                		}
                	}
                },
                getClusterHeight: function (feature) {
                	if (feature.cluster && feature.cluster.length == 1) {
                		if (!feature.cluster[0].category.marker_image) {
                			return Datea.map_functions.getClusterSize(feature);
                		}else{
                			feature.cluster[0].category.marker_image.height;
                		}
                	}else if (feature.cluster){
                		return Datea.map_functions.getClusterSize(feature);
                	}else{
                		if (!feature.cluster[0].category.marker_image) {
                			return Datea.map_functions.getClusterSize(feature);
                		}else{
                			feature.cluster[0].category.marker_image.height;
                		}
                	}
                },
                getOpacity: function (feature) {
                	if (feature.cluster && feature.cluster.length > 1) {
                		return 1;
                	}else{
                		return 0.75;
                	}
                }
                
            };
        }
        // Merge our options with the map's.
        olwidget.BaseVectorLayer.prototype.setMap.apply(this, arguments);

        // Add cluster strategy if needed.
        if (this.opts.cluster === true) {
            if (!this.strategies) {
                this.strategies = [];
            }
            var cluster = new OpenLayers.Strategy.Cluster();
            cluster.distance = 30;
            cluster.setLayer(this);
            this.strategies.push(cluster);
            cluster.activate();
        }
    },
    afterAdd: function() {
        olwidget.BaseVectorLayer.prototype.afterAdd.apply(this);
        var gjson = new OpenLayers.Format.GeoJSON();
        var features = [];
        
        for (var i in this.mapItems.models) {
        	var map_item = this.mapItems.models[i];
        	
        	if (map_item.get('position')) {
        		
        		var feature = gjson.read(
        			JSON.stringify(map_item.get('position'))
        		, 'FeatureCollection');

	            feature = olwidget.transformVector(feature,
	                this.map.displayProjection, this.map.projection);
	
	            if (feature.constructor != Array) {
	                feature = [feature];
	            }
	

	            for (var k = 0; k < feature.length; k++) {
                    feature[k].attributes = {};
                    feature[k].item_id = map_item.get('id');
                    feature[k].category = this.categories[map_item.get('category_id')];
	                 
	                features.push(feature[k]);
	            }
            }
        }
        this.addFeatures(features);
    },
    reload: function () {
    	this.destroyFeatures();
    	this.afterAdd();
    },
    
    open_popup: function (item_id, do_zoom) {
		
		if ($('#map-item-popup-'+item_id).size() > 0) return;
		
		this.map.selectControl.unselectAll();
		
		// find our feature -> check clusters
		var found = this.find_item_feature(item_id);
		if (do_zoom) {
			this.map.zoomToExtent(found.feature.geometry.getBounds());
			this.map.zoomTo(Math.min(this.map.getZoom(), this.map.opts.zoomToDataExtentMin));
			var found = this.find_item_feature(item_id);
		}
		
		this.map.selectControl.select(found.feature);
		if (found.page != 0) {
			this.map.popups[0].page = found.page;
			this.map.popups[0].setContentHTML();	
		}
	},
	
	find_item_feature: function(item_id) {
		var found_feat = false;
		var page = 0;
		for (var level1 in this.features) {
			var feat = this.features[level1];
			if (feat.cluster) {
				for (var level2 in feat.cluster) {
					if (feat.cluster[level2].item_id == item_id) {
						found_feat = feat;
						page = parseInt(level2);
						break;
					}
				}
			}else{
				if (feat.item_id && feat.item_id == item_id) {
					found_feat = feat;
				}
			}
			if (found_feat != false) break;
		}
		return {feature: found_feat, page: page};
	},
    
    CLASS_NAME: "Datea.map_functions.DateaMainMapItemLayer"
});


/*
 * The Map.  Extends an OpenLayers map.
 */
olwidget.DateaMainMap = OpenLayers.Class(OpenLayers.Map, {
    initialize: function(mapDivID, vectorLayers, options) {
        this.vectorLayers = vectorLayers;
        this.opts = this.initOptions(options);
        this.initMap(mapDivID, this.opts);
    },
    /*
     * Extend the passed in options with defaults, and create unserialized
     * objects for serialized options (such as projections).
     */
    initOptions: function(options) {
        var defaults = {
            // Constructor options
            mapOptions: {
                units: 'm',
                projection: "EPSG:900913",
                displayProjection: "EPSG:4326",
                maxExtent: [-20037508.34, -20037508.34, 20037508.34, 20037508.34],
                controls: ['LayerSwitcher', 'Navigation', 'PanZoom', 'Attribution']
            },
            // Map div stuff
            mapDivClass: '',
            mapDivStyle: {
                width: '460px',
                height: '500px'
            },
            layers: ['osm.mapnik'],
            defaultLon: 0,
            defaultLat: 0,
            defaultZoom: 4,
            zoomToDataExtent: true,
            zoomToDataExtentMin: 17
        };

        // deep copy all options into "defaults".
        var opts = olwidget.deepJoinOptions(defaults, options);

        // construct objects for serialized options
        var me = opts.mapOptions.maxExtent;
        opts.mapOptions.maxExtent = new OpenLayers.Bounds(me[0], me[1], me[2], me[3]);
        if (opts.mapOptions.restrictedExtent) {
            var re = opts.mapOptions.restrictedExtent;
            opts.mapOptions.restrictedExtent = new OpenLayers.Bounds(re[0], re[1], re[2], re[3]);
        }
        opts.mapOptions.projection = new OpenLayers.Projection(opts.mapOptions.projection);
        opts.mapOptions.displayProjection = new OpenLayers.Projection(
            opts.mapOptions.displayProjection);

        for (var i = 0; i < opts.mapOptions.controls.length; i++) {
            opts.mapOptions.controls[i] = new OpenLayers.Control[opts.mapOptions.controls[i]]();
        }
        return opts;
    },
    /*
     * Initialize the OpenLayers Map and add base layers
     */
    initMap: function(mapDivId, opts) {
        var mapDiv = document.getElementById(mapDivId);
        OpenLayers.Util.extend(mapDiv.style, opts.mapDivStyle);
        if (opts.mapDivClass) {
            mapDiv.className = opts.mapDivClass;
        }

        // Must have explicitly specified position for popups to work properly.
        if (!mapDiv.style.position) {
            mapDiv.style.position = 'relative';
        }

        var layers = [];
        for (var i = 0; i < opts.layers.length; i++) {
            var parts = opts.layers[i].split(".");
            layers.push(olwidget[parts[0]].map(parts[1]));

            // workaround for problems with Microsoft layers and vector layer
            // drift (see http://openlayers.com/dev/examples/ve-novibrate.html)
            if (parts[0] == "ve") {
                if (opts.mapOptions.panMethod === undefined) {
                    opts.mapOptions.panMethod = OpenLayers.Easing.Linear.easeOut;
                }
            }
        }

        // Map super constructor
        OpenLayers.Map.prototype.initialize.apply(this, [mapDiv.id, opts.mapOptions]);

        if (this.vectorLayers) {
            for (var i = 0; i < this.vectorLayers.length; i++) {
                layers.push(this.vectorLayers[i]);
            }
        } else {
            this.vectorLayers = [];
        }
        if (layers.length > 0) {
            this.addLayers(layers);
            if (this.baseLayer) {
                // Only initCenter if we have base layers -- otherwise, user is
                // responsible for adding and then calling initCenter.
                this.initCenter();
            }
        }
        this.selectControl = new OpenLayers.Control.SelectFeature(
            this.vectorLayers);
        this.selectControl.events.on({
            featurehighlighted: this.featureHighlighted,
            featureunhighlighted: this.featureUnhighlighted,
            scope: this
        });
        // Allow dragging when over features.
        this.selectControl.handlers.feature.stopDown = false;
        this.events.on({
            zoomend: this.zoomEnd,
            scope: this
        });
        this.addControl(this.selectControl);
        this.selectControl.activate();
        this.addControl(new olwidget.EditableLayerSwitcher());
    },
    initCenter: function() {
        if (this.opts.zoomToDataExtent) {
            var extent = new OpenLayers.Bounds();
            for (var i = 0; i < this.vectorLayers.length; i++) {
                var vl = this.vectorLayers[i];
                if (vl.opts.cluster) {
                    for (var j = 0; j < vl.features.length; j++) {
                        for (var k = 0; k < vl.features[j].cluster.length; k++) {
                            extent.extend(vl.features[j].cluster[k].geometry.getBounds());
                        }
                    }
                } else {
                    extent.extend(vl.getDataExtent());
                }
            }
            if (!extent.equals(new OpenLayers.Bounds())) {
                this.zoomToExtent(extent);
                this.zoomTo(Math.min(this.getZoom(), this.opts.zoomToDataExtentMin));
                return;
            }
        }
        // zoom to boundary if given
       	if (this.opts.defaultBoundary) {
       		var gjson = new OpenLayers.Format.GeoJSON();
        	var collection = gjson.read(
        		JSON.stringify(this.opts.defaultBoundary)
        	, 'FeatureCollection');
        	
        	var boundaryPolygon = olwidget.transformVector(collection[0],
                    this.displayProjection,
                    this.projection);
            this.zoomToExtent(boundaryPolygon.geometry.getBounds());
			this.zoomTo(Math.min(this.getZoom(), this.opts.zoomToDataExtentMin));
                    
       	}
        // zoomToDataExtent == false, or there is no data on any layer
        var center = new OpenLayers.LonLat(
            this.opts.defaultLon, this.opts.defaultLat);
        center = center.transform(this.displayProjection, this.projection);
        this.setCenter(center, this.opts.defaultZoom);
    },
    featureHighlighted: function(evt) {
        this.createPopup(evt);
    },
    featureUnhighlighted: function(evt) {
        this.deleteAllPopups();
    },
    zoomEnd: function(evt) {
        this.deleteAllPopups();
    },

    /**
     * Override parent to allow placement of popups outside viewport
     */
    addPopup: function(popup, exclusive) {
        if (exclusive) {
            //remove all other popups from screen
            for (var i = this.popups.length - 1; i >= 0; --i) {
                this.removePopup(this.popups[i]);
            }
        }

        popup.map = this;
        this.popups.push(popup);
        var popupDiv = popup.draw();
        if (popupDiv) {
            popupDiv.style.zIndex = this.Z_INDEX_BASE.Popup +
                                    this.popups.length;
            this.div.appendChild(popupDiv);
            // store a reference to this function so we can unregister on
            // removal
            this.popupMoveFunc = function(event) {
                var px = this.getPixelFromLonLat(popup.lonlat);
                popup.moveTo(px);
            };
            this.events.register("move", this, this.popupMoveFunc);
            this.popupMoveFunc();
        }
    },
    /**
     * Override parent to allow placement of popups outside viewport
     */
    removePopup: function(popup) {
        OpenLayers.Util.removeItem(this.popups, popup);
        if (popup.div) {
            try {
                this.div.removeChild(popup.div);
                this.events.unregister("move", this, this.popupMoveFunc);
            } catch (e) { }
        }
        popup.map = null;
    },
    /**
     * Build a paginated popup
     */
    createPopup: function(evt) {
        var feature = evt.feature;
        var lonlat;
        if (feature.geometry.CLASS_NAME == "OpenLayers.Geometry.Point") {
            lonlat = feature.geometry.getBounds().getCenterLonLat();
        } else {
            lonlat = this.getLonLatFromViewPortPx(evt.object.handlers.feature.evt.xy);
        }

        var popupHTML = [];
        if (feature.cluster) {
            if (feature.layer && feature.layer.opts &&
                    feature.layer.opts.clusterDisplay == 'list') {
                if (feature.cluster.length > 1) {
                    var html = "<ul class='olwidgetClusterList'>";
                    for (var i = 0; i < feature.cluster.length; i++) {
                        html += "<li>" + feature.cluster[i].attributes.html +
                            "</li>";
                    }
                    html += "</ul>";
                    popupHTML.push(html);
                } else {
                    popupHTML.push(feature.cluster[0].attributes.html);
                }
            } else {
                for (var i = 0; i < feature.cluster.length; i++) {
                	// ROD HACK !!!
                    //popupHTML.push(feature.cluster[i].attributes.html);
                    var id = feature.layer.mapItems.url+feature.cluster[i].item_id+'/';
                    var pop_html = new Datea.MapItemPopupView({
                    	model: feature.layer.mapItems.get(id),
                    }).render().$el.html();
                    popupHTML.push(pop_html);
                }
            }
        } else {
            if (feature.attributes.html) {
                popupHTML.push(feature.attributes.html);
            }
        }
        if (popupHTML.length > 0) {
            var infomap = this;
            var popup = new olwidget.Popup(null,
                    lonlat, null, popupHTML, null, true,
                    function() { infomap.selectControl.unselect(feature); },
                    this.opts.popupDirection,
                    this.opts.popupPaginationSeparator);
            if (this.opts.popupsOutside) {
               popup.panMapIfOutOfView = false;
            }
            this.addPopup(popup);
        }
    },
    deleteAllPopups: function() {
        // must clone this.popups array first; it's modified during iteration
        var popups = [];
        for (var i = 0; i < this.popups.length; i++) {
            popups.push(this.popups[i]);
        }
        for (var i = 0; i < popups.length; i++) {
            this.removePopup(popups[i]);
        }
        this.popups = [];
    },
    CLASS_NAME: "olwidget.Map"
});




