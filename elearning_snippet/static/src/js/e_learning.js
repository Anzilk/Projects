odoo.define('elearning_snippet.s_dynamic_snippet_elearning', function(require){
    'use strict';

    var core = require('web.core');
var sAnimation = require('website.content.snippets.animation');
var _t = core._t;
var ajax = require('web.ajax');
console.log("hello")


   sAnimation.registry.latest_courses = sAnimation.Class.extend({
selector : '.s_snippet_elearning',
start: function(){
console.log("hii")
    var self = this;
    console.log(this)
    ajax.jsonRpc('/elearning_snippet/elearning', 'call', {})
    .then(function (data) {
    console.log("dddd",data)
    if(data){
          self.$target.append(data);
        }
    });
},
});
});