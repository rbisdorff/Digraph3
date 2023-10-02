

/*
#
# Html/JavaScript implementation of digraphs graph export
# 
# Copyright (C) 2014  Gary Cornelius - University of Luxembourg
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
####################### 
*/

/**
*
* Declaration of some usefull global variables:
*
* width = window width;
* height = window height;
* xmlinput= used to save the xml input string before it is parsed;
* $xml = 
* xmlDoc = contains the parsed XML Document as returned by JQuery's parseXML() function;
* pairwise= contains the JSON array of pairwise comparisions in HTML format;
* json = contains the json array of data, the JSON array is of the D3 Data format;
* labels= global variable of all source label elements on an edge;
* labelt = global variable for the set of all the target label elements in the dom;
* path = global variable for the set of all path elements in the dom;
* force = global varibale for the D3 force function;
* freeze = value set to true if graph is frozen, false otherwise;
* svg = global variable for the svg element in the Dom;
* actions = global array containing all the nodes of a graph;
* relation = global variable containing all the raltions of a graph;
* valuationdomain = global variable containing the valuationdomain values valuationdomain["Min"], valuationdomain["Med"], valuationdomain["Max"];
* category = global variable containing the type of a graph, outranking or general;
* current = global variable to store the last selected node;
* type_label = variable used for the type label on the top right corner of the graph;
* graph_type = the variable used to describe the graph type and decide for the possible actions. choice: general, outranking
*
*/
var width,height,xmlinput="",$xml,xmlDoc,pairwise={},json,labels,labelt,path,force,freeze=false,svg,actions={},relation={},valuationdomain={"Min" : 0 , "Max":1, "Med" : 0.5},current,ticker=0,type_label,hide_status=false,graph_type="general";


////
////
//// BASIC FUNCTIONS
////
////

/**
 * Loaded only on the first load of the web page in order to allow automatic loading of the d3export.json with the same ticker number.
 * start = name of the default file that the graph should load;
 * @method first_load
 * @param {} start
 * @return 
 */
function first_load(start) {
  
   initialize(); 
  $.support.cors = true;
  $.ajax({
  url: start,
  async: false,
  dataType: 'json',
  /**
   * Description
   * @method success
   * @param {} data
   * @return 
   */
  success: function (data) {
              d3json=data; 
              xmlinput = d3json["xmcda2"];
              pairwise=$.parseJSON(d3json["pairwiseComparisions"]);
              var result = parseXMCDA2(xmlinput);
              actions = result[0];
              relation = result[1];
              type_label.text("Mode: '"+graph_type+"'");
                
               
  load(hide_status);
   
  }});

}    

/**
 * Initialization of our empty canvas.
 * @method initialize
 * @return 
 */
function initialize() {
  console.log("Initialization of our empty standart canvas.")
  ticker=0;
  width=$(window).width(), height=$(window).height(); //set width and height to the window size.;
  d3.selectAll("svg").remove(); // remove the current svg element (together with all the edges and nodes);
  svg = d3.select("#graph").append("svg") //append a new SVG element to the div tah with id="graph";
      .attr("width", width)
      .attr("height", height);


  /**
  * Create all arrow types.
  *
  * Full end arrow
  *
  */
  var defs= svg.append("svg:defs");
  defs.append("marker")
    .attr("id", "end-full")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 13)
    .attr("refY", -0.0)
    .attr("markerUnits","userSpaceOnUse")
    .attr("stroke-dasharray",0)
    .attr("markerWidth", 12)
    .attr("markerHeight", 12)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("d", "M0,-5L10,0L0,5z");
  /**
  *
  * Empty end arrow
  *
  */
  defs.append("marker")
    .attr("id", "end-empty")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 13)
    .attr("refY", -0.0)
    .attr("markerUnits","userSpaceOnUse")
    .attr("stroke-dasharray",0)
    .attr("markerWidth", 12)
    .attr("markerHeight", 12)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("stroke", "black")  
    .attr("fill", "white")  
    .attr("stroke-width", 2)  
    .attr("d", "M0,-5L10,0L0,5z");

  /**
  *
  * Full start arrow
  *
  */
  defs.append("marker")
    .attr("id", "start-full")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", -3)
    .attr("refY", -0.0)
    .attr("markerWidth", 12)
    .attr("markerHeight", 12)
    .attr("markerUnits","userSpaceOnUse")
    .attr("stroke-dasharray",0)
    .attr("orient", "auto")
    .append("svg:path")
    .attr("d", "M10,-5L0,0L10,5z");

  /**
  *
  * Empty start arrow
  *
  */
  defs.append("marker")
    .attr("id", "start-empty")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", -3)
    .attr("refY", -0.0)
    .attr("stroke-dasharray",0)
    .attr("markerWidth", 12)
    .attr("markerHeight", 12)
    .attr("markerUnits","userSpaceOnUse")
    .attr("orient", "auto")
    .append("svg:path")
    .attr("stroke", "black")  
    .attr("fill", "white")  
    .attr("stroke-width", 2)  
    .attr("d", "M10,-5L0,0L10,5z");

  /**
  *
  * Append background rectangle
  *
  */
  rect = svg.append("rect")
  .on("click",unfocusNode)
  .on("contextmenu", context_main)
  .on("dblclick",function() 
    {
      if(freeze==true)
      {
        ticker=0;
        force.resume();
        freeze=false;
      } 
      else {
        force.stop();
        freeze=true;
      }
    })
  .attr("width", "100%")
  .attr("height", "100%")
  .attr("fill", "#FAFAD2");
    
  /**
  *
  * Select all nodes and labels and inizialize the variables.
  *
  */
  node = svg.selectAll(".node"),
  labels = svg.selectAll("labels");

  /**
  *
  * Set up our force graph.
  *
  */
  force = d3.layout.force()
    .size([width, height])
    .linkDistance(200)
    .linkStrength(0.1)
    .charge(-3500)
    .gravity(0.5)
    .start();
  /**
  *
  * Set up the text label that describes the type of the graph.
  */
  type_label=svg.append("text")
    .attr("x", width-120)
    .attr("y", 20)
    .text("Mode: '"+graph_type+"'");
  /**
  *
  * Set up the copyright text label and the info icon on the botom left.
  *
  */
  svg.append("text")
    .attr("x", width-340)
    .attr("y", height -20)
    .text("D3 Data Driven Document, G. Cornelius, 2014");
  svg.append("image")
    .attr("width", 30)
    .attr("height", 30)
    .attr("xlink:href", "http://leopold-loewenheim.uni.lu/WWWgary/icons/info.png")
    .attr("x", 10)
    .on("click",function(o) {
      $('#infoModalLabel').modal('show');  
    })
    .attr("y",height-35);

    /**
     * Prompt a warning when attempting to close the window.
     * @method onbeforeunload
     * @return Literal
     */
    window.onbeforeunload = function(){
    return "Make sure to save your graph locally.";
  }; 
  }
  
  /**
   * Load function called to load a graph or rebuild a graph. 
   * @method load
   * @param {} hide
   * @return 
   */
  function load(hide) {
    freeze=false;
    initialize();

    json={"nodes": [],"links":[]};
    force
        .nodes(json.nodes)
        .links(json.links);
    json = buildD3Json(actions,relation,hide);
    force
        .nodes(json.nodes)
        .links(json.links);
    
    start();


  }

  /**
  * Start the graph
  * @method start
  * @return 
  */
 function start() {
  console.log("Drawing graph.")
  //Select all path elements and initialize it's attributes.
  path = svg.append("g").selectAll('path')
    .data(force.links())
    .enter().append("svg:path")
    .attr("class", function(d) { return "link " + d.type; })
    .attr("class", "link")
    .attr("stroke", function(d){if(d.type == -1 ){return "red";} else {return "#000";}} )
    .style("opacity",0.5)
    .attr("stroke-dasharray", function(d) { if(d.type == 5 || d.type ==6|| d.type ==7) return "3,3";})
    .attr("marker-end", 
      function(d) { 
        if(d.type == 4 || d.type ==6|| d.type ==7) 
          return "url(#end-empty)"; 
        if(d.type == 0 || d.type ==2|| d.type ==3) 
          return "url(#end-full)";})
    .attr("marker-start", 
      function(d) { 
        if(d.type == 3|| d.type ==5|| d.type ==7) 
          return "url(#start-empty)"; 
        if(d.type == 1 || d.type ==2|| d.type ==4) 
          return "url(#start-full)";
      })
      .on("contextmenu", context_edge);
  //Select all source labels and set it's attributes.
  labels = svg.append("g").selectAll('text')
    .data(force.links())
    .enter().append('text')
    .attr("dy", ".9em")
    .style("font-size", "12px")
    .text(function(d) {return d.value > valuationdomain["Max"] && d.value2 > valuationdomain["Max"] ? "" : d.value2;}); 
  //Select all target labels and set it's attributes.
  labelt = svg.append("g").selectAll('text')
    .data(force.links())
    .enter().append('text')
    .attr("dy", ".9em")
    .style("font-size", "12px")
    .text(function(d) {return d.value > valuationdomain["Max"] && d.value2 > valuationdomain["Max"] ? "" : d.value;}); 
  // Set the drag behaviour for D3.
  var node_drag = d3.behavior.drag()
        .on("dragstart", dragstart)
        .on("drag", dragmove)
        .on("dragend", dragend);
  // Select all node elements and set it's attributes.
  node = svg.append("g").selectAll(".node")
    .data(force.nodes())
    .enter().append("g")
    .attr("class", "node")
    .style("fill","#F6FBFF")
    .on("dblclick",releaseNodes)
    .on("dragstart", dragstart)
    .on("drag", dragmove)
    .on("dragend", dragend)
    .on("contextmenu", context_node)
    .call(node_drag);
  // Append a circle to  the nodes in order to color the nodes and set the sice, which allows us to append text to the nodes later.
  node.append("circle")
    .attr("r", 15);    
  // Append text to nodes.
  node.append("text")
    .attr("dx", 0)
    .attr("dy", ".35em")
    .style("font-family", "Comic Sans MS")
    .text(function(d) { return d.name; });
    force.start();
  /**
   * Tick function used to update the coordinates.
   * @return 
   */
  tick = function tick() {
    
      labels
      .attr("x", function(d) { return (((d.source.x + d.target.x) /2) + d.source.x)/2 ; }) 
      .attr("y", function(d) { return (((d.source.y + d.target.y) /2) + d.source.y)/2; });

    labelt
      .attr("x", function(d) { return (((d.source.x + d.target.x) /2) + d.target.x)/2 ; }) 
      .attr("y", function(d) { return (((d.source.y + d.target.y) /2) + d.target.y)/2; });

    path
      .attr('d', 
        function(d) {
          var deltaX = d.target.x - d.source.x,
          deltaY = d.target.y - d.source.y,
          dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
          normX = deltaX / dist,
          normY = deltaY / dist,
          sourcePadding = d.left ? 17 : 12,
          targetPadding = d.right ? 17 : 12,
          sourceX = d.source.x + (sourcePadding * normX),
          sourceY = d.source.y + (sourcePadding * normY),
          targetX = d.target.x - (targetPadding * normX),
          targetY = d.target.y - (targetPadding * normY);
          return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
        });
        
    node
      .attr("transform", 
        function(d) {
          return "translate(" + d.x + "," + d.y + ")"; 
        });  
    
    if(ticker>100) {
      force.stop();
      freeze=true;
    }
    ticker +=1;
  }




  force.on("tick",tick)
   .start();
  
   
  }
  
  
  ////
  ////
  ////  CONTEXT MENUS AND THEIR FUNCTIONS
  ////
  ////

  /**
   * Context-menu for right clicks on Nodes.
   * @method context_node
   * @param {} d
   * @return 
   */
  var context_node = function context_node(d) {
     console.log("Opening node context menu.");
     $('g.node').contextMenu('cntxtNode',
    {
        itemStyle:
        {
            fontFamily : 'Arial',
            fontSize: '13px'
        },
        bindings:
        {
            /**
             * Description
             * @param {} t
             * @return 
             */
            'inspect': function(t) {
                focusNode(d);

            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'editNode': function(t) {
                editNode(d);

            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'connectNode':function(t) {
                if(graph_type ==="general") {
               connectNode(d);
              }
              else 
                alert("Connecting not allowed.");
              
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'deleteNode':function(t) {
              //Delete a node from actions and all it's relations from the relation dictionnary.
              if(graph_type ==="general") {
                delete actions[d.name];
                delete relation[d.name];
                for(var x in relation) {
                  delete relation[x][d.name];
                }
              load(hide_status);
              }
              else 
                //Alert if the graph is not of the type outranking.
                alert("Deleting not allowed.");
            }
        }
    });
    d3.event.preventDefault();
  }

  /**
   * Context-menu for right clicks on Nodes.
   * @method context_edge
   * @param {} d
   * @return 
   */
  var context_edge = function context_edge(d) {
    console.log("Opening edge context menu.");
    $('path').contextMenu('cntxtEdge',
    {
        itemStyle:
        {
            fontFamily : 'Arial',
            fontSize: '13px'
        },
        bindings:
        {
            
            /**
             * Description
             * @param {} t
             * @return 
             */
            'inspectEdge': function(t) {
                inspectEdge(d);
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'invertEdge':function(t) {
                invertEdge(d);
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'editEdge':function(t) {
              // Edit the values of an edge.
              if(graph_type ==="general") {
                editEdge(d);
              }
              else 
                alert("Editing not allowed.");
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'deleteEdge':function(t) {
              // Delete an edge from the relation dictionnary.
              if(graph_type ==="general") {
                delete relation[d.source.name][d.target.name];
                delete relation[d.target.name][d.source.name];
                force.stop();
                load(hide_status);
              }
              else 
                //Alert if the graph is not of the type outranking.
                alert("Deleting not allowed.");
            }

        }
    });
    d3.event.preventDefault();
  }


  /**
   * Context-menu for right clicks on Background.
   * @method context_main
   * @param {} d
   * @return 
   */
  var context_main = function context_main(d) {
     console.log("Opening main context menu.");
     $("#hide").html(function(){ if(hide_status){return '<img alt="Hide" src="http://leopold-loewenheim.uni.lu/WWWgary/icons/hide.png" height="15" width="15" />Unhide';}else{return '<img alt="Hide" src="http://leopold-loewenheim.uni.lu/WWWgary/icons/hide.png" height="15" width="15" />Hide edges';}});
     $('rect').contextMenu('cntxtMenu',
     {
        itemStyle:
        {
            fontFamily : 'Arial',
            fontSize: '13px'
        },
        bindings:
        {
            /**
             * Description
             * @param {} t
             * @return 
             */
            'new': function(t) {
                hide_status=false;
                setTimeout(function(){$('#min').focus();},500);
                $('#newModal').modal('show');            
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'hide':function(t) {
              if(hide_status == false) {
               hide_status=true;
               load(hide_status);
              }
              else {
                hide_status=false;
                load(hide_status);
              }
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'import': function(t) {
                importJSON();

            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'export': function(t) {  
                exportXMCDA2(buildXMCDA2());
            },
            /**
             * Description
             * @param {} t
             * @return 
             */
            'reset': function(t) {
                if(json != null) { 
                  console.log("Resetting Graph.") ;
                  tick=0;
                  hide_status=false;
                  load(hide_status);
              }},
              /**
               * Description
               * @param {} t
               * @return 
               */
              'add': function(t) {
                if(graph_type==="general") {
                    $("#nodeAddId").attr("value","");
                    $("#addNodeModal").modal("show");
                    setTimeout(function(){$('#nodeAddId').focus();},500);

                  } else {
                    alert("Adding nodes not allowed.");
                  }
            }
        }
    });
    d3.event.preventDefault();
  }

  /**
   * Set all important values when creating a new graph. For the moment only valuationdomain min and max!
   * @method newGraph
   * @return 
   */
  function newGraph() {
                  var min = $('#min').attr("value"), max=$('#max').attr("value");
                  if((isNaN(String(min)) || isNaN(String(max))) || !(min < max)) {
                    alert("Please enter numeric values and Min < Max !");
                  }
                  else {
                    pairwise={};
                    actions={};
                    relation={};
                    xmlDoc=null;
                    xmlinput="";
                    initialize();
                    valuationdomain["Min"] = Number(min);
                    valuationdomain["Max"] = Number(max);
                    valuationdomain["Med"]  = valuationdomain["Min"]  + ((valuationdomain["Max"]  - valuationdomain["Min"] )/Number(2.0));
                    $('#newModal').modal('hide');  
                    graph_type="general";
                    type_label.text("Mode : '"+graph_type+"'");
                  }

  }
  /**
  * Stop force and free drag
  */
  var draging=false;
  /**
   * Description
   * @method dragstart
   * @param {} d
   * @param {} i
   * @return 
   */
  var dragstart = function dragstart(d,i) {
        if(d3.event.sourceEvent.which==1){
        draging=true;
       
      }
    }

  /**
   * Method that is called while dragging a node.
   * @method dragmove
   * @param {} d
   * @param {} i
   * @return 
   */
  var dragmove = function dragmove(d,i) {
        if(draging){
        d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy;
        tick();
        } 
    }

  /**
   * Method called on mouseup. A dragged node is frozen at the current coordinates.
   * @method dragend
   * @param {} d
   * @param {} i
   * @return 
   */
  var dragend = function dragend(d,i) {
        if(d3.event.sourceEvent.which==1){
        d.fixed = true; 
        tick();
        draging=false;
        }
    }
  /**
   * Check if a node is connected to with another one.
   * @method isConnected
   * @param {} a
   * @param {} b
   * @return LogicalExpression
   */
  function isConnected(a, b) {
    return linkedByIndex[b.index + "," + a.index] || linkedByIndex[a.index + "," + b.index];
  }
  /**
   * Check if a node is equal to another one.
   * @method isEqual
   * @param {} a
   * @param {} b
   * @return BinaryExpression
   */
  function isEqual(a, b) {
    return a.index == b.index;
  }
 
  ////
  ////
  ////   NODE CONTROLS
  ////
  ////
  /**
   * Release a node so it can move again freely according to physics.
   * @method releaseNodes
   * @param {} d
   * @return 
   */
  var releaseNodes=function releaseNodes(d) {
    console.log("Releasing node " + d.name);
    d.fixed = false; 
    ticker=0;
    force.start();
  }
  /**
   * Function called by the connect modal in order to allow the user to select the node to which he wants to connect to.
   * @method connectNode
   * @param {} d
   * @return 
   */
  function connectNode(d){
    var options = $("#selectNode");
    $("#selectNode").empty();
    for(var x in actions){
     if(x != d.name) 
      options.append($("<option />").val(x).text(x));    
    };
    current=d;
    $('#connNodeModal').modal('show');
   
  }
  /**
   * Save the new connection and reload the graph.
   * @method saveConnectNode
   * @return 
   */
  function saveConnectNode() {
    $('#connNodeModal').modal('hide');
    var e = document.getElementById("selectNode");
    var neighbour = e.options[e.selectedIndex].text;
    relation[current.name][neighbour] = valuationdomain["Max"] +1;
    relation[neighbour][current.name] = valuationdomain["Max"]+1;
    load(hide_status);
  }
  /**
   * Function used to add nodes to the graph and refresh the graph later to include them.
   * @method addNode
   * @return 
   */
  function addNode() {
    var nodeid = $("#nodeAddId").attr("value");
    //If no node id is selected prompt an alert and allows you to try again.
    if(nodeid ==="") {
      alert("Invalid node id!")
    }
    else
    {
      relation[nodeid]={};
      relation[nodeid][nodeid]= Number(valuationdomain["Med"]);  
      name = $("#nodename_add").attr("value");
      comment = $("#nodeComment_add").attr("value");
      if((name === "")&&(comment != "")){
       actions[nodeid] = {"name": "nameless","comment":comment};
    } else if((name != "")&&(comment === "")) {
      actions[nodeid] = {"name": name,"comment":"none"};
    }
    else if(((name != "")&&(comment != ""))){
      actions[nodeid] = {"name": name,"comment":comment};
    }
    else {
          actions[nodeid] = {"name": "nameless","comment":"none"};
    }
      load(hide_status);
      $("#addNodeModal").modal("hide");
    }
  }
  /**
   * Function called by the editGraph modal if a user wants to edit the values of a node.
   * @method editNode
   * @param {} d
   * @return 
   */
  function editNode(d) {
    $('#modNodeModal').modal('show');
    $('#nodeId').attr("value",d.name);
    $('#nodeComment').attr("value",d.comment);
    $('#nodename').attr("value",d.fullName);
  }

  /**
   * Save the edited node and reload the graph.
   * @method saveNode
   * @param {} d
   * @return 
   */
  function saveNode(d) {
    $('#modNodeModal').modal('hide');
    var comment = $('#nodeComment').attr("value");
    var fullName = $('#nodename').attr("value");
    actions[$('#nodeId').attr("value")]["comment"] =  comment;
    actions[$('#nodeId').attr("value")]["name"] =  fullName;
    $xml.find("alternatives").find('alternative[id="'+$("#nodeId").attr("value")+'"]').find('description').text(comment);
    $xml.find("alternatives").find('alternative[id="'+$("#nodeId").attr("value")+'"]').attr('name',fullName);
    load(hide_status);
    
  }
  var linkedByIndex = {};
  /**
   * Implementation which works as follows:
   * - Select node.
   * - Push non connected nodes and edges in the background.
   * @method focusNode
   * @param {} d
   * @return 
   */
  function focusNode(d) {
    linkedByIndex={}
    console.log("Focusing node " + d.name);
    var circle = d3.select();
    json.links.forEach(
      function(i) {
        linkedByIndex[i.source.index + "," + i.target.index] = true;
    });
    /**
    * Select all node elements, and set their opacity.
    *
    */
    svg.selectAll(".node")
      .transition(500)
      .style("opacity", 
        function(o) {
          return isConnected(o, d) || isEqual(o,d) ? 1 : 0.1 ;
        })
      .style("fill", 
        function(o) {
          if(isConnected(o, d)) return "#F6FBFF";
          else if(isEqual(o,d)) return "lightpink";
          return "#000";

        }); 
    /**
    *
    * Select all path elements and set their opacity and cursor behaviour.
    */
    path
      .transition(500)
      .style("cursor", 
        function(o) {
           return o.source.index === d.index || o.target.index === d.index ? "pointer" : "default" ;
        })
      .style("opacity", 
        function(o) {
          return o.source.index === d.index || o.target.index === d.index ? 1 : 0.05;
        });
    /**
    *
    * Select all source labels and set their opacity.
    */
    labels
      .transition(500)
      .style("opacity", 
        function(o) {
          return o.source.index === d.index || o.target.index === d.index ? 1 : 0;
        });
    /**
    *
    * Select all target labels and set their opacity.
    */
    labelt
      .transition(500)
      .style("opacity", 
        function(o) {
          return o.source.index === d.index || o.target.index === d.index ? 1 : 0;
        }); 
  }


    
    
  /**
   * The unfocus function of focusNode 
   * @method unfocusNode
   * @param {} d
   * @return 
   */
  var unfocusNode = function unfocusNode(d) {
      console.log("Unfocus node.");
      //Select all nodes and set their opacity.
      node
          .transition(500)
          .style("opacity", 1.0)
          .style("fill", "#F6FBFF");
      //Select all path and set their opacity.
      path
          .transition(500)
          .style("opacity", 0.5 )
          .style("cursor", "pointer");
      //Select all source labels and set their opacity.
      labels
          .transition(500)
          .style("opacity", 1 );
      //Select all target labels and set their opacity.
      labelt
          .transition(500)
          .style("opacity", 1 );
    }


  ////
  ////
  ////   EDGE CONTROLS
  ////
  ////
  /**
   * Function called to initialize the inspectEdge modal with the correct values.
   * @method inspectEdge
   * @param {} d
   * @return 
   */
  function inspectEdge(d) {
    if (graph_type != "general"){
      $('#modEdgeModal').modal('show');
      $('#source').html((pairwise[d.source.name][d.target.name]).toString());
      $('#target').html((pairwise[d.target.name][d.source.name]).toString());
    }
    else {
      alert("pairwiseComparision not possible with this graph.");
    }
  }

  /**
   * Function called if we want to invert an Edge, and reload the graph afterwards.
   * @method invertEdge
   * @param {} d
   * @return 
   */
  function invertEdge(d) {
    if (pairwise[d.source.name] == null){
      relation[d.source.name][d.target.name] =  (Math.floor((valuationdomain["Max"]- Number(relation[d.source.name][d.target.name]) + valuationdomain["Min"])*100)/100).toFixed(2);
      relation[d.target.name][d.source.name] =  (Math.floor((valuationdomain["Max"]- Number(relation[d.target.name][d.source.name]) + valuationdomain["Min"])*100)/100).toFixed(2);
      load(hide_status);
    }
    else {
      alert("Invert not possible.");
    }
  }

    
/**
 * Function called by the editEdge modal if a user wants to edit the values of an Edge.
 * @method editEdge
 * @param {} d
 * @return 
 */
function editEdge(d) {
    $('#editEdgeModal').modal('show');
    
    $('#nodeTarget').attr("value",relation[d.target.name][d.source.name]);
    document.getElementById("pnodetarget").innerHTML=d.target.name + " to " + d.source.name;
    
    $('#nodeSource').attr("value",relation[d.source.name][d.target.name]);
    document.getElementById("pnodesource").innerHTML=d.source.name + " to " + d.target.name;
    
    $('#nodeTarget').attr("name",d.target.name);
    $('#nodeSource').attr("name",d.source.name);

  }

  /**
   * Save the edited edge and reload the graph.
   * @method saveEdge
   * @return 
   */
  function saveEdge() {
    if($('#nodeSource').attr("value")>=valuationdomain["Min"] && $('#nodeSource').attr("value") <= valuationdomain["Max"] && $('#nodeTarget').attr("value")>=valuationdomain["Min"] && $('#nodeTarget').attr("value") <= valuationdomain["Max"]){
    $('#editEdgeModal').modal('hide');
    relation[$('#nodeSource').attr("name")][$('#nodeTarget').attr("name")] =  ((Math.floor(Number($('#nodeSource').attr("value"))*100))/100).toFixed(2);
    relation[$('#nodeTarget').attr("name")][$('#nodeSource').attr("name")] =  ((Math.floor(Number($('#nodeTarget').attr("value"))*100))/100).toFixed(2);
    load(hide_status);
    }
    else alert("Error: Value must be between " + valuationdomain["Min"] + " and " + valuationdomain["Max"] +" !");
  }

  /**
   * Open the import menu and load the file into the xmlinput and pairwise variables.
   * @method importJSON
   * @return 
   */
  function importJSON() {
    console.log("Importing JSON file.")
    var reader;
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        $('#upModalLabel').modal('show');
        /**
         * Description
         * @method handleFileSelect
         * @param {} evt
         * @return 
         */
        function handleFileSelect(evt) {
           var files = document.getElementById('xml').files;
           if (!files.length) {
             alert('Please select a file!');
             return;
          }
          var file = files[0];
          var start =  0;
          var stop = file.size - 1;
          reader= new FileReader();
          var blob = file.slice(start, stop + 1);
          //readAsBinaryString() not in specifications.
          reader.readAsText(blob); 
          actions={};
          relation={};
          /**
           * Description
           * @method onloadend
           * @param {} evt
           * @return 
           */
          reader.onloadend = function(evt) { 
            try{
              d3json=$.parseJSON(evt.target.result); 
              xmlinput = d3json["xmcda2"];
              pairwise=$.parseJSON(d3json["pairwiseComparisions"]);
              var result = parseXMCDA2(xmlinput);
              actions = result[0];
              relation = result[1];
              load(hide_status);
              var x = $('#upModalLabel').modal('hide');
              type_label.text("Mode: '" + graph_type +"'");
            }
               
            catch(err){
              alert("Unexpected format.");
            }

              
          };
          }
         
          document.getElementById('open').addEventListener('click', handleFileSelect, false);

          } else {
            alert('The File APIs are not fully supported in this browser.');
          }
   return ;
  }
  
  /**
   * Parse our XMCDA2 file and load all important variables into memory.
   * @method parseXMCDA2
   * @param {} xmlinput
   * @return ArrayExpression
   */
  function parseXMCDA2(xmlinput) {
      console.log("Parsing XMCDA2 File.")
      xmlDoc = $.parseXML(xmlinput);
      $xml = $( xmlDoc );
      var actions={},category;
      // Get the valuation domain from the XML file and calculate the Medium value.
      valuationdomain["Min"] = Number($xml.find('alternativesComparisons').find('valuation').find('quantitative').find('minimum').children().text());
      valuationdomain["Max"] = Number($xml.find('alternativesComparisons').find('valuation').find('quantitative').find('maximum').children().text());
      valuationdomain["Med"]  = Number(valuationdomain["Min"]  + ((valuationdomain["Max"]  - valuationdomain["Min"] )/2));
      // Select the filename and decide the graph type.
      fileName = $xml.find("projectReference").attr("id");
      if(fileName.indexOf("outranking") > -1){
        graph_type = "outranking";
      }
      else {
        graph_type= "general"
      }
      //Get all nodes from the XML file.
      $xml.find("alternatives").find('alternative').each(
        function() { 
            var id = this.getAttribute('id');
            actions[id] = {};
            actions[id]['name'] = this.getAttribute('name');
            $(this).find('description').children().each(function() {
              actions[id][this.tagName] = $(this).text();
            }
              );
        });

      for(var x in actions) {
        relation[x] = {};
      }
      //Get all edges from the XML file.
      $xml.find('alternativesComparisons').find('pairs').find('pair').each(
        function() {
          try{
          relation[$(this).find('initial').find('alternativeID').text()][$(this).find('terminal').find('alternativeID').text()] = (Math.floor(parseFloat($(this).find('value').find('real').text())*100)/100).toFixed(2);
          }
          catch(err) {
          relation[$(this).find('initial').find('alternativeID').text()][$(this).find('terminal').find('alternativeID').text()] = (Math.floor(parseInt($(this).find('value').find('integer').text())*100)/100).toFixed(2);
          }
        });
      
      // Return the actions and relation array.
      return [actions,relation];
  }

  /**
   * Build a D3 Json file in order to initialize the graph with nodes and links.
   * @method buildD3Json
   * @param {} actions
   * @param {} relation
   * @param {} hide
   * @return dataset
   */
  function buildD3Json(actions,relation,hide) {
   console.log("Building D3 Json for graph visualization.")
   var dataset = {"nodes":[],"links":[]}
   var actionkeys=[];
   // Put all the actions into the nodes array.
   if(!Object.keys(actions).length == 0)
   {
   for(node in actions){
            actionkeys.push(node);
            try {
               dataset["nodes"].push({"name": node ,"group":1, "comment": actions[node]["comment"],"fullName": actions[node]["name"]});
            }
            catch(err) {
                dataset["nodes"].push({"name": node ,"group":1, "comment": "none", "fullName":"nameless"});
            }
    }
    //Set the min, med and max value into variables.
    var Min=valuationdomain["Min"],Max=valuationdomain["Max"],Med=valuationdomain["Med"];
    if(Object.keys(relation).length >0){
      for( var i=0;  i<actionkeys.length; i++ ){
            for( var j=i+1;  j<actionkeys.length; j++ ){
              /* Arrow types:
              r(a,b) < Med & r(b,a) < Med  a    b : none
              r(a,b) > MAX & r(b,a) > MAX  a -- b : -1 initialization
              r(a,b) > Med & r(b,a) < Med  a  --> b :0 done
              r(a,b) < Med & r(b,a) > Med  a  <-- b :1 done
              r(a,b) > Med & r(b,a) > Med  a <--> b :2 done
              r(a,b) > Med & r(b,a) = Med  a o--> b :3 done
              r(a,b) = Med & r(b,a) > Med  a <--o b :4 done
              r(a,b) < Med & r(b,a) = Med  a o..  b :5 done 
              r(a,b) = Med & r(b,a) < Med  a  ..o b :6 done
              r(a,b) = Med = r(b,a)        a o..o b :7 done
              */
                if(relation[actionkeys[i]][actionkeys[j]] > Max && relation[actionkeys[j]][actionkeys[i]] > Max)
                    dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": -1, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] > Med && relation[actionkeys[j]][actionkeys[i]] > Med)
                    dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 2, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] > Med && relation[actionkeys[j]][actionkeys[i]] == Med)
                  hide ? dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 0, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])}) : dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 3, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] == Med && relation[actionkeys[j]][actionkeys[i]] > Med)
                  hide ? dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 1, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])}) : dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 4, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] == Med && relation[actionkeys[j]][actionkeys[i]] == Med)
                  hide ? dataset:  dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 7, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] > Med && relation[actionkeys[j]][actionkeys[i]] <  Med)
                    dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 0, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] == Med && relation[actionkeys[j]][actionkeys[i]] <  Med)
                  hide ? dataset: dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 6, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] < Med && relation[actionkeys[j]][actionkeys[i]] >  Med)
                    dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 1, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                else if(relation[actionkeys[i]][actionkeys[j]] < Med && relation[actionkeys[j]][actionkeys[i]] ==  Med)
                  hide ? dataset: dataset["links"].push({"source":String(actionkeys[i]) , "target" : String(actionkeys[j]), "type": 5, "value" : String(relation[actionkeys[i]][actionkeys[j]]), "value2" : String(relation[actionkeys[j]][actionkeys[i]])});
                }
    }}
    
    }
    return dataset;
  }

  /**
   * Export the XMCDA2 formatted graph.
   * @method exportXMCDA2
   * @return 
   */
  function exportXMCDA2() {
      //Export of Javascript variables cannot be done easily. This is a nasty work-around.
      console.log("Exporting current graph.")
      window.URL = window.webkitURL || window.URL;

      var contentType = 'text/xmcda2';
      try{
      var xmcda2File = new Blob([new XMLSerializer().serializeToString(xmlDoc)], {type: contentType});

      var a = document.createElement('a');
      a.download = 'general_digraph.xmcda2';
      a.href = window.URL.createObjectURL(xmcda2File);
      a.id="exportt";
      a.textContent = 'Download XMCDA2 file';

      a.dataset.downloadurl = [contentType, a.download, a.href].join(':');
      $(a).appendTo("#graph")[0].click();
      $("#exportt").remove();
    }
    catch(e) {
      alert("Oops. Export not possible.")
    }
  }

  /**
   * Build a valid XMCDA2 encoded file.
   * @method buildXMCDA2
   * @param {} fileName
   * @param {} name
   * @param {} relationName
   * @param {} relationType
   * @param {} category
   * @param {} subcategory
   * @param {} author
   * @param {} reference
   * @param {} valuationType
   * @return xmlinput
   */
  function buildXMCDA2(fileName,name,relationName,relationType,category,subcategory,author,reference,valuationType){
        fileName= fileName || "general_digraph";
        name=name||"general";
        relationName=relationName|| 'R';
        relationType=relationType||'general';
        category=category||'random';
        subcategory=subcategory||'valued'
        author= author||"digraphs Module RB";
        reference=reference||'saved from Javascript';
        valuationType=valuationType||'standard';
        var xmcda= '<?xml version="1.0" encoding="UTF-8"?>'
        xmcda = xmcda + '<?xml-stylesheet type="text/xsl" href="xmcdaXSL.xsl"?>' 
        xmcda = xmcda +'<xmcda:XMCDA xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.decision-deck.org/2009/UMCDA-2.0.0 file:../XMCDA-2.0.0.xsd" xmlns:xmcda="http://www.decision-deck.org/2009/XMCDA-2.0.0">'
        // write description
        xmcda = xmcda + '<projectReference id="'+fileName+'" name="'+name+'">' ;
        xmcda=xmcda+'<title>Stored Digraph in XMCDA-2.0 format</title>';
        xmcda=xmcda+'<id>'+fileName+'</id>';
        xmcda=xmcda+'<name>'+name+'</name>';
        xmcda=xmcda+('<type>root</type>');
        xmcda=xmcda+('<user>'+author+'</user>');
        xmcda=xmcda+'<version>'+reference+'</version>';
        xmcda=xmcda+('</projectReference>');
        //write nodes
        var na = actions.length;
        xmcda=xmcda+('<alternatives mcdaConcept="Digraph nodes">');
        xmcda=xmcda+('<description>');
        xmcda=xmcda+('<title>Nodes of the digraph</title>');
        xmcda=xmcda+('<type>alternatives</type>');
        xmcda=xmcda+('<comment>Set of nodes of the digraph.</comment>');
        xmcda=xmcda+('</description>');
        var alternativeName="";
        for(var x in actions){
            try{
                alternativeName = actions[x].name;
              }
            catch(err){
                alternativeName = 'nameless';
            }
            xmcda=xmcda+('<alternative id="'+x+'" name="'+alternativeName+'">');
            xmcda=xmcda+('<description>');
            xmcda=xmcda+('<comment>');
            try{
                xmcda=xmcda+(actions[x]['comment']);}
            catch(e){
                xmcda=xmcda+('No comment');
            }
            xmcda=xmcda+('</comment>');
            xmcda=xmcda+('</description>');
            xmcda=xmcda+('<type>real</type>');
            xmcda=xmcda+('<active>true</active>');
            xmcda=xmcda+('<reference>false</reference>');
            xmcda=xmcda+('</alternative>');
        }
        xmcda=xmcda+('</alternatives>');
        //write valued binary Relation
        xmcda=xmcda+('<alternativesComparisons id="1" name="'+relationName+'">');
        xmcda=xmcda+('<description>');
        xmcda=xmcda+('<title>Randomly Valued Relation</title>');
        xmcda=xmcda+('<comment>'+category+' '+subcategory+' %s Digraph</comment>');
        xmcda=xmcda+('</description>');
        xmcda=xmcda+('<valuation name="valuationDomain">');
        xmcda=xmcda+('<description>');
        xmcda=xmcda+('<subTitle>Valuation Domain</subTitle>');
        xmcda=xmcda+('</description>');
        xmcda=xmcda+('<quantitative>');
        var Max = valuationdomain['Max'],
        Min = valuationdomain['Min'];
        if (valuationType === 'integer') {
            xmcda=xmcda+('<minimum><integer>'+Math.floor(Min)+'</integer></minimum>');
            xmcda=xmcda+('<maximum><integer>'+Math.floor(Max)+'</integer></maximum>');
          }
        else{
            xmcda=xmcda+('<minimum><real>');
            xmcda=xmcda+(Min);
            xmcda=xmcda+('</real></minimum>');
            xmcda=xmcda+('<maximum><real>');
            xmcda=xmcda+(Max);
            xmcda=xmcda+('</real></maximum>');
          }
        xmcda=xmcda+('</quantitative>');
        xmcda=xmcda+('</valuation>');
        xmcda=xmcda+('<comparisonType>'+relationName+'</comparisonType>');
        xmcda=xmcda+('<pairs>');
        xmcda=xmcda+('<description>');
        xmcda=xmcda+('<subTitle>Valued Adjacency Table</subTitle>');

        xmcda=xmcda+('<comment>'+category+' ' + subcategory+ ' Digraph</comment>' );
        xmcda=xmcda+('</description>');
        for(var x in actions){
            for(var y in actions){
                xmcda=xmcda+('<pair>');
                xmcda=xmcda+('<initial><alternativeID>');
                xmcda=xmcda+x;
                xmcda=xmcda+('</alternativeID></initial>');
                xmcda=xmcda+('<terminal><alternativeID>');
                xmcda=xmcda+y;
                xmcda=xmcda+('</alternativeID></terminal>');
                xmcda=xmcda+('<value><real>');
                if(relation[x][y] != null)
                {
                xmcda=xmcda + relation[x][y];}
                else { xmcda=xmcda + Number(valuationdomain["Med"]);}
                xmcda=xmcda+('</real></value>');
                xmcda=xmcda+('</pair>');
            }
        }
        
        xmcda=xmcda+('</pairs>');
        xmcda=xmcda+('</alternativesComparisons>');
        xmcda=xmcda+('</xmcda:XMCDA>');
       

  xmlinput=xmcda;
  xmlDoc = $.parseXML(xmlinput);
  return xmlinput;
  }
