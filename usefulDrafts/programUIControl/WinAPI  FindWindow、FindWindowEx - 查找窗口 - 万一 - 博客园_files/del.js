var DelphiKeywords =	
'absolute|abstract|and|array|as|asm|assembler|at|automated|' +
'begin|case|cdecl|class|const|constructor|contains|' +
'default|destructor|dispid|dispinterface|div|do|downto|dynamic|' +
'else|end|except|export|exports|external|' +
'far|file|final|finalization|finally|for|forward|function|' +
'goto|if|implementation|implements|in|index|inherited|initialization|inline|interface|is|' +
'label|library|message|mod|near|nil|nodefault|not|' +
'object|of|on|operator|or|out|overload|override|' +
'package|packed|pascal|private|procedure|program|property|protected|public|published|' +
'raise|read|readonly|record|reference|register|reintroduce|repeat|requires|resident|resourcestring|' +
'safecall|sealed|set|shl|shr|static|stdcall|stored|strict|string|' +
'then|threadvar|to|try|type|unit|until|uses|var|varirnt|virtual|' +
'while|with|write|writeonly|xor';

var CppKeywords =
'__declspec|__exception|__fastcall|__finally|__published|__try|' +
'break|case|catch|char|class|const|const_cast|continue|' +
'default|delete|deprecated|dllexport|dllimport|do|double|dynamic_cast|' +
'else|enum|explicit|extern|false|float|for|friend|goto|if|inline|int|long|bool|' +
'mutable|naked|namespace|new|noinline|noreturn|nothrow|' +
'private|protected|public|register|reinterpret_cast|return|' +
'selectany|short|sizeof|static|static_cast|struct|switch|' +
'template|this|thread|throw|true|try|typedef|typeid|typename|' +
'union|unsigned|using|uuid|virtual|void|volatile|whcar_t|while';

var CsKeywords =
'abstract|as|base|bool|break|byte|case|catch|char|checked|class|const|continue|' +
'decimal|default|delegate|do|double|else|enum|event|explicit|extern|' +
'false|finally|fixed|float|for|foreach|from|get|goto|group|' +
'if|implicit|in|int|interface|internal|into|is|join|let|lock|long|' +
'namespace|new|null|object|operator|orderby|out|override|' +
'params|partial|private|protected|public|readonly|ref|return|' +
'sbyte|sealed|select|set|short|sizeof|stackalloc|static|string|struct|switch|' +
'this|throw|true|try|typeof|uint|ulong|unchecked|unsafe|ushort|using|' +
'value|var|virtual|void|volatile|where|while|yield';

var CsClass = 
'Serializable|Console|Convert|Object|DllImport|EventArgs|_Default|Page|Math|Char|StringInfo|DateTime|' +
'IEnumerator|Random|StringBuilder|MidpointRounding|TimeSpan|Array|ArrayList|BitArray|Enumerable|' +
'Queryable|ParallelQuery|ParallelEnumerable|BitVector32|CollectionsUtil|HybridDictionary|ListDictionary|' +
'NameValueCollection|OrderedDictionary|StringCollection|StringDictionary|Hashtable|Queue|Stack|SortedList|' +
'DictionaryEntry|ICollection|BitConverter|BitVector32|CollectionsUtil|ListDictionary|HybridDictionary|' +
'NameValueCollection|OrderedDictionary|StringCollection|StringDictionary|Section|UInt16|UInt32|UInt64|UIntPtr|' +
'KeysCollection|Dictionary|KeyValuePair|SortedDictionary|HashSet|SortedSet|List|LinkedList|LinkedListNode|' +
'SynchronizedCollection|SynchronizedKeyedCollection|SynchronizedReadOnlyCollection|Lookup|OrderedParallelQuery|' +
'KeyCollection|ValueCollection|Collection|KeyedCollection|ObservableCollection|ReadOnlyCollection|ReadOnlyObservableCollection|' +
'BlockingCollection|ConcurrentBag|ConcurrentDictionary|ConcurrentQueue|ConcurrentStack|OrderablePartitioner|Partitioner'; //随时补充

var JsKeywords =
'break|false|in|this|void|continue|for|new|true|while|delete|function|null|' +
'typeof|with|else|if|return|var|case|debugger|export|super|catch|default|' +
'extends|switch|class|do|finally|throw|const|enum|import|try|' +
'package|class|interface|instanceof|as|override|get|set|prototype|dynamic|final|internal|public|private|protected|static|implements'; //这会为 as3

//window.onload = function() {
  var pres = document.getElementsByTagName("PRE");
  for (var i=0; i< pres.length; i++) {
    //Delphi
    if (pres[i].className == "Delphi") {
        var obj = pres[i].childNodes[0];
        if ((obj != null) && (obj.tagName == "TEXTAREA")) {
            str = obj.innerHTML;
        } else {
            str = pres[i].innerHTML;
        }
        r1 = "(\\(\\*[\\s\\S]*?\\*\\))";           // (* *)
        r2 = "((?:http:)?//.*)";                   // "//" and not "http://"
        r3 = "({(?!\\$)[\\s\\S]*?})";              // { }
        r4 = "(\\{\\${1}[a-zA-Z]+.+\\})";          // {$ }
        r5 = "('.*?')";                            // ' '
        r6 = "([\\$\\#]{1,2}[a-fA-F0-9]+)\\b";     // $Hex or #Number
        r7 = "\\b(\\d+\\.?\\d*)\\b";               // Number
        r8 = "\\b(" + DelphiKeywords + ")\\b";     // Key

        rs = r1 + '|' + r2 + '|' + r3 + "|" + r4 + "|" + r5 + "|" + r6 + "|" + r7 + "|" + r8;
        rr = '<font color=#008000>$1$2$3</font>' +
            '<font color=#008284>$4</font>' +
            '<font color=#0000FF>$5$6$7</font>' +
            '<font color=#000080><b>$8</b></font>'; 
        re = new RegExp(rs,"g");
        str = str.replace(re, rr);
		str = str.replace(/\x20{2}/gm, '&nbsp; ');
        pres[i].innerHTML = "<pre>" + str + "</pre>";
    }
    //End Delphi
    
    //C/C++
    if (pres[i].className == "cpp") {
        var obj = pres[i].childNodes[0];
        if ((obj != null) && (obj.tagName == "TEXTAREA")) {
            str = obj.innerHTML;
        } else {
            str = pres[i].innerHTML;
        }
        r = new RegExp('<(?!hr).+( |>)','gi');
        var arr = str.match(r);

        if(arr != null) for(var n=0; n<arr.length; n++) {
            an = arr[n]; an = arr[n].replace('<','&lt;'); an = an.toLowerCase(); 
            str = str.replace(arr[n], an);
        }

        r1 = "((?:http:)?//.*)";
        r2 = "(/\\*[\\s\\S]*?\\*/)"; 
        r3 = '(".*?")';
        r4 = "('.*?')";
        r5 = "(#.*)";
        r6 = "\\b(" + CppKeywords + ")\\b";

        rs = r1 + '|' + r2 + '|' + r3 + '|' + r4 + '|' + r5 + '|' + r6;
        rr = '<font color=#008000>$1$2</font>' +
            '<font color=#0000FF>$3</font>' +
            '<font color=#800080>$4</font>' +
            '<font color=#008284>$5</font>' +
            '<font color=#000080><b>$6</b></font>'; 
        re = new RegExp(rs,"g");
        str = str.replace(re, rr);
		str = str.replace(/\x20{4}/gm, '&nbsp;   ');
        pres[i].innerHTML = "<pre>" + str + "</pre>";
    }
    //End C/C++

    //JavaScript
    if (pres[i].className == "js") {
        var obj = pres[i].childNodes[0];
        if ((obj != null) && (obj.tagName == "TEXTAREA")) {
            str = obj.innerHTML;
        } else {
            str = pres[i].innerHTML;
        }
        r = new RegExp('<(?!hr).+( |>)','gi');
        var arr = str.match(r);

        if(arr != null) for(var n=0; n<arr.length; n++) {
            an = arr[n]; an = arr[n].replace('<','&lt;'); an = an.toLowerCase(); 
            str = str.replace(arr[n], an);
        }

        r1 = "((?:http:)?//.*)";
        r2 = "(/\\*[\\s\\S]*?\\*/)"; 
        r3 = '(".*?")';
        r4 = "('.*?')";
        r5 = "(#.*)";
        r6 = "\\b(" + JsKeywords + ")\\b";

        rs = r1 + '|' + r2 + '|' + r3 + '|' + r4 + '|' + r5 + '|' + r6;
        rr = '<font color=#008000>$1$2</font>' +
            '<font color=#CC0066>$3</font>' +
            '<font color=#CC0066>$4</font>' +
            '<font color=#008284>$5</font>' +
            '<font color=#000080><b>$6</b></font>'; 
        re = new RegExp(rs,"g");
        str = str.replace(re, rr);
		str = str.replace(/\x20{2}/gm, '&nbsp; ');
        pres[i].innerHTML = "<pre>" + str + "</pre>";
    }
    //End JavaScript

    //cs
    if (pres[i].className == "cs") {
        var obj = pres[i].childNodes[0];
        if ((obj != null) && (obj.tagName == "TEXTAREA")) {
            str = obj.innerHTML;
        } else {
            str = pres[i].innerHTML;
        }

        r = new RegExp('</?(?!hr)\\w+( |>)','gi');
        var arr = str.match(r);
        if(arr != null) for(var n=0; n<arr.length; n++) {
            an = arr[n]; an = arr[n].replace('<','&lt;'); an = an.toLowerCase(); 
            str = str.replace(arr[n], an);
        }

        r1 = "(#if DBG[\\s\\S]+?#endif)";
        r2 = "(#[a-z ]*)";
        r3 = "(/// *&lt;[/\\w]+>)";
        r4 = "(/\\*[\\s\\S]*?\\*/)";
        r5 = "((?:http:)?//.*)";
        r6 = '(@?".*?")';
        r7 = "('.*?')";
        r8 = "\\b(" + CsKeywords + ")\\b";
        r9 = "\\b(" + CsClass + ")\\b";

        rs = r1 + '|' + r2 + '|' + r3 + '|' + r4 + '|' + r5 + '|' + r6 + '|' + r7 + '|' + r8 + '|' + r9;
        rr = '<font color=#808080>$1$2$3</font>' +
            '<font color=#008000>$4$5</font>' +
            '<font color=#A31515>$6$7</font>' +
            '<font color=#0000FF>$8</font>' +
            '<font color=#2B91AF>$9</font>'; 
        re = new RegExp(rs,"g");
        str = str.replace(re, rr);
		str = str.replace(/\x20{4}/gm, '&nbsp;   ');
        pres[i].innerHTML = "<pre>" + str + "</pre>";
    }
    //End cs

    //XML
    if (pres[i].className == "XML") {
        var obj = pres[i].childNodes[0];
        if ((obj != null) && (obj.tagName == "TEXTAREA")) {
            str = obj.innerHTML;
        } else {
            str = pres[i].innerHTML;
        }
        r1 = "(&lt;!--[\\s\\S]*?--&gt;)";  //<!-- -->
		r2 = '(&lt;\\?xml.+&gt;)';     //<?xml version=....
		r3 = '(&lt;\\!DOCTYPE.*&gt;)';     //<!DOCTYPE...
        r4 = '("[\\w\\W]*?")';                    // ""
		r5 = "( [\\w-]+(?==))";            //属性

        rs = r1 + '|' + r2 + '|' + r3 + "|" + r4 + "|" + r5;
        rr = '<font color=#008000>$1</font>' +
			'<font color=#909090>$2$3</font>' +
			'<font color=#CC3300>$5</font>';
		if (pres[i].id == "DTD") { 
		  rr += '<font color=#505050>$4</font>'; 
		} else {
          rr += '<font color=#0000FF>$4</font>'; 
		}
        re = new RegExp(rs,"gm");
        str = str.replace(re, rr);

		re = new RegExp('(&lt;/?(?![?!]).*?&gt;)', 'g');
		str = str.replace(re, '<font color=#663300>$1</font>');

		str = str.replace(/\x20{2}/gm, '&nbsp; ');
        
		if (pres[i].id == "DTD") { 
		  pres[i].innerHTML = "<pre><font color='#505050'>" + str + "</font></pre>"; 
		} else {
          pres[i].innerHTML = "<pre><font color='#0000FF'>" + str + "</font></pre>";
		}
    }
    //End XML
  }
//}
//document.execCommand("Stop");