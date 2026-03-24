- return：
	- state=approved：支付
- notify：
	- state=completed：完成
# 如

## return
- cancelURL（仅仅只是跳转到页面）会同时携带token=xxx

- query参数
```json
{
  "PayerID": "96TSFL2KRJATU",
  "paymentId": "PAYID-NHA7MXI7FD586121L562103F",
  "token": "EC-3DX50422CG0125912"
}
```


### 支付

```json
{
  "intent": "sale",
  "payer": {
    "payment_method": "paypal",
    "status": "VERIFIED",
    "payer_info": {
      "email": "sb-vimrl50136254@business.example.com",
      "first_name": "John",
      "last_name": "Doe",
      "payer_id": "96TSFL2KRJATU",
      "country_code": "C2",
      "shipping_address": {
        "recipient_name": "Doe John",
        "line1": "NO 1 Nan Jin Road",
        "city": "Shanghai",
        "country_code": "C2",
        "postal_code": "200000",
        "state": "Shanghai"
      }
    }
  },
  "transactions": [
    {
      "amount": {
        "total": "0.01",
        "currency": "USD",
        "details": {
          "subtotal": "0.01",
          "shipping": "0.00",
          "handling_fee": "0.00",
          "shipping_discount": "0.00",
          "insurance": "0.00"
        }
      },
      "payee": {
        "merchant_id": "TUTQ6H4E6PQ8S",
        "email": "li_li_li87222_tseller@163.com"
      },
      "description": "xxxx",
      "custom": "1774319195249756300",
      "item_list": {
        "items": [
          {
            "name": "xxxx",
            "description": "xxxx",
            "quantity": 1,
            "price": "0.01",
            "tax": "0.00",
            "currency": "USD"
          }
        ],
        "shipping_address": {
          "recipient_name": "Doe John",
          "line1": "NO 1 Nan Jin Road",
          "city": "Shanghai",
          "country_code": "C2",
          "postal_code": "200000",
          "state": "Shanghai"
        }
      },
      "related_resources": [
        {
          "sale": {
            "id": "6WC7557180098591U",
            "amount": {
              "total": "0.01",
              "currency": "USD",
              "details": {
                "subtotal": "0.01",
                "shipping": "0.00",
                "handling_fee": "0.00",
                "shipping_discount": "0.00",
                "insurance": "0.00"
              }
            },
            "payment_mode": "INSTANT_TRANSFER",
            "state": "completed",
            "protection_eligibility": "ELIGIBLE",
            "protection_eligibility_type": "ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE",
            "transaction_fee": {
              "currency": "USD",
              "value": "0.01"
            },
            "parent_payment": "PAYID-NHA7MXI7FD586121L562103F",
            "create_time": "2026-03-24T02:34:47Z",
            "update_time": "2026-03-24T02:34:47Z",
            "links": [
              {
                "href": "https://api.sandbox.paypal.com/v1/payments/sale/6WC7557180098591U",
                "rel": "self",
                "method": "GET"
              },
              {
                "href": "https://api.sandbox.paypal.com/v1/payments/sale/6WC7557180098591U/refund",
                "rel": "refund",
                "method": "POST"
              },
              {
                "href": "https://api.sandbox.paypal.com/v1/payments/payment/PAYID-NHA7MXI7FD586121L562103F",
                "rel": "parent_payment",
                "method": "GET"
              }
            ]
          }
        }
      ]
    }
  ],
  "redirect_urls": null,
  "id": "PAYID-NHA7MXI7FD586121L562103F",
  "create_time": "2026-03-24T02:26:37Z",
  "state": "approved",
  "update_time": "2026-03-24T02:34:47Z",
  "links": [
    {
      "href": "https://api.sandbox.paypal.com/v1/payments/payment/PAYID-NHA7MXI7FD586121L562103F",
      "rel": "self",
      "method": "GET"
    }
  ]
}
```
## notify
- application/x-www-form-urlencoded

```json
{
  "address_city": "Shanghai",
  "address_country": "China",
  "address_country_code": "CN",
  "address_name": "Doe John",
  "address_state": "Shanghai",
  "address_status": "confirmed",
  "address_street": "NO 1 Nan Jin Road",
  "address_zip": "200000",
  "business": "li_li_li87222_tseller@163.com",
  "charset": "windows-1252",
  "custom": "1774321233812131100",
  "discount": "0.00",
  "first_name": "John",
  "insurance_amount": "0.00",
  "ipn_track_id": "fd2b7639924eb",
  "item_name1": "\u001a\u001a \u001a\u001a\u001a 1 \u001a\u001a\u001a 1\u001a",
  "item_number1": "",
  "last_name": "Doe",
  "mc_currency": "USD",
  "mc_fee": "0.01",
  "mc_gross": "0.01",
  "mc_gross_1": "0.01",
  "notify_version": "3.9",
  "num_cart_items": "1",
  "payer_email": "sb-k7uqe50117373@personal.example.com",
  "payer_id": "F52RYH4YNZA8S",
  "payer_status": "verified",
  "payment_date": "20:03:29 Mar 23, 2026 PDT",
  "payment_fee": "0.01",
  "payment_gross": "0.01",
  "payment_status": "Completed",
  "payment_type": "instant",
  "protection_eligibility": "Eligible",
  "quantity1": "1",
  "receiver_email": "li_li_li87222_tseller@163.com",
  "receiver_id": "TUTQ6H4E6PQ8S",
  "residence_country": "CN",
  "shipping_discount": "0.00",
  "shipping_method": "Default",
  "test_ipn": "1",
  "transaction_subject": "\u001a\u001a\u001a 1 \u001a\u001a\u001a 1\u001a",
  "txn_id": "3VX9037352150350A",
  "txn_type": "cart",
  "verify_sign": "AtwgJGeg7F.2cyihvFfz-4l6V8nPAEVI8jPS1mVlLxljMHrdjhT7y9WT"
}

```

### 完成
```json
{
  "id": "6WC7557180098591U",
  "amount": {
    "total": "0.01",
    "currency": "USD",
    "details": {
      "subtotal": "0.01"
    }
  },
  "payment_mode": "INSTANT_TRANSFER",
  "state": "completed",
  "protection_eligibility": "ELIGIBLE",
  "protection_eligibility_type": "ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE",
  "transaction_fee": {
    "currency": "USD",
    "value": "0.01"
  },
  "parent_payment": "PAYID-NHA7MXI7FD586121L562103F",
  "create_time": "2026-03-24T02:34:47Z",
  "update_time": "2026-03-24T02:34:47Z",
  "links": [
    {
      "href": "https://api.sandbox.paypal.com/v1/payments/sale/6WC7557180098591U",
      "rel": "self",
      "method": "GET"
    },
    {
      "href": "https://api.sandbox.paypal.com/v1/payments/sale/6WC7557180098591U/refund",
      "rel": "refund",
      "method": "POST"
    },
    {
      "href": "https://api.sandbox.paypal.com/v1/payments/payment/PAYID-NHA7MXI7FD586121L562103F",
      "rel": "parent_payment",
      "method": "GET"
    }
  ],
  "custom": "1774319195249756300"
}
```