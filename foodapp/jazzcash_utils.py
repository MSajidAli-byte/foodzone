"""
JazzCash Payment Gateway Utilities
"""
import hmac
import hashlib
from datetime import datetime, timedelta
from django.conf import settings

def generate_jazzcash_payload(amount, order_id, invoice_id):
    """
    Generate JazzCash payment payload with secure hash
    """
    txn_datetime = datetime.now()
    expiry_datetime = txn_datetime + timedelta(hours=1)
    txn_ref_no = f"TXN{txn_datetime.strftime('%Y%m%d%H%M%S')}"
    
    # Convert amount to paisa (multiply by 100)
    amount_paisa = str(int(float(amount) * 100))
    
    post_data = {
        "pp_Version": "1.1",
        "pp_TxnType": "",
        "pp_Language": "EN",
        "pp_MerchantID": settings.JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": settings.JAZZCASH_PASSWORD,
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        "pp_TxnRefNo": txn_ref_no,
        "pp_Amount": amount_paisa,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": txn_datetime.strftime("%Y%m%d%H%M%S"),
        "pp_BillReference": invoice_id,
        "pp_Description": f"Order #{order_id} Payment",
        "pp_TxnExpiryDateTime": expiry_datetime.strftime("%Y%m%d%H%M%S"),
        "pp_ReturnURL": settings.JAZZCASH_RETURN_URL,
        "pp_SecureHash": "",
        "ppmpf_1": str(order_id),
        "ppmpf_2": "",
        "ppmpf_3": "",
        "ppmpf_4": "",
        "ppmpf_5": ""
    }
    
    # Generate secure hash
    ordered_keys = [
        "pp_Amount", "pp_BankID", "pp_BillReference", "pp_Description", "pp_Language",
        "pp_MerchantID", "pp_Password", "pp_ProductID", "pp_ReturnURL", "pp_SubMerchantID",
        "pp_TxnCurrency", "pp_TxnDateTime", "pp_TxnExpiryDateTime", "pp_TxnRefNo",
        "pp_TxnType", "pp_Version", "ppmpf_1", "ppmpf_2", "ppmpf_3", "ppmpf_4", "ppmpf_5"
    ]
    
    hash_string = '&'.join(f"{key}={post_data[key]}" for key in ordered_keys)
    secure_hash = hmac.new(
        settings.JAZZCASH_INTEGRITY_SALT.encode('utf-8'),
        hash_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest().upper()
    
    post_data["pp_SecureHash"] = secure_hash
    
    return {
        'post_url': settings.JAZZCASH_POST_URL,
        'post_data': post_data,
        'txn_ref_no': txn_ref_no
    }
