odoo.define('spreadsheet.spreadsheet', function (require) {
"use strict";

var FormRenderer = require('web.FormRenderer');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');

FormRenderer.include({
    events: _.extend({}, FormRenderer.prototype.events, {
    'click #bold': '_onclick',
            'dblclick ': '_onEditDblClick',
            'blur .tablecolumn': '_onBlur',
//            'blur .font size': '_selection_onblur'
        }),
    custom_events: _.extend({}, FormRenderer.prototype.custom_events, {
        button_clicked: '_onButtonClicked',
    }),

    _render: function () {
        return this._super.apply(this, arguments)
        },

    _onButtonClicked: function(ev) {
        var ButtonClass = ev.data.attrs.name;
        var mode = this.mode
        if(ButtonClass === 'spreadsheet'){
            var self = this
            ev.stopPropagation();
            this.$el.html(QWeb.render('template.spreadsheet'));
//            function for add tools
            function add_tools() {
             var toolbardiv = document.getElementById("toolbar");
             toolbardiv.style.height = '35px';
             var div_bold = document.getElementById("bold");
             div_bold.style.marginLeft = "100px";
             div_bold.style.marginTop = "-30px";
             div_bold.style.height = "35px";
//   selection tag for fontsize
                    var select = document.createElement("select");
                    console.log(select,"select tag")
                    select.name = "Font size";
                    select.id = "fontsize";
                    select.style.height = "35px";
                    select.style.width = "70px";
                    select.style.marginLeft = "10px";
                        var option = document.createElement("option");
                        option.value = 13;
                        option.text = 13;
                    for(var i=13; i<=96;i++)
                    {
                        var option = document.createElement("option");
                        option.value = i;
                        option.text = i;
                        select.appendChild(option);
                    }
                    toolbardiv.appendChild(select);
//input tag for bold
                    var input_bold = document.createElement("input");
                    input_bold.size = '4';
                    input_bold.value = "B";
                    input_bold.style.textAlign ="center";
                    input_bold.style.height ="30px";
                    input_bold.readOnly ="true";
                    input_bold.id="inputbold";
                    input_bold.style.backgroundColor ="#8e9490";
                    div_bold.appendChild(input_bold);
                    input_bold.hidden = true;

                    var input_unselect = document.createElement("input");
                    input_unselect.size = '4';
                    input_unselect.value = "B";
                    input_unselect.style.textAlign ="center";
                    input_unselect.style.height ="30px";
                    input_unselect.readOnly ="true"
                    input_unselect.id="boldunselect"
                    div_bold.appendChild(input_unselect);
//input tag for italics
                    var input_italics = document.createElement("input");
                    input_italics.size = '4';
                    input_italics.value = "I";
                    input_italics.readOnly ="true";
                    input_italics.id="inputitalics";
                    input_italics.style.backgroundColor ="#8e9490";
                    input_italics.style.height ="30px";
                    input_italics.style.textAlign ="center";
                    div_bold.appendChild(input_italics);
                    input_italics.hidden = true;

                    var input_unselect_italics = document.createElement("input");
                    input_unselect_italics.size = '4';
                    input_unselect_italics.value = "I";
                    input_unselect_italics.readOnly ="true";
                    input_unselect_italics.id="unselectitalics";
                    input_unselect_italics.style.textAlign ="center";
                    input_unselect_italics.style.height ="30px";
                    div_bold.appendChild(input_unselect_italics);

//input tag for underline
                    var input_underline = document.createElement("input");
                    input_underline.size = '4';
                    input_underline.value = "U";
                    input_underline.readOnly ="true";
                    input_underline.id="inputunderline";
                    input_underline.style.backgroundColor ="#8e9490";
                    input_underline.style.height ="30px";
                    input_underline.style.textAlign ="center";
                    div_bold.appendChild(input_underline);
                    input_underline.hidden = true;

                    var input_unselect_underline = document.createElement("input");
                    input_unselect_underline.size = '4';
                    input_unselect_underline.value = "U";
                    input_unselect_underline.readOnly ="true";
                    input_unselect_underline.id="unselectunderline";
                    input_unselect_underline.style.textAlign ="center";
                    input_unselect_underline.style.height ="30px";
                    div_bold.appendChild(input_unselect_underline);
//input tag for left alignment
                    var input_left_align = document.createElement("i");
                    input_left_align.id="inputleftalign";
                    input_left_align.className="fa fa-align-left";
                    input_left_align.style.backgroundColor ="#8e9490";
                    input_left_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_left_align);
                    input_left_align.hidden = true;

                    var input_unselect_left_align = document.createElement("i");
                    input_unselect_left_align.className="fa fa-align-left";
                    input_unselect_left_align.id="unselectleftalign";
                    input_unselect_left_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_unselect_left_align);

 //input tag for center alignment
                    var input_center_align = document.createElement("i");
                    input_center_align.id="inputcenteralign";
                    input_center_align.className="fa fa-align-center";
                    input_center_align.style.backgroundColor ="#8e9490";
                    input_center_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_center_align);
                    input_center_align.hidden = true;

                    var input_unselect_center_align = document.createElement("i");
                    input_unselect_center_align.className="fa fa-align-center";
                    input_unselect_center_align.id="unselectcenteralign";
                    input_unselect_center_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_unselect_center_align);

 //input tag for right alignment
                    var input_right_align = document.createElement("i");
                    input_right_align.id="inputrightalign";
                    input_right_align.className="fa fa-align-right";
                    input_right_align.style.backgroundColor ="#8e9490";
                    input_right_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_right_align);
                    input_right_align.hidden = true;

                    var input_unselect_right_align = document.createElement("i");
                    input_unselect_right_align.className="fa fa-align-right";
                    input_unselect_right_align.id="unselectrightalign";
                    input_unselect_right_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_unselect_right_align);


  //input tag for top alignment
                    var input_top_align = document.createElement("i");
                    input_top_align.id="inputtopalign";
                    input_top_align.className="fa fa-align-left fa-rotate-180";
                    input_top_align.style.backgroundColor ="#8e9490";
                    input_top_align.style.paddingRight= "20px";
                    div_bold.appendChild(input_top_align);
                    input_top_align.hidden = true;

                    var input_unselect_top_align = document.createElement("i");
                    input_unselect_top_align.className="fa fa-align-left fa-rotate-180";
                    input_unselect_top_align.id="unselecttopalign";
                    input_unselect_top_align.style.paddingRight= "20px";
                    div_bold.appendChild(input_unselect_top_align);

   //input tag for vertical center alignment
                    var input_ver_center_align = document.createElement("i");
                    input_ver_center_align.id="inputvercenteralign";
                    input_ver_center_align.className="fa fa-align-justify";
                    input_ver_center_align.style.backgroundColor ="#8e9490";
                    input_ver_center_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_ver_center_align);
                    input_ver_center_align.hidden = true;

                    var input_unselect_ver_center_align = document.createElement("i");
                    input_unselect_ver_center_align.className="fa fa-align-justify";
                    input_unselect_ver_center_align.id="unselectvercenteralign";
                    input_unselect_ver_center_align.style.paddingLeft= "10px";;
                    div_bold.appendChild(input_unselect_ver_center_align);


//input tag for bottom alignment
                    var input_bottom_align = document.createElement("i");
                    input_bottom_align.id="inputbottomalign";
                    input_bottom_align.className="fa fa-align-left ";
                    input_bottom_align.style.backgroundColor ="#8e9490";
                    input_bottom_align.style.paddingLeft= "10px";
                    div_bold.appendChild(input_bottom_align);
                    input_bottom_align.hidden = true;

                    var input_unselect_bottom_align = document.createElement("i");
                    input_unselect_bottom_align.className="fa fa-align-left ";
                    input_unselect_bottom_align.id="unselectbottomalign";
                    input_unselect_bottom_align.style.paddingLeft= "10px";;
                    div_bold.appendChild(input_unselect_bottom_align);
                     }
//                     function for create a  table with spreadsheet values
            function addTable(row, column) {
                var args = [
                    self.allFieldWidgets["document.document_1"][0].value,
                    self.allFieldWidgets["document.document_1"][1].value.res_id,
                ];

                self._rpc({
                    model: 'ir.attachment',
                    method: 'get_doc_file_data',
                    args: args,
                }).then(function (result) {
                var row_id;
                var col_id;
                var id;
                    var k = 65;
                    var val = 1;
                    var myTableDiv = document.getElementById("myDynamicTable");
                    var table = document.createElement('TABLE');
                    table.border = '1';
                    var tableBody = document.createElement('TBODY');
                    table.appendChild(tableBody);

                for (var i = 0; i < row; i++) {
                    var tr = document.createElement('TR');
                    tableBody.appendChild(tr);

                    for (var j = 0; j < column; j++) {
                        var td = document.createElement('TD');
                        const attribute = document.createAttribute("class");
                        attribute.value = "tablecolumn";
                        td.setAttributeNode(attribute);


                        td.width = '90px';
                        td.height = '30px';
                        td.dataset.row = i;
                        td.dataset.column = j;
                        row_id = i.toString();
                        col_id = j.toString();
                        id = row_id+col_id
                        td.id = id
                        if(i == 0 || j == 0){
                            td .style.textAlign = "center";
		                    td .style.backgroundColor = "#F5F5F5";
                        }
                        if(i == 0 && j != 0){
		                    var str = String.fromCharCode(k);
                            td.appendChild(document.createTextNode(str));
                            k += 1;
                        }
                        if(j == 0 && i !=0){
                            td.appendChild(document.createTextNode(val));
                            val += 1;
                        }
                        var row_len = result[0].length
                        var col_len = result[0][0].length
                        if(i != 0 && j != 0){
                            for(var k = 0; k < row_len; k++){
                                for(var l = 0; l < col_len; l++){
                                    if(k+1 === i && l+1 === j && result[0][k][l] != null){
                                        td.appendChild(document.createTextNode(result[0][k][l]));
                                        td .style.fontSize =result[4][k][l]+'px';
//                                        td .style.color ='FF000000'
//                                        console.log(result[0][k][l],"value")
//                                        console.log(result[5][k][l],"align")
//                                        console.log(td,"td")
                                        if(result[1][k][l] ==1){
                                        td .style.fontWeight ="bold";
                                        }
                                        if(result[2][k][l] ==1){
                                        td .style.fontStyle ="italic";
                                        }
                                        if(result[3][k][l] =='single'){
                                        td .style.textDecoration ="underline";
                                        }
                                        if(result[5][k][l] =='center'){
                                        td .style.textAlign = "center";
                                        }
                                        if(result[5][k][l] =='left'){
                                        td .style.textAlign = 'left';
                                        }
                                        if(result[5][k][l] =='right'){
                                        td .style.textAlign = 'right';
                                        }
                                        if(result[6][k][l] =='center'){
                                        td .style.verticalAlign = 'middle';
                                        }
                                        if(result[6][k][l] =='top'){
                                        td .style.verticalAlign = 'top';
                                        }
                                        if(result[6][k][l] =='bottom'){
                                        td .style.verticalAlign = 'bottom';
                                        }
                                    }
                                }
                            }
                        }
                        tr.appendChild(td);
                    }
                }
                myTableDiv.appendChild(table);
            });
        }
        add_tools();
        addTable(30,25);
        }
    },

    _onEditDblClick: function(ev) {
    console.log(ev,"ev")
    console.log(ev.target.style.fontWeight,"td current")
    if(ev.target.classList[0] =="tablecolumn")
    {
    const att = document.createAttribute("contentEditable");
        var $tag = $(ev.target)[0]
        att.value = "true";
//        setAttributes($tag, {"contentEditable": "true", "class": "tablecoloumn"});
        $tag.setAttributeNode(att);
        }
        var font = ev.target.style.fontSize;
        font = font.slice(0, -2);
        console.log(font ,"after slice")
       $('#fontsize').val(font);
       if(font == '')
       {
       $('#fontsize').val(13);
       }
    var bold = document.getElementById('inputbold')
     var not_bold = document.getElementById("boldunselect");
     var not_italics = document.getElementById("unselectitalics");
    var italics = document.getElementById("inputitalics");
    var not_underline = document.getElementById("unselectunderline");
    var underline = document.getElementById("inputunderline");
    var not_left_align = document.getElementById("unselectleftalign");
    var left_align = document.getElementById("inputleftalign");
    var not_center_align = document.getElementById("unselectcenteralign");
    var center_align = document.getElementById("inputcenteralign");
    var not_right_align = document.getElementById("unselectrightalign");
    var right_align = document.getElementById("inputrightalign");
     var not_top_align = document.getElementById("unselecttopalign");
    var top_align = document.getElementById("inputtopalign");
    var not_ver_center_align = document.getElementById("unselectvercenteralign");
    var ver_center_align = document.getElementById("inputvercenteralign");
    var not_bottom_align = document.getElementById("unselectbottomalign");
    var bottom_align = document.getElementById("inputbottomalign");
//    cell already have formats then tools are selected
    if(ev.target.style.fontWeight == "bold")
    {
       bold.hidden = false;
       not_bold.hidden = true;
    }
    else
    {
    bold.hidden = true;
       not_bold.hidden = false;
    }
     if(ev.target.style.fontStyle == "italic")
    {
       italics.hidden = false;
       not_italics.hidden = true;
    }
    else
    {
    italics.hidden = true;
       not_italics.hidden = false;
    }
    if(ev.target.style.textDecoration == "underline")
    {
       underline.hidden = false;
       not_underline.hidden = true;
    }
    else
    {
     underline.hidden = true;
       not_underline.hidden = false;
    }

     if(ev.target.style.textAlign == "left")
    {
       left_align.hidden = false;
       not_left_align.hidden = true;
    }
    else
    {
     left_align.hidden = true;
       not_left_align.hidden = false;
    }
     if(ev.target.style.textAlign == "center")
    {
       center_align.hidden = false;
       not_center_align.hidden = true;
    }
    else
    {
     center_align.hidden = true;
       not_center_align.hidden = false;
    }
    if(ev.target.style.textAlign == "right")
    {
       right_align.hidden = false;
       not_right_align.hidden = true;
    }
    else
    {
     right_align.hidden = true;
       not_right_align.hidden = false;
    }



    if(ev.target.style.verticalAlign == "top")
    {
       top_align.hidden = false;
       not_top_align.hidden = true;
    }
    else
    {
     top_align.hidden = true;
       not_top_align.hidden = false;
    }
     if(ev.target.style.verticalAlign == "middle")
    {
       ver_center_align.hidden = false;
       not_ver_center_align.hidden = true;
    }
    else
    {
     ver_center_align.hidden = true;
       not_ver_center_align.hidden = false;
    }
     if(ev.target.style.verticalAlign == "bottom")
    {
       bottom_align.hidden = false;
       not_bottom_align.hidden = true;
    }
    else
    {
     bottom_align.hidden = true;
       not_bottom_align.hidden = false;
    }




    },

    _onBlur:function(event){
    console.log(event,"event")
    var row = event.target.attributes[1].nodeValue
    var column = event.target.attributes[2].nodeValue
    var changed_value = event.target.textContent
    var orginal_fontsize = document.getElementById('fontsize').value
//    to set bold  to coloumn value on bold tool select
    var selectbold = document.getElementById('inputbold')
    var boldvalue
    if (selectbold.hidden == false)
    {
    event.target.style.fontWeight ="bold"
    boldvalue =true
    }
    else
    {
    event.target.style.fontWeight ="normal"
    boldvalue =false
    }

//    to set italics  to coloumn value on italics tool select
    var select_italics = document.getElementById('inputitalics')
    var italics_value
    if (select_italics.hidden == false)
    {
    event.target.style.fontStyle ="italic"
    italics_value =true
    }
    else
    {
    event.target.style.fontStyle ="normal"
    italics_value =false
    }
//   to set underline  to coloumn value on underline tool select
    var select_underline = document.getElementById('inputunderline')
    var underline_value
    if (select_underline.hidden == false)
    {
    event.target.style.textDecoration ="underline"
    underline_value ="single"
    }
    else
    {
    event.target.style.textDecoration ="none"
    underline_value = "none"
    }

//       to set horizontal align   to coloumn value on horizontal align tools select
    var select_left_align = document.getElementById('inputleftalign')
    var select_center_align = document.getElementById('inputcenteralign')
    var select_right_align = document.getElementById('inputrightalign')
    var align_value
    if (select_left_align.hidden == false)
    {
    event.target.style.textAlign ="left"
    align_value ="left"
    }
    else if(select_center_align.hidden == false)
    {
    event.target.style.textAlign ="center"
    align_value = "center"
    }
    else if (select_right_align.hidden == false)
    {
    event.target.style.textAlign ="right"
    align_value = "right"
    }
    else
    {
    event.target.style.textAlign ="left"
    align_value ="left"
    }

    //       to set vertical align   to coloumn value on vertical align tools select
    var select_top_align = document.getElementById('inputtopalign')
    var select_ver_center_align = document.getElementById('inputvercenteralign')
    var select_bottom_align = document.getElementById('inputbottomalign')
    var vertical_align_value
    if (select_top_align.hidden == false)
    {
    event.target.style.verticalAlign ="top"
    vertical_align_value ="top"
    }
    else if(select_ver_center_align.hidden == false)
    {
    event.target.style.verticalAlign ="middle"
    vertical_align_value = "center"
    }
    else if (select_bottom_align.hidden == false)
    {
    event.target.style.verticalAlign ="bottom"
    vertical_align_value = "bottom"
    }
    else
    {
    event.target.style.verticalAlign ="bottom"
    vertical_align_value ="bottom"
    }
    var fontsize = orginal_fontsize+'px'
    event.target.style.fontSize= fontsize;
        var docId = this.allFieldWidgets["document.document_1"][1].value.res_id
        this._rpc({
               model: 'ir.attachment',
               method: 'add_data_spreadsheet',
               args: [changed_value,docId, row, column,
                orginal_fontsize, boldvalue, italics_value, underline_value,
                 align_value, vertical_align_value ],
            }).then(function (result) {
            });

    },
        _onclick:function(event){
    var not_bold = document.getElementById("boldunselect");
    var bold = document.getElementById("inputbold");
    if(event.target.id == 'boldunselect')
    {
    not_bold.hidden = true;
    bold.hidden = false;
    }
    if(event.target.id == 'inputbold')
    {
    not_bold.hidden = false;
    bold.hidden = true;
    }


 var not_italics = document.getElementById("unselectitalics");
    var italics = document.getElementById("inputitalics");
    if(event.target.id == 'unselectitalics')
    {
    not_italics.hidden = true;
    italics.hidden = false;
    }
    if(event.target.id == 'inputitalics')
    {
    not_italics.hidden = false;
    italics.hidden = true;
    }

    var not_underline = document.getElementById("unselectunderline");
    var underline = document.getElementById("inputunderline");
    if(event.target.id == 'unselectunderline')
    {
    not_underline.hidden = true;
    underline.hidden = false;
    }
    if(event.target.id == 'inputunderline')
    {
    not_underline.hidden = false;
    underline.hidden = true;
    }

     var not_left_align = document.getElementById("unselectleftalign");
    var left_align = document.getElementById("inputleftalign");
    var not_center_align = document.getElementById("unselectcenteralign");
    var center_align = document.getElementById("inputcenteralign");
    var not_right_align = document.getElementById("unselectrightalign");
    var right_align = document.getElementById("inputrightalign");

    if(event.target.id == 'unselectleftalign')
    {
    not_left_align.hidden = true;
    left_align.hidden = false;
    not_center_align.hidden = false;
    center_align.hidden = true;
    not_right_align.hidden = false;
    right_align.hidden = true
    }
    if(event.target.id == 'inputleftalign')
    {
    not_left_align.hidden = false;
    left_align.hidden = true;
    }


    if(event.target.id == 'unselectcenteralign')
    {
    not_center_align.hidden = true;
    center_align.hidden = false;
    not_left_align.hidden = false;
    left_align.hidden = true;
    not_right_align.hidden = false;
    right_align.hidden = true
    }
    if(event.target.id == 'inputcenteralign')
    {
    not_center_align.hidden = false;
    center_align.hidden = true;
    }


     if(event.target.id == 'unselectrightalign')
    {
    not_right_align.hidden = true;
    right_align.hidden = false;
    not_left_align.hidden = false;
    left_align.hidden = true;
    not_center_align.hidden = false;
    center_align.hidden = true
    }
    if(event.target.id == 'inputrightalign')
    {
    not_right_align.hidden = false;
    right_align.hidden = true;
    }

     var not_top_align = document.getElementById("unselecttopalign");
    var top_align = document.getElementById("inputtopalign");
    var not_ver_center_align = document.getElementById("unselectvercenteralign");
    var ver_center_align = document.getElementById("inputvercenteralign");
    var not_bottom_align = document.getElementById("unselectbottomalign");
    var bottom_align = document.getElementById("inputbottomalign");

    if(event.target.id == 'unselecttopalign')
    {
    not_top_align.hidden = true;
    top_align.hidden = false;
    not_ver_center_align.hidden = false;
    ver_center_align.hidden = true;
    not_bottom_align.hidden = false;
    bottom_align.hidden = true
    }
    if(event.target.id == 'inputtopalign')
    {
    not_top_align.hidden = false;
    top_align.hidden = true;
    }
    if(event.target.id == 'unselectvercenteralign')
    {
    not_ver_center_align.hidden = true;
    ver_center_align.hidden = false;
    not_top_align.hidden = false;
    top_align.hidden = true;
    not_bottom_align.hidden = false;
    bottom_align.hidden = true
    }
    if(event.target.id == 'inputvercenteralign')
    {
     not_ver_center_align.hidden = false;
    ver_center_align.hidden = true;
    }
     if(event.target.id == 'unselectbottomalign')
    {
    not_bottom_align.hidden = true;
    bottom_align.hidden = false;
    not_top_align.hidden = false;
    top_align.hidden = true;
    not_ver_center_align.hidden = false;
    ver_center_align.hidden = true
    }
    if(event.target.id == 'inputbottomalign')
    {
    not_bottom_align.hidden = false;
    bottom_align.hidden = true;
    }
    },
});
});