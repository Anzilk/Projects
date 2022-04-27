odoo.define('pos_remove_orderlines.ClearAll', function(require){
    'use strict';


    var Registries = require('point_of_sale.Registries');
     const { Gui } = require('point_of_sale.Gui');
//     console.log("regestries", Registries)
  const PosComponent = require('point_of_sale.PosComponent');
  const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');

   class OrderLineClearALL extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
         async onClick() {
         const { confirmed } = await this.showPopup("ConfirmPopup", {
                       title: this.env._t('Clear Orders?'),
                       body: this.env._t('Are you sure you want to delete all orders from the cart?'),
                   });
               if(confirmed){
                const order = this.env.pos.get_order();
                console.log("order",order)
                 order.remove_orderline(order.get_orderlines());
                 }
//            if (orderline) {
//                const product = orderline.get_product();
//                const quantity = orderline.get_quantity();
//                this.showPopup('ProductInfoPopup', { product, quantity });
//            }
            }
            }

    OrderLineClearALL.template='OrderLineClearALL'
     ProductScreen.addControlButton({
        component: OrderLineClearALL,
        condition: () => true,
        position: ['before', 'SetFiscalPositionButton'],

    });


   Registries.Component.add(OrderLineClearALL);
     return OrderLineClearALL;

//
    });
