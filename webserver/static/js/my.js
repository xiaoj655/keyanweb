/*function addBookmark(url,title) {
    if (window.sidebar){ 
        window.sidebar.addPanel(title, url,""); 
    } else if( document.all ){
        window.external.AddFavorite(url, title);
    } else if( window.opera && window.print ){
        return true;
    }
}
function AddFavorite(sURL, sTitle)
  {
	  try
	  {
		window.external.addFavorite(sURL, sTitle);
	  }
	  catch(e)
	  {
		try
		{
		  window.sidebar.addPanel(sTitle, sURL, "");
		}
		catch(e)
		{
		  alert("加入收藏失败，请使用Ctrl+D进行添加");
		}
	  }
	} 
*/
function funSelAll(){
    var selects=document.getElementsByName("selected");
    if(document.getElementsByName("All")[0].checked==true){
        for(var i=0;i<selects.length;i++){
            selects[i].checked=true;
        }
    }
    else{
        for(var i=0;i<selects.length;i++){
            selects[i].checked=false;
        }
    }
  }

function funSelOne(){
    var one=document.getElementsByName("selected");
    var all=document.getElementsByName("All")[0];
    var selCount=0;
    var unSelCount=0;
    for(var i=0;i<one.length;i++){
        if(one[i].checked==true){
            selCount++;
        }
        if(one[i].checked==false){
            unSelCount++;
        }
        if(selCount==one.length){
            all.checked=true;
        }
        if(unSelCount>0){
            all.checked=false;
        }
    }
  }
  

function checkSelected(){
    var selects=document.getElementsByName("selected");
    var selCount=0;
    for(var i=0;i<selects.length;i++){
        if(selects[i].checked==true){
            selCount++;
        }
    }
    if(selCount<1){
        alert("please select some sequences!");
        return false;
    }
    //alert("Right~~~");
    return true;
    //alert(selects.length);
    //alert(all[0].checked);
    //alert(selects[0].checked);
    
  }         


function checkArgument(){
    // Sequence input cannot be both null.
    if (document.getElementById("rec_seq").value == "" && document.getElementById("upload_ind").value == ""){
        alert("You must input the sequences in textarea or upload sequence file.");
        document.upload_form.rec_seq.focus();
        return false;
    }

    // Sequence input cannot be both true.
    if (document.getElementById("rec_seq").value != "" && document.getElementById("upload_ind").value != ""){
        alert("You cannot both input the sequences in textarea and upload sequence file.");
        document.upload_form.rec_seq.focus();
        return false;
    }

    // check the size of the upload file
    if (document.getElementById("upload_ind").value != ""){
        if  (checkFileSize("upload_ind") == false){
            document.upload_form.rec_seq.focus();
            return false; 
        }
    }
	
	// cutoff can be null.
    if (document.getElementById("cutoff").value == ""){
        alert("The number of iteration is necessary!");        
        return false;
    }
	
	email_addr = document.getElementById("Email").value.toLowerCase();
    if((email_addr !='') && (!isEmail(email_addr))){
        alert("The Email address is invalid!");
        return false;
    }
	
    //timedCount(c);
    return true;
}

function isEmail(str){
    var myRegExp = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    return myRegExp.test(str)
}

function setAutoForm() {
    document.forms[0].rec_seq.value = ">d3f3za_ d.144.1.0 (A:) automated matches {Cryptosporidium parvum [TaxId: 353152]}\n" +
		"DINQYYTLENTIGRGSWGEVKIAVQKGTRIRRAAKKIPKYFVEDVDRFKQEIEIMKSLDH\n"+
    "PNIIRLYETFEDNTDIYLVMELCTGGELFERVVHKRVFRESDAARIMKDVLSAVAYCHKL\n"+
    "NVAHRDLKPENFLFLTDSPDSPLKLIDFGLAARFKPGKMMRTKVGTPYYVSPQVLEGLYG\n"+
    "PECDEWSAGVMMYVLLCGYPPFSAPTDSEVMLKIREGTFTFPEKDWLNVSPQAESLIRRL\n"+
    "LTKSPKQRITSLQALEHEWFEKQLSSSPRNLL\n";
 
	document.getElementById("cutoff").value = "5";
}

function setAutoFormmix() {
    document.forms[0].rec_seq.value = ">d5cvmb1 d.15.1.1 (B:1-59) Ubiquitin {Human (Homo sapiens) [TaxId: 9606]}\n" +
    "MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDY\n";
 
	document.getElementById("cutoff").value = "5";
}

function setAutoFormmixhmmer() {
    document.forms[0].rec_seq.value = ">d3daha1 c.61.1.0 (A:5-165) automated matches {Burkholderia pseudomallei [TaxId: 320372]}\n" +
		"DGLMVFTGNANPALAQEVVKILGIPLGKAMVSRFSDGEIQVEIQENVRGKDVFVLQSTCA\n"+
    "PTNDNLMELMIMVDALKRASAGRITAAIPYFGYARQDRRPRSARVAISAKVVANMLEIAG\n"+
    "VERIITMDLHADQIQGFFDIPVDNIYATPILLGDLRKQNYP\n";
 
	document.getElementById("cutoff").value = "5";
}

function setAutoFormall() {
    document.forms[0].rec_seq.value = ">d1fnna2 c.37.1.20 (A:1-276) CDC6, N-domain {Pyrobaculum aerophilum [TaxId: 13773]}\n" +
		"AIVVDDSVFSPSYVPKRLPHREQQLQQLDILLGNWLRNPGHHYPRATLLGRPGTGKTVTL\n"+
    "RKLWELYKDKTTARFVYINGFIYRNFTAIIGEIARSLNIPFPRRGLSRDEFLALLVEHLR\n"+
    "ERDLYMFLVLDDAFNLAPDILSTFIRLGQEADKLGAFRIALVIVGHNDAVLNNLDPSTRG\n"+
    "IMGKYVIRFSPYTKDQIFDILLDRAKAGLAEGSYSEDILQMIADITGAQTPLDTNRGDAR\n"+
    "LAIDILYRSAYAAQQNGRKHIAPEDVRKSSKEVLFG\n";
 
	document.getElementById("cutoff").value = "5";
}

function setAutoFormallhmmer() {
    document.forms[0].rec_seq.value = ">d2b7ea1 a.159.2.1 (A:4-59) Pre-mRNA-processing protein PRP40 {Baker's yeast (Saccharomyces cerevisiae) [TaxId: 4932]}\n" +
		"EAEKEFITMLKENQVDSTWSFSRIISELGTRDPRYWMVDDDPLWKKEMFEKYLSNR\n";
 
	document.getElementById("cutoff").value = "5";
}
function setAutoFormnull() {
    document.forms[0].rec_seq.value = ">d1psya_ a.52.1.3 (A:) 2S albumin RicC3 {Castor bean (Ricinus communis) [TaxId: 3988]}\n" +
		"AEFMESKGEREGSSSQQCRQEVQRKDLSSCERYLRQSSSRRSTGEEVLRMPGDENQQQES\n"+
		"QQLQQCCNQVKQVRDECQCEAIKYIAEDQIQQGQLHGEESERVAQRAGEIVSSCGVRCMR\n"+
		"QTRTN\n";
 
	document.getElementById("cutoff").value = "5";
}
function setAutoFormnullhmmer() {
    document.forms[0].rec_seq.value = ">d1hypa_ a.52.1.1 (A:) Soybean hydrophobic protein {Soybean (Glycine max) [TaxId: 3847]}\n" +
		"PSCPDLSICLNILGGSLGTVDDCCALIGGLGDIEAIVCLCIQLRALGILNLNRNLQLILN\n"+
		"SCGRSYPSNATCPRT\n";
 
	document.getElementById("cutoff").value = "5";
}

function setAutoFormCOVID() {
    document.forms[0].rec_seq.value = ">6LU7_1|Chain A|main protease|Severe acute respiratory syndrome coronavirus 2 (2697049)\n" +
		"SGFRKMAFPSGKVEGCMVQVTCGTTTLNGLWLDDVVYCPRHVICTSEDMLNPNYEDLLIRKSNHNFLVQAGNVQLRVIGH\n"+
		"SMQNCVLKLKVDTANPKTPKYKFVRIQPGQTFSVLACYNGSPSGVYQCAMRPNFTIKGSFLNGSCGSVGFNIDYDCVSFC\n"+
		"YMHHMELPTGVHAGTDLEGNFYGPFVDRQTAQAAGTDTTITVNVLAWLYAAVINGDRWFLNRFTTTLNDFNLVAMKYNYE\n"+
		"PLTQDHVDILGPLSAQTGIAVLDMCASLKELLQNGMNGRTILGSALLEDEFTPFDVVRQCSGVTFQ";
 
	document.getElementById("cutoff").value = "5";
}

function checkFileExtend(id){
    // Check the upload file type, it must be txt or fasta type.
    var filePath = document.getElementById(id).value;

    if (filePath != ""){
        var re = /(\\+)/g;
        filePath = filePath.replace(re,"#");
        var path_split = filePath.split("#");
        var filename = path_split[path_split.length - 1];
        var name_split = filename.split(".");
        var extend = name_split[name_split.length - 1];
        var extendAllowed = "txt, fasta";
        var resIndex = extendAllowed.lastIndexOf(extend);
        if (resIndex >= 0)
            return true;
        else{
            alert("The upload file must be txt or fasta type.");
            document.upload_form.upload_ind.focus();
            return false;
        }
    }

    return true;
}

function showSequence(id) {
    var seq = document.getElementById(id).innerText;
    seqwindow = window.open("about:blank", id, "height=250, width=450,toolbar=no,enubar=no");
    seqwindow.document.write('<p style="word-wrap: break-word">' + '>' + seq +'</p>');
}

function checkFileSize(id){
    var maxsize = 1024 * 1024;
    var errMsg = 'The size of file should be less than 1M!';
    var browserCfg = {};
    var ua = window.navigator.userAgent;
    if (ua.indexOf("MSIE")>=1){
        browserCfg.ie = true;
    }else if(ua.indexOf("Firefox")>=1){
        browserCfg.firefox = true;
    }else if(ua.indexOf("Chrome")>=1){
        browserCfg.chrome = true;
    }
    var obj_file = document.getElementById(id);
    var filesize = 0;
    if(browserCfg.firefox || browserCfg.chrome ){
        filesize = obj_file.files[0].size;
    }else if(browserCfg.ie){
        var obj_img = document.getElementById('tempimg');
        obj_img.dynsrc=obj_file.value;
        filesize = obj_img.fileSize;
    }
    if(filesize>maxsize){
        alert(errMsg);
        return false;
    }
    return true;
}

var c=0
var t
function timedCount()
{
    document.getElementById('time').value=c;
    c=c+1;
    t=setTimeout("timedCount()",1000);
    document.getElementById('txt').style.visibility="visible";
    return true;
}
