

# 如
## return

- https://docs.stripe.com/payments/checkout/how-checkout-works
- https://docs.stripe.com/payments/accept-a-payment
- 支付服务重定向让浏览器发起的请求，参数在query里。
	- 就session_id参数，需要用sdk再调用api获取session信息

- payment_status
	- unpaid
	- paid
	- no_payment_required
- status
	- open
	- complete
	- expired  24 小时后过期

### 未支付

```json
{
  "adaptive_pricing": {
    "enabled": true
  },
  "after_expiration": null,
  "allow_promotion_codes": false,
  "amount_subtotal": 400,
  "amount_total": 400,
  "automatic_tax": {
    "enabled": false,
    "liability": null,
    "provider": "",
    "status": ""
  },
  "billing_address_collection": "",
  "cancel_url": "",
  "client_reference_id": "",
  "client_secret": "cs_test_xxx",
  "collected_information": null,
  "consent": null,
  "consent_collection": null,
  "created": 1774256096,
  "currency": "cny",
  "currency_conversion": null,
  "customer": null,
  "customer_creation": "if_required",
  "customer_details": {
    "address": null,
    "email": "user@qq.com",
    "name": "",
    "phone": "",
    "tax_exempt": "none",
    "tax_ids": null
  },
  "customer_email": "",
  "custom_fields": [],
  "custom_text": {
    "after_submit": null,
    "shipping_address": null,
    "submit": null,
    "terms_of_service_acceptance": null
  },
  "discounts": [],
  "expires_at": 1774342496,
  "id": "cs_test_wwww",
  "invoice": null,
  "invoice_creation": {
    "enabled": false,
    "invoice_data": {
      "account_tax_ids": null,
      "custom_fields": null,
      "description": "",
      "footer": "",
      "issuer": null,
      "metadata": {},
      "rendering_options": null
    }
  },
  "line_items": {
    "has_more": false,
    "url": "/v1/checkout/sessions/cs_test_wwww/line_items",
    "total_count": 0,
    "data": [
      {
        "amount_discount": 0,
        "amount_subtotal": 400,
        "amount_tax": 0,
        "amount_total": 400,
        "currency": "cny",
        "description": "xxxxxxx",
        "discounts": null,
        "id": "li_1TE4GCGLfJRXFUwHtBrAZXd2",
        "object": "item",
        "price": {
          "active": false,
          "billing_scheme": "per_unit",
          "created": 1774256096,
          "currency": "cny",
          "currency_options": null,
          "custom_unit_amount": null,
          "deleted": false,
          "id": "price_1TE4GCGLfJRXFUwHxkqymMMN",
          "livemode": false,
          "lookup_key": "",
          "metadata": {},
          "nickname": "",
          "object": "price",
          "product": {
            "active": false,
            "created": 0,
            "default_price": null,
            "deleted": false,
            "description": "",
            "id": "prod_UCSHzzI5XfUkEV",
            "images": null,
            "livemode": false,
            "marketing_features": null,
            "metadata": null,
            "name": "",
            "object": "",
            "package_dimensions": null,
            "shippable": false,
            "statement_descriptor": "",
            "tax_code": null,
            "type": "",
            "unit_label": "",
            "updated": 0,
            "url": ""
          },
          "recurring": null,
          "tax_behavior": "unspecified",
          "tiers": null,
          "tiers_mode": "",
          "transform_quantity": null,
          "type": "one_time",
          "unit_amount": 400,
          "unit_amount_decimal": "400"
        },
        "quantity": 1,
        "taxes": null
      }
    ]
  },
  "livemode": false,
  "locale": "",
  "metadata": {
    "out_trade_no": "1774256092603328600"
  },
  "mode": "payment",
  "object": "checkout.session",
  "optional_items": null,
  "origin_context": "",
  "payment_intent": {
    "amount": 0,
    "amount_capturable": 0,
    "amount_details": null,
    "amount_received": 0,
    "application": null,
    "application_fee_amount": 0,
    "automatic_payment_methods": null,
    "canceled_at": 0,
    "cancellation_reason": "",
    "capture_method": "",
    "client_secret": "",
    "confirmation_method": "",
    "created": 0,
    "currency": "",
    "customer": null,
    "description": "",
    "excluded_payment_method_types": null,
    "id": "pi_3TE4GJGLfJRXFUwH1Ylk7jjo",
    "last_payment_error": null,
    "latest_charge": null,
    "livemode": false,
    "metadata": null,
    "next_action": null,
    "object": "",
    "on_behalf_of": null,
    "payment_method": null,
    "payment_method_configuration_details": null,
    "payment_method_options": null,
    "payment_method_types": null,
    "presentment_details": null,
    "processing": null,
    "receipt_email": "",
    "review": null,
    "setup_future_usage": "",
    "shipping": null,
    "source": null,
    "statement_descriptor": "",
    "statement_descriptor_suffix": "",
    "status": "",
    "transfer_data": null,
    "transfer_group": ""
  },
  "payment_link": null,
  "payment_method_collection": "if_required",
  "payment_method_configuration_details": {
    "id": "pmc_1Qr8SvGLfJRXFUwHq6Og9DnY",
    "parent": ""
  },
  "payment_method_options": {
    "acss_debit": null,
    "affirm": null,
    "afterpay_clearpay": null,
    "alipay": null,
    "amazon_pay": null,
    "au_becs_debit": null,
    "bacs_debit": null,
    "bancontact": null,
    "boleto": null,
    "card": null,
    "cashapp": null,
    "customer_balance": null,
    "eps": null,
    "fpx": null,
    "giropay": null,
    "grabpay": null,
    "ideal": null,
    "kakao_pay": null,
    "klarna": null,
    "konbini": null,
    "kr_card": null,
    "link": null,
    "mobilepay": null,
    "multibanco": null,
    "naver_pay": null,
    "oxxo": null,
    "p24": null,
    "payco": null,
    "paynow": null,
    "paypal": null,
    "pix": null,
    "revolut_pay": null,
    "samsung_pay": null,
    "sepa_debit": null,
    "sofort": null,
    "swish": null,
    "us_bank_account": null
  },
  "payment_method_types": [
    "card",
    "alipay",
    "wechat_pay",
    "link"
  ],
  "payment_status": "unpaid",
  "permissions": null,
  "phone_number_collection": {
    "enabled": false
  },
  "presentment_details": null,
  "recovered_from": "",
  "redirect_on_completion": "always",
  "return_url": "http://localhost:8081/stripe_return?session_id={CHECKOUT_SESSION_ID}",
  "saved_payment_method_options": null,
  "setup_intent": null,
  "shipping_address_collection": null,
  "shipping_cost": null,
  "shipping_options": [],
  "status": "open",
  "submit_type": "",
  "subscription": null,
  "success_url": "",
  "tax_id_collection": null,
  "total_details": {
    "amount_discount": 0,
    "amount_shipping": 0,
    "amount_tax": 0,
    "breakdown": null
  },
  "ui_mode": "embedded",
  "url": "",
  "wallet_options": null
}
```


### 支付

```json
{
  "adaptive_pricing": {
    "enabled": true
  },
  "after_expiration": null,
  "allow_promotion_codes": false,
  "amount_subtotal": 400,
  "amount_total": 400,
  "automatic_tax": {
    "enabled": false,
    "liability": null,
    "provider": "",
    "status": ""
  },
  "billing_address_collection": "",
  "cancel_url": "",
  "client_reference_id": "",
  "client_secret": "",
  "collected_information": null,
  "consent": null,
  "consent_collection": null,
  "created": 1774256386,
  "currency": "cny",
  "currency_conversion": null,
  "customer": null,
  "customer_creation": "if_required",
  "customer_details": {
    "address": {
      "city": "",
      "country": "",
      "line1": "",
      "line2": "",
      "postal_code": "",
      "state": ""
    },
    "email": "user@qq.com",
    "name": "",
    "phone": "",
    "tax_exempt": "none",
    "tax_ids": []
  },
  "customer_email": "",
  "custom_fields": [],
  "custom_text": {
    "after_submit": null,
    "shipping_address": null,
    "submit": null,
    "terms_of_service_acceptance": null
  },
  "discounts": [],
  "expires_at": 1774342786,
  "id": "cs_test_www",
  "invoice": null,
  "invoice_creation": {
    "enabled": false,
    "invoice_data": {
      "account_tax_ids": null,
      "custom_fields": null,
      "description": "",
      "footer": "",
      "issuer": null,
      "metadata": {},
      "rendering_options": null
    }
  },
  "line_items": {
    "has_more": false,
    "url": "/v1/checkout/sessions/cs_test_www/line_items",
    "total_count": 0,
    "data": [
      {
        "amount_discount": 0,
        "amount_subtotal": 400,
        "amount_tax": 0,
        "amount_total": 400,
        "currency": "cny",
        "description": "xxx",
        "discounts": null,
        "id": "li_1TE4KsGLfJRXFUwH7YIOjHpg",
        "object": "item",
        "price": {
          "active": false,
          "billing_scheme": "per_unit",
          "created": 1774256386,
          "currency": "cny",
          "currency_options": null,
          "custom_unit_amount": null,
          "deleted": false,
          "id": "price_1TE4KsGLfJRXFUwHL1Xrht7t",
          "livemode": false,
          "lookup_key": "",
          "metadata": {},
          "nickname": "",
          "object": "price",
          "product": {
            "active": false,
            "created": 0,
            "default_price": null,
            "deleted": false,
            "description": "",
            "id": "prod_UCSHzzI5XfUkEY",
            "images": null,
            "livemode": false,
            "marketing_features": null,
            "metadata": null,
            "name": "",
            "object": "",
            "package_dimensions": null,
            "shippable": false,
            "statement_descriptor": "",
            "tax_code": null,
            "type": "",
            "unit_label": "",
            "updated": 0,
            "url": ""
          },
          "recurring": null,
          "tax_behavior": "unspecified",
          "tiers": null,
          "tiers_mode": "",
          "transform_quantity": null,
          "type": "one_time",
          "unit_amount": 400,
          "unit_amount_decimal": "400"
        },
        "quantity": 1,
        "taxes": null
      }
    ]
  },
  "livemode": false,
  "locale": "",
  "metadata": {
    "out_trade_no": "1774256382025448500"
  },
  "mode": "payment",
  "object": "checkout.session",
  "optional_items": null,
  "origin_context": "",
  "payment_intent": {
    "amount": 0,
    "amount_capturable": 0,
    "amount_details": null,
    "amount_received": 0,
    "application": null,
    "application_fee_amount": 0,
    "automatic_payment_methods": null,
    "canceled_at": 0,
    "cancellation_reason": "",
    "capture_method": "",
    "client_secret": "",
    "confirmation_method": "",
    "created": 0,
    "currency": "",
    "customer": null,
    "description": "",
    "excluded_payment_method_types": null,
    "id": "pi_3TE4L6GLfJRXFUwH0xPlsxYW",
    "last_payment_error": null,
    "latest_charge": null,
    "livemode": false,
    "metadata": null,
    "next_action": null,
    "object": "",
    "on_behalf_of": null,
    "payment_method": null,
    "payment_method_configuration_details": null,
    "payment_method_options": null,
    "payment_method_types": null,
    "presentment_details": null,
    "processing": null,
    "receipt_email": "",
    "review": null,
    "setup_future_usage": "",
    "shipping": null,
    "source": null,
    "statement_descriptor": "",
    "statement_descriptor_suffix": "",
    "status": "",
    "transfer_data": null,
    "transfer_group": ""
  },
  "payment_link": null,
  "payment_method_collection": "if_required",
  "payment_method_configuration_details": {
    "id": "pmc_1Qr8SvGLfJRXFUwHq6Og9DnY",
    "parent": ""
  },
  "payment_method_options": {
    "acss_debit": null,
    "affirm": null,
    "afterpay_clearpay": null,
    "alipay": null,
    "amazon_pay": null,
    "au_becs_debit": null,
    "bacs_debit": null,
    "bancontact": null,
    "boleto": null,
    "card": null,
    "cashapp": null,
    "customer_balance": null,
    "eps": null,
    "fpx": null,
    "giropay": null,
    "grabpay": null,
    "ideal": null,
    "kakao_pay": null,
    "klarna": null,
    "konbini": null,
    "kr_card": null,
    "link": null,
    "mobilepay": null,
    "multibanco": null,
    "naver_pay": null,
    "oxxo": null,
    "p24": null,
    "payco": null,
    "paynow": null,
    "paypal": null,
    "pix": null,
    "revolut_pay": null,
    "samsung_pay": null,
    "sepa_debit": null,
    "sofort": null,
    "swish": null,
    "us_bank_account": null
  },
  "payment_method_types": [
    "card",
    "alipay",
    "wechat_pay",
    "link"
  ],
  "payment_status": "paid",
  "permissions": null,
  "phone_number_collection": {
    "enabled": false
  },
  "presentment_details": null,
  "recovered_from": "",
  "redirect_on_completion": "always",
  "return_url": "http://localhost:8081/stripe_return?session_id={CHECKOUT_SESSION_ID}",
  "saved_payment_method_options": null,
  "setup_intent": null,
  "shipping_address_collection": null,
  "shipping_cost": null,
  "shipping_options": [],
  "status": "complete",
  "submit_type": "",
  "subscription": null,
  "success_url": "",
  "tax_id_collection": null,
  "total_details": {
    "amount_discount": 0,
    "amount_shipping": 0,
    "amount_tax": 0,
    "breakdown": null
  },
  "ui_mode": "embedded",
  "url": "",
  "wallet_options": null
}
```