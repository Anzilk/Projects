odoo.define('pos_remove_orderlines.removeline', function(require){
    'use strict';

//
    var models = require('point_of_sale.models');
    console.log("models", models)
    var Registries = require('point_of_sale.Registries');
     console.log("regestries", Registries)
    var OrderWidget = require('point_of_sale.OrderWidget');
    console.log("orderwidget", OrderWidget)
    var Orderline = require('point_of_sale.Orderline');

    var _super_orderline = models.Orderline.prototype;
    console.log("super", _super_orderline)
//    console.log(models.Orderline,"hyuioyt")
//    console.log(models.Orderline.extend,"gggggg")
    const deleteorderline = (Orderline) =>
        class extends Orderline {
        removelines() {


            this.trigger('numpad-click-input',{ key: 'Backspace' });
            this.trigger('numpad-click-input',{ key: 'Backspace' });
//            console.log("tyguhijok")
        }
    };
    Registries.Component.extend(Orderline,deleteorderline);
     return Orderline;

    });