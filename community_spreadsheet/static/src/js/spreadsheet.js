odoo.define('spreadsheet.spreadsheet', function (require) {
"use strict";

var FormRenderer = require('web.FormRenderer');
var core = require('web.core');
var QWeb = core.qweb;
var rpc = require('web.rpc');

FormRenderer.include({
    events: _.extend({}, FormRenderer.prototype.events, {
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
            function addnewTable() {
             var myTableDiv1 = document.getElementById("myDynamicTable");
            console.log("hii")
//            var table1 = document.createElement('TABLE');
//                    table1.border = '1';
//                    var tableBody1 = document.createElement('TBODY');
//                    table1.appendChild(tableBody1);
//                    var tr1 = document.createElement('TR');
//                    tableBody1.appendChild(tr1);
//                    var td1 = document.createElement('TD');
//                     tr1.appendChild(td1);
//                     td1.value = '1ufkdl'
//                     td1.width = '90px';
//                        td1.height = '30px';
//                        myTableDiv1.appendChild(table1);
//                        td1.id = "font"

                    var select = document.createElement("select");
                    select.name = "Font size";
                    select.id = "font size"
                     const attribute = document.createAttribute("style");
                        attribute.value = "width:90px";
                        select.setAttributeNode(attribute);
                        var option = document.createElement("option");
                        option.value = 13;
                        option.text = 13;
                    for(var i=6; i<=96;i++)
                    {
                        var option = document.createElement("option");
                        option.value = i;
                        option.text = i;
                        select.appendChild(option);
                    }
                    myTableDiv1.appendChild(select);
                     }
                     console.log(this,"thisnew")
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
                        var row_len = result.length
                        var col_len = result[0].length
                        if(i != 0 && j != 0){
                            for(var k = 0; k < row_len; k++){
                                for(var l = 0; l < col_len; l++){
                                    if(k+1 === i && l+1 === j){
                                        td.appendChild(document.createTextNode(result[k][l]));
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
        addnewTable();
        addTable(30,25);
        }
    },

    _onEditDblClick: function(ev) {
    console.log(ev.target,"ev")
    console.log(ev.target.classList[0],"ev")
    const att = document.createAttribute("contentEditable");
        var $tag = $(ev.target)[0]
        att.value = "true";
//        setAttributes($tag, {"contentEditable": "true", "class": "tablecoloumn"});
        $tag.setAttributeNode(att);
//        if($(ev.target)[0].localName === 'td'){
//            $($tag).replaceWith(`<input class="edit_td" value="${$tag.innerText}">${$(self).text()}</input>`);
//        }
//            function setAttributes(el, attrs) {
//              for(var key in attrs) {
//                el.setAttribute(key, attrs[key]);
//              }
//            }
    },

    _onBlur:function(event){
    console.log(this,"this")
    console.log(event,"event")
    console.log(event.target,"target")
//    const attribute = document.createAttribute("style");
//                        attribute.value = "font-size:";
//                        event.target.setAttributeNode(attribute);
    var row = event.target.attributes[1].nodeValue
    var column = event.target.attributes[2].nodeValue
    var changed_value = event.target.textContent
    var fontsize = document.getElementById('font size').value
    fontsize = fontsize+'px'
    console.log(fontsize,"fontsize")
    event.target.style["font-size"]= fontsize;
//    setAttributes(event.target, {"style": fontsize});
//     function setAttributes(el, attrs) {
//     console.log("hiiiiiiii")
//              for(var key in attrs) {
//                el.setAttribute(key, attrs[key]);
//              }
//            }

    console.log(row,"row",column,"col",changed_value,"changed_value")
//    console.log(event.target.attributes[0].nodeValue,"row")
//    console.log(event.target.attributes[1].nodeValue,"coloumn")
//    console.log(event.target.textContent,"value")

//    var value = document.getElementById(event.target.attributes[2]).value
//    console.log(a,"values")
//    var row_limit;
//    var col_limit;
//    var id;
//    var a;
//    var array = [];
//
//    for (var i = 0; i < 30; i++) {
//    for(var j=0;j<25;j++)
//    {
//     row_limit = i.toString();
//    col_limit = j.toString();
//    id = row_limit+col_limit
////   console.log(id,"rowcol")
//
//    a = document.getElementById(id).innerHTML
////    console.log(a,"td")
//     array[i,j] = a
//     console.log("index",i,j,"array" ,array[i,j]);
//
//    }
//
//    }
//    console.log("array element", array)

//        var inputValue = $('.edit_td').val();
//        console.log("inputvalue", inputvalue)
//        var inputColumn = $('.edit_td')[0].nextSibling.attributes[3].value - 1
//        console.log(inputColumn,"column")
//        var inputRow = $('.edit_td')[0].nextSibling.attributes[2].value
        var docId = this.allFieldWidgets["document.document_1"][1].value.res_id
        console.log(this.allFieldWidgets[0],"docid")
        this._rpc({
               model: 'ir.attachment',
               method: 'add_data_spreadsheet',
               args: [changed_value,docId, row, column ],
            }).then(function (result) {
            console.log(result,"result")
//                if (result === true) {
////                    location.reload();
//                    console.log('Passs')
//                }
//                else{
//                    console.log("Error")
//                    }
            });

    },
//    _selection_onblur:function(event){
//    console.log("hii this",this)
//    },


});

});