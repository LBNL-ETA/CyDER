
var platformMoz = (document.implementation && document.implementation.createDocument);
var platformIE6 = (!platformMoz && document.getElementById && window.ActiveXObject);
var noXSLT      = (!platformMoz && !platformIE6);

var urlXML;
var urlXSL;
var target;
var i;
var DefaultTreeMode;
var displayedChromeMessage = false;

function initializeTree(defTreeMode) {
    if (noXSLT) {
        alert("Sorry, this doesn't work in your browser");
        return;
    }
   
    urlXML = get_report_filename()
    urlXSL = "tree/tree.xsl";
    target = document.getElementById("xmlContent");
    
	DefaultTreeMode = defTreeMode;
    Transform();
}

function get_report_filename() {
    var filename;
    var i;
    var j;
    var c;
    var fileId;

    filename = document.URL;
    j = filename.length;
    k = 0
    for (i=filename.length-1; i>=0; i--) {
        c = filename.charAt(i)
        
        if ((j == filename.length) && (c == '.')) {
            j = i;
        }
        if ((c == '/') || (c == '\\')) {
            break;
        }
    }
    if (i != -1) {
        return 'xml/' + filename.substring(i+1,j) + '.xml'
    } else {
        return 'xml/report.xml'
    }
}

function LoadDocument(file) {
	try { //Internet Explorer
		xmlDoc=new ActiveXObject("Msxml2.FreeThreadedDOMDocument.6.0");
		xmlDoc.async=false;
		xmlDoc.load(file);
		return xmlDoc;
	} catch(e) {
		try { //Firefox, Mozilla, Opera, etc.
			xmlDoc=document.implementation.createDocument("", "", null);
			xmlDoc.async=false;
			xmlDoc.load(file);
			return xmlDoc;
		} catch(e) {
			try { //Google Chrome
				var xmlhttp = new window.XMLHttpRequest();
				xmlhttp.open("GET", file, false);
				xmlhttp.send(null);
				xmlDoc = xmlhttp.responseXML.documentElement;
				return xmlDoc;
			} catch(e) {
				if (!displayedChromeMessage) {
					alert('To use this page on Chrome, you need to launch Chrome using arguments "--allow-file-access-from-files". Or use another Internet browser.');
					displayedChromeMessage = true;
				}
			}
		}
	}
}

function Transform() {
    var docXML = LoadDocument(urlXML);
    var docXSL = LoadDocument(urlXSL);
	
	if (window.ActiveXObject || "ActiveXObject" in window) {
		var cache = new ActiveXObject('Msxml2.XSLTemplate.6.0');
        cache.stylesheet = docXSL;

        var processor = cache.createProcessor();
        processor.input = docXML;
        processor.addParameter("DefaultTreeMode", DefaultTreeMode);
        
        processor.transform();
        target.innerHTML = processor.output;
    } else {
        var processor = new XSLTProcessor();
        processor.importStylesheet(docXSL);

        processor.setParameter(null, "DefaultTreeMode", DefaultTreeMode);
        
        var fragment = processor.transformToFragment(docXML, document);
        while (target.hasChildNodes())
        {
            target.removeChild(target.childNodes[0]);
        }
        target.appendChild(fragment);
    }
}

//----------------------------------------------------
function cancelBuble(event) {
    if (window.event) {
        window.event.cancelBubble = true;
    } else if (event && event.preventDefault && event.stopPropagation) {
        event.preventDefault();
        event.stopPropagation();
    }    
}

//----------------------------------------------------
function clickOnEntity(event, entity) {
    // cancel buble    
    cancelBuble(event)

    if(entity.getAttribute("open") == "false") {
        expand(entity)
    } else {
        collapse(entity)
    }
    
    // cancel buble
    cancelBuble(event)
}

//----------------------------------------------------
function expand(entity) {
    // Variable declarations
    var oImage
    var i
    
    // Get class name
    if (platformMoz)
        cl = entity.getAttribute("CLASS");
    else if (platformIE6)
        cl = entity.className

    // Get and change image
    if (cl == "item") {
        oImage = entity.getElementsByTagName('img')[0]
        oImage.src = entity.getAttribute("openimage")
    }
    
    for (i = 0 ; i < entity.childNodes.length ; i++) {
        node = entity.childNodes[i]
        if((node.tagName == "DIV") || (node.tagName == "div")) {
            // Display child
            node.style.display = "block"
        }
    }
    entity.setAttribute("open","true")
}

//----------------------------------------------------
function collapse(entity) {
    // Variable declarations
    var oImage
    var i

    // Get class name
    if (platformMoz)
        cl = entity.getAttribute("CLASS");
    else if (platformIE6)
        cl = entity.className

    // Get and change image
    if (cl == "item") {
        oImage = entity.getElementsByTagName('img')[0]
        oImage.src = entity.getAttribute("closeimage")
    }
    for (i = 0 ; i < entity.childNodes.length ; i++) {
        node = entity.childNodes[i]
        if((node.tagName == "DIV") || (node.tagName == "div")) {
            // Display child
            node.style.display = "none"
        }
    }
    
    entity.setAttribute("open","false")
}

//----------------------------------------------------
function expandAllFromString(entityString) {
    entity = document.getElementById(entityString);
    expandAll(entity, 1)
}

function expandAll(entity, isRoot) {
    var i
    // expand current node
    expand(entity)

    // expand children
    for (i = 0 ; i < entity.childNodes.length ; i++) {
        if ((entity.childNodes[i].tagName == "DIV") || (entity.childNodes[i].tagName == "div")) {
            expandAll(entity.childNodes[i], 0)
        }
    }
}

//----------------------------------------------------
function collapseAllFromString(entityString) {
    entity = document.getElementById(entityString);
    collapseAll(entity, 1)
}

function collapseAll(entity, isRoot) {
	var i
    // collapse current node
    idStr = entity.id
    if ( isRoot == 0 ) {
        collapse(entity)
    }
    // expand children
    for (i = 0 ; i < entity.childNodes.length ; i++) {
        if((entity.childNodes[i].tagName == "DIV") || (entity.childNodes[i].tagName == "div")) {
            collapseAll(entity.childNodes[i], 0)
        }
    }
}
